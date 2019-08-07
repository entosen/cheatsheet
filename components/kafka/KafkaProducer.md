
kafka Producer についてまとめる。

(諸事情により 0.8.2。さっさとバージョンあげよう)


## 参考にしたもの

- Kafka Producer の API ドキュメント
    - http://kafka.apache.org/082/javadoc/org/apache/kafka/clients/producer/KafkaProducer.html
        - これの冒頭、および、sendメソッド
    - http://kafka.apache.org/082/javadoc/org/apache/kafka/clients/producer/Callback.html
- Kafka のドキュメント 0.8.2 https://kafka.apache.org/082/documentation.html
    - その日本語訳 http://mogile.web.fc2.com/kafka/documentation.html
- 図
    - https://www.slideshare.net/gwenshap/kafka-reliability-when-it-absolutely-positively-has-to-be-there
    - https://www.slideshare.net/ConfluentInc/reliability-guarantees-for-apache-kafka
    - https://www.slideshare.net/JiangjieQin/producer-performance-tuning-for-apache-kafka-6314760



## Kafka Producer のAPIドキュメントから

### 概要

この producer はスレッドセーフです。
一般的に、最大限性能を出すためには全てのスレッドで1つのプロデューサーを共有すべき。

プロデューサーは単一のバックグラウンドスレッドを持ち、
それが I/O およびブローカーとコミュニケーションするための TCP コネクションを保持します。
プロデューサーを使用後に close し忘れると、リソースリークに繋がります。




### sendメソッド

非同期的に、レコードをトピックに送信し、送信が到達完了した際に渡されたコールバックを起動します。

送信は非同期に行われるので、このメソッドはレコードを送信待ちのバッファに格納した時点で即座にリターンします。
これにより、多くのレコードを、それぞれの返答を待つためにブロックすることなく、並行に送信することができます。

送信の結果は RecordMetadata で、これはレコードを実際に送信したパーティションとオフセットが格納されています。

sendの呼び出しは非同期なので、戻り値は RecordMetadata の Future となります。
この Future の get() を呼び出すことで、成功していれば Metadata が返され、
もしくは、失敗していた場合には何らかの例外が throw されます。

もし、単純なブロッキング型の呼び出しをやりたい場合は、以下のように Future を get() することでできます
```
producer.send(new ProducerRecord<byte[],byte[]>("the-topic", "key".getBytes(), "value".getBytes())).get();
```


完全にノンブロッキングな使い方を望む人は、Callback パラメータ を使うことができます。
このコールバックはリクエストが完了したときに呼び出されます。
コールバック関数は以下のような形をしています。

```
public void onCompletion(RecordMetadata metadata, Exception e){ }
```

- 成功時は `metadata != null` で `e == null`
- 失敗時は `metadata == null` で `e != null`


同じパーティションに向けられた複数のコールバックは、順序通りの実行が保証されます。

注意: コールバックは プロデューサーの I/Oスレッドで実行されるので、
コールバックの処理は適当に軽くするべき。
さもないと、他のスレッドから投入されたメッセージの送信が遅延するでしょう。
もし、ブロックしたり、計算量が多いコールバックを実行したいなら、
コールバックの中で独自の Executor を使い(訳注:別スレッドを生成し)、並列処理とすることをおすすめします。

プロデューサーは送信待ちのレコードのバッファを持っています。
このバッファはハードリミットがあり、それは設定(total.memory.bytes) で制御できます。
もし、I/Oスレッドがブローカーにデータを転送する量より速く send() が呼ばれると、
そのバッファーは、やがて足りなくなるでしょう。
その場合のデフォルトの挙動は、I/Oスレッドの処理が追いついてバッファに空きができるまで、
send() の呼び出しはブロックされます。
しかしながら、ノンブロッキングが望まれる場合には、block.on.buffer.full=false の設定をすることで、
バッファが足りない場合に、かわりに例外を投げるようになります。


## Kafka ドキュメントから

### 4.4 プロデューサー

#### ロードバランシング

プロデューサーはデータを、そのパーティションのリーダーになっているブローカーに、
他のルーティング機構の介入なく、直接送信します。
プロデューサーのこの動作を手助けするために、全てのKafkaノードは、
どのサーバーが生きているか、あるトピック・パーティションのリーダーとなっているのはどのサーバか、
についてのリクエストについて随時答えています。
これによりプロデューサーは適切なノードに直接通信することが可能になります。

メッセージをどのパーティションに送るかを決めるのはクライアントの仕事です。
これはある種のランダムなロードバランシングを実装することでランダムに行うか、
何らかのセマンティックなパーティション関数を使って行うことができます。
セマンティックなパーティショニングのために、キーを指定したり、それをハッシュとするインターフェースが用意されています。
(またそれらのパーティショニングの関数をユーザが上書きすることも可能です)

