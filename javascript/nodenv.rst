==============
nodenv
==============

https://github.com/nodenv/nodenv

複数の nodejs をインストールして、切り替えながら使えるツール。



インストール
===========================

mac
--------

::

    brew install nodenv

    /usr/local/bin/nodenv に入る

最初の設定。

下記を .zshrc に書くらしい::

    eval "$(nodenv init -)"

個人的には、非インタラクティブシェル用に、PATHの設定だけは .zprofile に書いておいた方がいいと思う。::

    // .zprofile の末尾の方
    export PATH="$HOME/.nodenv/shims:${PATH}"

    // .zshrc の末尾の方
    eval "$(nodenv init -)"


GitHubから入れる
------------------------

参考 https://github.com/nodenv/nodenv#basic-github-checkout

※ homebrew の場合は nodenv 本体と node-build の両方が入っているらしい。

この手順ではそれぞれいれないといけないので注意。
忘れると nodenv install ができない。


::

    git clone https://github.com/nodenv/nodenv.git ~/.nodenv
    (~/.nodenv に入る。)

    mkdir ~/.nodenv/plugins
    git clone https://github.com/nodenv/node-build.git ~/.nodenv/plugins/node-build
    git clone https://github.com/nodenv/nodenv-aliases.git ~/.nodenv/plugins/nodenv-aliases
    (これも入れておくとupdateが楽)
    git clone https://github.com/nodenv/nodenv-update.git ~/.nodenv/plugins/nodenv-update

::

    // .zprofile の末尾の方
    export PATH="$HOME/.nodenv/bin:$PATH"
    export PATH="$HOME/.nodenv/shims:${PATH}"

    // .zshrc の末尾の方
    eval "$(nodenv init -)"


global につかうnodeを1つ指定しておく
---------------------------------------

ディレクトリに ``.node-version`` が置いてなかった場合に動くnodeバージョンを1つ指定しておく::

    nodenv global 20.12.0



アップデート
===========================

新しい node.js のバージョンが見えない場合は、

homebrewで入れている場合::

    brew upgrade nodenv node-build

GiHubから入れている場合::

    (nodenv-update plugin が入っている場合)
    nodenv udpate 

    (そうでない場合)
    cd ~/.nodenv/plugins/node-build
    git pull


チートシート
======================

::

    nodenv install -l          # インストール可能なバージョン一覧 (--list でも可)
    nodenv install <version>   # インストール

    nodenv shell <version>   # (優先度1) 指定したバージョンで、環境変数 ``NODENV_VERSION`` をセットする
    nodenv shell             # どのバージョンが使われるか表示

    nodenv local <version>   # (優先度2) 指定したバージョンで、 カレントディレクトリに ``.node-version`` ファイルを作る
    nodenv local --unset     # カレントディレクトリに .node-version ファイルがあれば削除
    nodenv local             # どのバージョンが使われるか表示

    nodenv global <version>  # (優先度3) 指定したバージョンで ``~/.nodenv/version`` を作る
    nodenv global            # どのバージョンが使われるか表示

    nodenv versions          # インストールしているversion一覧と、どのバージョンが使われるか
    nodenv version           # どのバージョンが使われるか

    nodenv rehash            # shimsを作成しなおす (後述)

    nodenv which npm         # activeバージョンのパスを表示する
    nodenv whence npm        # そのコマンドがインストールされているバージョン一覧

優先度
===========

https://github.com/nodenv/nodenv#choosing-the-node-version

- (優先度1) ``NODENV_VERSION`` 環境変数で指定されたもの (ref. nodenv shell)
- (優先度2-1) 実行しようとしたスクリプトのディレクトリから上にたどって見つかった ``.node-version``  (ref. nodenv local)
- (優先度2-2) カレントディレクトリから上にたどって見つかった ``.node-version``  (ref. nodenv local)
- (優先度3) ``~/.nodenv/version`` (ref. nodenv global)
- (優先度4) システムにインストールされているバージョン。もっと後ろのPATHを探すらしい。


仕組み
===========

https://github.com/nodenv/nodenv#how-it-works

PATH環境変数の先頭に ``~/.nodenv/shims`` を追加することで、
node, npm, npx, corepack コマンドを一旦nodenvのものが受け取る。

それは、優先度に従い、どのバージョンのnodejsに向けるかを決定し、
そのバージョンの正式なコマンドに受け渡す。

つまり、コマンド実行ごとに、向き先を決めるということをしている。



利点

- PATH環境変数の記述は固定でよいので、.zshrcなどに固定で書いておけばよい。


環境変数を変えたり持ち回ったりしないので、シェル以外から起動するVSCodeなどとも相性がよい。


shims
-------------------

shimsで横取りするコマンドは、各nodejsバージョンの bin 以下に存在するコマンド。

``nodenv rehash`` は、手元に取得済みのnodejs全バージョンについて、bin 以下にあるコマンドを調べて、
それと同名のshimsを作成しなおす。




nodenv init - でやっていること
=======================================

::

    export PATH="/Users/hogehoge/.nodenv/shims:${PATH}"
    export NODENV_SHELL=zsh
    source '/usr/local/Cellar/nodenv/1.4.1/libexec/../completions/nodenv.zsh'
    command nodenv rehash 2>/dev/null
    nodenv() {
      local command
      command="${1:-}"
      if [ "$#" -gt 0 ]; then
        shift
      fi
      case "$command" in
      rehash|shell)
        eval "$(nodenv "sh-$command" "$@")";;
      *)
        command nodenv "$command" "$@";;
      esac
    }


- ``nodenv() {...}`` のところは、nodenv rehash と shell は、そのシェルに対して影響を与える必要があり、
  execではなくて eval する必要があるので、そのための仕組み。
