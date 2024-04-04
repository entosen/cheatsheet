===================================
corepack
===================================

パッケージマネージャ (npm, pnpm, yarnなど) を管理(バージョンの選択、インストール)するツール。

- プロジェクトで指定したパッケージマネージャー・バージョンを自動で取得し使わせることができる
- 指定した以外のパッケージマネージャの使用を禁止することができる

corepack は、pnpm, yarn などと同名コマンド(shim)を作ることで、コマンド呼び出しを横取りして動作する。

実現すること

- どのパッケージマネージャ、どのバージョンを使うかを決定する
- 必要ならダウンロード
- 本物コマンドを起動
- 指定した以外のパッケージマネージャーを起動した場合は、エラーにし、使うべきパッケージマネージャを教えてくれる

例

package.json に ::

    {
      "packageManager": "yarn@2.0.0-rc.29"
    }

と書いておけば、yarn コマンドを打つと、勝手に裏で yarn@2.0.0-rc.29 がインストールされてから実行される。

それ以外の例えば pnpm を打つと、エラーになる。



参照ドキュメント

- https://nodejs.org/api/corepack.html
- https://github.com/nodejs/corepack
- `corepack is 何? <https://zenn.dev/teppeis/articles/2021-05-corepack>`__



インストール
================

corepack コマンド自体は、Node.js v14.19.0 以上では標準でバンドルされるようになっている。

nodenv で Node.js (最近のやつ) を入れたら corepack コマンドは使える状態になっていた。

::

    corepack enable
    corepack enable npm  

``corepack enable`` は、そのnodeコマンドと同じディレクトリに、yarn, pnpm などのシンボリックリンクを作成する。

そのため、 nodenv で複数バージョンの node.js が存在場合には、今使っているnode.jsバージョンにしか効かないので注意。

また、 nodenv を使っている場合は、場合によっては ``nodenv rehash`` も必要になる。


コマンド
================

注

- corepack における「インストール」とは、実質は、ダウンロードしてきてキャッシュディレクトリに保存すること。
- corepack-0.20.0 からCLIが結構変わっている (`#291 <https://github.com/nodejs/corepack/issues/291>`__)

::

    corepack -h        # ヘルプ
    corepack -v        # バージョン表示

    corepack enable

        (そのnodeバージョンで) corepack を有効にする(yarnとpnpm)。
        具体的には、yarn と pnpm に対し、同名のcorepackのshimを配置することで、corepackの管理下に置く。

        shim は which corepack と同じディレクトリに配置される。
        そのため、nodenvなどで複数バージョンのnodeがある場合には、今呼んでいるnodeバージョンにしか反映しない。

        nodenv を使っている場合、この後に nodenv rehash をやらないとバイナリが見えないことがあるので注意。

    corepack enable npm

        npm も corepack の管理下にする。これにより、
        - npm のバージョン指定やダウンロードがcorepackの仕組みで行われる
        - 別のパッケージマネージャを指定しているときに npm を呼ぶとエラーになるようになる。

    corepack disable   # enable の反対。shim を削除する


    corepack use 'yarn'    
    corepack use 'npm@10.4.0'    
    corepack use 'pnpm@7.x'    
    corepack use 'yarn@*'

        package.json の packageManager の項目に書き込む。
        - バージョンのrange指定を満たす最新リリースのバージョン番号を取得し、
        - それを package.json の packageManager の項目に書き込む。(ハッシュ値も付けてくれる)
        - 同時に指定バージョンをダウンロード、インストール。

    corepack up

        package.json の packageManager の項目を、
        既存の値と同じメジャーバージョンで最新のものに更新する。
        同時にそのバージョンをダウンロード、インストール。

    corepack install 

        package.json の packageManager の設定に従い、
        該当のパッケージマネージャ・バージョン をダウンロード、インストール。
        通常は yarn などの実行で自動でインストールはされるので、
        このコマンドを直接叩くことはなさそう。

    corepack intall -g 'yarn@^1'

        指定したパッケージマネージャーをダウンロード、インストール。
        さらに、lastKnownGood.json をそのバージョンで更新。
        これにより、package.json が見つからない or packageManager が未指定 の環境で
        npm, yarn, pnpm を呼んだときのバージョンは、このコマンドで指定したものになる。

    corepack cache clean    # (0.25.0以降のみ) キャッシュを削除。(lastKnownGool.jsonは残る)
    corepack cache clear    # 同上

    corepack prepare yarn@1.22.9 --activate
        0.20.0 で deprecated になっている。
        おそらく corepack install -g yarn@1.22.0 と同じ = lastKnownGood.json に書き込む。


``corepack enable`` をやっておけば、
yarn, yarnpkg, pnpm, pnpx を実行したときに、必要なら該当バージョンが自動でダウンロードされる。
(npm は対象外なので、同様にしたいのであれば、さらに ``corepack enable npm`` が必要。)


どのパッケージマネージャ・バージョンが使われるか
=========================================================


- package.json に "packageManager" の指定がある場合

  - そのパッケージマネージャ・バージョンを使う。必要ならダウンロード・インストールする。
  - それ以外のパッケージマネージャが呼ばれた場合には、エラーにして、メッセージを出す

