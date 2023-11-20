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