例えば、もし選択されたキーがユーザidであれば、指定されたユーザについての全てのデータは同じパーティションに送信されるでしょう。
コンシューマは、あるユーザの情報が単一のpartitionに入ってくるということを仮定できます。
このような locality-sensitive な処理をコンシューマで可能とするために、明確にこのようなデザインとしています。


#### 非同期send


Batching (訳注:まとめて一度に送信) は、効率の観点で大きな要素です。
Batchingを実現するために、Kafka producer は、データを一旦メモリに蓄積し、1つのリクエストで大きなひとかたまりとして送信しようとします。

この Batching機能は、蓄積するメッセージの個数の上限や待つ時間の上限を設定することができるようになっています。(64k ro 10ms)
これにより、より多くのメッセージを蓄積し、サーバ上でのI/O操作を少なくすることができます。

この buffering は設定可能であり、遅延時間とスループットのトレードオフを取ることができるようになります。


### 3.4 New Producer Configs

- bootstrap.servers
    - Kafkaクラスタへの初期の接続を確立するために使うホスト/ポートのペアのリスト。
      クライアントはブートストラッピングのためにここでどのサーバが指定されたかに関わらず全てのサーバを利用するでしょう。
      このリストはサーバの完全なセットを見つけるために使われる初期のホストにのみ影響を与えます。
      このリストはhost1:port1,host2:port2,...の形式でなければなりません。
      これらのサーバは完全なクラスタの会員(動的に変わるかも知れません)を見つけるための初期接続に使われるため、
      このリストはサーバの完全なセットを含む必要はありません (しかし、サーバがダウンした場合のために1つ以上が望まれるかも知れません)。
- acks
    - プロデューサーがリーダーノードに要求する受信完了ackの数
    - acks=0 : 0に設定されるとプロデューサはサーバからの承認を全く待たないでしょう。
      レコードはソケットバッファに追加されるとすぐに、送信されたものと見なされます。
      この場合サーバがレコードを受け取ったかどうかの保証はできません。
      そしてretries 設定は効果が無いでしょう (クライアントは一般的に障害を知らないため)。
      各レコードについて返されるオフセットは常に -1 に設定されるでしょう。
    - acks=1 これは、リーダーはレコードをローカルログに書き込むが、すべてのフォロワーからの完全な応答を待たずに応答するでしょう。
      この場合、リーダは通知の直後でフォロワーがリプリケートする前に失敗すべきで、その後レコードが喪失するでしょう。
    - acks=all これは、リーダーはレコードに応答するためにin-syncレプリカの完全なセットを待つだろうことを意味します。
      これは、少なくとも1つのin-syncレプリカが生きている限りレコードは失われないだろうことを保証します。これはもっとも強力な利用可能な保証です。これは acks=-1 設定と同じです。
- buffer.memory
    - プロデューサがサーバに送られるのを待っているレコードをバッファするために使うことができるメモリの総バイト数。
      サーバに配送することができるより早くレコードが入ってきた場合、block.on.buffer.full の設定に基づき、blockするか例外を投げるでしょう。
    - この設定は大まかにプロデューサが利用しようとする総メモリに対応しますが、
      プロデューサが使用する全てのメモリがバッファリングに使われるわけではないためハードバウンドではありません。
      いくつかの追加のメモリが圧縮(圧縮が有効な場合)と、やってきているリクエストを保持するために使われるでしょう。
- compression.type
    - プロデューサによって生成されるデータを圧縮するかどうかの指定。
    - デフォルトは none (つまり、非圧縮)。有効な値は、none, gzip, snappy です。
      圧縮はデータをバッチ化した全体に対して行われます。つまりバッチの効果は圧縮率にも影響するでしょう (多くのbatching により、高い圧縮率を実現できます)。
- retries
    - 0より大きい値を設定すると、クライアントは一時的なエラーによる障害による送信の全てのレコードを再送信するでしょう。
      この再試行はクライアントがエラー時にレコードを再送するのと変わらないことに注意してください。
      これによりレコードの順番が変わる可能性があるます。例えば、2つのレコードを1つのパーティションに送信し、
      最初が失敗して再送したが、2つ目は成功していたとすると、2つ目のバッチのレコードが最初に現れるかもしれない。
- batch.size
    - 多数のレコードが同じパーティションに送信される時はいつも
      プロデューサはレコードをより少ないリクエストにまとめようと(バッチ化しようと)するでしょう。
      これはクライアントとサーバの両方でパフォーマンスを助けます。
      この設定はデフォルトのバッチサイズをバイトで指定します。
    - このサイズより大きいバッチレコードには何も試行されないでしょう。
    - ブローカーに送信されるリクエストは複数のバッチを含むでしょう。各パーティションについて1つの送信することが可能なデータを持つバッチです。
    - 小さなバッチサイズはバッチ化を一般的でなくし、スループットを下げるかもしれません(バッチサイズ 0はバッチ化を完全に無効にするでしょう)。
      大きなバッチサイズは追加のレコードに備えて指定されたバッチサイズのバッチを常に割り当てるため、メモリを幾分贅沢に使うかもしれません。
