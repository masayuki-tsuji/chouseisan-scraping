# chouseisan-scraping
調整さんをスクレイピングするツール

## 環境

- AWS Lambda

## デプロイ手順

1. 必要パッケージのインストール for Linux
  ```bash
    docker-compose up
  ```

2. ZIPファイルの作成
  ```bash
    ./scripts/zip.sh
  ```

3. S3にアップロード
4. AWS LambdaにS3からファイルをアップロードする