




# 変数

## 値

val --- 後で再代入できない
var --- 何度でも代入できる

val msg = "Hello, world!"
val msg2: java.lang.String = "Hello, world!" // 型明示
val msg3: String = "Hello, world!"           // 単純名

msg3 = "Good Bye, world!" // 再代入。varじゃないとエラーになる。

初期値。
var v: Int = _   // その型のデフォルト値を指定できる。

## 数値型

```
Int (32bit整数) : 255, 0377(8進数非推奨), 0xff(16進数)
    BigInt("0377", 8)  // どうしても8進数表記を使いたいとき
Long (64bit整数) : 255L, 0377L, 0xffL, 255:Long
Double : 1.0, 1.(これはダメになった), 1d, 1.0d, 1e2, 2e-1
Float : 1.0f, 1f, 1e2f, 2e-1f, 1:Float
Byte (8bit整数) : 123.toByte, 123.asInstanceOf[Byte], 123:Byte, v:Byte=123
Short (16bit整数): 123.toShort, 123.asInstanceOf[Short], 123:Short, v:Short=123
BigInt : BigInt(123), 123:BigInt
BigDecimal : BigDecimal(1.0), 1:BigDecimal, BigDecimal(1,2)→0.01
Boolean: true, false
```

```
// 数値→ 数値変換
数値.toInt
同様に、 toLong, toByte, toShort, toDouble, toFloat

// 数値 → 文字列
"%02x".format(byte)    // 16進表示文字列に変換
255.toHexString   // "ff"
255.toOctalString // "377"
bytes.map(b=>"%02x".format(b)).mkString(" ")  // Array[Byte]の16進表記

// 文字列 → 数値
"123" toInt
"3.14" toDouble

Integer.parseInt("77", 8)     // 63       八進表記の "77" を十進数に直すと 63
java.lang.Long.parseLong("123456789ABCDEF", 16)   // 十六進数

// Array[Byte] ←→ 文字列
str: String = new String(bb, "UTF-8")
bb: Array[Byte] = str.getBytes("UTF-8")


// Array[Byte] ←→ 数値  (いわゆる pack,unpack)
http://docs.oracle.com/javase/jp/8/docs/api/java/nio/ByteBuffer.html
    import java.nio.ByteBuffer
    import java.nio.ByteOrder

    // 整数型 → バイト列
    val buffer: ByteBuffer = ByteBuffer.allocate(4)
    buffer.order(ByteOrder.BIG_ENDIAN) // or LITTLE_ENDIAN
    buffer.putInt(i)
    buffer.array()   // Array[Byte] が返る。

    // バイト列 → 整数型
    // val buffer: ByteBuffer = ByteBuffer.allocate(サイズ)
    val buffer: ByteBuffer = ByteBuffer.wrap(bytearray)
    val i = buffer.getInt()

    buffer 内の相対アクセスのための位置ポインタのリセットについて、
    clear(), flip(), rewind() あたりの操作ができるが、
    ちゃんと調べていない。

```


## コレクション

配列 Array --- 単一型、ミュータブル(変更可能)

// String型、長さ3、中身は null, null, null
val greetStrings: Array[String] = new Array[String](3)
val greetStrings = new Array[String](3)  

// Array.applyメソッドがファクトリーメソッドになっている
val numNames = Array("zero", "one", "two") 

// 多次元配列

val a = Array.ofDim[Int](10, 9)
val b = Array.ofDim[Int](2, 3, 4)

リスト List --- 単一型、イミュータブル(変更不可)

初期化
val oneTwoThree = List(1,2,3)   // List.apply
val oneTwoTherr = 1 :: 2 :: 3 :: Nil
val thrill = "Will" :: "fill" :: "until" :: Nil
val nulllist = List()  // 空リスト
val nulllist = Nil     // 空リスト

操作
thrill(2)   // 要素の取得。先頭の添え字は0。
thrill.head   // 先頭要素を返す
thrill.last   // 末尾要素を返す
thrill.init   // 末尾を除いた残りのリストを返す
thrill.tail   // 先頭を除いた残りのリストを返す
thrill.drop(2)   // 先頭の2要素を除いた残りのリストが返される
thrill.dropRight(2)   // 末尾の2要素を除いた残りのリストが返される

