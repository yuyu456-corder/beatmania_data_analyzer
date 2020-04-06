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

    # 必要なHTML要素を取得する
    table = soup.find_all("table", class_="style_table")[1]
    tbody = table.find("tbody").extract()

    # table内の各要素内のテキストノードを取得
    for row in tbody.find_all("tr"):
        cols = row.find_all("td", class_="style_td")

        # ヘッダ部分の行の場合
        if len(cols) < MAX_COLUMNS:
            # Beatmaniaのバージョンを示す行の場合、それを記憶する
            if (cols[0].get("colspan") == str(MAX_COLUMNS)):
                # 元のHTMLでは、バージョン部分の"Beatmania IIDX"と"substream"などは
                # ２つの<strong>に分けて書かれているため結合する
                strongs = cols[0].findAll("strong")
                version = " ".join([strong.text for strong in strongs])
                logging.info(version, "の楽曲詳細をパースします...")
            continue

        # 各曲の詳細情報の行の場合
        song_info = {}  # この曲の情報を格納する辞書

        # この曲のカラム内容を一つずつ辞書に登録していく
        for index, col in enumerate(cols):
            song_info["version"] = version

            # DFとテーブル双方のヘッダ順序が一致していることを前提に順に登録
            header = df_headers[index]
            song_info[header] = col.text

        df = df.append(song_info, ignore_index=True)

    return df


if __name__ == "__main__":

    # このヘッダーは実物のHTMLに即した順序で作ること
    table_headers = [
        'sp_b',
        'sp_n',
        'sp_h',
        'sp_a',
        'sp_l',
        'dp_n',
        'dp_h',
        'dp_a',
        'dp_l',
        'bpm',
        'genre',
        'title',
        'artist',
    ]

    # データフレーム独自のカラムを後尾に追加
    df_headers = table_headers + ['version']

    input_uri = "./test.html"
    output_uri = "./songs.csv"

    df = analyze_soup(get_soup(input_uri), df_headers)
    df.to_csv(output_uri, mode="w", index=True, header=True)
