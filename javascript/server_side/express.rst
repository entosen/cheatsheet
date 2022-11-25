=======================================
express
=======================================





express と nodejs の httpモジュール は違う？


::

    GET
        パスパラメータ
        クエリパラーメタ
    POST
        body   map型っぽくなっている？


::

    res.status(403)    // レスポンス ステータスの指定

    res.set('Content-Type', 'text/plan')   // レスポンスヘッダ

    実際にレスポンスを返すメソッド
        1つの通信で1度しか呼べない。
        res.send(body)   // 文字列を送信。 object,array の場合は JSON文字列化して送信。
        res.json(obj)    // オブジェクトをJSON文字列にして送信
        res.end()        // なにも返さない

    ルーティング
        Application もしくは Router でやる。



    ミドルウェア
        app.use( (req, res, next) => {} )

        express.json
        express.urlencoded


    get,post などと use の順番。あと、path指定の部分。
    どいういう風に影響範囲が決まる？
        1列に並んでる？？？？


        app.use()→コールバックは1つだけかかります。
        app.all()→複数のコールバックを取ることができます。

        app.use()は、urlが指定されたパスで始まるかどうかのみを確認します。
        しかし、app.all()は完全なパスに一致します。


tips

エラーをキャッチしてエラー処理するラッパー。

::

    module.exports =  asyncMiddleware = fn =>
        (req, res, next) => {
            Promise.resolve(fn(req, res, next))
                .catch(next);
        };