val list3 = list1 ::: list2  // 連結した新しいList
val newlist = 1 :: list2     // 先頭に要素を追加した新しいList。cons操作。

thrill.isEmpty   // 空かどうかを返す
thrill.length   // 要素数を返す

thrill.reverse  // 逆順のリストを返す
thrill.mkString(", ")  // 文字列として、引数を間に挟んで連結。

// 関数渡す系
thrill.foreach(s => print(s))     // 各要素に対し処理を実行
thrill.foreach(print)             // 上と同様
thrill.map( s=> s+"y" )    // 各要素に関数を適用した結果のListを返す

thrill.count(s => s.length == 4)  // 条件に合う要素数。例だと 2が返る。
thrill.exists(s => s == "until") // 条件にあう要素が１つでもあれば true
thrill.forall(s => sendsWith("l"))  // 全ての要素が条件に合っていれば true

thrill.filter(s => s.length == 4) // 条件に合う要素だけのListを返す
thrill.remove(s=>s.length==4)  // 条件に合う要素を除いた残りのListを返す

thrill.sort((s,t)=>s.charAt(0).toLower < t.charAt(0).toLower) // ソート


タプル --- 型を問わない。イミュータブル。

val pair = (99, "Luftballons")
println(pair._1)   // 1から始まる！
println(pair._2)


集合 Set
var jetSet = Set("Boeing", "AirBus")   // イミュータブルのSet
jetSet.contains("Cessna")  // 要素の存在をチェック

jetSet += "Lear" 
    // ミュータブルの場合は、要素の追加
    // イミュータブルの場合は、 jetSet = jetSet + "Lear" となり、
    // 要素が追加された別Setが作られ、jetSet にBoundされる。

ミュータブルなSetを使いたい場合
import scala.collection.mutable.Set
イミュータブルは
import scala.collection.immutable.Set  // これは通常不要

HashSetってのもあるよ。


Option型

```
Option[A] --- 値が返らないときがある場合によく使う。
    Some[A] --- 値が返ったとき
    None    --- 値がないとき

opt.isEmpty
opt.isDefined
ops.nonEmpty
```


マップ Map

これも scala.collection.{immutable,mutable} の２つがある。
HashMapもある。

import scala.collection.mutable.Map
val treasureMap = Map[Int, String]()

// 要素の追加
//  k -> v という書き方は、2要素タプル (k, v) を返す。
//  実際は全てのオブジェクトに備わっている ->演算子。
treasureMap += (1 -> "Go to island.")
treasureMap += (2 -> "Find big X on ground.")
treasureMap += (3 -> "Dig.")

println(treasureMap(2))


イミュータブルMap
val romanNumeral = Map(
  1->"I", 2->"II", 3->"III", 4->"IV", 5->"V"
)



## イテレータ

Collections - イテレータ - Scala Documentation
http://docs.scala-lang.org/ja/overviews/collections/iterators.html

```
// 変換
it.toArray       // it が返す要素を配列に集める。
it.toList
it.toIterable
it.toSeq
it.toIndexedSeq
it.toStream
it.toSet
it.toMap        // it が返すキー/値ペアをマップに集める。
```


0 to 2  // 0,1,2


## 型、Any, AnyVal, AnyRef, Unit, Null, Nothing, 同一比較

参考  
http://www.ne.jp/asahi/hishidama/home/tech/scala/any.html

```
---------------------------
     Any
---------------------------
AnyVal     AnyRef
---------  ----------------
Unit       通常のクラス
Int        (Java・Scala)
Long       ----------------
Double     
など       Null
---------  ----------------
     Nothing
---------------------------
```

Any: 
    ==, != : オブジェクトの値(内容)が等しいかどうかを返す。 
             実態は equals()メソッド
    isInstanceOf[T], asInstanceOf[T]
AnyRef: 
    ==, != : オブジェクトの値（内容）が等しいかどうかを返す。
             自分自身がnullの場合はargもnullのときtrue。
             null以外の場合はequals()メソッドを呼び出す。
    eq, ne : インスタンスが同一かどうかを返す。Javaの「==」に相当。
    getClass(), 
    ##(), hashCode(), 
    synchronized[T](arg:T)
