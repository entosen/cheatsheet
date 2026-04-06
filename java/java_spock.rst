=====================
Spock
=====================

SpockはJava・Groovyアプリケーション向けの、テストフレームワーク

Hello, World 的な
=======================

TODO

::

  import spock.lang.*




参考ドキュメント
===========================


- 本家2.3: https://spockframework.org/spock/docs/2.3/index.html
- 本家2.4-SNAPSHOT: https://spockframework.org/spock/docs/2.4-SNAPSHOT/index.html
- 日本語: (古い) https://spock-framework-reference-documentation-ja.readthedocs.io/ja/latest/index.html


用語
=================

system under test, SUT
  テストしている対象。テスト対象のクラスやメソッド。
  大きさは問わない。1つのクラスでもよいしアプリケーション全体でもよい。

system under specification, SUS
  SUT と同義

fixture
  テストを構成する要素全般をひとまとめに呼んだもの。
  ある状態のSUS + 相互作用するまわりのもの。
  環境とかsnapshotとか呼ばれるもの。



基本構造
=================

::

  import spock.lang.Specification

  class MyFirstSpecification extends Specification {
    // fields
    // fixture methods
    // feature methods
    // helper methods
  }


Flelds
-------------

::

  // インスタンス・フィールドはフィーチャーメソッドごとに独立している。
  // (フィーチャーメソッドごとにインスタンスが作られている。)
  def obj = new ClassUnderSpecification()
  def coll = new Collaborator()

  // フィーチャーメソッド間で共有したいときは、@Shared をつける
  @Shared res = new VeryExpensiveResource()

  // static フィールドは(これも共有されるが) 定数値だけに使うこと
  static final PI = 3.141592654


Fixture Methods
------------------------

::

  def setupSpec() {}      // 最初のフィーチャーメソッドの前に実行。@Shard付きフィールドにしか影響できない
  def setup() {}          // 各フィーチャーメソッドの前に実行
  def cleanup() {}        // 各フィーチャーメソッドの後に実行
  def cleanupSpec() {}    // 最後のフィーチャーメソッドの後に実行。@Shard付きフィールドにしか影響できない


もしテストクラスを継承していた場合、自動的に親クラスのsetup()/cleanup() が呼ばれる。(明示的に呼ぶ必要はない)
setup系は親クラスから順に。cleanup系は子クラスから順に。


Feature Methods
------------------------

概念的フェーズ

- 準備
- 刺激
- 期待する反応
- 片付け


::

  def "pushing an element on the stack"() {
    // フィーチャーメソッドとして認識されるためには、1つ以上の明示的なブロック(ラベル)がないといけない

    // ---------------------------------------------------------
    // given: は必ず最初。1回だけ。
    // 省略可。その場合、最初のラベルまでは given に属するとみなされる。
    // setup: は given: のエイリアス
    given:      
    def stack = new Stack()
    def elem = "push me"

    // -----------------------------------------------------------
    // when と then はセットで。when が刺激、then が期待する結果。
    // when と then は複数組あってもよい。
    when:
    stack.push(elem)

    // then は書けるものが決まっている。(conditions, 例外conditions, interactions, 変数定義)
    then:
    !stack.empty               // condition。 boolean式(正確にはboolean以外の型の式でもよい。その場合Groovy truthかどうか)
    stack.size() == 1
    stack.peek() == elem

    thrown(EmptyStackException)          // 例外condition。例外が飛ぶことを期待。
    
    def e = thrown(EmptyStackException)  // さらに例外 の中身をチェックしたい場合はこのようにする。
    // EmptyStackException e = thrown()  // 上のはこうも書ける。引数なしのthrown()は左辺の型を期待する。
    e.cause == null

    notThrown(NullPointerException)      // 特定の例外が飛ばないことをチェックしたいときはこう
    noExceptionThrown()                  // いかなる例外も飛ばないことをチェックしたいときはこう

    1 * subscriber1.receive("event")     // interactons というのは Mock を使ったこういうやつ
    1 * subscriber2.receive("event")     // 詳しくは mock のところで。

    // -----------------------------------------------------------
    // expect: は、whenとthenが一緒になったような感じ。刺激と反応を1つの評価式で。
    // condition と 変数定義しか書けない。
    // ガイドライン的には、副作用が発生するものは when,then 、副作用のない純粋な関数の場合は expect がよい。
    expect:
    Match.max(1, 2) == 2

    // ---------------------------------------------------------------
    // cleanup: 1回だけ。後ろには where: ブロックしか来ない。
    // ここに至るまでに例外が発生しても実行される (finally みたいな感じ)
    cleanup:
    file.delete()
    file?.delete()  // (tip) こんな感じに書くとnullでもエラーにならない
  }

