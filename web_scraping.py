# 必要なファイルのインポート
import logging
# 取得したHTMLファイルをパースするライブラリ
from bs4 import BeautifulSoup
import pandas as pd

# ログレベルの変更
logging.basicConfig(level=logging.DEBUG)

# 曲の部分のカラム数
MAX_COLUMNS = 13


def get_soup(uri):
    '''スクレイピング対象のHTMLファイルを指定する。
    指定した文字コードでも対応できない2バイト文字等の対応としてerrors='ignore'を設定している
    '''
    with open(uri, encoding="euc_jp", errors="ignore") as html_file:
        soup = BeautifulSoup(html_file, "html.parser")
        return soup


def analyze_soup(soup, df_headers):
    '''
    soupから抜き出した曲情報詳細をデータフレームとして返却
    '''

    df = pd.DataFrame(columns=df_headers)

    # パースを無視したtd要素のリスト
    failed_cell_data = []

    # 必要なHTML要素を取得する
    table = soup.find_all("table", class_="style_table")[1]
    tbody = table.find("tbody").extract()

    # table内の各要素内のテキストノードを取得
    for row in tbody.find_all("tr"):
        cols = row.find_all("td", class_="style_td")

        # ヘッダ部分の行など予想されるテーブルのヘッダに合わない場合
        if len(cols) < MAX_COLUMNS:
            # Beatmaniaのバージョンを示す行の場合、それを記憶する
            if (cols[0].get("colspan") == str(MAX_COLUMNS)):
                # 元のHTMLでは、バージョン部分の"Beatmania IIDX"と"substream"などは
                # ２つの<strong>に分けて書かれているため結合する
                strongs = cols[0].findAll("strong")
                version = " ".join([strong.text for strong in strongs])
                logging.info(version + " の楽曲詳細をパースします...")
            # rowspanで結合され、指定したヘッダより少ないセル数の行はパース対象外として別途格納する
            elif len(row.findAll("td")) < MAX_COLUMNS:
                for failed_data in cols:
                    failed_cell_data.append(failed_data.text)
            continue

        # この曲の情報を格納する辞書
        song_info = {}

        # この曲のカラム内容を一つずつ辞書に登録していく
        for index, col in enumerate(cols):
            song_info["version"] = version

            # DFとテーブル双方のヘッダ順序が一致していることを前提に順に登録
            header = df_headers[index]
            song_info[header] = col.text

        # 単純に行を追加したいだけなので元のインデックスを参照する必要がないのでinnore_indexをTrueにしている
        df = df.append(song_info, ignore_index="True")

    # パース対象外として別途保存したデータを出力する
    logging.info("failed parsing data>>>")
    logging.info(failed_cell_data)

    return df


if __name__ == "__main__":

    # このヘッダーは実物のHTMLに即した順序で作ること
    table_headers = [
        'title',
        'sp_b',
        'sp_n',
        'sp_h',
        'sp_a',
        'sp_l',
        'dp_n',
        'dp_h',
        'dp_a',
        'dp_l',
        'time',
        'movie',
        'layer',
    ]

    # データフレーム独自のカラムを後尾に追加
    df_headers = table_headers + ['version']

    input_uri = "./test.html"
    output_uri = "./note_list.csv"

    df = analyze_soup(get_soup(input_uri), df_headers)
    df.to_csv(output_uri, mode="w", index=True, header=True)