AnyVal: Java のネイティブ型に相当



Unit は型なし。()。 Java の void に相当。
Nothing: exit(i) の返り値や、常に例外が返るもの。値が戻らない。
null は Nullというクラスの値。AnyRefの全てのクラス(の変数)に代入できる。





# 関数・メソッド

## 関数定義

```
// 引数の型アノテーションは省略できない
// 戻り型アノテーションは省略可 (つけた方がよい)
// 引数は必ず val 扱いなので、"val" の明示は不要
def max(x: Int, y: Int): Int = {
  ...
}

// 返り値がUnit型の場合は、返り値型と "=" を省略できる
// 逆にこういう書き方をした場合は、返り値は Unit になる。
def myPrint(str:String) { ... }

// 1文だけならにょろかっこ省略可
def max(x: Int, y:Int): Int = if (x > y) x else y

// return文がなければ、計算された最後の値を返す
return ~(sum & 0xFF) + 1  // return はかっこで囲む必要はない
```

## 関数リテラル

```
arg => println(arg)
(arg: String) => println(arg)
```


関数リテラルが１つの引数を取る1文から構成される場合は、
引数を明示的に指定しなくても済む。
部分適用された関数(partially applied function)


## 関数を表す型

```
(引数の型, …) => 戻り型
(Int, Long) => Double
Int => Long    // 引数が１つの場合は、丸括弧を省略可
() => String   // 引数がない場合
=> String      // 丸括弧が無いのは、関数の型ではなく、名前渡し。 TODO

// 関数を指す変数・関数を引数にとる関数
var f : ((Int) => String) = null   
def test(f: (Int) => String) = { f(1) + f(2) + f(3) }
```


## 呼び出し
max(3,5)

// メソッドのパラメタが１つだけなら、ドットや括弧を使わずに呼び出せる
0 to 2              // (0).to(2)
Console println 10  // Console.println(10)
1 + 2               // (1).+(2)

※ 演算子の結合性 コロンは右、それ以外は左。

// 変数に括弧で囲んだ1つ以上の値を適用 -> applyメソッドが呼ばれる
myarray(2)  // myarray.apply(2) が呼ばれる。結果2番目の要素が返る。
// 括弧で囲んだ1つ以上の引数を伴う変数への代入 -> updateメソッドが呼ばれる
myarray(2) = "Hello"  // myarray.update(2, "Hello")


def greet() = println("Hello, world")  // 引数なし



名前渡し。
http://www.ne.jp/asahi/hishidama/home/tech/scala/def.html
関数を取る関数。関数がいつ評価されるか。
関数が渡るのか、関数を実行した結果が渡るのか。



# クラス と オブジェクト

## 基本型のクラス定義

最初に省略をしていない基本的な形を示す。
そのあとで色々な簡略形、および追加情報の書き方を示す。

```scala
class Rational(n: Int, d: Int) extends 親クラス {
  // クラス名直後の引数は、基本コンストラクタの引数となる

  require(d != 0)   // 事前条件

  type 型名 = 型

  // フィールド定義
  //    val でも var でも可。 デフォルトは public
  //    書かれた順で初期化されていく
  private val g = gcd(n.abs, d.abs)
  val numer: Int = n / g
  val denom: Int = d / g
  var 変数名:型 = _   // 初期値をその型のデフォルト値とする
  var 変数名:型       // 注: これだけだと、abstruct型にしろと怒られる TODO

  // 基本コンストラクタ
  //   クラス本体に書かれた(フィールド/メソッド定義以外の)任意のコードは、
  //   基本コンストラクタにコンパイルされる。
  println("Created " + n + "/" + d)

  // 補助コンストラクタ。 this という名前で定義。
  // 最初の処理として同じクラスの他コンストラクタを呼び出さないといけない。
  def this(n: Int) = this(n,1)

  // メソッド定義  
  //   関数定義と同様。 デフォルトは public
  //   メソッド引数は val のみ。なのであえてvalとは書かない。
  def add(b: Byte): Unit = {  
    sum += b
  }

  // 1行でも書ける。
  // メンバ変数を参照する場合は this を使う。ほとんどの場合は省略できる。
  def lessThan(that: Rational) = 
    this.numer * that.donom < that.numer * this.denom

  // 戻り型がUnitの場合は、戻り型と"=" を省略し中かっこで囲む書き方も可。
  def add(b: Byte) { sum += b }   

  // オーバーライド の場合は "override" をつける
  override def toString = numer + "/" + denom   

  // 演算子の定義も同様
  def + (that: Rational): Rational = ...
  def * (that: Rational): Rational = ...

  // 多重定義 オーバーロード
  def + (i: Int): Rational = ...

  // アクセス指定
  private def gcd(a: Int, b: int): Int = 
    ...

  // TODO
  def apply(...) { ... }
}
```

