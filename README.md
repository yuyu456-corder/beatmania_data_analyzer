# beatmania_data_analyzer

KONAMI社のアーケード音楽ゲーム”beatmaniaIIDX”のプレイヤーのスキルを分析するツール  
公式のサービスで自分のプレイヤーデータがCSV形式で提供されるため、これを上手くつかって自分のプレイデータを分析・可視化して  
モチベーション維持やデータサイエンス的なことが出来るのではと思い立てたプロジェクト。

## ファイル構成

 - parse_json.py ：同ディレクトリのCSVファイルを読み込むプログラム
 - myPlaydata.json ：parseJson.pyによって出力されたJSONファイル
 - beatmaniaPlayData.csv ：解析対象のCSVファイル

## 実装機能

  - CSVファイルを読み込んでデータ取得、JSONファイルに出力
    - pandasライブラリでDBチックに各値を参照できるようにした
    - JavaScript等によるWeb上でのデータ可視化などを視野に入れてJSONファイルに出力している。

## あったらいい機能

  - プレーデータ可視化
    - 時系列にプレー内容や成績（EXスコア、ミスカウント）などをWebブラウザ上に出力
  - プレーデータ分析
    - 音楽ゲームという特性上、曲（譜面）によってプレイヤーごとに体感難易度が変わるものがある。これを”体感”ではなく、統計的に数値化したい。
    - サンプル数が自分＋αじゃとても足りないため、公開Webサービスまで持って行かないと難しそう
    - 自分のプレイ傾向などだったら可能か？
  - 曲（譜面）情報のDB化
    - 曲（譜面）自体にも、曲の長さ、ノーツ数、平均ノーツ数、アーティスト名などさまざな情報があるので、DB可して管理しやすくしたい。

## 実行方法

  - 前提としてpython3の実行環境が必要
  1. `cd beatmania_data_analyzer/`
  1. `pip install pipenv (--user)`
  - この作業は初回のみ
  1. `pipenv shell`
  1. `pipenv install`
  1. `python parseJson.py`
  - 同ディレクトリにmyPlaydata.jsonが出力される

## 対応中の不具合

## 開発環境
 - VSCode/Git
 - Python3/Pipenv
    - Pandas (Library)