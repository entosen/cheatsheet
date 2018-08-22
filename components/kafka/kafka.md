## 前準備

会社のパッケージ管理コマンドを使う場合
```
xinst install -dry xjava_jdk

それと、この辺のパッケージを入れた。

xinst: jports_jline__jline-0.9.94_1
xinst: jports_junit__junit-4.4_1
xinst: jports_log4j__log4j-1.2.16_1
xinst: jports_org_slf4j__slf4j_api-1.6.4_1
xinst: jports_org_slf4j__slf4j_log4j12-1.6.4_1
xinst: xxxxx_multimode-3.0.4
xinst: xjava_jdk-1.8.0_60.58
xinst: xjava_log4j-1.2.17.13
xinst: xjava_vmwrapper-2.1.7
xinst: zookeeper_client-3.4.5_66
```

個人で試す場合は、kafkaの QuickStart にあるように、tar ball をダウンロードしてくる。

```
$ wget "https://archive.apache.org/dist/kafka/0.8.2.1/kafka_2.11-0.8.2.1.tgz"
$ tar xzvf kafka_2.11-0.8.2.1.tgz
$ cd kafka_2.11-0.8.2.1
```

サービスの環境であれば、適切なkafkaの環境が作られていれば、/opt/kafka に必要なファイルがある前提。

scala でコードを書く場合の build.sbt のサンプル
```
// https://gist.github.com/miguno/7718835
// The excludes of jms, jmxtools and jmxri are required as per https://issues.apache.org/jira/browse/KAFKA-974.
// The exclude of slf4j-simple is because it overlaps with our use of logback with slf4j facade;  without the exclude
// we get slf4j warnings and logback's configuration is not picked up.
// 
// build時に、jms,jmxtools,jmxri などが取ってこれなくてエラーになってしまうことを回避。
// また、ロギングにlogbackを使う場合は、slf4j が衝突するので、それを回避。
libraryDependencies += ("org.apache.kafka" %% "kafka" % "0.10.0.0"
  exclude("org.slf4j", "slf4j-log4j12")
  exclude("javax.jms", "jms")
  exclude("com.sun.jdmk", "jmxtools")
  exclude("com.sun.jmx", "jmxri")
  // exclude("org.slf4j", "slf4j-simple")
)
```




## 概念

Kafka クラスタを直接表す名前などはなく、
Kafka Broker の設定(server.property)で、`zookeeper.connect` が同じものが同じクラスタとして構成される。

各Kafka Broker の `broker.id` は、Kafka クラスタの中でユニークに設定しないといけない。

基本的には、クラスタの中のどれかのBrokerを指定すれば、それはクラスタを指定したことになる。
(各コマンドの、`broker-list`, `bootstrap.servers` など)
ものによっては、zookeeper を指定することで、クラスタを指定するものもある。
(`--zookeeper`)


## コマンド

### zookeeper の起動・停止


起動

```
bin/zookeeper-server-start.sh config/zookeeper.properties
```

zookeeper.properties
```
# the directory where the snapshot is stored.
dataDir=/tmp/zookeeper
# the port at which the clients will connect
clientPort=2181
# disable the per-ip limit on the number of connections since this is a non-production config
maxClientCnxns=0
```


停止
```
bin/zookeeper-server-stop.sh
```

引数なし。
psしてPIDを見つけてきて、kill -s TERM している。


確認。

zookeeper の中身を見たいときは、
zookeeper-clientのパッケージに入っている zkCli.sh を使う。以下のような感じ。
```
bin/zkCli.sh localhost:2181

help

ls /systemA
ls /systemA/kafka
get /systemA/kafka
```



### kafka-server の起動・停止

起動
```
bin/kafka-server-start.sh config/server.properties
```

代表的な設定
```
# The id of the broker. This must be set to a unique integer for each broker.
# Kafkaクラスタ内でユニークにする
broker.id=0

listeners=PLAINTEXT://:9092

log.dirs=/tmp/kafka-logs

zookeeper.connect=localhost:2181
```

停止
```
bin/kafka-server-stop.sh
```

引数なし
psしてPIDを見つけてきて、kill -s TERM している。



### Topic操作系

各コマンドのオプションにつける `--zookeeper` の指定。
基本的に server.property の `zookeeper.connect` の設定に合わせる。

```
例
localhost:2181
ホストが複数の場合、後にパスがつく場合もある
host1.example.com:2181,host2.example.com:2181/systemA/kafka
```


#### 表示系

```
bin/kafka-topics.sh
    --describe  詳細情報の表示
    --list      トピック名だけの表示

    --zookeeper <urls>   [必須] zookeeperのアドレス。localhost:2181 など

    --topic <topic名>  特定のTopicについてだけ表示する。指定しなければ全Topic
```

