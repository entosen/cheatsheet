

================================
Windows の py.exe
================================


Windows にpythonをインストールした場合には、 ``py.exe`` というランチャーが付いてくる。


実行::

    py              # インタプリタが起動
    py sample.py    # 指定したpythonスクリプトを実行

    # python モジュールを実行 (-m オプションを使う)
    py -m pip freeze 
    py -3.5 pip install xxxx    # バージョン指定するならこの位置


バージョンの選択::

    py       # 最後にインストールしたバージョン？最新？のpythonを実行
    py -3.6  # Python 3.6 を実行
    py -3    # 最新のPython 3.x を実行
    py -2    # Python 2.x を実行


確認::

    py --list  もしくは  py -0
        # 使用可能な python バージョンを表示
    py --list-paths  もしくは py -0p
        # 使用可能な python バージョンとパスを表示
        # '*' が付いているのがデフォルト

    py -V         # 選択されたバージョンのpython で python -V  (バージョンの表示のみ)を実行
    py -m pip -V  # 選択されたバージョンのpython で -m pip -V  を実行 




shebang
-----------

py.exe が shebang行を解釈して適切なバージョンのpythonを起動する。

なので、厳密なパスではなく、下記のような柔軟な書き方ができる。

unix環境と移植可能なようにするために、`/usr/bin/python` 形式がいいと思う。

::

    #!/usr/bin/env python
    #!/usr/bin/python
    #!/usr/local/bin/python
    #!python

    #!python3.5     # あえて 3.5 で実行したい場合