- package.json に "packageManager" の指定がない場合

  - 呼んだコマンドのパッケージマネージャを使う
  - バージョンは

    - ``~/.cache/node/corepack/lastKnownGood.json`` に記載の、パッケージマネージャーごとのバージョン
    - (``COREPACK_DEFAULT_TO_LATEST=0 にしない限り``) npmレジストリでそのパッケージマネージャの最新のバージョンを調べる
    - (``COREPACK_DEFAULT_TO_LATEST=0 の場合``) `ハードコード <https://github.com/nodejs/corepack/blob/main/config.json>`__ された、パッケージマネージャーごとのデフォルトバージョン



仕組み
=============

shims
-------------

バイナリプロキシになっているらしい。nodenvみたいな。

PATHの前の方にいて、npm, pnpm, yarn などのコマンドを横取り、適切なバージョンの本物コマンドを起動する。

やっていること

- どのパッケージマネージャ、どのバージョンを使うかを決定する
- 必要ならダウンロード
- 本物コマンドを起動


``corepack enable`` をすると、node コマンドと同じディレクトリに、
対応パッケージマネージャ(yarn, pnpm)のコマンドと同名のシンボリックリンクが作られる。::

    % ls -l ~/.nodenv/versions/20.11.0/bin/

    corepack@ -> ../lib/node_modules/corepack/dist/corepack.js
    node*
    npm@ -> ../lib/node_modules/npm/bin/npm-cli.js
    npx@ -> ../lib/node_modules/npm/bin/npx-cli.js
    pnpm@ -> ../lib/node_modules/corepack/dist/pnpm.js         # これ
    pnpx@ -> ../lib/node_modules/corepack/dist/pnpx.js         # これ
    yarn@ -> ../lib/node_modules/corepack/dist/yarn.js         # これ
    yarnpkg@ -> ../lib/node_modules/corepack/dist/yarnpkg.js   # これ

さらに ``corepack enable npm`` をすると、npm もシンボリックリンクに置き換えられる::

    npm@ -> ../lib/node_modules/corepack/dist/npm.js           # これ
    npx@ -> ../lib/node_modules/corepack/dist/npx.js           # これ

   
これによって、これらのコマンドを corepack が一旦横取りする。


cacheディレクトリ
---------------------------

実際のバージョンが入るディレクトリは、 ``~/.cache/node/corepack/`` ::

上で「インストール」とか「ダウンロード」とか言っていたものは、ここに入る。


corepack-0.25.0 以降::

    ~/.cache/node/corepack/
        lastKnownGood.json
        v1/
            npm/
                10.4.0/
                10.5.0/
            pnpm/
                8.15.5/
            yarn/
                1.22.22/
        

corepack-0.25.0 未満::

    ~/.cache/node/corepack/
        lastKnownGood.json
        npm/
            10.4.0/
            10.5.0/
        pnpm/
            8.15.5/
        yarn/
            1.22.22/
        
Known Good Releases
----------------------------

各パッケージマネージャで、バージョン未指定の場合にデフォルトで使うバージョンを保持する。

- 場所は ``~/.cache/node/corepack/lastKnownGood.json`` にある。
- ユーザーで1つなので、nodeバージョンによらず、全体に効く。

例::

    {
      "pnpm": "8.15.5+sha1.a58c038faac410c947dbdb93eb30994037d0fce2",
      "yarn": "1.22.22+sha1.ac34549e6aa8e7ead463a7407e1c7390f61a6610",
      "npm": "10.5.0+sha1.726f91df5b1b14d9637c8819d7e71cb873c395a1"
    }

lastKnownGood.json に書き込むタイミング。

参考 → https://github.com/nodejs/corepack/tree/main?tab=readme-ov-file#known-good-releases

- 各パッケージマネージャの最新バージョンをnpmレジストリで調べたとき

  - (普通に使っているだけで、このバージョンチェックは行われているようだ)
  - lastKnownGood.json にまだ指定無しの場合、その最新バージョンで追加される

- ``corepack install -g <spec>`` を実行したとき

  - lastKnownGood.json を指定した値で強制的に更新する

- lastKnownGood.json に既に記載のバージョンに対し、メジャーバージョンは同じで、より新しいバージョンをダウンロードしたとき
  (0.25.0以降 `#364 <https://github.com/nodejs/corepack/issues/364>`__)

  - その値に更新する
  - corepack use で、lastKnownGoal.json より新しいバージョンを指定した場合など。




package.json の packageManager 値
----------------------------------------

::

    {
      "packageManager": "npm@10.5.0+sha256.17ca6e08e7633b624e8f870db81a78f46afe119de62bcaf0a7407574139198fc"
    }

``corepack use npm@10.5.0`` などとすると、package.json の packageManager 値を書き換えてくれる。

corepack-0.26.0 以降では、package.json に packageManager 値が未指定の場合は、
自動的に(勝手に)値を足してくれるようになる。
(`#413 <https://github.com/nodejs/corepack/issues/413>`__)
