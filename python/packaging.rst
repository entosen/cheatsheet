=====================================
パッケージ管理、仮想環境
=====================================

参考

- `Pythonパッケージユーザーガイド（Python Packaging User Guide）<https://packaging.python.org/ja/latest/>`__


pythonのパッケージは ``pip`` を使って入れる。

pipで入れるパッケージは、pythonのバージョン(X.Y)ごとに独立して管理される。
なので、狙ったバージョンの python,pip を使ってインストールしないといけない。

また、下記のインストール先の違いもある。

- グローバル

  - ``sudo python3 -m pip install``
  - 管理者権限がないとできない
  - ``/usr`` 以下に入る

- user

  - ``python3 -m pip --user install``
  - ``~/.local`` 以下に入るらしい


- 仮想環境




インストールされる場所

`PEP 370 – Per user site-packages directory | peps.python.org <https://peps.python.org/pep-0370/>`__

- グローバル

  - 標準の場所::

      (Unix, Mac)
          [base dir]   
          [site dir]   /usr/local/lib/python3.6/site-packages
          [data dir]   /usr/local/lib/python3.6
          [script dir] /usr/local/bin

      (Windows)
          [base dir]   %APPDATA%/Python
          [site dir]   %APPDATA%/Python/Python36/site-packages
          [data dir]   %APPDATA%/Python/Python36
          [script dir] %APPDATA%/Python/Scripts

- user

  - 標準の場所::

      (Unix, Mac)
          [base dir]   ~/.local
          [site dir]   ~/.local/lib/python3.6/site-packages
          [data dir]   ~/.local/lib/python3.6
          [script dir] ~/.local/bin

      (Windows)
          [base dir]   %APPDATA%/Python
          [site dir]   %APPDATA%/Python/Python36/site-packages
          [data dir]   %APPDATA%/Python/Python36
          [script dir] %APPDATA%/Python/Scripts

  - 上記は環境変数 ``PYTHONUSERBASE`` で変更することができる (base dirを指定)

    - ``python -m site --user-base``  で確認


  

調べ方::

    python3 -m pip show <パッケージ名>

メモ

- グローバルか user どちらかに入っていれば、パッケージは使える

  - グローバルに既に条件を満たすパッケージが入っている場合、 ``pip install --user`` してもスキップされることがある::

        Requirement already satisfied: requests in /usr/local/lib/python3.6/site-packages (2.26.0)
  
  - pip list は、グローバルと user が区別される


パッケージ管理, pip
==========================

起動::

    python3 -m pip     # unix, mac の場合、これがおすすめ
    py -m pip          # windwos の場合、これがおすすめ。どのバージョンのpythonにpipするかわかりやすい

    pip 
    pip3

    python3 -m pip -V       # どのpythonバージョンのpipが起動するか確認


::

    python3 -m pip freeze    # インストールされているパッケージ一覧を表示
    python3 -m pip list      # インストールされているパッケージ一覧を表示。微妙に違うらしい。

    // インストール
    python3 -m pip install パッケージ
    python3 -m pip install パッケージ==バージョン番号
    python3 -m pip install -r requirement.txt    # テキストファイルに書かれたパッケージを一括でインストール

    // 更新
    python3 -m pip install --upgrade <パッケージ>

    // アンインストール
    python3 -m pip uninstall パッケージ 

    // 検索
    python3 -m pip search 検索ワード

    // パッケージの情報
    py -m pip show <パッケージ>


バージョン指定の仕方::

    TODO


仮想環境
=====================

概要

- venv

  - python標準。 Python 3.3 以降で使える
  - python自体のバージョンは管理できないらしい。venvでディレクトリを作ったときのバージョンのpythonが使われる。

- virtualenv

  - 別途インストールする必要がある。Python 2.7 以降で使える

- pipenv

  - TODO



venv
=====================

できること

