===================================
npm
===================================

`npm Docs <https://docs.npmjs.com/>`__



コマンド
=====================

::

    // ls: list, ll, la でも同じ
    npm ls                 # 直接依存のものだけ
    npm ls --all           # ツリー状に再帰的に
    npm ls <package>       # そのパッケージに到る依存関係のみをツリー状に表示


    // インストール系
    npm install <package>         # パッケージをアプリにインストールする
    npm install <package> -g      # パッケージをグローバルにインストールする
    npm install <package> -D      # devDependecies としてパッケージをアプリにインストールする

    // run系
    npm run コマンド名            # package.json に登録したコマンドを実行する。
                                  # start や test など一部のコマンド名は run キーワードを省略可能

    npm audit                     # パッケージの脆弱性を確認する

    npm publish                   # レポジトリにパッケージを公開する

    npm init                      # package.json を初期化する


package.json
=======================

TODO サンプル

package.json のバージョン指定
-------------------------------

数字3つの、いわゆるセマンティックバージョニング。

major . minor . patch

- major: 過去と互換性がない変更
- minor: 後方互換性のある機能追加、古い機能の削除、大きなリファクタリング
- patch: bug fixes


※下記ではわかりやすさのため、範囲の最大を ``9999`` で示している。
(厳密には桁上がりして lt する)

::

    {
      "dependencies": {

        "sample": "1.0.0",     // 厳密に同じバージョン
        "sample": ">=1.0.0",   // 不等号 (>, >=, <, <=)
        "sample": ">=1.0.2 <2.1.2",   // 複数の不等号をANDで。
        "sample": "1.0.0 - 1.2.4",   // 範囲指定。後端も含む。 1.0.0 <= x <= 1.2.4
 
        // *,x はワイルドカード
        "sample": "*",        // あらゆるバージョン
        "sample": "",         // あらゆるバージョン
        "sample": "1.x.x",    // 1.0.0 - 1.9999.9999
 
        // ^ は、指定バージョン以上で、一番左の0以外の数字のバージョンを更新しないような、更新が可能
        // (覚え方) ハット→頭を守る
        "sample": "^1.2.3",   // 1.2.3 - 1.9999.9999
        "sample": "^0.2.3",   // 0.2.3 - 0.2.9999
        "sample": "^0.0.3",   // 0.0.3

        // ~ 
        // minor version が指定されている場合
        // 指定バージョン以上、patch-level の更新のみ許容する
        // (覚え方) しっぽ。しっぽが上がるのはかまわない。
        "sample": "~1.2.3",   // 1.2.3 - 1.2.9999
        "sample": "~1.2",     // 1.2.0 - 1.2.9999
        // minor version が指定されていない場合
        // 指定バージョン以上、minor-level までの更新のみ許容する
        "sample": "~1",      // 1.0.0 - 1.9999.9999

        // ORも書ける
        "qux": "<1.0.0 || >=2.3.1 <2.4.5 || >=2.5.2 <3.0.0",
      }
    }

厳密には下記を参照のこと

- https://docs.npmjs.com/cli/v8/configuring-npm/package-json#dependencies
- https://github.com/npm/node-semver

