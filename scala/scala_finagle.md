
Finegle


## Future

https://twitter.github.io/util/docs/index.html#package
http://qiita.com/taketon_/items/f8757ae6c00b08aeb0c8

Futureの状態
- 未完了
- 成功
- 失敗


### Futureを返す(生成する)方法

```
// やりたい処理(失敗するかもしれない処理)全体を Future の apply で囲う。
val f = Future {
    やりたい処理
    失敗なら例外を投げる。
    成功なら値を返す。
}

// 以下ではだめ。(例外がFutureの外にあり、捕捉されない)
def hoge(i: Int): Future[Int] = {
    ...
    Future(999)
}
```

【注】
com.twitter.util.Future の apply は非同期実行(並列実行)してくれない。
並列実装したいときは、後述の FuturePool を使う。


その他テスト時などに便利な生成方法

```
// 固定値のFutureを作る
Future.value[Int](10)
Future.exception[Int](new IlligalArgumentException("hoge"))

// Promiseは 1回だけsetすることができる Future
val pr = new Promise[Int] // この状態ではまだ未確定
pr.setValue(100) // 成功値で確定

val prex = new Promise[Int]
prex.setException(new IlligalArgumentException("hoge")) // 失敗値で確定
```

### Futureの基本操作

```
// 値が確定しているかのチェック(Boolean)
f.isDefined
// 値を取り出す
Await.result(f) // 確定するまでブロック。 成功:Futureの中の型、失敗:例外

// 成功時に起動される処理を登録する。引数は Future の中身の型
f.onSuccess( (i) => { ... } )
// 失敗時に起動される処理を登録する。引数は Exception 
f.onFailure( (ex) => { ... } )
// どちらも、関数の戻り値は Unit 型のため、
// これらにより Future の中身を変えたりすることはできない。
// なので、あまり使い所は多くない。
```

### 処理の連鎖

前段の処理が成功したときだけ、後段を実行する
```
// flatMap でつなげる
val f1: Future[A] = Future(処理1 Aを返す)
val f2: Future[B] = f1.flatMap( Aを受け取ってFuture[B] を返す )
Await.result(f2) // B もしくは例外

// Map でつなげる
val f1: Future[A] = Future(処理1 Aを返す)
val f2: Future[B] = f1.Map( Aを受け取ってB を返す )
Await.result(f2) // B もしくは例外

// for でやる (flatMapと同等)
val f = for {
  u <- authenticate(request) // 右辺はFuture。uはその中身が入る。
  b <- isBanned(u)  // 右辺はFuture。 b にはその中身が入る。
} yield (u, b)    // これが Futureに包まれて返る。
```

前段の処理が失敗したときに、リカバーする処理に連鎖する。

```
val f1: Future[A] = Future(Aを返す処理)
val rescueFunc: PartialFunction[Throwable, Future[A]] = {
  case ex: IndexOutOfBoundsException => Future {
    ...
    代替の値を返す
  }
}
val f2 = f1.rescue(rescueFunc)
```

### 複数のFutureを扱う(並列に複数の処理を動かすため)

- 1つでもエラーが発生したら全体をエラー扱いにする → collect, join
- いくつかエラーが発生しても全てのFutureが完了していることを保証したい → collectToTry, Await.all

#### Future.collect と Futue.join

```
// Future.collect は、同じ型のFutureのSeq をひとまとめにする。結果はSeqで返る
val fs: Seq[Future[A]] = Seq(...)
val f = Future.collect(fs)  // f の型は Future[Seq[A]]

// Future.join は、異なる型のFutureをひとまとめにする。結果はタプルで返る
val f1: Future[A] = ...
val f2: Future[B] = ...
val f3: Future[C] = ...
val f = Future.join(f1, f2, f3) // fの型は Future[(A,B,C)]
```

collectやjoinでまとめたFutureは、
- 全てのFutureが成功で完了してはじめて、成功で完了
- どれかのFutureが失敗すると、その時点で即座に失敗で完了
  (成功した部分があったとしても結果を取れない。)

#### Future.collectToTry

collectToTry でまとめたFutureは、
どれかで例外が発生したとしても、全Futureが終了するまで、完了しない
```
// Future.collect は、同じ型のFutureのSeq をひとまとめにする。結果はTryのSeqで返る
val fs: Seq[Future[A]] = Seq(...)
val f = Future.collectToTry(fs)  // f の型は Future[Seq[Try[A]]]

val result = Await.result(f)
val try0 = result.head
try0.isReturn // 成功していたらtrue
try0.isThrow  // 失敗していたらtrue
try0.get // 成功していたら値が取れる、失敗していたら例外が飛ぶ
```

#### Await.all

とにかく全Futureが完了になるまで待つ。戻り型は Unit。

Seq で渡さないといけないが、どうせ戻り型がUnitなので、Seq[Future[Any]]にキャストすれば、型違いのFutureでも渡せるはず。

```
import com.twitter.conversions.time._
Await.all(Seq(f1, f2, f3), 1.seconds)
// もしくは可変長引数のバージョン(こちらはtimeoutの指定が不要・不可)
Await.all(f1, f2, f3)
Await.all(Seq(f1, f2, f3): _*)
```

#### Future.select

```
// Future.select は
// どれか１つが(成功・失敗問わず)完了するという状態を表すFutureが返る。
val fs: Seq[Future[A]] = Seq(...)
val f1 = Future.select(fs) 

// どれか1つが完了すると
// 完了したFutureに対応する Try[A] と、残りの Seq[Future[A]] が返る
val (try1, remainders1) = Await.result(f1)
val result1 = try1.get  // Try[A]型なので、値を得るためには get が必要

// remainders は Seq[Future[A]] 型なので、
// 再度 select に渡すことを繰り返すことで、順に処理できる。
val f2 = Furure.select(remainders1) 
```