- パッケージを、グローバルおよびuserのものと別の管理にできる
- pythonコマンド, pipコマンドを特定バージョンのものに限定する (venvでディレクトリを作ったときのpythonバージョンのもの)

  - なので、 ``python`` ``pip``  と打つだけでよい。 
    ``python3``, ``python3.6``, ``pip3``, ``pip3.6`` とかやらなくてよい。


参考

- https://docs.python.org/ja/3/library/venv.html
- 

Python 3.x.x 下に組み込まれた機能なので，Python 自体のバージョンは管理できない．

Unixの場合::

    python3 -m venv <DIR>
    source <DIR>/bin/activate

    deactivate

Windowsの場合::

    py -m venv <DIR>

    <DIR>\Scripts\activate.bat   # source 不要。コマンドプロンプトの場合
    <DIR>\Scripts\Activate.ps1   # source 不要。powershellの場合

    deactivate

project dir の下に ``venv`` とか ``.venv``  というディレクトリで作るのが一般的なのか？::

    cd <project dir>
    python3 -m venv .venv


何が起こっているか、もう少し詳しく。
-------------------------------------------

``python3 -m venv <DIR>`` で ``<DIR>`` 内に下記の構造ができる::

    .
    ├── bin/
    │   ├── activate
    │   ├── activate.csh
    │   ├── activate.fish
    │   ├── easy_install*
    │   ├── easy_install-3.6*
    │   ├── pip*
    │   ├── pip3*
    │   ├── pip3.6*
    │   ├── python -> python3*
    │   └── python3 -> /usr/bin/python3*
    ├── include/
    ├── lib/
    │   └── python3.6/
    │        └── site-packages/
    │             ├── __pycache__/
    │             ├── easy_install.py
    │             ├── pip/
    │             ├── pip-9.0.3.dist-info/
    │             ├── pkg_resources/
    │             ├── setuptools/
    │             └── setuptools-39.2.0.dist-info/
    ├── lib64 -> lib/
    └── pyvenv.cfg

``source <DIR>/bin/activate`` でやっているのは::

    VIRTUAL_ENV 環境変数 を <DIR> に
    PATH="$VIRTUAL_ENV/bin:$PATH"; export PATH
    かつ、それまでの値を _OLD_なんとかに覚えておく
    あと プロンプト PS1 をごにょごにょやっている


virtualenv
=====================

参考ドキュメント

- [Pythonの仮想環境を構築できるvirtualenvを使ってみる - Qiita](http://qiita.com/H-A-L/items/5d5a2ef73be8d140bdf3)

::

    # 事前準備
    python3 -m pip install --user virtualenv

    # 仮想環境の作成
    mkdir /path/to/PythonTest
    virtualenv --no-site-packages /path/to/PythonTest

    # その仮想環境を使いたいとき (おそらくPATHなど必要な環境変数がセットされる)
    source /path/to/PythonTest/bin/activate

    # 仮想環境終了 (環境変数などを元に戻す)
    deactivate




========================
モジュールの配布
========================

`Python モジュールの配布 — Python 3.11.2 ドキュメント <https://docs.python.org/ja/3/distributing/index.html>`_
`Pythonパッケージユーザーガイド（Python Packaging User Guide） — Python Packaging User Guide <https://packaging.python.org/ja/latest/>`_


なんかいろいろ方法があるみたい

- distutils  (古い)
- setuptools (現在の標準っぽい)
- poetry (未調査)
- flit (未調査)


パッケージ化のためのツールに、setuptools (新) と disutils (古) がある。

下記は setuptools での方法。


::

    python -m pip install setuptools wheel twine

setup.py::

    from setuptools import setup

    setup(
        name="boatrace.models",
    )

2020年5月リリースの setuptools-46.4.0 以降は今まで setup() で指定した項目の多くが setup.cfg で指定できるようになっている




<パッケージ名>.egg-info, build, dist のディレクトリが作成されるので、 .gitignore に入れておく。
参考: https://github.com/github/gitignore/blob/main/Python.gitignore


PyPI

- 本番: https://pypi.org/
- テスト環境: https://test.pypi.org/


.pypirc



