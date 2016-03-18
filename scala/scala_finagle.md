
Finegle


## Future

https://twitter.github.io/util/docs/index.html#package

val f: Future

値を取り出す
Await.result(f) → 成功:Futureの中の型、失敗:例外






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
