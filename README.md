# beatmania_data_analyzer

KONAMI 社のアーケード音楽ゲーム”beatmaniaIIDX”のプレイヤーのスキルを分析するツール  
公式のサービスで自分のプレイヤーデータが CSV 形式で提供されるため、これを上手くつかって自分のプレイデータを分析・可視化して  
モチベーション維持やデータサイエンス的なことが出来るのではと思い立てたプロジェクト。

## ファイル構成

- parse_json.py ：同ディレクトリの CSV ファイルを読み込むプログラム
- web_scraping.py :web スクレイピングを行うプログラム
  - table 要素の各 td をスクレイピングする
- myPlaydata.json ：parseJson.py によって出力された JSON ファイル
- beatmaniaPlayData.csv ：解析対象の CSV ファイル

## master に push、merge する前に(Merge Policy)

- README.md 記載の実装機能が問題なく動作することを確認すること

## 実装機能

- CSV ファイルを読み込んでデータ取得、JSON ファイルに出力
  - pandas ライブラリで DB チックに各値を参照できるようにした
  - JavaScript 等による Web 上でのデータ可視化などを視野に入れて JSON ファイルに出力している。

## あったらいい機能

- プレーデータ可視化
  - 時系列にプレー内容や成績（EX スコア、ミスカウント）などを Web ブラウザ上に出力
- プレーデータ分析
  - 音楽ゲームという特性上、曲（譜面）によってプレイヤーごとに体感難易度が変わるものがある。これを”体感”ではなく、統計的に数値化したい。
  - サンプル数が自分＋ α じゃとても足りないため、公開 Web サービスまで持って行かないと難しそう
  - 自分のプレイ傾向などだったら可能か？
- 曲（譜面）情報の DB 化
  - 曲（譜面）自体にも、曲の長さ、ノーツ数、平均ノーツ数、アーティスト名などさまざな情報があるので、DB 可して管理しやすくしたい。

## 実行方法

- 前提として python3 の実行環境が必要

1. `cd beatmania_data_analyzer/`
1. `pip install pipenv (--user)`：この作業は初回のみ
1. `pipenv shell`
1. `pipenv install (--dev)`：必要に応じて dev-packages もインストールする
1. `python parseJson.py`：同ディレクトリに myPlaydata.json が出力される
1. `python web_scraping.py`：同ディレクトリの HTML ファイル(test.html)のスクレイピングを行う

## 対応中の不具合

- Web スクレイピングは rowspan に対応できず failed parse data として出力される

## 開発環境

- VSCode/Git
- Python3/Pipenv
  - Pandas (Library)
  - BeautifulSoup4 (Library)
