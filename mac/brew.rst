=============================
home brew
=============================


参照
===================

- 公式: `Homebrew — The Missing Package Manager for macOS (or Linux) <https://brew.sh/>`__
- formula 一覧が載っているサイト: `Homebrew Formulae <https://formulae.brew.sh/>`__



用語
============

- formula: いわゆるパッケージ
- cask:    macOS のアプリ



@でバージョン指定のものもある。

tapから入れたものは、user/repo/formula名 みたいな感じになっている。
--full-name を付けない限りは formula名だけ見える。



Cheatsheet
==================

ヘルプ

::

    brew help 


一覧 list

インストール済みのパッケージを表示

::

    brew list [<options>] [<FORMULA|CASK>...]


        --full-name  # フルネーム
        --versions   # バージョン番号も表示
        -l         # ls -l みたいな感じ。

検索 search

インストールできるパッケージを検索

::

    brew search text
    brew search /text/    # 正規表現


インストール

::

    brew install python3   

    brew install --cask firefox    # caskを入れる場合


更新系

::

    brew update        # brew自体の更新

アンインストール::

    brew uninstall FORMULA|CASK


tap/untap

公式以外のリポジトリを使う。

::

    brew tap   # tapしているもの一覧

    brew tap <user/repo>          # https://github.com/user/repo のリポジトリの浅いクローン
    brew tap <user/repo> <URL>    # 上記のURL指定。 github.com 以外にあるリポジトリを使う場合

    brew untap <user/repo>...     # tap の削除

    brew tap-pin <user/repo>
    brew tap-unpin <user/repo>

        優先順位
        - pinされたtap
        - 公式のもの
        - 他のtap

    あえて tap したものを入れたいときは完全修飾名を指定する
    brew install user/repo/vim


仕組み
==============

どのディレクトリにインストールされるか
-------------------------------------------

特に指定しなければ、 

- ``/usr/local/Cellar/<package名>/<version/`` に実体が入る
- ``/usr/local/opt/<package名>`` が Celler 配下の実体ディレクトリへのシンボリックリンクが置かれる
- ``/usr/local/bin/`` or ``/usr/local/sbin`` に実体コマンドへのシンボリックリンクが置かれる(置かれないものもある)


``brew --prefix`` で確認できる。


``@version`` 付きのパッケージ
----------------------------------

``@version`` 付きのパッケージは完全に別パッケージ扱いになるっぽい。::

    % ls -l /usr/local/Cellar
    go/
    go@1.22/

``@version`` 付きのパッケージは ``/usr/local/bin`` などへのシンボリックリンクを作らないことがある。
(作ったらバージョン違いで衝突しちゃうしね)。

go info で見ると下記のようなメッセージが出ているものは、シンボリックリンクを作らない。::

    go@1.22 is keg-only, which means it was not symlinked into /usr/local,
    because this is an alternate version of another formula.

    If you need to have go@1.22 first in your PATH, run:
      echo 'export PATH="/usr/local/opt/go@1.22/bin:$PATH"' >> ~/.zshrc


