=========================
go の実行環境
=========================

goの実行環境とは。環境を切り替えるとは。
===============================================

goの実行環境を切り替えるというのは、下記の2つを切り替えることと言える。

- GOROOT : どこの Go SDK を使うか
- GOPATH : go install や go mod の置き場をどこにするか

go env コマンドで、各設定値がどこに向いているかを確認できる。

参考

- `GOROOT および GOPATH | GoLand ドキュメント <https://pleiades.io/help/go/configuring-goroot-and-gopath.html>`__


GOROOT
---------

GOROOT : どこの Go SDK を使うか。

Go SDK とは、いわゆる「インストール」で入れているやつで、
``go1.20.4.linux-amd64.tar.gz`` のようなファイルを解凍してできるツリー。
``go`` 実行ファイルを含んでいる。

標準のインストールの仕方だと ``/usr/local/go`` 。

GOROOTを切り替えるというのは、どのディレクトリに置かれた ``go`` 実行ファイルを使うかに等しい。
つまり、PATH 環境変数を切り替えることになる。

GOROOT 環境変数 は必ずしもセットする必要はないっぽい。
もしセットする場合は、PATH で見つかる ``go`` と矛盾がないようにしておいた方がいいと思う。


GOPATH
-----------

GOPATH : go install や go mod の置き場をどこにするか

go install や go mod で取得してきたファイルの置き場。
逆に go はコンパイル時にそのディレクトリを参照して mod を読み込む。

デフォルトは ``~/go`` 。

その中には

- ``$GOPATH/bin``

  - go install で入れた実行ファイルが入っている。 gopls, golangci-lint, mockgen とか。

- ``$GOPATH/pkg/mod``

  - go.mod とか go mo で入れたライブラリが入っている。::

      ~/go/pkg/mod/github.com/stretchr/testify@v1.8.1/...
      ~/go/pkg/mod/github.com/stretchr/testify@v1.8.2/...

昔は、開発のワーキングディレクトリごとにGOPATHを指定しないといけなかったらしい。
開発しているソースと、go mod で取ってきたものが、1つのワーキングディレクトリにないといけなかった？

だが、今はそうではない。GOPATH はセットせずに ``~/go`` に向けておいてもかまわない。

    調べてみるとどうやら昔(Go1.11以前)は$GOPATH/src配下でしか開発できなかったらしい。
    その後Go modulesの導入により$GOPATH/srcにプロジェクトを置かなければならないという制約からは解放されたので、
    各プロジェクト毎にGOPATHを指定するみたいなことがいらなくなったという経緯のようです。

    https://zenn.dev/creamstew/articles/20e7a00c2eb161edbb1e


GOPATH も基本はセットしなくてよい。何かの理由で分けたいという場合はセットする。


PATH環境変数について
----------------------------

goで開発するにあたり、環境変数PATH には、GOROOT/bin とGOPATH/bin は入れておいた方がよい。

例::

    export PATH="$PATH:/use/local/go/bin:/home/hogehoge/go/bin"

セキュリティ的な理由で、GOPATH/bin は末尾の方に置いておいた方がよい。


まとめると
----------------------------

GOROOT を切り替えたいなら、

- (1) PATH環境変数で、狙ったバージョンの go コマンドが動くようにしろ
- (2) GOROOT環境変数は必要ないはずだが、もしセットするなら矛盾のないようにセットしろ

GOPATH を切り替えたいなら

- (3) GOPATH環境変数をセットしろ
- (4) PATH環境変数に GOPATH/bin を含めろ (末尾の方がよい)




標準のインストール方法
==================================

手動インストール
---------------------------------

https://go.dev/doc/install

こんな感じで、ダウンロードしてきた tar.gz を解凍して、
``/usr/local/go`` 以下に配置すればOK。

::

    (多分 sudo が必要)
    rm -rf /usr/local/go && tar -C /usr/local -xzf go1.20.4.linux-amd64.tar.gz


PATH環境変数に、GOROOT/bin, GOPATH/bin 相当のパスを追加する。::

    export PATH="$PATH:/usr/local/go/bin:$HOME/go/bin"

入る場所::

    % which go
    /usr/local/go/bin/go

    % go version
    go version go1.20.4 linux/amd64

    % go env (抜粋)
    GOROOT="/usr/local/go"
    GOPATH="/home/hogehoge/go"


mac で brew で入れる場合
-----------------------------------------

::

    brew install go

PATH環境変数に、GOROOT/bin, GOPATH/bin 相当のパスを追加する。::

    (/usr/local/bin は既に入ってるだろうから省略)
    export PATH="$PATH:$HOME/go/bin"

入る場所::

    /usr/local/bin/go
    -> /usr/local/Cellar/go/1.22.2/bin/go
    -> /usr/local/Cellar/go/1.22.2/libexec/bin/go 
      (にシンボリックリンクが張られてる)

    % go version 
    go version go1.22.2 darwin/amd64

    % go env (抜粋)
    GOROOT='/usr/local/Cellar/go/1.22.2/libexec'
    GOPATH='/Users/hogehoge/go'

    


複数バージョンをインストールする方法
================================================

サマリ
-----------

標準のインストール場所

- GOROOT: ``/usr/local/go``
- GOPATH: ``~/go``

go標準の仕組みの複数インストール

