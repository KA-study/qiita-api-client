# Qiita API Client

CLIベースのQiita記事検索クライアント。
Qiita API v2を利用して記事を取得し、条件検索・整形表示・AI要約を行う。

---

## 背景

API利用とデータ処理の基礎理解を目的として開発した。

---

## 機能

- Qiita API v2を利用した記事検索
- キーワード/タグ検索
- 選択可能なソート機能
- CLI引数による操作
- 記事情報の整形表示
- AIによる記事要約・読者レベル推定
- データ正規化処理
- 型ヒントを用いた実装

---

## 使用方法例

### 実行例

```bash
python main.py --tag python --sort likes --keyword scraping --ai True
```
### 出力例

```bash
=======result========

[1] 流行りのAI全盛りでテック系のニュース動画を自動作成する
    tags: ['Python', 'TextToSpeech', 'DALLE', '生成AI', 'GPT-4']
    likes: 58
    created_at: 2023-11-29 18:14:58
    url: https://qiita.com/yabish/items/cae596621f1b113f9c31

    ai_summary: これはモック環境で生成された要約です。実際のOpenAI APIは呼び出していません。
    ai_level: beginner
    ai_cost: 150
```
---

## アーキテクチャ

### 全体フロー

```text
CLI input
    ↓
Query Builder
    ↓
Qiita API Client
    ↓
Data Normalizer
    ↓
AI Processor
    ↓
Sorter
    ↓
OutPut Formatter
```

### AI処理フロー

```text
Article Data
    ↓
Cost Check / Optimization
    ↓
AI Processing (summary / level estimation)
    ↓
Store Result
    ↓
Return Processed Data
```

---

## プロジェクト構造

```text
program_files/
├main.py
├config.py
│
├ai/
│   ├ai_processor.py
│   ├api_client.py
│   ├cost_manager.py
│   ├cost_repository.py
│   ├definitions.py
│   ├manager.py
│   ├normalizer.py
│   ├processor_manager.py
│   └repository.py
│
├docs/
│   └decision_log.py
│
├fetch/
│   └fetcher.py
│
├output/
│   └output.py
│
├processor/
│   ├processor.py
│   └score.py
│
└storage/
    ├scheme.py
    └storage.py
```

---

## 必要な初期設定

### 環境

- Python 3.12+
- OpenAI API(AI機能を使用する場合)

### 環境変数

- OPENAI_API_KEY=your_api_key

---

## 入力オプション一覧

- --keyword: キーワード検索
- --tag: タグ検索
- --stocks: 取得記事のstock数下限
- --query: その他のクエリ条件
- --sort: ソート条件
- --number_of_articles: 取得記事数
- --ai: AI処理有効化

---

## 設計メモ

以下の分離設計に力を入れた。
- API取得層
- データ整形層
- 処理層
- 出力層
- 永続化層
- コスト制御層

---

## 開発者あとがき
まず、このプログラムを作成した理由は、上記でも述べたように、Pythonについての理解を深め、より実践的な知識・技術を得るためであった。
そういった意味で、この開発は大成功であったとここで述べたい。私が学んだことの一部を以下に示す。
- 責務を分離すること
- 関数やクラスに分離したコードの独立性を高めること
- 内部処理を利用者に意識させないこと
- 相互参照を避けること
- 特殊オブジェクトはクラス化などして閉じ込めること
- TypedDict,dataclassなどを用いて意味付けを行うこと

加えて、より理解を深め、習得しないといけないと学んだこともあった。以下にその一部を示す。
- 変数・関数・クラス・ファイルの明確な命名
- 定数・クラス型の管理
- より明快な責務分離
- コミットの粒度
- 単一の作業には単一の目的のみを持たせること
- 適切なコメントの埋め込み方
- 適切なdecision_logの使い方
- こまめにREADMEを更新すること
- ネストやif羅列を回避するためにアルゴリズム
これら多くのことを次に生かせるように、大事なことを整理してプログラミング学習に励みたいと思う。