where で、データ駆動のテストが可能。

::

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

filterブロックで、whereのイテレーションの一部をスキップさせることができる

::

  where:
  i << (1..5)

  filter:
  i != 3

filterブロックの中は Condition Block として扱われる。
つまり、暗黙のassert化が行われる。
assertが失敗したイテレーションはスキップされる。





暗黙assert, Condition Block 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

then と expect ブロックでは、 ``assert`` キーワードを明示しなくても、
暗黙的に condition となる仕組みがある。(暗黙assert化、implicit assert, Condition Block)。

仕組みとしては、コンパイル時にコード・式を構文解析して変換しているらしい。

どの部分で暗黙assert化されるかは超重要！！！
間違うと条件が無視されたりするので、きちんと理解しておく！


暗黙のassertとみなされるもの

- **Condition Block直下** の値を返す式

  - boolean を返す式は、当然その true/false で判定
  - それ以外の型でも Groovy truth かどうかで判定

- Spockの with, verifyAll, verifyEach に渡しているクロージャーの中身
- @Verify, @VerifyAll が付いたメソッドの中身
- @ConditionBlock が付いたメソッドに渡しているクロージャーの中身

::

  a == 15          // 暗黙assert化。 boolean式
  a % 3 == 0       // 暗黙assert化。 boolean式
  a - 15           // 暗黙assert化。 数値

  isPrime(a)       // 暗黙assert化。 void以外の関数呼び出し。
                   // 関数の結果はassertとして扱われるが、関数の中身のコードは暗黙assert化されない。

  // Spock の with などの中身も暗黙assert化される。返り値はvoid。
  with(a) {
    it % 5 == 0    // 暗黙assert化
    it > 7         // 暗黙assert化
  }


暗黙assertとみなされないもの

- 戻り値がvoidのメソッド呼び出し
- 変数への代入
- interaction
- if, switch, for, while
- 例外のキャプチャ ``def e = thrown(RuntimeException)``
  (これは「例外が発生すること」自体を Spock の別の仕組みで検証しているため、
  この行自体が true/false で判定されるわけではありません。)
- 普通の関数・メソッド・クロージャーの中身

::

  var b = (a == 15)  // 代入はassert化されない。それに含まれる式もassert化されない。

  if (a > 10) {      // if などのブロックの中はassert化されない。
      a == 20        // それに含まれる式もassert化されない
  }


注意が必要なケース
~~~~~~~~~~~~~~~~~~~~


通常は呼び出したメソッドの中までは暗黙assert化されない。
独自メソッドの中を暗黙assert化したい場合は、 ``@Verify``, ``@VerifyAll`` を付けるとできる。
(Helper Methodの項で詳しく) ::

  then:
  helper1(a)     // この行自体はassert化される。つまり、関数の結果がtrueかどうかの判定。

  ---
  boolean helper1(int i) {
    i % 3 == 0    // この式はassert化されない。
    i % 5 == 0    // この式はassert化されない。
    i != 15       // この式はassert化されない。結果はこのメソッドの返り値として返される。
  }


Spock の with, verifyAll, verifyEach は特殊で、そこに渡しているクロージャーの中身は暗黙assert化される。
それ以外の普通のクロージャーの中身は暗黙assertされない。
クロージャーの中身を暗黙assert化する独自メソッドを作りたい場合 ``@ConditionBlock`` を付けるとできる。(後述)


強制assert、暗黙assert回避
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

もし、暗黙assert化されないところで condition チェックしたい場合は、
以下のように明示的に ``assert`` を使う。

::

  assert stack.empty


逆に、暗黙assertされるケースでそれを回避したい場合は ``!!`` を付ける。

例::

  !!aList.each { assert it > 0 }

- 各要素について判定を行う。 
  eachのクロージャーには暗黙assert化は効かないので、明示的なassertが必要。
- eachの戻り値は元のコレクション自体。
  もし入力が空リストだった場合、eachの結果は空リストとなり、
  暗黙assert化されるとそこで失敗してしまう。
  なので ``!!`` を付けて暗黙assert化を回避。


