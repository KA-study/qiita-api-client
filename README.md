# QiitaScraper

## 概要
Qiitaから記事のメタ情報を取得し、条件に応じてソート・出力するCLIツールです。

## 背景
スクレイピングとデータ処理の基礎理解を目的として開発しました。

## 機能
- タグ指定による記事取得
- キーワード検索
- 選択可能なソート機能
- CSV/JSON形式での出力

## 使い方
```bash
python main.py --tag python --sort likes --keyword scraping
```

## ファイル構造
- main.py: CLIエントリーポイント。各モジュールを統合して実行する。
- scraper.py: Qiitaから記事メタ情報を取得する。
- processor.py: フィルタ・ソートなどデータ処理を行う。
- output.py: CSV/JSON形式で出力する。

## 使用技術
- Python 
- requests
- BeautifulSoup
- argparse

## 設計の工夫
- メタ情報のみに限定し、コンパクトで実用的なプログラムを設計。
- scraper/ processor/ output　に責務を分離し、保守性と拡張性を確保。

