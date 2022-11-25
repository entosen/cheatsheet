####################################
Node.js 
####################################

Node用に提供されているAPIについてまとめる。


*************************
モジュール
*************************

モジュール ＝ Javascriptのファイル？

下記3種類がある。

- coreモジュール

  - node.js で用意されているもの
  - ``/``, ``./``, ``../`` いずれでも始まらない。
  - fs, os, http, child_process
  - グローバル(requireしなくても使えるもの)とそうでないものがある

    - process, buffer, stream, url など

- fileモジュール

  - ``/``, ``./``, ``../`` いずれかで始まる
  - 相対パスで探索

- npmモジュール

  - コアモジュールではなく ``/``, ``./``, ``../`` いずれでも始まらない。
  - カレントディレクトリもしくは上位にある ``node_modules`` ディレクトリを探索




モジュールは任意の方の値をエクスポートすることができる。

- オブジェクトをエクスポートする
- 関数を1つエクスポートする
- カスタマイズ可能なもの (関数1つ返すパターンの1種。関数を1回呼ぶと使いたいものになる)



モジュールを使う側::

    // オブジェクトをエクスポートするもの。一般的には各プロパティが関数
    const calculator = require('./calculator.js')
    const v1 = calculator.func1(2,3)
    const v2 = calculator.func2(100)


    // 関数を1つだけエクスポートするもの。
    createError = require("http-errors")

    const calc = require('./calc.js');
    const v3 = calc(2,3)


    // カスタマイズ可能なもの
    const debug = require('debug')('main')

    const fsSync = require("fs")
    const fsAsync = require("fs").promises


エクスポートする側::

    // オブジェクトをエクスポートするもの。一般的には各プロパティが関数
    module.exports = {
        func1(a,b) {
            ...
        },
        func2(a) {
            ...
        },
    }

    // 関数を1つだけエクスポートするもの。
    module.exports = function() {...}


    // カスタマイズ可能なもの。1枚関数でラップしている
    module.exports = function(prefix) {
        return function(message) {
            console.log(`${prefix} ${message}`)
        }
    }

    // TODO require("fs").promises のやつ



知っておくとよいこと

- module.exports は、最初は空オブジェクトが入っている。
- export は、module.exports (が最初に指している空オブジェクト) への参照が入っている
- 分かって使うのはよいが、基本的には混ぜるな。


インポート(require関数)は、Nodeアプリが起動したときに1回だけインポートして、2回目以降は使い回す。
cf.カスタマイズの部分は都度実行される。




************
TODO
************

オライリーの初めてのJavascript 20章

- fs
- process
- path
- os
- child_process
- stream
- http



::

    fs.readFileSync(filepath)
    fs.readFile(filepath, cb)


    http client の作り方
    http.get
        on(イベント, cb)
            'data'
            'end'
            'error'
        pipe(...)


    http server の作り方
        net.createServer(...)   // これは http ではなく、TCPレベルのサーバ
        http.createServer(...)

        res.writeHead(200, {'Content-Type': 'application/json'})
        res.end(body)

    url

