==================================
pyenv
==================================

.. seealso::

   - https://github.com/pyenv/pyenv#readme
   - https://github.com/pyenv/pyenv/blob/master/COMMANDS.md


コマンド cheatsheet
==========================

::

  === help系 ===
  pyenv help
  pyenv help <command>
  pyenv command 

  === インストール系 ===
  pyenv install -l     # インストール可能なバージョンの一覧表示
  pyenv install <version>
  pyenv uninstall <version> ...

  pyenv rehash       # インストール後にshimsが増えた場合に使う。

  === バージョン選択系 ===
  pyenv version        # 今activeなバージョンと理由の表示
  pyenv versions       # インストール済みバージョンの一覧と選択の表示

  pyenv local <version>  # localで使うバージョンを指定
                         # (.python-versionをカレントディレクトリに作る)
  pyenv local --unset

  pyenv global <version>  # global で使うバージョンを指定
                          # (~/.pyenv/versionを書く)
  pyenv global system     # pyenv をスルーしてPATHの以降のものを使う

  pyenv shell <version>   # シェルで使うバージョンを指定
                          # (環境変数 PYENV_VERSION をセット)
  pyenv shell --unset

  === 調査系 ===
  pyenv which python3    # そのコマンドが、どこ(どのバージョンの)ものかを表示
  pyenv whence python3

  pyenv root              # /home/user/.pyenv  pyenvのroot dirを表示
  pyenv prefix <version>  # そのバージョンの実体ディレクトリを表示
  pyenv latest <prefix>   # バージョンを一部省略した場合の解釈
  pyenv shims             # shims (ファサードしているコマンド)の一覧

  === シェル系 ===
  pyenv init
  pyenv complete


バージョン指定を一部省略した場合::

  <version> 表記の例
  3.8.10         # フル指定
  3.8            # それの最新パッチバージョン
  3:latest       # それの最新バージョン


- install は、利用可能な最新バージョン ( ``pyenv latest -k``)
- uninstall は省略不可
- それ以外は install済みの最新バージョン ( ``pyenv latest`` )


仕組み
==================

ファサードになる shims を PATH の前の方に置くことで、
python関係のコマンドを横取りする。


どのバージョンのpythonが動くか (優先度順)

1. 環境変数 ``PYENV_VERSION``  ( ``pyenv shell`` でセット)
2. カレントディレクトリの ``.python-version`` ( ``pyenv local`` でセット)
3. カレントディレクトリから上にたどって見つかった ``.python-version``
4. ``$(pyenv root)/version`` ファイル。 ( ``pyenv global`` でセット)
5．globalでも見つからないときは、以降のPATHにあるもの (systemと呼んでいる)
