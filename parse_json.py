# 必要なライブラリのインポート
import pandas as pd

if __name__ == "__main__":

    # CSVファイルの読み込み
    my_play_dataframe = pd.read_csv(
        "./beatmaniaPlayData.csv")

    # 読み込んだCSVファイルのdataframeのデータ長を取得
    data_length = len(my_play_dataframe.index)

    # 読み込んだCSVで欲しい列のヘッダ名を設定する
    # このデータを使って分散などの統計データを取る予定
    music_title = my_play_dataframe["タイトル"]

    hyper_difficulty = my_play_dataframe["HYPER 難易度"]
    hyper_ex_score = my_play_dataframe["HYPER EXスコア"]
    hyper_misscount = my_play_dataframe["HYPER ミスカウント"]
    hyper_cleartype = my_play_dataframe["HYPER クリアタイプ"]
    hyper_dj_level = my_play_dataframe["HYPER DJ LEVEL"]

    another_difficulty = my_play_dataframe["ANOTHER 難易度"]
    another_ex_score = my_play_dataframe["ANOTHER EXスコア"]
    another_miss_count = my_play_dataframe["ANOTHER ミスカウント"]
    another_cleartype = my_play_dataframe["ANOTHER クリアタイプ"]
    another_dj_level = my_play_dataframe["ANOTHER DJ LEVEL"]

    latest_play_dateTime = my_play_dataframe["最終プレー日時"]
    play_count = my_play_dataframe["プレー回数"]

    # numpyで統計データを取る
    # another_ex_scoreが既にlistなのでnumpyが使用できる

    # 各曲全て参照する
    # ここで曲（行）ごとのデータが取得できる
    for index in range(data_length):
        print("Now Index is: %d " % index)
        # ヘッダ部分はループ処理から除外する
        if index == 0:
            continue
        # 稼働中バージョンでプレイ済みの曲のみ抽出
        if play_count[index] > 0:
            print("Title: %s " % music_title[index])
            print("HYPER EX score: %s " % hyper_ex_score[index])
            print("ANOTHER EX score: %s " % another_ex_score[index])
            print("HYPER Cleartype: %s " % hyper_cleartype[index])
            print("ANOTHER Cleartype: %s \n" % another_cleartype[index])

    # JSONファイルとして変換し出力する
    # force_asciiで2バイト文字のエスケープを回避する
    my_play_dataframe.to_json("./myPlayData.json", force_ascii=False)

    print("JSON file creation done!")