- フィールド名とメソッド名には、同じ名前をつけることはできない。
  (Scalaは ()がなくても呼び出せるので)
- 変数・定数・メソッド等の宣言（val・var・def・type）において
  「= ～」を書かなかった場合、抽象フィールド・抽象メソッドを定義したことになる。
- クラス名の後ろのカッコは「クラスパラメーター」。
  - これを元に基本コンストラクターが生成される。
    -  基本コンストラクタはクラスパラメータと同じ引数をとる。


## アクセス指定子

デフォルトは public。
protected, private。
protected[hoge], private[hoge] という指定の仕方もあり TODO

http://www.ne.jp/asahi/hishidama/home/tech/scala/class.html#h_access_modifiers

基本コンストラクタにアクセス指定子を付けたい場合は、以下のようにする。

```
class MyClass private (val a:Int, val b:Int) {... }
              ^^^^^^^
```

## クラス定義・継承・トレイトまわり

```
class クラス名 { ... }

// 継承。TODO 親クラスのコンストラクタに連鎖する？
class クラス名 extends 他クラス { ... }   

// 親クラスの引数つきコンストラクタに連鎖させる場合
class クラス名 extends 親クラス(値, ...) { ... }

// トレイト (Javaのインターフェースのようなもの)
class クラス名 extends 親クラス with トレイト
class クラス名 extends 親クラス with トレイト1 with トレイト2
class クラス名 extends トレイト
class クラス名 extends トレイト1 with トレイト2

abstract class クラス名 { }  // 必ず他クラスで継承して使う
final class クラス名  { }    // これ以上継承させたくない
sealed class クラス名  { }  // 同一ソースファイル内では継承可

クラス本体に書くことがない場合は、{ } 省略可。
```


## コンストラクタ・フィールド定義・初期化

Scalaでは、classのブロックの中に直接処理を書くのがコンストラクターになる。
(基本コンストラクタ)

```
class クラス名 {
  //ここに初期処理を記述
}

// 基本コンストラクタに引数を持たせたい場合
class クラス名(引数名:型, …) {
  //ここに初期処理を記述
}

// 基本コンストラクターの引数をただ単にフィールドの初期値としたいだけの場合、
// コンストラクターの引数にval・varを付けると、それがフィールドになる。
class Example(
  val n0: Int,
  var n1: Int
) {                 //  中身が不要であれば、中かっこも省略できる
}

//  引数のデフォルト値も指定できる
class Example(
  val n0: Int = 1,
  var n1: Int = 2
)
```


基本コンストラクターの引数にval・varを付けなくても、
メソッド内から使用できる。
この場合、暗黙にprivateな不変フィールド（val）が定義されて、値が保持される。

```
class Example(a0:Int, a1:Int) {
  val n0 = a0

  def foo() = a1

  def add(that: Example) = {
    new Example(this.a0 + that.a0, this.a1 + that.a1) 
    // ↑ このようなアクセスはできない。
  }
}
```

### 補助コンストラクタ (コンストラクタのオーバーロード)

this という名前のメソッドを定義。

補助コンストラクターの先頭では必ずthis(～)という呼び出しを行い、自分より前に定義されたコンストラクターを呼び出す必要がある。

```
class Example(a0:Int, a1:Int) {
  val n0 = a0
  var n1 = a1

  def this(a: Int) = this(a, 2)
  def this()       = this(1)
}
```


## インスタンス生成 (new)

