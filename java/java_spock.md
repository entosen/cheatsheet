# Spock

SpockはJava・Groovyアプリケーション向けの、テストフレームワーク

## Hello, World 的な

データ駆動テスト
```
import spock.lang.*

class Math extends Specification {
    @Unroll
    def "maximum of #a and #b is #c"() {  // 引数省略
        expect:
        Math.max(a, b) == c

        where:         // テストケースのバリエーションをこんな感じで書く
        a | b || c     // 1行目はテーブルヘッダ。データ変数を定義。
        1 | 3 || 3     // 以降データ行
        7 | 4 || 4
        0 | 0 || 0
    }
}
```


## 参考ドキュメント

- 本家: http://spockframework.org/spock/docs/1.1/index.html
- 日本語: https://spock-framework-reference-documentation-ja.readthedocs.io/ja/latest/index.html

- 会社
    - Spock導入ガイド: 会社のコンフル/pages/viewpage.action?pageId=1623921361
    - Spock文法Tips: 会社のコンフル/pages/viewpage.action?pageId=704843889



## 基本構造

```
class MyFirstSpecification extends Specification {
  // fields
  // fixture methods
  // feature methods
  // helper methods
}
```

Flelds

```
  // フィールドはフィーチャーメソッドごとに独立している。
  def obj = new ClassUnderSpecification()
  def coll = new Collaborator()

  // フィーチャーメソッド間で共有したいときは、@Shard をつける
  @Shard res = new VeryExpensiveResource()

  // static フィールドは(これも共有されるが) 定数値だけに使うこと
  static final PI = 3.141592654
```

Fixture Methods

```
  def setup() {}          // 各フィーチャーメソッドの前に実行
  def cleanup() {}        // 各フィーチャーメソッドの後に実行
  def setupSpec() {}      // 最初のフィーチャーメソッドの前に実行。@shard付きフィールドにしか影響できない
  def cleanupSpec() {}    // 最後のフィーチャーメソッドの後に実行。@shard付きフィールドにしか影響できない
```

もしテストクラスを継承していた場合、自動的に親クラスのsetup()/cleanup() が呼ばれる。(明示的に呼ぶ必要はない)
setup系は親クラスから順に。cleanup系は子クラスから順に。


Feature Methods

概念的フェーズ

- 準備
- 刺激
- 期待する反応
- 片付け


```
  def "pushing an element on the stack"() {
    // フィーチャーメソッドとして認識されるためには、1つ以上の明示的なブロック(ラベル)がないといけない

    // ---------------------------------------------------------
    // setup: は必ず最初。1回だけ。
    // 省略可。その場合、最初のラベルまでが setup とみなされる。
    // given: は setup: のエイリアス
    setup:      
    def stack = new Stack()
    def elem = "push me"

    // -----------------------------------------------------------
    // when と then はセットで。when が刺激、then が期待する結果。
    when:
    stack.push(elem)

    // then は書けるものが決まっている。(conditions, 例外conditions, interactions, 変数定義)
    then:
    !stack.empty               // condition。 boolean式、もしくは、true と比較可能な式    
    stack.size() == 1
    stack.peek() == elem

    thrown(EmptyStackException)          // 例外condition
    
    def e = thrown(EmptyStackException)  // さらに例外 の中身をチェックしたい場合はこのようにする
    // EmptyStackException e = thrown()  // 上のはこうも書ける
    e.cause == null

    notThrown(NullPointerException)      // 例外が飛ばないことをチェックしたいときはこう

    1 * subscriber1.receive("event")     // interactons というのは Mock を使ったこういうやつ
    1 * subscriber2.receive("event")     // 詳しくは mock のところで。

    // -----------------------------------------------------------
    // expect: は、whenとthenが一緒になったような感じ。刺激と反応を1文で。
    // condition と 変数定義しか書けない。
    expect:
    Match.max(1, 2) == 2

    // ---------------------------------------------------------------
    // cleanup: 1回だけ。後ろには where: ブロックしか来ない
    // ここに至るまでに例外が発生しても実行される (finally みたいな感じ)
    cleanup:
    file.delete()
  }
```

もし、then: と expect: 以外で condition チェックしたい場合は、以下のように assert を使う。

```
    assert stack.empty
```

ちなみに、Java では `==` が参照の一致、`a.equals(b)` が内容の一致のチェックだが、
Groovy では `==` が内容の一致。参照の一致をチェックしたい場合は `a.is(b)` を使う。


where で、データ駆動のテストが可能。

```
  def "computing the maximum of two numbers"() {
    expect:
    Math.max(a, b) == c

    // ---------------------------------------------------------------
    // where を書くなら必ずメソッドの最後。1回だけ。
    // データ駆動の際に使う。詳細はデータ駆動のところで
    where:
    a << [5, 3]
    b << [1, 9]
    c << [5, 9]
  }
```

Helper Methods

ブロックを含まないメソッド。
フィーチャーメソッドの共通な一部機能を外出しするのに使う。

tip: condition部分を関数化した場合、失敗時の表示をわかりやすくするために以下のように書く
```
void matchesPreferredConfiguration(pc) {   // 返り値型 void にしておいた方がいい。
  assert pc.vendor == "Sunny"
  assert pc.clockRate >= 2333
  assert pc.ram >= 4096
  assert pc.os == "Linux"
}
```

With

