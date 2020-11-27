============================================
nvm および node.js のバージョンマネージャー
============================================

nvm はじめ、node,npmのバージョンを並行インストール、切り替えて使える仕組みをまとめる。

nvm
===========

公式: `GitHub - nvm-sh/nvm: Node Version Manager - POSIX-compliant bash script to manage multiple active node.js versions <https://github.com/nvm-sh/nvm>`__

インストール or アップグレード
-------------------------------------

標準のインストール方法 (ただし後述の問題があるので、これはやらない) ::

    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.0/install.sh | bash

    .bashrc に以下のような記述が挿入される。
        export NVM_DIR="$HOME/.nvm"
        [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
    この記述があることで、nvm コマンドが使えるのと、現在有効になっているnpmへパスが通る

ただし、この nvm.sh が WSL1 環境だとやたら重い(10秒ほど)。

シェルを開くたびに毎度10秒固まっては困るので、下記のようにする

.bashrcなどをいじらない指定(PRFILE=/dev/null)をしてインストール::

    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.0/install.sh | PROFILE=/dev/null bash

.bashrc などに以下の記述を追加::

    # ---------------------------
    # nvm 遅延ロード
    # ---------------------------
    # NVM の nvm.sh を遅延ロードしてシェルの起動を高速化する - Qiita
    # https://qiita.com/uasi/items/80865646607b966aedc8
    # ただし、nvm を一度起動するまで、node, npm, npx などが使えないので注意
    ### nvm original
    # export NVM_DIR="$HOME/.nvm"
    # [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
    export NVM_DIR="$HOME/.nvm"
    if [ -s "$NVM_DIR/nvm.sh" ] ; then
        nvm() {
            unset -f nvm
            source "${NVM_DIR}/nvm.sh"
            nvm "$@"
        }
    fi

ターミナルを開き直すなどして、.bashrc を読み込む。

これで、ターミナルを開いてもすぐには nvm.sh は読み込まれず、初回のnvmの実行のときに読み込まれるようになる。
ただし、それまで、node, npm, npx などが使えないので注意。

確認(nvm.shを呼んだ後)::

    command -v nvm

コマンド概要
------------------

- ``nvm use <version>`` をすることで、PATHなどに該当バージョンのnode,npm,npxが追加される。
- nvm.sh を呼んだ直後は、 ``default`` の alias が張られているバージョンで、PATHなどの環境変数がセットされる。(nvm useしてもaliasは変わらない)
- 初めてインストールしたバージョンに、自動的に ``default`` の alias が張られるっぽい。

::

    nvm --help     # ヘルプ表示

    # node.js のバージョンの 一覧を確認 (時間がかかるので LTS のみにしている)
    nvm ls-remote --lts

    # node.js の特定のバージョンをインストール
    nvm install v10.22.1

    # インストールされているものとaliasを確認
    nvm ls
        ->     v10.22.1
               v10.23.0
        default -> v10.22.1
        node -> stable (-> v10.23.0) (default)
        stable -> 10.23 (-> v10.23.0) (default)
        iojs -> N/A (default)
        unstable -> N/A (default)
        lts/* -> lts/fermium (-> N/A)
        lts/argon -> v4.9.1 (-> N/A)
        lts/boron -> v6.17.1 (-> N/A)
        lts/carbon -> v8.17.0 (-> N/A)
        lts/dubnium -> v10.23.0
        lts/erbium -> v12.19.1 (-> N/A)
        lts/fermium -> v14.15.1 (-> N/A)

    nvm ls --no-alias

    nvm alias [<pattern>]        # 表示
    nvm alias <name> <version>   # alias を張る

    nvm use <version>              # PATH環境変数を切り替える
    nvm exec <version> <command>   # PATH環境変数をセットした環境でコマンドを実行
    nvm run <version> [<args>]     # PATH環境変数をセットした環境で node コマンドを実行


    # 今使われる node のバージョンなどを確認
    nvm current
    which node
    which npm
    which npx
    node --version
    npm --version
    echo $PATH
    printenv | grep NVM


仕組み
------------------

nvmは、$HOME/.nvm 以下にインストールされる。

nvm install した各バージョンの node.js は、$HOME/.nvm/versions/node/ 以下に格納される。

nvm.sh でやっていることは

- nvm コマンドに相当するシェル関数を定義する (サブシェルには引き継がれない)
- 環境変数PATHに default alias 指すバージョンの node.js の bin を追加する

nvm use をやると

- 環境変数PATHに 指定バージョンの node.js の bin を追加or差し替えする

PATH以外にもいいくつかの環境変数をいじるらしい::

    NVM_BIN=/home/<username>/.nvm/versions/node/v10.22.1/bin
    NVM_INC=/home/<username>/.nvm/versions/node/v10.22.1/include/node
    PATH=/home/<username>/.nvm/versions/node/v10.22.1/bin:....

    MANPATH
    NODE_PATH