```
new クラス名
new クラス名(引数...)
(実例)
val myclass = new ChecksumAccumulator
val myclass = new ChecksumAccumulator(引数...)

// 「new クラス名～」の後に波括弧「{}」を付けることで、
// 元のクラスを拡張したインスタンスを生成することが出来る。
// (そのクラスを継承した無名クラス)
new クラス名またはトレイト名 { 追加の定義 }
new クラス名またはトレイト名(引数...) { 追加の定義 }

new クラスまたはトレイト名         with トレイト1 with …
new クラスまたはトレイト名(引数…) with トレイト1 with …
new クラスまたはトレイト名         with トレイト1 with … { メンバー定義 }
new クラスまたはトレイト名(引数…) with トレイト1 with … { メンバー定義 }

// 一度きりのクラスはこんな風にすることも可
new { メンバー定義 }

// ??? TODO
new { 事前初期化   }  with トレイト1 with … { メンバー定義 }
```

注  
よくサンプルで見かける「Array(1,2,3)」「Array("a","b","c")」「List(1,2,3)」
といったnewを使わない初期化方法は、newが省略されているわけではなく、
コンパニオンオブジェクトの apply()メソッドの呼び出しである。


## パラメータ化された型(parameterized types）・いわゆるジェネリクス

http://www.ne.jp/asahi/hishidama/home/tech/scala/generics.html

クラスのジェネリクス

```scala
class Example[T] {        // 型パラメータが１つ
  protected var t: T = _
  def set(t: T): Unit = { this.t = t }
  def get(): T = { t }
}

val s = new Example[String]   // 使うとき

class Example[T, U] {     // 型パラメータが２つ
  def method1(t: T): Unit = { println(t) }
  def method2(u: U): Unit = { println(u) }
}

val s = new Example[String, Int]     // 使うとき
val s = new Example[String, Int]()

// 型パラメタが２つのときは中置記法が使える
val s = new (String Example Int)    //  Example[String, Int]
val s = new (String Example Int)()  
val s = new (String Example Int Example Long)   // Example[Example[String,Int], Long]
```

メソッドだけを型パラメタ化することも可能

```
def メソッド名[型パラメーター, …](引数, …) ～
class Example {
  def method[T](t: T): T = { t }
}

val obj = new Example 
val s = obj.method("abc")         // 使うとき。型推論してくれる
val s = obj.method[String](null)  // 明示的に型の指定
```

### 変異指定

中身の親子関係が、入れ物の親子関係にも言えるか。

```
以下親子関係を
(親) A <--- B <--- C (子)  のように矢印で表す。

MyList[A] <--- MyList[B] の関係が成り立つか？

MyList[T] :  無関係 (不変、nonvariant、厳密)
MyList[+T] :  MyList[A] <--- MyList[B] といえる  (共変、covariant)
MyList[-T] :  MyList[A] ---> MyList[B] といえる  (反変、contravariant)
```

- ミュータブルなコンテナは不変にすべき
- イミュータブルなコンテナは共変にすべき
- 変換処理の入力は反変に、出力は共変にすべき


## シングルトンオブジェクト

```
object ChecksumAccumulator {
  ... // クラス定義と同じような形
}
```

シングルトンオブジェクトがクラスと同じ名前を持つとき、
そのクラスのコンパニオンオブジェクトと呼ぶ。
逆にクラスを、シングルトンオブジェクトのコンパニオンクラスと呼ぶ。
クラスとコンパニオンオブジェクトは、同じソースファイルで定義しなければならない。
互いの非公開メンバーにアクセスできる。

コンパニオンクラスと同じ名前を共有しないシングルトンオブジェクトは、
スタンドアロンオブジェクトと呼ばれる。

class Queue[T] { ... }
object Queue { ... }
というのも可能か？(互いの非公開メンバにアクセスできるか？)

# 識別子

英数字識別子 
(アンダースコアは使わない流儀)
  小文字始まりキャメルケース
    length, flatMap, s
    フィールド、メソッドのパラメタ、ローカル変数、関数など
  大文字始まりキャメルケース
    BigInt, List, UnbalancedTreeMap
    クラス、トレイト
    定数も (ここだけjavaの流儀と違う)

演算子識別子

ミックス識別子

リテラル識別子




# 制御構造

if ( 条件式 ) { ... }
if ( 条件式 ) 単文


## match式

