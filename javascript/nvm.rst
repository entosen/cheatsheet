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

    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

    (SHELL環境変数に応じて) .bashrc, .zshrc どちらかに以下のような記述が挿入される。
        export NVM_DIR="$HOME/.nvm"
        [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
        [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

    この記述があることで、nvm コマンドが使えるのと、現在有効になっているnpmへパスが通る


ただし、この nvm.sh が WSL1 環境だとやたら重い(10秒ほど)。

シェルを開くたびに毎度10秒固まっては困るので、下記のようにする

.bashrcなどをいじらない指定(PRFILE=/dev/null)をしてインストール::

    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | PROFILE=/dev/null bash

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
- ``nvm use`` とだけやった場合は、カレントディレクトリから上で ``.nvmrc`` を探し、そこに記載のバージョンが使われる
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


普通は、node と npm がセットで入る(例えば、 node-v14系 と npm-6系 がセットで入る)。
もし、npmだけそれよりも新しいものを使いたい場合、下記どちらかで ::

    # 現在のnode環境の npmを、その環境をサポートしている最新の npm にアップグレードする
    nvm install-latest-npm

    # インストール時に --latest-npm を付けると、インストール作業後に npm を最新にする
    nvm install --latest-npm <version>

※上記 ``nvm install-latest-npm`` が WSL1 の環境だと下記のようになり、
うまくいかなかった。::

    Attempting to upgrade to the latest working version of npm...
    * Installing latest `npm`; if this does not work on your node version, please report a bug!
    npm ERR! code EACCES
    npm ERR! syscall rename
    npm ERR! path /home/<username>/.nvm/versions/node/v14.18.2/lib/node_modules/.staging/npm-6e367097/node_modules/string-width
    npm ERR! dest /home/<username>/.nvm/versions/node/v14.18.2/lib/node_modules/.staging/string-width-fb5376b2
    npm ERR! errno -13
    npm ERR! Error: EACCES: permission denied, rename '/home/<username>/.nvm/versions/node/v14.18.2/lib/node_modules/.staging/npm-6e367097/node_modules/string-width' -> '/home/<username>/.nvm/versions/node/v14.18.2/lib/node_modules/.staging/string-width-fb5376b2'
    npm ERR!  [OperationalError: EACCES: permission denied, rename '/home/<username>/.nvm/versions/node/v14.18.2/lib/node_modules/.staging/npm-6e367097/node_modules/string-width' -> '/home/<username>/.nvm/versions/node/v14.18.2/lib/node_modules/.staging/string-width-fb5376b2'] {
    npm ERR!   cause: [Error: EACCES: permission denied, rename '/home/<username>/.nvm/versions/node/v14.18.2/lib/node_modules/.staging/npm-6e367097/node_modules/string-width' -> '/home/<username>/.nvm/versions/node/v14.18.2/lib/node_modules/.staging/string-width-fb5376b2'] {
    npm ERR!     errno: -13,
    npm ERR!     code: 'EACCES',
    npm ERR!     syscall: 'rename',
    npm ERR!     path: '/home/<username>/.nvm/versions/node/v14.18.2/lib/node_modules/.staging/npm-6e367097/node_modules/string-width',
    npm ERR!     dest: '/home/<username>/.nvm/versions/node/v14.18.2/lib/node_modules/.staging/string-width-fb5376b2'
    npm ERR!   },
    npm ERR!   errno: -13,
    npm ERR!   code: 'EACCES',
    npm ERR!   syscall: 'rename',
    npm ERR!   path: '/home/<username>/.nvm/versions/node/v14.18.2/lib/node_modules/.staging/npm-6e367097/node_modules/string-width',
    npm ERR!   dest: '/home/<username>/.nvm/versions/node/v14.18.2/lib/node_modules/.staging/string-width-fb5376b2'
    npm ERR! }
    npm ERR! 
    npm ERR! The operation was rejected by your operating system.
    npm ERR! It is likely you do not have the permissions to access this file as the current user
    npm ERR! 
    npm ERR! If you believe this might be a permissions issue, please double-check the
    npm ERR! permissions of the file and its containing directories, or try running
    npm ERR! the command again as root/Administrator.

    npm ERR! A complete log of this run can be found in:
    npm ERR!     /home/<username>/.npm/_logs/2021-12-01T04_29_17_648Z-debug.log



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