assertはするが、失敗時の出力が大きくなりすぎる場合、
明示的assertに ``!!`` を付ける下記の記述で抑制できる。::

  // メッセージ付き
  assert !!(foo == bar): "fooとbarが一致しない"
  →
    (foo == bar)

    foobar

  // メッセージなし
  assert !!(foo == bar)
  →
    (foo == bar)
  

tips
~~~~~~~~~~~

ちなみに、Java では ``==`` が参照の一致、``a.equals(b)`` が内容の一致のチェックだが、
Groovy では ``==`` が内容の一致。参照の一致をチェックしたい場合は ``a.is(b)`` を使う。


失敗した assert の箇所でそのテストは終了する。(以降の処理・assertはされない。)
すべてのassertをひととおりやってまとめて結果を見たい場合は、後述の verifyAll を使う。



@ConditionBlock
-----------------------------

``@ConditionBlock`` を付けたメソッドが取るClosure引数の中身は Condition Block として扱われる。
つまりClosureの中で暗黙assert化が行われる。

``@ConditionBlock`` が効く条件

- クロージャーがリテラルとして渡されており、
  かつ Groovy コンパイラが（コンパイル時に）そのメソッドにつながる型を特定できること
- アノテーション付きメソッドが、コンパイル時に型が分かっているオブジェクトに対して呼び出されていること（def ではない）

::

    // SomeConditions.evaluate() が @ConditionBlock 付きで定義されているとする

    SomeConditions conds = new SomeConditions()
    conds.evaluate { ... }              // conds の型が決まるのでOK

    def conds = this
    conds.evaluate { ... }              // conds の型が決まらないのでダメ
    
    
また、アノテーション付きメソッドがオーバーロードされている場合、
すべてのオーバーロードにおけるクロージャー引数はコードブロックとして扱われます。









Helper Methods
---------------------------

ブロック(given: とか then: とか)を含まないメソッド。
フィーチャーメソッドの共通な一部機能を外出しするのに使う。
典型的には、setup/cleanup関連とcondition関連がある。

setup/cleanup関連のヘルパーメソッドは難しくない。

ここでは condition関係のヘルパーメソッドについて書く。

条件をヘルパーメソッドに外出しした場合

メソッドの中は暗黙assert化されないので、 
判定するためには、1つの条件式にして結果をreturnしないといけない。
ただしこのの書き方だと assert 失敗の結果がしょぼくなる。どの条件で失敗したかわからない。

::

  def matchesPreferredConfiguration(pc) {
    pc.vendor == "Sunny"
    && pc.clockRate >= 2333
    && pc.ram >= 4096
    && pc.os == "Linux"
  }

もしくは明示的にassert化する。これならどの条件で失敗したか分かる。::

  void matchesPreferredConfiguration(pc) {   // 返り値型 void にしておいた方がいい。
    assert pc.vendor == "Sunny"
    assert pc.clockRate >= 2333
    assert pc.ram >= 4096
    assert pc.os == "Linux"
  }

もしくは ``@Verify`` を付ける。
こうすると暗黙assert化が効くようになる。
::

  @Verify
  void matchesPreferredConfiguration(pc) {   // 返り値型 void もしくは def でないといけない
    pc.vendor == "Sunny"
    pc.clockRate >= 2333
    pc.ram >= 4096
    pc.os == "Linux"
  }


また ``@VerifyAll`` を付けると、同様に verifyAll 相当の挙動になる。
つまり、暗黙assert化され、かつ、途中で止まらずにひととおりのassertを検証し、最後にまとめて結果を返す。


with
------------

※ Groovy標準のwith と Spockのwith を混同しないように！

Groovy標準のwith

- ::

    obj.with {...}

- オブジェクトのインスタンスメソッド
- 戻り値は最後の式の値
- 暗黙assert化なし 
  (Spock2.4-M7未満までは、Spockがうまいことこの形もConditionBlockとして暗黙assert化されていたっぽい。
  でも2.4-M7ではもうされなくなった。)


Spockのwith → spock.lang.Specification.with

- ::

    void with(target, closure)
    void with(target, type, closure)    // typeでitの型が明確になる。補完が効いたり。

- spock.lang.Specification のメソッド (静的メソッドっぽく見える)
- 戻り値は void
- 暗黙assert化あり