```
定数パターン(5,true,"hoge"などなど) --- その値にマッチするかどうか
ワイルドカードパターン(_) --- 何にでもマッチ。ただし右辺で参照できない。

var n = 1
val s = n match {
  case 1 => "いち"
  case 2 => "に"
  case 3 => "さん"
  case _ => "たくさん"
}

変数パターン --- 何にでもマッチ。その変数にbind。

  パターンに変数(valでも)を書いた場合の注意
  * 変数名が大文字で始まる単純名: 定数パターン。その値にマッチするか。
  * 変数名が小文字で始まる単純名: 変数パターン。つまり何にでもマッチ。
  * `変数名` とした場合: 定数パターン
  * オブジェクト名.変数名とした場合(this.pi, obj.piなど): 定数パターン


コンストラクタパターン
シーケンスパターン
タプルパターン
型付パターン




## 繰り返し

while ( 条件式 ) { ... }

args.foreach( 関数 )

for (arg <- args ) println(arg)


## 例外

try {
  式
  …
} catch {
  case e: IllegalArgumentException      => println("arg " + e)
  case e: IllegalStateException         => println("sta " + e)
  case e: UnsupportedOperationException => println("ope " + e)
  …
} finally {
  式
}


# main関数 コマンドライン引数

scalaプログラムのエントリポイントになるには、
mainメソッドを持つスタンドアロンシングルトンオブジェクトが必要。

object Summer {
  def main(args: Array[String]) {   // 引数は Array[String]。
    ...                             // 結果型 Unit 。なので等号が省略。
  }
}

Appトレイトを使うと少しコードが短くなる。
mainメソッドに入れるはずだったコードを、オブジェクトの中かっこの中に書く。
ただし制限がある
- JVMの制限から、マルチスレッドプログラムは明示的なmainメソッドが必要
  (コップ本の 4.5 Applicationトレイトのところ)

object Summer extends App {
  ...
  args 使えるよ。
}

以前あった Applicationトレイトは、2.9.0.final以降でdeprecatedになりました。


args   // コマンドライン引数
C/C++ と違って、最初の引数が args(0) に入る。
プログラム名(C/C++ の argv[0] に相当)は、



# ファイル操作


## テキストファイルの読み込み (Sourceクラス)

fromFile()で返されるSource（実際はBufferedSource）は、Char（文字）の並び。
getLines()メソッドを呼び出すと行毎の文字列（String）の並びになる。

```
// 1行ずつ処理
for (line <- Source.fromFile(args(0)).getLines()) { 
  println(line.length + " " + line)
}

Source.fromFile("abc.txt").getLines.toList  // 全行をリストに格納

Source.fromFile("abc.txt", "MS932")   // エンコード指定
```


## バイナリファイルの読み込み

FileInputStream を使う。

TODO

## その他ファイル操作

```
val f = new File(filePath)
val str = f.getName()   // パスからファイル名部分のみを取得。いわゆるbasename
val str = f.fetParent() // パスから親のパス部分のみを取得。いわゆる dirname
```



# こんなときはどうする？

## 乱数

scala.util.Random を使う。
http://www.scala-lang.org/api/current/#scala.util.Random

```
import scala.util.Random
rnd = new Random()
rnd = new Random(i)

rnd.nextInt()    // 範囲は Int 全体
rnd.nextInt(imax)   // 範囲は、[0, imax)