describe の表示
```
Topic:my-replicated-topic       PartitionCount:1        ReplicationFactor:3     Configs:
        Topic: my-replicated-topic      Partition: 0    Leader: 1       Replicas: 1,2,0 Isr: 1,2,0
Topic:test      PartitionCount:1        ReplicationFactor:1     Configs:
        Topic: test     Partition: 0    Leader: 0       Replicas: 0     Isr: 0

Leader: リーダーになっているサーバの broker.id
Replicas: リーダーか生存しているかにかかわらず、そのパーティションのレプリカを保持するサーバの broker.id
Isr: Replicas のうち、現在生存して、リーダーに追いついているサーバの broker.id (in-sync-replicas)
```

勝手に `__consumer_offsets` という topic ができていることがある。
高レベルのConsumerをつなぐと自動でできるのか？
各コンシューマーがどこまでよんだかのオフセットをbroker間でやり取りするために必要？


また、zookeeper 内の情報を眺めることで同様の情報を得ることができる。

前述の zkCli.sh を用いる

```
brokers
    ids
    	0      --- broker.id に対する brokerサーバの ホスト名、ポート、など
	1
    topics
	トピック名          --- パーティション・レプリカ構成、担当するBrokerの割当。
	    partitions      
		0
		    state   --- そのタイミングでの leaderのID、irsの値
		1
		2
```

#### 作成(create)

```
bin/kafka-topics.sh 
    --create 

    --zookeeper <urls>   [必須] zookeeperのアドレス。localhost:2181 など 

    --topic <topic名>              作成するトピック名
    --replication-factor <整数>    1パーティションあたりのレプリカ数
    --partitions <整数>            パーティション数
```

brokerサーバ数より、partitions や replication-factor が小さい場合、
どのサーバにレプリカが置かれるか、どのサーバがリーダーになるかは、作成時にランダムに決められるっぽい。


#### 変更(alter)

```
bin/kafka-topics.sh
    --alter
    ...
```

#### 削除(delete)

```
bin/kafka-topics.sh
    --delete
    --zookeeper <urls>   [必須] zookeeperのアドレス。localhost:2181 など 
    --topic <topic名>    削除するトピック名
```

delete するためには、kafka broker の property に、`delete.topic.enable` が `true` になっていないといけない。

そうでない場合は、削除のマークがつけられるだけ。
上記設定を有効にした後、最初の起動の時点で削除される。




### 送受信


#### 標準入力から読み込んで kafka に送信

```
bin/kafka-console-producer.sh 
    --broker-list <broker-list>  [必須] brokerの HOST1:PORT1,HOST2:PORT2 (localhost:9092 など。) 
                                 とっかかりになるだけなので、クラスタ内のBroker少なくとも1台書けばよい。
				 正確な情報はそのBrokerに接続し自動で取得される。
    --topic <topic名>            [必須] topic名
```

`broker-list` は、あくまでクラスタの少なくとも１つのBrokerを指定すればよい。
クラスタの最新の構成はそこから自動的に取得されているようだ。
なので、topicに割り当てられてないbrokerを指定したとしても、きちんと担当のbrokerに書き込まれる。


#### kafkaから読み込んで 標準出力に出力 (高レベルのIFを利用。どれがリーダーかとか、partitionとか意識しなくていい。)

```
bin/kafka-console-consumer.sh 
    --zookeeper <urls>   [必須] zookeeperのアドレス。localhost:2181 など。古い指定の方法かも。
                         かわりに --bootstrap-server で broker を指定するのが新しい方法らしい。

    --topic <topic名>
    --from-beginning    過去のオフセットがない場合、ログの先頭から読み込む。
                        この指定がない場合、ログの末尾以降から読み込む。

    --property print.key=true
    ??効かない?? --property print.value=true  (デフォルト)
    --property key.deserializer=org.apache.kafka.common.serialization.StringDeserializer
    --property value.deserializer=org.apache.kafka.common.serialization.LongDeserializer

```
どこまで読んだかのオフセットが Zookeeper に保存されているようだ。
ただプロセスをstopすると、Zookeeperからも消えてしまうようだ。



#### kafkaから読み込んで、標準出力に出力 (低レベルのIFを利用。partition を指定)

```
bin/kafka-simple-consumer-shell.sh
    --broker-list localhost:9092   kafka broker のリストを指定
    --topic <topic名>
    --partition <番号>

    --offset <int>           番号指定。-1:末尾, -2:先頭(デフォルト)
    --max-messages <int>     コンシュームするメッセージ数。デフォルト2147483647
    --no-wait-at-logend      末尾まで行ったらプロセス終了
    --print-offset
    --property print.key=true
    ??効かない?? --property print.value=true  (デフォルト)
    --property key.deserializer=org.apache.kafka.common.serialization.StringDeserializer
    --property value.deserializer=org.apache.kafka.common.serialization.LongDeserializer

    --formatter kafka.tools.NoOpMessageFormatter     Valueを表示させたくないとき。
```

### Broker のオフセット情報を参照する

書き込まれ Broker内に入っているオフセットを確認する。

```
bin/kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic test3 --time -1

test3:2:2
test3:1:1
test3:0:2

    --time -1 : 最後のオフセット値を表示
    --time -2 : 最初のオフセット値を表示
    --time 時刻 : その時刻のオフセット値を表示  (この指定効かないぽい？)
```