ここで、Try[A] 型について

- Try[A] は Return[A] と Throw[A] の共通の親クラス
  - Return[A] は成功を表す
  - Throw[A] は失敗を表す

```
val try1: Try[A] = ...

try1.isReturn // R:true, T:false
try1.isThrow  // R:false, T:true
try1.apply() // R:値を返す、T:例外を投げる
try1.get()   
try1.getOrElse(default: A)  // R:値を返す、T:defaultを返す
```




### 並列実行 ThreadPool

twitter の `Future { 処理 }` は、どちらかというと抽象的なIF実装という側面が強く、
処理を別スレッドで実行してくれない(処理が終わって始めいてFutureが返ってくる)。

別スレッドで実行するためには、FuturePoolインスタンスを使う。
使い方の例は、FuturePool のテストを参照。→ [FuturePoolTest.scala](https://github.com/twitter/util/blob/af1fbc7af36a755117fd2b4dca8bd3fac825363d/util-core/src/test/scala/com/twitter/util/FuturePoolTest.scala)

すごく簡単に書くと。

```scala
val executor = Executors.newFixedThreadPool(1)
val pool = FuturePool(executor)

val f = pool { やりたい処理 }
```

- executor: java.util.concurrent.ExecutorService
  - javaの世界で thread を生成して処理を行わせるためのIF。
- pool: FuturePool
  - 上述のjavaの世界のExecutorServiceを、Scalaの twitter.Future の世界に合うようにラップするクラス。

#### java の ExecutorService

クラス図
    TODO

[ExcutorService](http://docs.oracle.com/javase/jp/8/docs/api/java/util/concurrent/ExecutorService.html)
インターフェース。Threadをプールしておいて使い回すことを想定したIF。

- 処理を開始する submitメソッド。
- プール全体を解放する shutdown, shutdownNowメソッド

このIFを実装したクラスとして以下がある。基本は ThreadPoolExecutor 。

- ThreadPoolExecutor: スレッドのプール
- ScheduledThreadPoolExecutor: スケジュール予約実行機能(一定時間後に実行、一定間隔で繰り返し実行)ができる
- ForkJoinPoll: ForkJoinTask用。軽量で速いけれど制限がある。純粋な計算だけのような処理に向いている。

ThreadPoolExecutorは、カスタマイズできるパラメータがコンストラクタ引数として提供されている。
詳細は [ThreadPoolExecutorのjavadoc](http://docs.oracle.com/javase/jp/8/docs/api/java/util/concurrent/ThreadPoolExecutor.html)
に記載があるので、理解しておく。
以下で挙げている各デフォルト構成のThreadPoolの違いを理解するためにも、理解しておくとよい。

通常使用するケースにおいては、ThreadPoolExecutor を直接newするのではなく、
Executorsのファクトリーメソッドを使うことで、取得できる。

```
// ThreadPoolExecutor(int corePoolSize, int maximumPoolSize, 
//                    long keepAliveTime, TimeUnit unit, 
//                    BlockingQueue<Runnable> workQueue)

public static ExecutorService newFixedThreadPool(int nThreads) {
    return new ThreadPoolExecutor(nThreads, nThreads,
				  0L, TimeUnit.MILLISECONDS,
				  new LinkedBlockingQueue<Runnable>());
}
→ 指定したスレッド数をプールし、それを使い回す。
   (実際は最初からn個あるのではなく、最初のn回でnスレッド起動される)
   待ちタスクが入るキューは無制限

public static ExecutorService newSingleThreadExecutor() {
    return new FinalizableDelegatedExecutorService
	(new ThreadPoolExecutor(1, 1,
				0L, TimeUnit.MILLISECONDS,
				new LinkedBlockingQueue<Runnable>()));
}
→ スレッドは１つしか生成せず、それを使い回す。
   待ちタスクが入るキューは無制限。

public static ExecutorService newCachedThreadPool() {
    return new ThreadPoolExecutor(0, Integer.MAX_VALUE,
				  60L, TimeUnit.SECONDS,
				  new SynchronousQueue<Runnable>());
}
→ 必要に応じて、上限なしにスレッドが生成される。
   処理済みでアイドル状態のスレッドがあれば、それを使い回す。
   60秒間アイドル状態が続くスレッドは解放される。
```



#### scala twitter の FuturePool

クラス図


ソースコード
https://github.com/twitter/util/blob/master/util-core/src/main/scala/com/twitter/util/FuturePool.scala

interruptibleとは
https://twitter.github.io/util/docs/index.html#com.twitter.util.Future@interruptible():com.twitter.util.Future[A]

- ExecutorServiceFuturePool は、
    - worker thred が既に動き出していたら、Futureにinterrupted があっても worker thread は interrupted されない。
- InterruptibleExecutorServiceFuturePool は、
    - worker thred が既に動き出していたら、Futureにinterrupted があったら worker thread に interrupted が伝播される。

ちょっとよくわかっていない...。


FuturePool の作り方。

java側の ThreadPoolExecutor を引数に渡して
```
val pool = FuturePool(executor)
もしくは
val pool = FuturePool.interruptible(executor)
```

予め用意されている FuturePool
https://twitter.github.io/util/docs/index.html#com.twitter.util.FuturePool$
  - FuturePool.unboundedPool
	 - java.util.concurrent.Executors.newCachedThreadPool を利用
  - FuturePool.interruptibleUnboundedPool
	 - java.util.concurrent.Executors.newCachedThreadPool を利用(interruptible版)
  - FuturePool.immediatePool
	 - ExecutorService を使わず、単に Future で囲んで返す(並列実行しない)





## http.Request


```
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
```


値を取り出す

```
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
```



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
