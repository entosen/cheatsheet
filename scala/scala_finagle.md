
Finegle


## Future

https://twitter.github.io/util/docs/index.html#package

val f: Future

�l�����o��
Await.result(f) �� ����:Future�̒��̌^�A���s:��O






## http.Request
val request = http.Request(http.Method.Get, "/")
request.host = "www.scala-lang.org"

val request = RequestBuilder()
  .url("http://www.example.com/test")
  .addParameter("key", "value")   // this doesn't exist
  .buildGet()      // POST�̏ꍇ�� .buildPost
request    // should be a GET request for http://www.example.com/test?key=value

.url(new URL("https", host, 443, path))
.buildPost(wrappedBuffer(payload))
.buildPost(Buf.Utf8(string))


�l�����o��

req.method: Method
    == Method.Get
    == Method.Post
req.uri: String   �� �p�X�ƃN�G���X�g�����O�̕���
req.host: Option[String]
req.path: String
req.referer: Option[String]
req.remoteAddress: InetAddress
  req.remoteAddress.getHostAddress: String �� Ip�A�h���X
  req.remoteAddress.getHostName: String �� �z�X�g��
req.remoteHost: String (111.111.111.111�`���̕�����)
req.userAgent: Option[String]

req.contentString: String
req.cookie: CookieMap



## http.Response

http://twitter.github.io/finagle/docs/#com.twitter.finagle.http.Status$

```
���
http.Response(req.version, http.Status.Ok)
setContentString(s)

�l�����o��
res.statusCode: Int
res.statusCode == http.Status.Ok.code
res.status.reason     // "Bad Request"
res.getContentString: String
res.toString   //  Response("HTTP/1.1 Status(400)")

```