- GOROOT: ``~/sdk/go<version>``
- GOPATH: ``~/go``  (同じものを使う。特に変更しない)
- VSCode の Go 拡張の切り替えは、まとめの (1) しかやらない。

goenv

- GOROOT: ``~/.goenv/versions/<version>``
- GOPATH: ``~/go/<version>``    (versionごとに分ける戦略）
- まとめの (1)(2)(3) をやってくれる

  - (1) ``go`` コマンドに関しては shims がディスパッチするので、 PATH に ``~/.goenv/shims`` が入ってさえいれば切り替わる。
    GOROOT/bin を PATH に入れる必要はない。
  - (2)(3) ``goenv rehash`` をすることで、その時点で確定したバージョンに、自動で GOROOT, GOPATH 環境変数がセットされる。
  - (4) GOPATH/bin に入っているコマンドも shims が作られるので、PATHに ``~/.goenv/shims`` が入ってさえいれば切り替わる。



go標準の仕組みで、複数バージョンインストール(ちょっと前のやつ)
-------------------------------------------------------------------

go標準の仕組みで、複数バージョンをインストールする方法が用意されている。

https://go.dev/doc/manage-install

(参考) Goバージョン一覧 https://go.dev/dl/


::

    $ go install golang.org/dl/go1.21.0@latest
        → ~/go/bin/go1.21.0 ができる。

    $ ~/go/bin/go1.21.0 download
        → tar.gz をダウンロードしてきて展開しているっぽい
        → ~/sdk/go1.21.0 の下に展開される (ちょっと気に食わない)

確認::

    % ~/sdk/go1.21.0/bin/go version
    go version go1.21.0 linux/amd64

    % ~/sdk/go1.21.0/bin/go env
    GOROOT='/home/hogehoge/sdk/go1.21.0'
    GOPATH='/home/hogehoge/go'

GOPATH は共通のものを使う戦略のようで、特にいじらない。

``~/sdk/go<version>/bin`` をPATHに追加することで、それの環境に差し替わる。


go 1.21 以降の自動でインストールされるやつ
-----------------------------------------------------

Go 1.21 以降では、goコマンドを実行したときに、
go.mod ファイル内の go 行のバージョン指定を見て、
自動で指定のバージョンのgoをダウンロードしてきて、それで実行される。

ただ、必ず指定のバージョンが使われるわけではなく

- go.mod 指定のバージョンの方が、入っている go より新しい場合は、そのバージョンがダウンロードされる
- go.mod 指定のバージョンの方が、入っている go より古い場合は、ダウンロードされない？


ちょっとよくわかっていないんだが、
これはユーザーが狙ったバージョンを選択するというよりは、
ビルドの一連の流れの中で必要になるケースがあって、そのとき困らないようにって感じなのかな。

狙ってあるバージョンを使いたいという場合は、goenv なりを使った方がいいと思う。



goenv
-----------------------

:doc:`goenv`

(1)(2)(3)(4) 全部できる感じなので、これがお勧め。

ただ、理解した上で、まめに goenv rehash しないとハマる。



mac の brew で複数バージョン
--------------------------------

``@version`` 付きのパッケージも用意されているが。

::

    go        # 最新バージョン
    go@1.22   # go-1.22.x の最新バージョン

``@version`` 付きのパッケージは、/usr/local/bin/go にシンボリックを作ってくれない。::

    % brew info go@1.22

    go@1.22 is keg-only, which means it was not symlinked into /usr/local,
    because this is an alternate version of another formula.

    If you need to have go@1.22 first in your PATH, run:
      echo 'export PATH="/usr/local/opt/go@1.22/bin:$PATH"' >> ~/.zshrc

つまり、PATH 環境変数を自力で都度うまいことしないといけない。




VSCode の Go の複数バージョン対応
---------------------------------------------

ウィンドウ下部に go のバージョンが表示されている。

そこをクリックして、Choose Go Environment で使う go を選択することができる。

候補としては、下記は認識してくれるっぽい。

- 今の PATH 環境変数で見つかる go  (← 未指定の場合はこれが使われるっぽい)
- ``/usr/local/go/bin/go`` (goの標準のインストール先)
- ``~/sdk/go<version>/bin/go`` (goの追加のインストール先)

その他、ファイルパス手動指定することもできる。

この選択は、そのワークスペース(≒ディレクトリ)に紐付けて記憶される。

この状態で VSCode のターミナルを開くと

- PATH の先頭に、選択したバージョンの go があるディレクトリが自動で追加されているので、
  ``go`` とやるだけで狙ったバージョンが起動する。


GOPATHに関しては、特にいじらない戦略のようだ。

つまり、まとめの (1) だけやってくれる。


どの GOROOT, GOPATH を使っているかは、"Locate Configured Go Tools" で表示することができるので、
どこの場所の go を使っているか、GOVERSION, GOROOT, GOPATH あたりを確認するとよい。


goenv を使う場合のTips

- VSCode の UI からの選択は使わずに、goenv での選択に任せる
- PATHで go コマンドとして、goenv の shims ヒットすれば、goenv で選択したバージョンを認識してくれる。

  - おそらく 見つかった go で ``go version`` している。
  - GOPATH についても、環境変数でなく ``go env GOPATH`` で認識しているようなので、
    shims 経由で go を起動すれば、GOPATH環境変数を付けた上で本物の go コマンドを起動しているので、
    うまく切り替わる。




