==============
goenv
==============

https://github.com/go-nv/goenv/tree/master

複数のバージョンの go をインストールして、切り替えながら使えるツール。



インストール
===========================

git clone で入れる::

    git clone https://github.com/go-nv/goenv.git ~/.goenv

    update は git fetch & merge する


最初の設定

.zprofile の下の方に下記を追加::

    export GOENV_ROOT="$HOME/.goenv"      # goenv自体がどこにインストールされているかを指定
    export PATH="$GOENV_ROOT/bin:$PATH"   # goenvコマンドを実行するため

    export PATH="$PATH:$GOENV_ROOT/shims"  # goenv の shims に横取りさせるため。
                                           # goenv init でもセットされるが、
                                           # 非インタラクティブシェルでもセットした方がよいと思ってこちらに。

    # なお、この shims より前に go (/usr/local/go/binなど) がいるとうまく動かないので注意。


.zshrc の下の方に下記を追加::

    eval "$(goenv init -)"


ドキュメントには、下記を入れろと書いてあるが、入れなくてよい。むしろ入れるとうまく切り替わらないはず。::

    入れてはダメ
    export PATH="$GOROOT/bin:$PATH"
    export PATH="$PATH:$GOPATH/bin"




チートシート
======================

https://github.com/go-nv/goenv/blob/master/COMMANDS.md

::

    TODO 下記nodenvのものそのまま持ってきただけ

    goenv help               # ヘルプ表示。ただし全部は出ていない。

    goenv install -l         # インストール可能なバージョン一覧
    goenv install <version>  # インストール

    goenv shell <version>    # (優先度1) 指定したバージョンで、環境変数 ``GOENV_VERSION`` をセットする
    goenv shell              # どのバージョンが使われるか表示

    goenv local <version>    # (優先度2) 指定したバージョンで、 カレントディレクトリに ``.go-version`` ファイルを作る
    goenv local --unset      # カレントディレクトリに .go-version ファイルがあれば削除
    goenv local              # どのバージョンが使われるか表示

    goenv global <version>   # (優先度3) 指定したバージョンで ``~/.goenv/version`` を作る
    goenv global             # どのバージョンが使われるか表示

    goenv versions           # インストールしているversion一覧と、どのバージョンが使われるか
    goenv version            # どのバージョンが使われるか

    goenv rehash             # 全バージョンをスキャンして shims を作り直す。
                             # かつ、現在選択されているバージョンで GOROOT, GOPATH 環境変数をセットする。
                             # goenv install した後、go install した後、ディレクトリ移動などでバージョンが切り替わった後、
                             # 実行しておくこと。

    nodenv which npm         # activeバージョンのパスを表示する
    nodenv whence npm        # そのコマンドがインストールされているバージョン一覧

    goenv command            # コマンド一覧。おそらく補完用

優先度
===========

https://github.com/go-nv/goenv/blob/master/HOW_IT_WORKS.md

- (優先度1) ``GOENV_VERSION`` 環境変数で指定されたもの (ref. goenv shell)
- (優先度2) カレントディレクトリから上にたどって見つかった ``.go-version``  (ref. goenv local)
- (優先度3) ``~/.goenv/version`` (ref. goenv global)
- (優先度4) システムにインストールされているバージョン。もっと後ろのPATHを探すらしい。


仕組み
===========

全体観
-----------

https://github.com/go-nv/goenv/blob/master/HOW_IT_WORKS.md

大きく2つの機能・タイミングがある

- shims による go 関連コマンドのディスパッチ。

  - go 関連コマンドを実行したタイミングで、バージョンの選択判定、環境変数の設定、本物のバイナリの起動が行われる。
  - (事前に goenv rehash しておくことで、
     全バージョンの GOROOT/bin, GOPATH/bin にあるバイナリに相当するshimsが作られている。)

- goenv rehash による GOROOT, GOPATH 環境変数の設定

  - goenv rehash を明示的に打つか、``eval "$(goenv init -)"`` をしたタイミング
  - その時点で決定したバージョンに相当する GOROOT, GOPATH 環境変数が今のシェルにセットされる

この2つは実行タイミングが違うくせに、整合性は取らないといけないので、
特に、ディレクトリ移動で .go-version により選択バージョンが変わった場合など、
手動で goenv rehash を打つなどして整合を取る必要がある。

ディレクトリ

- GOROOT: ``~/.goenv/versions/<version>``
- GOPATH: ``~/go/<version>``    (versionごとに分ける戦略）



shims
------------------

PATH環境変数に ``~/.goenv/shims`` を追加することで、go コマンドを一旦goenvのものが受け取る。

それは、優先度に従い、どのバージョンのgoに向けるかを決定し、
そのバージョンの正式なコマンドに受け渡す。

つまり、コマンド実行ごとに、向き先を決めるということをしている。

shims が何をやっているか

- https://github.com/go-nv/goenv/blob/523fd841aece25828200f47d59a8d44072aaec4b/libexec/goenv-rehash#L42-L72

  - (program名($0)が ``go*`` にマッチした場合のみ)、引数に実在するファイルがあれば、GOENV_FILE_ARG 環境変数にセット
  - goenv exec に渡す

- https://github.com/go-nv/goenv/blob/master/libexec/goenv-exec

  - 使うバージョンを決定。GOENV_VERSION 環境変数にセット。
  - (バージョンが "system" でない場合)

    - GOROOT 環境変数を実際のバージョンのものにセット
    - GOPATH 環境変数を実際のバージョンのものにセット

  - PATH環境変数の先頭に、実行している本物コマンドの場所と GOROOT/bin を追加
  - 本物のコマンドを実行


利点

- PATH環境変数の記述は固定でよいので、.zshrcなどに固定で書いておけばよい。

  - 環境変数を変えたり持ち回ったりしないので、シェル以外から起動するVSCodeなどとも相性がよい。
    (GOROOT と GOPATH は変える必要があるが。)



goenv rehash
--------------------

goenv rehash することで、shims が作り直される。

- 全バージョンの GOROOT/bin と GOPATH/bin にある実行ファイル名で shims が作られる。
- なので、PATHには shims だけが入っていればよく、GOROOT/bin, GOPATH/bin 相当のパスは入れなくてよい。

対象ディレクトリ

https://github.com/go-nv/goenv/blob/523fd841aece25828200f47d59a8d44072aaec4b/libexec/goenv-rehash#L87-L105

全バージョンについて、下記をスキャン

- ``${GOENV_ROOT}/versions/${version}/bin/*``  (GOROOT相当)
- ``${HOME}/go/${version}/bin/*`` (GOPATH相当)



``goenv init -`` で出てくるスクリプト
=========================================

https://github.com/go-nv/goenv/blob/master/libexec/goenv-init

::

    export GOENV_SHELL=zsh
    export GOENV_ROOT=/home/hogehgoe/.goenv
    if [ "${PATH#*$GOENV_ROOT/shims}" = "${PATH}" ]; then
      export PATH="$PATH:$GOENV_ROOT/shims"
    fi
    source '/home/hogehoge/.goenv/libexec/../completions/goenv.zsh'
    command goenv rehash 2>/dev/null
    goenv() {
      local command
      command="$1"
      if [ "$#" -gt 0 ]; then
        shift
      fi

      case "$command" in
      rehash|shell)    
        eval "$(goenv "sh-$command" "$@")";;
      *)
        command goenv "$command" "$@";;
      esac
    }
    goenv rehash --only-manage-paths


- ``goenv() {...}`` のところは、goenv rehash と shell は、そのシェルに対して影響を与える必要があり、
  execではなくて eval する必要があるので、そのための仕組み。