- client.id
    - リクエストする時にサーバに渡されるid文字列。
      これの目的は、サーバ側のリクエストのログに論理アプリケーション名を追加することで、ip/portを超えたリクエストのソースの追跡をすることです。
- linger.ms
    - プロデューサは、リクエストの転送間に到着した全てのレコードを、1つのバッチリクエストにまとめまようとします。
      通常、この挙動は、忙しい状況(レコードが送出されるよりも速く到着しているとき、
      つまりバッファに複数のリクエストがたまっているとき)ときにだけ実現します。
      しかし、ある状況では、クライアントはそんなに忙しくない場合でもリクエストの数を減らしたいと思うかも知れません。
      この設定は少しの人為的な遅延によってこれを成し遂げます。
      つまり、すぐにレコードを送信するのではなく、プロデューサは一緒にバッチ化することができるように
      他のレコードが来るのを指定された遅延まで待つでしょう。
      これはTCPでのNagleアルゴリズムへの相似として考えることができます。
    - この設定ではバッチ処理の遅延の上限が与えられます: 
      パーティションについて一旦batch.size分のレコードを取得すると、それはこの設定に関係なく即座に送信されるでしょう。
      しかしもしこのパーティションについて集約されたバイトがこれより少ない場合、
      より多くのレコードが現れるまで指定された時間だけ'linger(居残る)'でしょう。
      この設定のデフォルトは 0 です (つまり、遅延はありません)。
      例えば、`linger.ms=5` に設定すると、送信されるリクエストの数を減らす効果がありますが、
      負荷が無い時にレコードの送信に5msのレイテンシが増加するでしょう。
- max.request.size
    - リクエストの最大バイトサイズ。
      この設定は大きなリクエストを送信することを避けるためにプロデューサが1つのリクエスト内で送信するレコードのバッチの数を制限するでしょう。
      これは最大レコードバッチサイズの効果的なキャップでもあります。
    - サーバはこれとは異なる上限値を持つかもしれないことに注意してください。
- receive.buffer.bytes
    - データを読み込む時に使われるTCPレシーバーバッファ (SO_RCVBUF) のサイズ。値が -1 であれば、OSのデフォルトが使われるでしょう。
- send.buffer.bytes
    - データを送信する時に使われるTCP送信バッファ (SO_SNDBUF)のサイズ。値が -1 であれば、OSのデフォルトが使われるでしょう。
- timeout.ms
    - この設定は、サーバ(リーダー)がフォロワーからのackを待つ時間の上限を指定します。(それはプロデューサー側の acks の設定で指定された数のackを満たすために)
    - もしタイムアウトの時間内に求められた数のackが得られなかった場合、エラーが戻されます。
    - このタイムアウトの計測はサーバ側で行われるので、(プロデューサーからの)ネットワーク遅延は含みません。
- block.on.buffer.full
    - バッファに空きがないとき、新しいレコードを受けるのをストップする(ブロックする)か、例外を投げます。
    - デフォルトは true でブロックします。
    - しかしながら、ブロッキングが望まれない状況では、即座にエラーとした方がよいことがあります。
    - false にセットすることでこれを実現できます。
    - その場合、プロデューサーはバッファがいっぱいの場合、 BufferExhaustedException を送信します。
- metadata.fetch.timeout.ms
    - あるトピックへの初回のデータ送信時に、そのトピックについてのメタデータ(各パーティションがどのホストに割り当たっているか)を取得する必要があります。
    - この設定はメタデータ受信のタイムアウト値を設定します。そのタイムアウト時間内に取得が成功しなかった場合は、例外を返します。
- metadata.max.age.ms
    - 強制的にメタデータをリフレッシュするまでの時間をミリ秒単位で指定します。
    - パーティーションリーダーの変更が全く観測されなかったとしても、率先して新しいブローカーやパーティションを発見するために、この時間が経過した場合はリフレッシュします。
- metrics.num.samples
    - メトリクスを計算するために保持される標本の数
- metrics.sample.window.ms
    - メトリクスの標本が計算されるための時間の窓。
- reconnect.backoff.ms
    - 指定されたホストに再接続しようとするまで待機する時間。これにより短いループ内でホストに繰り返し接続することを防ぎます。
- retry.backoff.ms
    - 指定されたトピックパーティションへの失敗したリクエストを再試行しようとするまで待機する時間。
      これにより短時間に送信と失敗を繰り返すような事象を回避します。


## 図

以下の資料に、Producer内部のバッファ、および、I/Oスレッド、Batching に関しての図がある。

- https://www.slideshare.net/gwenshap/kafka-reliability-when-it-absolutely-positively-has-to-be-there
- https://www.slideshare.net/ConfluentInc/reliability-guarantees-for-apache-kafka
- https://www.slideshare.net/JiangjieQin/producer-performance-tuning-for-apache-kafka-6314760