```
  def "offered PC matches preferred configuration"() {
    when:
    def pc = shop.buyPc()

    then:
    with(pc) {
      vendor == "Sunny"      // pc.vendor == "Sunny" と同じ
      clockRate >= 2333
      ram >= 406
      os == "Linux"
    }

    // こんな感じで、interaction でも使える
    with(service) {
      1 * start()    // serice.start() と同じ
      1 * doWork()   
      1 * stop()
    }
  }

```

Documentaion ブロックにコメントをつける

```
    setup: "open a database connection"
    // code goes here
    and: "seed the customer table"    // and: で setup の中をいくつかに分割し、コメントをつけれる
    // code goes here
    and: "seed the product table"
    // code goes here
```

Extensions
```
@Timeout
@Ignore
@IgnoreRest
@FailsWith

```


## データ駆動テスト





## Mock


```


def "should send messages to all subscribers"() {
    setup:
    Subscriber subscriber = Mock()    // もしくは、 def subscriber = Mock(Subscriber)
    Subscriber subscriber2 = Mock()   //            def subscriber2 = Mock(Subscriber)

    when:
    publisher.send("hello")

    then:
    1 * subscriber.receive("hello")
    1 * subscriber2.receive("hello")

    // もし変数宣言と一緒に書きたい場合は interaction{} で囲む。
    // spockがmockのインタラクション定義をwhenの直前に移動することに起因。
    then: 
    interaction {
      def message = "hello"
      1 * subscriber.receive(message)
    }
}
```

デフォルトの動作は、戻り値の型に応じたデフォルト値(false, 0, nullなど)を返すだけ。
ただし、Object.equals、Object.hashCode、Object.toStringメソッドは例外。
いわゆる緩いモック。予期しないメソッド呼び出しをしても例外を投げない。

定義していないモック呼び出しを失敗としたい場合は、下記の記述を最後に入れておく。
Strict Mocking 。
```
0 * _
```

多重度

```
1 * subscriber.receive("hello")      // exactly one call
0 * subscriber.receive("hello")      // zero calls
(1..3) * subscriber.receive("hello") // between one and three calls (inclusive)
(1.._) * subscriber.receive("hello") // at least one call
(_..3) * subscriber.receive("hello") // at most three calls
_ * subscriber.receive("hello")      // any number of calls, including zero
                                     // (rarely needed; see 'Strict Mocking')
```

対象制約

```
1 * subscriber.receive("hello") // a call to 'subscriber'
1 * _.receive("hello")          // a call to any mock object
```

メソッド制約

```
1 * subscriber.receive("hello") // a method named 'receive'
1 * subscriber./r.*e/("hello")  // a method whose name matches the given regular expression
                                // (here: method name starts with 'r' and ends in 'e')

1 * subscriber.status           // getterメソッドの代わりに、Groovy のプロパティ構文が使える
1 * subscriber.setStatus("ok")  // setterの場合はそうはできないので、setterで書く
```

引数制約

```
1 * subscriber.receive("hello")     // an argument that is equal to the String "hello"
1 * subscriber.receive(!"hello")    // an argument that is unequal to the String "hello"
1 * subscriber.receive()            // the empty argument list (would never match in our example)
1 * subscriber.receive(_)           // any single argument (including null)
1 * subscriber.receive(*_)          // any argument list (including the empty argument list)
1 * subscriber.receive(!null)       // any non-null argument
1 * subscriber.receive(_ as String) // any non-null argument that is-a String
1 * subscriber.receive({ it.size() > 3 }) // an argument that satisfies the given predicate
                                          // (here: message length is greater than 3)

複数の引数を持つメソッドでも一緒
1 * process.invoke("ls", "-a", _, !null, { ["abcdefghiklmnopqrstuwx1"].contains(it) })

その他いろいろなんでも系
1 * subscriber._(*_)     // any method on subscriber, with any argument list
1 * subscriber._         // shortcut for and preferred over the above
1 * _._                  // any method call on any mock object
1 * _                    // shortcut for and preferred over the above
```

スタビング(値を返す、副作用を発生させる)

setup などモックインスタンスを作るときと同時に振る舞いを宣言してもいいし、
最後の例の様に、持っキングと同時に宣言してもいい。
ただし、同じメソッドについて行う場合は、1度でやる必要がある。
```
// `>>` を書く場合は左に多重度は必要ない
subscriber.receive(_) >> "ok"   // いつも同じ値を返す

subscriber.receive("message1") >> "ok"     // 引数に応じた値を返す
subscriber.receive("message2") >> "fail"

subscriber.receive(_) >>> ["ok", "error", "error", "ok"]   // 呼ばれるごとの返り値を指定

// 動的に値を返す
subscriber.receive(_) >> { args -> args[0].size() > 3 ? "ok" : "fail" }
subscriber.receive(_) >> { String message -> message.size() > 3 ? "ok" : "fail" }   // 名前付きで受ける

// 副作用の実行
subscriber.receive(_) >> { throw new InternalError("ouch") }   // 例外を投げる

// モッキングと同時に
1 * subscriber.receive("message1") >> "ok"
1 * subscriber.receive("message2") >> "fail"
```

Stub
Spy, パーシャルモック



## Tips

Groovy の仕様なのか意図していない使い方なのか、
Groovyでは java側で定義されたクラスの private なフィールドも触れるっぽい。

Groovy の小数リテラルは、特に何もしていしないとBigDecimal型になる。
