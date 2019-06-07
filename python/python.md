
## パッケージ管理、環境

### virtualenv

参考ドキュメント

- [Pythonの仮想環境を構築できるvirtualenvを使ってみる - Qiita](http://qiita.com/H-A-L/items/5d5a2ef73be8d140bdf3)

```
# 事前準備
sudo easy_install virtualenv

# 仮想環境の作成
mkdir /path/to/PythonTest
virtualenv --no-site-packages /path/to/PythonTest

# その仮想環境を使いたいとき (おそらくPATHなど必要な環境変数がセットされる)
source /path/to/PythonTest/bin/activate

# 仮想環境終了 (環境変数などを元に戻す)
deactivate
```

### パッケージ管理, pip

```
pip 
python -m pip
py -m pip          # windwos の場合、これがおすすめ。どのバージョンのpythonにpipするかわかりやすい

py -m php -V       # どのpythonバージョンのpipが起動するか確認


py -m pip freeze               # インストールされているパッケージ一覧を表示
py -m pip list                 # インストールされているパッケージ一覧を表示。微妙に違うらしい。

// インストール
py -m pip install パッケージ
py -m pip install パッケージ==バージョン番号
py -m pip install -r requirement.txt    # テキストファイルに書かれたパッケージを一括でインストール

// アンインストール
py -m pip uninstall パッケージ 

// 検索
py -m pip search 検索ワード
```