### Consumerの情報を参照する

※ SimpleConsumer を使った場合は、ステートレスなのでこれらの情報は作られない。

※ コンシューマーの情報は、コンシューマーが起動しているときにしか入ってない。

zookeeper にどうはいっているか。
```
consumers
    GroupID
	ids
	    コンシューマーID    --- {"version":1,"subscription":{"test3":1},"pattern":"white_list","timestamp":"1475144589113"}
	owners
	    topic名
		パーティション番号     --- コンシューマノードID (そのパーティションを処理するコンシューマは(グループ内で)１つ。そのID)
	offsets
	    topic名
	    	パーティション番号     --- 整数値。そのパーティションから読み込み済みの位置


コンシューマID = コンシューマ名_ホスト名_時刻？_何か
     console-consumer-74776_myhost.example.co.jp-1475144589045-2c230a99
コンシューマノードID = 
     console-consumer-74776_myhost.example.co.jp-1475144589045-2c230a99-0
```

コンシューマーグループ一覧を表示

```
% bin/kafka-consumer-groups.sh --zookeeper localhost:2181 --list
console-consumer-74776
...
```

コンシューマーグループ内のオフセット値などの詳細を表示。
(Brokerにどれくらい入っていて、どこまで読んだか)

```
% bin/kafka-consumer-groups.sh --zookeeper localhost:2181 --describe --group console-consumer-74776

GROUP                          TOPIC                          PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG             OWNER
console-consumer-74776         test3                          0          1               1               0               console-consumer-74776_host1.example.com-1475144589045-2c230a99-0
console-consumer-74776         test3                          1          0               0               0               console-consumer-74776_host1.example.com-1475144589045-2c230a99-0
console-consumer-74776         test3                          2          1               1               0               console-consumer-74776_host1.example.com-1475144589045-2c230a99-0



こちらも同様だが、Deprecated 。Broker情報が出せる。
% bin/kafka-run-class.sh kafka.tools.ConsumerOffsetChecker --zookeeper localhost:2181 --group console-consumer-74776 --broker-info
% bin/kafka-consumer-offset-checker.sh --zookeeper localhost:2181 --group console-consumer-19735 --broker-info

Group           Topic                          Pid Offset          logSize         Lag             Owner
console-consumer-74776 test3                          0   1               1               0               console-consumer-74776_myhost.example.co.jp-1475144589045-2c230a99-0
console-consumer-74776 test3                          1   0               0               0               console-consumer-74776_myhost.example.co.jp-1475144589045-2c230a99-0
console-consumer-74776 test3                          2   1               1               0               console-consumer-74776_myhost.example.co.jp-1475144589045-2c230a99-0
BROKER INFO
2 -> myhost.example.co.jp:9094
1 -> myhost.example.co.jp:9093
0 -> myhost.example.co.jp:9092
```



### Kafka Connect

(以下、ちょっと認識あやしい)

自分で Producer/Consumer コードを書かなくても、
以下のような典型的な処理は Connector として汎用的な形で用意されている。

- ファイルをkafkaに入力する
- kafkaからファイルに出力する
- ある kafka を別の kafka につなぐとか

Connectorを選択し、必要な設定をして、Kafka Connect (worker) で動かしてあげることで、
自分でコードを書かなくても、kafkaに流す/取り出すことができる。

Kafka Connect ってのが worker で、
Connector っていうのが実装っぽい。
Kafka Connect が Connector を動かす。

```
bin/connect-standalone.sh
Usage: ConnectStandalone worker.properties connector1.properties [connector2.properties ...]

bin/connect-standalone.sh \
    config/connect-standalone.properties \
    config/connect-file-source.properties \
    config/connect-file-sink.properties
```

1つ目のファイルが、Kafka Connect の設定ファイル。
つなぎにいくBrokerや、シリアライズフォーマット。

connect-standalone.properties (主要なもの)

```
bootstrap.servers=localhost:9092



```

2つ目以降のファイルが、各Connectorの設定ファイル。


```
# config/connect-file-source.properties
name=local-file-source
connector.class=FileStreamSource
tasks.max=1
file=test.txt
topic=connect-test

# config/connect-file-sink.properties
name=local-file-sink
connector.class=FileStreamSink
tasks.max=1
file=test.sink.txt
topics=connect-test%        
```

おそらく、
name, connector.class, が、connect共通の設定だと思う。
それ以降 tasks.max, file, topic は、connect固有の設定だと思う。

おそらく、
Connecterクラスを継承したクラス(既存でいくつかあるか、特殊なら自分で書く)を作っておいて、
それを複数個動かす。動かすための枠組みが ConnectStandalone ？


Connect は、入出力の形が、Connect data という形に統一されている？(縛りがある？)
その形式に変換する設定が、Converter ？？

```
foo
bar
というファイルが
{"schema":{"type":"string","optional":false},"payload":"foo"}
{"schema":{"type":"string","optional":false},"payload":"bar"}
こんな感じにkafkaの中を流れている。
```

