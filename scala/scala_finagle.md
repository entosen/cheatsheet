
Finegle


## Future

https://twitter.github.io/util/docs/index.html#package
http://qiita.com/taketon_/items/f8757ae6c00b08aeb0c8

Futureの状態
- 未完了
- 成功
- 失敗


val f: Future

Future を作る
f = Future(response)    // これでいいのか？

値を取り出す
Await.result(f) → 成功:Futureの中の型、失敗:例外


### Future を返す関数側

```
def mySlowService(request: String): Future[String] = {
  ...
  // 問題が起こったときは、例外を投げる
  throw new HogehogeException("...")
  ...
  // 問題なく処理ができたときは、結果をFutureでくるんで返す
  Future("hogehoge")
}
```

### Futureを返す関数を呼び出す側

```
val myFuture = mySlowService(request)
val serviceResult = myFuture.get()
  // 未完了なら完了までブロックする
  // 成功なら、Futureの中身(つまり実行結果)を返す
  // 失敗なら、例外を投げる

```

flatMap で処理をつなげる



## http.Request
val request = http.Request(http.Method.Get, "/")
request.host = "www.scala-lang.org"

val request = RequestBuilder()
  .url("http://www.example.com/test")
  .addParameter("key", "value")   // this doesn't exist
  .buildGet()      // POSTの場合は .buildPost
request    // should be a GET request for http://www.example.com/test?key=value

.url(new URL("https", host, 443, path))
.buildPost(wrappedBuffer(payload))
.buildPost(Buf.Utf8(string))


値を取り出す

req.method: Method
    == Method.Get
    == Method.Post
req.uri: String   → パスとクエリストリングの部分
req.host: Option[String]
req.path: String
req.referer: Option[String]
req.remoteAddress: InetAddress
  req.remoteAddress.getHostAddress: String → Ipアドレス
  req.remoteAddress.getHostName: String → ホスト名
req.remoteHost: String (111.111.111.111形式の文字列)
req.userAgent: Option[String]

req.contentString: String
req.cookie: CookieMap



## http.Response

http://twitter.github.io/finagle/docs/#com.twitter.finagle.http.Status$

```
作る
http.Response(req.version, http.Status.Ok)
setContentString(s)

値を取り出す
res.statusCode: Int
res.statusCode == http.Status.Ok.code
res.status.reason     // "Bad Request"
res.getContentString: String
res.toString   //  Response("HTTP/1.1 Status(400)")

```