```


## 日時、時刻、日付

```
begin: Long = System.nanoTime();  // 経過時間の測定に使用
```


# チートシート

## アンダーバー(_) について

[Scalaでアンダースコアの意味が分からなかったらここを見る - Qiita](http://qiita.com/edvakf@github/items/0caeb282db18a1e65823)

```
import scala._    // Wild card -- all of Scala is imported
import scala.{ Predef => _, _ } // Exception, everything except Predef
def f[M[_]]       // Higher kinded type parameter
def f(m: M[_])    // Existential type
_ + _             // Anonymous function placeholder parameter
m _               // Eta expansion of method into method value
m(_)              // Partial function application
_ => 5            // Discarded parameter
case _ =>         // Wild card pattern -- matches anything
val (a, _) = (1, 2) // same thing
for (_ <- 1 to 10)  // same thing
f(xs: _*)         // Sequence xs is passed as multiple parameters to f(ys: T*)
case Seq(xs @ _*) // Identifier xs is bound to the whole matched sequence
var i: Int = _    // Initialization to the default value
def abc_<>!       // An underscore must separate alphanumerics from symbols on identifiers
t._2              // Part of a method name, such as tuple getters
```


暗黙の型変換

// implicit --- 暗黙の型変換を定義。 
// インタプリターが見えるスコープに書かないとだめ。class内に書いてはだめ。
implicit def intToRational(x: Int) = new Rational(x)

トレイト
    ミックスイン合成









# sbt

> [warn] there were 5 deprecation warnings; re-run with -deprecation for details

こんな風に言われたとき、以下のようにする。

```
$ sbt
> set scalacOptions in ThisBuild ++= Seq("-unchecked", "-deprecation")
とか
> set scalacOptions += "-unchecked"

> compile
> exit
```

標準出力に余計なものを出さない。
```
./sbt --error 'set showSuccess := false'  'set outputStrategy := Some(StdoutOutput)' "runMain Hogehoge" > 1.out 
```



# scalatest

## FlatSpec

- http://doc.scalatest.org/2.2.4/index.html#org.scalatest.FlatSpec

```scala
package org.scalatest.examples.flatspec.pending

import org.scalatest.FlatSpec

// この単位(クラスの単位)を Suite と呼ぶ
class SetSpec extends FlatSpec with GivenWhenThen {

  markup { """
ここに markdown の形式で自由に
ドキュメントが書けるよ。
...
...
  """ }

  behavior of "An empty Set"

  // この単位(メソッドの単位)を Test と呼ぶ
  it should "have size 0" in {       // should,must,can が使える

    assert(Set.empty.size === 0)     // 失敗時: "2 did not equal 1"
    assertResult(2) { a - b }        // 失敗時: "Expected 2, but got 3."

    // clue 付き
    assert(Set.empty.size === 0, "this is a clue")
    assertResult(3, "this is a clue") { 1 + 1 }
  }

  it should "produce NoSuchElementException when head is invoked" in {
    intercept[NoSuchElementException] {   // 例外が発生することを期待する場合
      Set.empty.head
    }

    withClue("this is a clue") {          // clue付き
      intercept[IndexOutOfBoundsException] {
	"hi".charAt(-1)
      }
    }
  }

  it should "fail,cancelなど" in {
    fail()                // 失敗を発生させる
    fail("メッセージ") 

    assume(database.isAvailable)
    assume(database.isAvailable, "The database was down again")
    assume(database.getAllUsers.count == 9)

    cancel()
    cancel("メッセージ")
  }

  // GivenWhenThen の例
  "A mutable Set" should "allow an element to be added" in {
    Given("an empty mutable Set")   // 事前状態を表現する
    val set = mutable.Set.empty[String]

    When("an element is added")    // 刺激や操作を表現する
    set += "clarity"

    Then("the Set should have size 1")  // 事後状態を表現する
    assert(set.size === 1)

    And("the Set should contain the added element")
    assert(set.contains("clarity"))

    info("That's all folks!")
  }

  // Ignore。一時的にテストを無効に。でも忘れないように、実行すると見える。
  //  c.f.  DoNotDiscover 
  ignore should "..." in {...}                 //  it -> ignore
  "An empty Set" should "...." ignore { ...}   // in -> ignore

  // pending の場合、 `is (pending)` と書くか、メソッドの最後を pending にする
  // `in (pending)` でもOKなようだ。
  it should "..." is (pending)  

  it should "......" in {
    ...   // GivenやWhenなどは通常どおりに出力される。その他コードも実行される
    pending
  }

