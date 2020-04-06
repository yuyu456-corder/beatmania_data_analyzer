# 必要なファイルのインポート
import logging
# 取得したHTMLファイルをパースするライブラリ
from bs4 import BeautifulSoup

# ログレベルの変更
logging.basicConfig(level=logging.DEBUG)

# 取得したいHTMLファイルのURLを指定する
# get_url = ""

# soup形式でHTMLをパースする
# URLを指定してリクエストを送ってHTMLを取得する場合の処理
# Webサーバ側の負荷を考慮し、1秒以上間隔を空けてリクエストを送る
# sleep(1)
# get_html = urllib.request.urlopen(get_url)
# soup = bs(html, "html.parser")

# スクレイピング対象のHTMLファイルを指定する
# 指定した文字コードでも対応できない2バイト文字等の対応としてerrors='ignore'を設定している
with open("./test.html", encoding="euc_jp", errors="ignore") as html_file:
    soup = BeautifulSoup(html_file, "html.parser")

# スクレイピング対象のテーブルの最大カラム数
MAX_COLUMNS = 13
# thead要素内のセルの数
TABLE_HEADER_CELLS = 15
# CSVに出力するテーブルから取得した値(dict)
get_table_data_dict = {0: []}
# table要素内の値をループ処理で取得するためのカウンタ
key_id_counter = 0
row_cell_counter = 0
# table要素の1行ごとのtd要素を格納するlist
get_row_list_tmp = []
# rowspanにより取得できなかった行のセルと行数を記録するlist
failed_row_data = []
ignore_cells = 0

# 必要なHTML要素を取得する
get_table = soup.find_all("table", class_="style_table")[1]
get_tbody = get_table.find("tbody").extract()

# table内の各要素内のテキストノードを取得
for get_td in get_tbody.find_all("td", class_="style_td"):

    # 現在の取得したtd要素内のテキスト
    # f'checking td element: {get_td.text} \n'

    # rowspanで連結されたtd要素の対応
    # 現在は無視して、取得できなかったデータを別途表示することで対応
    if (get_td.get("rowspan") is not None):
        # 取得できないデータの情報を格納
        failed_row_data.append(get_td.text)
        # 結合した1行目以降のセル数の計算
        ignore_cells = ((int(get_td.get("rowspan")) - 1) *
                        MAX_COLUMNS) - int(get_td.get("rowspan"))
        # print("ignore cells: %d" % ignore_cells)
        # 破棄される予定のtd要素を別途格納する
        for failed_td in get_row_list_tmp:
            failed_row_data.append(failed_td)
        # 行のセル数のカウンタの初期化
        row_cell_counter = 0
        # get_row_list_tmpの初期化
        get_row_list_tmp = []
        logging.info("loop continued")
        continue
    # 結合されている行数分だけパースしている行を無視する
    # 最初の結合しているセルのパースは行った後にこの処理は行われる
    if (ignore_cells > 0):
        failed_row_data.append(get_td.text)
        # 行のセル数のカウンタの初期化
        row_cell_counter = 0
        # get_row_list_tmpの初期化
        get_row_list_tmp = []
        ignore_cells -= 1
        logging.info("loop continued")
        continue

    # colspanで連結されたtd要素は取得しない
    check_concatenated_by_colspan = get_td.get("colspan")
    if check_concatenated_by_colspan is not None:
        logging.info("loop continued")
        continue

    # 現在取得したtd要素の状態によってcurrent_td_textで場合分けしている
    # 配列にtd要素を追加していく
    get_row_list_tmp.append(get_td.text)
    row_cell_counter += 1

    # 1行分のtd要素が取得が取得されたらdictのkey部分を切り替え別のdictに保存する
    if row_cell_counter == MAX_COLUMNS:

        # 1行分のテーブルのtd要素をいれたらそのlistを現在のcounterをkeyとしてdictに格納する
        get_table_data_dict[key_id_counter] = get_row_list_tmp
        print(get_table_data_dict[key_id_counter])
        # dictのkeyの切り替え
        key_id_counter += 1
        # 行のセル数のカウンタの初期化
        row_cell_counter = 0
        # get_row_list_tmpの初期化
        get_row_list_tmp = []

# print(get_table_data_dict)

# 取得できなかったtd要素を表示する
print("failed parse data>>>")
print(failed_row_data)

# 出力時にヘッダ部分をどう扱うか考える


if __name__ == "__main__":
    pass
