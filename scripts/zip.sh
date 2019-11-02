#!/bin/bash

# 設定ファイルの読み込み
source `dirname $0`/.env

# 変数定義
NOW=`date +'%Y%m%d%H%M%S'`
ZIP_FILE=$OUT_DIR/function.zip

# 既存ZIPファイルの退避
if [ -f $ZIP_FILE ]; then
  mv $ZIP_FILE ${ZIP_FILE}.${NOW}
fi

# パッケージディレクトリをアーカイブへ登録
if [ -d $PACKAGE_DIR ]; then
  cd $PACKAGE_DIR
  zip -r9 $ZIP_FILE .
fi

# ソースコードをアーカイブへ登録
cd $SRC_DIR
zip -rg $ZIP_FILE .

# 内容の表示
unzip -l $ZIP_FILE

exit 0
