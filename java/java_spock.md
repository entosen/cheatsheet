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



