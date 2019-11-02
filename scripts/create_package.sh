#!/bin/bash

# 設定ファイルの読み込み
source `dirname $0`/.env

# 変数定義
PACKAGE_FILE=$CONF_DIR/requirement_package.txt

# Linux判定
if [ "$(uname)" == 'Darwin' ]; then
  echo "Error: AWS LambdaがLinuxで動作するためパッケージの作成もLinuxで行って下さい。"
  exit 1
fi

# 既存パッケージの削除
if [ -d $PACKAGE_DIR ]; then
  rm -rf $PACKAGE_DIR
fi

# モジュールのインストール
PIP_LIST=`cat $PACKAGE_FILE`
for module in $PIP_LIST;
do
  pip install -t $PACKAGE_DIR $module
done

exit 0