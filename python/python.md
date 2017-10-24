
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
pip freeze               // インストールされているパッケージ一覧を表示
pip install パッケージ   // インストール
```