  // Notifiers と alerters
  it should "..." in {
    ...
    info("info is recorded")              // テスト結果内に表示
    markup("markup is *also* recorded")   // テスト結果内に表示
    note("notes are sent immediately")    // 即座に表示(緑色)
    alert("alerts are also sent immediately")   // 即座に表示(黄色)
    ...
  }
}
```

主語(Subject)

- behavior of "An empty Set" のように指定する
- 短縮形として、`"An empty Set" should "have size 0" in { ... }` のように
  itのところに直接書いても良い
- it は、直前の主語の指定を継続する
- 複数形用に they も使うことができる

助動詞

- should, must, can

Ignore

- クラスごと ignore にする場合は、クラスに `@Ignore` をつける

Notifiers と alerters

- info と markup は、テスト結果内に表示。成否によって色が変わる
  - 仕様の記述の一部である場合はこちらを使う
- noteとalert は即座に表示。HTMLレポートには表示されない
  - 長いテストでどこまで進んでいるかを示す場合などに使う

テストのタグづけ

- テストメソッドにタグを付けてグループ化する。
  その単位でテストのやる/やらないを指定できたりするようだ。
- とりあえずは、使わなくてもなんとかなるので、省略

Matcher

- assert系の代わりに、より英語の自然な形で記述できるらしい。
- これも使わなくてもなんとかなるので、省略
- http://www.scalatest.org/user_guide/using_matchers

テストの流れ ( http://doc.scalatest.org/2.2.4/org/scalatest/ParallelTestExecution.html )

- 通常は、各テストクラス(suite)は並行して実行され、
  suiteの中の各テストはシーケンシャルに実行される
- 通常、suiteの中の各テストは同一のsuiteのインスタンスの中で実行される。
  そのため、あるテストでインスタンスに対して変更があると、
  次のテストに影響してしまうので、(テストの独立性を維持するためには)
  きちんと後処理する必要がある。
- 基本的には、各テストはどういう順序で実行されても大丈夫なように、
  独立性を高く書いたほうがよい
- OneInstancePerTestトレイトを入れると、
  テストごとにsuiteインスタンスが作成されるようになる。
- ParallelTestExecutionトレイトを入れると、各テストが並行して実行される。
  ParallelTestExecutionトレイトには OneInstancePerTest が含まれるので、


## FunSpec

```scala
import org.scalatest.FunSpec

class SetSpec extends FunSpec {

  describe("A Set") {
    describe("when empty") {               // describe は入れ子にできる
      it("should have size 0") {           // テストは it もしくは they で。
        assert(Set.empty.size == 0)
      }

      it("should produce NoSuchElementException when head is invoked") {
        intercept[NoSuchElementException] {
          Set.empty.head
        }
      }

      it("should have size 0") (pending)   // pending のときはこう書く

      ignore("....") {...}    // ignoreする場合は、こう書く
      
      // Given("..."), When("..."), Then("..."), And("...")
    }
  }
}
```



# scaladoc

- [Scaladoc - Scaladoc for Library Authors - Scala Documentation](http://docs.scala-lang.org/overviews/scaladoc/for-library-authors.html "Scaladoc - Scaladoc for Library Authors - Scala Documentation")
- [Scaladoc - Scala Style Guide v1.2.5 documentation](http://yanana.github.io/scala-style/scaladoc/ "Scaladoc - Scala Style Guide v1.2.5 documentation")

markdown(風？) 使える。HTMLタグも使える。
```
`monospace`       // 等幅
''italic text''   // 斜体
'''bold text'''   // 太字
__underline__     // 下線
^superscript^     // 上付き
,,subscript,,     // 下付き
[[entity link]], e.g. [[scala.collection.Seq]]      // クラスなどへのリンク
[[http://external.link External Link]],             // 外部リンク
  e.g. [[http://scala-lang.org Scala Language Site]]

コード: 
{{{
...code...
}}}

=Heading=, ==Sub-Heading==, etc
- ordered lists  (効かない？)
1., i., I., a.  numbered lists
```

置けるところ:  
フィールド、メソッド、クラス、トレイト、オブジェクト、パッケージ(特殊)。  
コンストラクタはクラスと同一なので、@constructor タグを使う。

```
クラス:  
    @constructor
メソッド: 
    @return  戻り値(one per metohd)
メソッド, コンストラクタ and/or クラス tags
    @throw
    @param f  ...    引数に関する説明 (one per parameter)
    @tparam T ...    type parameterに関する説明 (one per type parameter)
Usage tags
    @see
    @note
    @example
    @usecase
Other
    @auther
    @version
    @since
    @todo
    @deprecated
    @migration
    @inheritdoc
マクロ
    @define <name> <definition>
    $name
```