Spockの with に渡すクロージャーはConditionBlockとみなされ、暗黙assert化される。

::

  def "offered PC matches preferred configuration"() {
    when:
    def pc = shop.buyPc()

    then:
    with(pc) {
      vendor == "Sunny"      // pc.vendor == "Sunny" と同じ。
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



verifyAll
-------------------

通常は、assertionが失敗したら、それ以降は評価されない。

失敗してもひととおりのassertionをして最後にまとめて結果がほしい場合は、
下記のように verifyAll を使う。

::

    void verifyAll(target, closure)
    void verifyAll(target, type, closure)    // typeでitの型が明確になる。補完が効いたり。
    void verifyAll(closure)


withのような使い方をするバージョン(引数1つ)::

  then:
  verifyAll(pc) {
    vendor == "Sunny"
    clockRate >= 2333
    ram >= 406
    os == "Linux"
  }

引数なしバージョン::

  expect:
  verifyAll {
    2 == 2
    4 == 4
  }

verifyAll のクロージャーの中身も暗黙assert化される。


verifyEach
--------------------

リストなどの評価。

List同値性チェック::

  def list = [1, 2, 3]
  assert list == [1, 2, 4]

Set同値性チェック::

  def set = [1, 2, 3] as Set
  assert set == [1, 2, 4] as Set

Every Method::

  def list = [1, 2, 3]
  assert list.every { it == 2 }   // 通常のクロージャーの中は暗黙assert化されない

↑通常のクロージャーの中は暗黙assert化されない。単に最後の値が結果としてreturnしているだけ。
everyは結果のリストがすべてtrueならtrueを返す。それがassertされる。

VerifyEach Method::

  void verifyEach(things, closure)
  void verifyEach(things, namer, closure)

::

  def list = [1, 2, 3]
  verifyEach(list) { it == 2 }   // クロージャーの中は暗黙assert化される

  // namer:失敗時のitの表示方法を指定。デフォルトでは toString()
  def list = [1, 2, 3]
  verifyEach(list, { "int($it)" }) { it == 2 }

  // リストのindexもクロージャーに渡す
  def list = [1, 2, 3]
  def expected = [1, 3, 4]
  verifyEach(list) { it, i -> it == expected[i] }

- クロージャーの中は暗黙assert化される
- 失敗したときの表示が、要素ごとに分かれてされるので、分かりやすい
- 途中で止まらずに、すべての要素をひととおりassertして最後にまとめて結果を上げる



Documentaion ブロックにコメントをつける
-----------------------------------------------

::

    given: "open a database connection"
    // code goes here
    and: "seed the customer table"    // and: で given の中をいくつかに分割し、コメントをつけれる
    // code goes here
    and: "seed the product table"
    // code goes here


Extensions
--------------------

::

  @Timeout
  @Ignore
  @IgnoreRest
  @FailsWith




データ駆動テスト
=========================


データ駆動テスト::

  import spock.lang.*

  class Math extends Specification {
      @Unroll  // 付けなくてもよくなったはず。
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




Interaction Based Testing, Mock, Stub
=====================================================


::

  def "should send messages to all subscribers"() {

      setup:
      Publisher publisher = new Publisher()
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

Mockは interface に対しても class に対しても作ることができる。

デフォルトの動作は、戻り値の型に応じたデフォルト値(false, 0, nullなど)を返すだけ。
ただし、Object.equals、Object.hashCode、Object.toStringメソッドは例外。
いわゆる緩いモック。予期しないメソッド呼び出しをしても例外を投げない。

定義していないモック呼び出しを失敗としたい場合は、下記の記述を最後に入れておく。
Strict Mocking 。
::

  0 * _


Mocking
-------------------------

多重度

::

  1 * subscriber.receive("hello")      // exactly one call
  0 * subscriber.receive("hello")      // zero calls
  (1..3) * subscriber.receive("hello") // between one and three calls (inclusive)
  (1.._) * subscriber.receive("hello") // at least one call
  (_..3) * subscriber.receive("hello") // at most three calls
  _ * subscriber.receive("hello")      // any number of calls, including zero
                                       // (rarely needed; see 'Strict Mocking')


対象制約

::

  1 * subscriber.receive("hello") // a call to 'subscriber'
  1 * _.receive("hello")          // a call to any mock object


メソッド制約

::

  1 * subscriber.receive("hello") // a method named 'receive'
  1 * subscriber./r.*e/("hello")  // a method whose name matches the given regular expression
                                  // (here: method name starts with 'r' and ends in 'e')

  1 * subscriber.status           // getterメソッド(getStatus)の代わりに、Groovy のプロパティ構文が使える
  1 * subscriber.setStatus("ok")  // setterの場合はそうはできないので、setterで書く


引数制約

::

  1 * subscriber.receive("hello")     // an argument that is equal to the String "hello"
  1 * subscriber.receive(!"hello")    // an argument that is unequal to the String "hello"

  // 同値性制約の例
  1 * check('string')
  1 * check(1)
  1 * check(null)
  1 * check(var)                         // 変数との比較でもOK
  1 * check([1,2])                       // Listとの比較
  1 * check([foo: 'bar', hoge: 'fuga'])  // Mapとの比較
  1 * check(new Person('sam'))           // Object との比較
  1 * check(person())                    // メソッド呼び出しの結果と比較

  1 * subscriber.receive()            // the empty argument list (would never match in our example)
  1 * subscriber.receive(_)           // any single argument (including null)
  1 * subscriber.receive(*_)          // any argument list (including the empty argument list)
  1 * subscriber.receive(!null)       // any non-null argument
  1 * subscriber.receive(_ as String) // any non-null argument that is-a String

  1 * subscriber.receive(endsWith("lo")) // an argument matching the given Hamcrest matcher (org.hamcrest.Matchers.*) .
                                         // 引数が Hamcrest matcher にマッチするかどうか。
                                         // a String argument ending with "lo" in this case

  // コード(クロージャー)による制約
  1 * subscriber.receive({ it.size() > 3 && it.contains('a') })
        // an argument that satisfies the given predicate.
        // (here: 長さ3を超え、'a'を含んでいる)

  1 * subscriber.receive({ it.contains('foo')} as String)  // 型制約と組み合わせる場合

  1 * list.add({
    verifyAll(it, Person) {
      firstname == 'William'
      lastname == 'Kirk'
      age == 45
    }
  })

        // 実際に渡された引数が it に入る。
        // このクロージャーは、thenブロックと同じように condition block として扱われる。
        // つまり、各行は暗黙assert化される。
        // assertが発生しなかったら、そのinteractionがマッチしたことになる。


  複数の引数を持つメソッドでも一緒
  1 * process.invoke("ls", "-a", _, !null, { ["abcdefghiklmnopqrstuwx1"].contains(it) })

  その他いろいろなんでも系
  1 * subscriber._(*_)     // any method on subscriber, with any argument list
  1 * subscriber._         // shortcut for and preferred over the above
  1 * _._                  // any method call on any mock object
  1 * _                    // shortcut for and preferred over the above


スタビング(値を返す、副作用を発生させる)
--------------------------------------------------

setup などモックインスタンスを作るときと同時に振る舞いを宣言してもいいし、
最後の例の様に、モッキングと同時に宣言してもいい。
ただし、同じメソッドについて行う場合は、1度でやる必要がある。
::

  // ``>>`` を書く場合は左に多重度は必要ない
  subscriber.receive(_) >> "ok"   // いつも同じ値を返す

  subscriber.receive("message1") >> "ok"     // 引数に応じた値を返す
  subscriber.receive("message2") >> "fail"

  subscriber.receive(_) >>> ["ok", "error", "error", "ok"]   // 呼ばれるごとの返り値を指定

  // 動的に値を返す
  subscriber.receive(_) >> { args -> args[0].size() > 3 ? "ok" : "fail" }
    // ↑クロージャーが、単一の型なし引数で定義されている場合は、args[] 方式
  subscriber.receive(_) >> { String message -> message.size() > 3 ? "ok" : "fail" } 
    // ↑クロージャーが、複数の引数 or 型付き引数で定義されている場合は、 one-by-one方式

  // 副作用の実行
  subscriber.receive(_) >> { throw new InternalError("ouch") }   // 例外を投げる

  // モッキングと同時に
  1 * subscriber.receive("message1") >> "ok"
  1 * subscriber.receive("message2") >> "fail"


Stub
Spy, パーシャルモック



Tips
===================

Groovy の仕様なのか意図していない使い方なのか、
Groovyでは java側で定義されたクラスの private なフィールドも触れるっぽい。

Groovy の小数リテラルは、特に何もしていしないとBigDecimal型になる。





