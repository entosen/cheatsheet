




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

演算子
```
a / b  // 割り算。どちらかがFloat系なら少数点以下も計算。
       // 両方整数型なら 商。
a % b  // 剰余。 
       // どちらかがFloat系でも可。整数の商と、Double型の余り

```


```
// 数値→ 数値変換
数値.toInt
同様に、 toLong, toByte, toShort, toDouble, toFloat

// 数値 → 文字列
"%02x".format(byte)    // 16進表示文字列に変換
255.toHexString   // "ff"
255.toOctalString // "377"

// 文字列 → 数値
"123" toInt
"3.14" toDouble

Integer.parseInt("77", 8)     // 63       八進表記の "77" を十進数に直すと 63
java.lang.Long.parseLong("123456789ABCDEF", 16)   // 十六進数

// Array[Byte] ←→ 文字列
str: String = new String(bb, "UTF-8")
bb: Array[Byte] = str.getBytes("UTF-8")


// Array[Byte] → 16進表記文字列
bytes.map(b=>"%02x".format(b)).mkString(" ")  // Array[Byte]の16進表記文字列
bytes.map("%02x".format(_)).mkString(" ")  

// なにか → Byte列を作る
bytes = Array[Byte](0x32, 0x7f)   // 0x7f 以下限定。
bytes = Array[Int](0x32, 0xff).map(_.toByte)  
bytes = Array(0x32, 0xff).map(_.toByte)  


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


## 文字列

ドキュメントは java の String と、scala の StringOps を見る。
- http://docs.oracle.com/javase/jp/8/docs/api/java/lang/String.html

```
val s: String = "hogehoge"
val s: String = "foo\nbar"
val s = """abc
          |\n\n\n
          |def""".stripMergin
// 3つクオートの中ではエスケープは効かない
// stripMergin は marginChar(デフォルトは '|' 以降のみを有効に)

s.length
s.size
s.codePointCount(0, s.length)

s.equalsIgnoreCase("ABC")
s.isEmpty
s.nonEmpty

// 検索
s.indexOf('a')
s.latIndexOf('a')
s.indexOfSlice("abc", 0)   // 正規表現ではない。第2引数は、n回目のマッチの位置。
s.lastIndexOfSlice("abc", 0) 
s.contains('b')
s.contains("abc")

// 置換
s.replace('a', 'x')    // 全部置換
s.replace("ab", "x")   // "ab" を "x" に置換。正規表現使えない

s.replaceAll("[a-z]+", "123")   // 正規表現使える
s.replaceFirst("[a-z]+", "123")

s * n
```

### StringBuilder

```
val buf = new StringBuilder()
buf.append("aaaaa\n")
buf.append("bbbbb\n")
buf.result
```

### 加工文字列リテラル 

printfのようなことができる。 scala-2.10.0 より。

> http://docs.scala-lang.org/ja/overviews/core/string-interpolation.html

```scala
// s補完子
println(s"Hello, $name")       // Hello, James
println(s"1 + 1 = ${1 + 1}")  // 任意の式が受けられる

// f補完子
println(f"$name%s is $height%2.2f meters tall")

// raw補完子
raw"a\nb"    // エスケープを実行しない
```


## コレクション

ミュータブル(変更可能)とイミュータブル(変更不可)がある。

形として代表的なのは

- Seq (順序を持つ)
- Set (順序を持たない。重複許さない)
- Map (value を key に引っ掛けて格納できるやつ)

### Traversable

参考

- [Scalaコレクションメソッドメモ(Hishidama's Scala collection method Memo)](http://www.ne.jp/asahi/hishidama/home/tech/scala/collection/method.html#h_foreach)
- [Collections - Traversable トレイト - Scala Documentation](http://docs.scala-lang.org/ja/overviews/collections/trait-traversable.html)

コレクションは Traversable トレイトを mix-in しているので、
以下の操作ができる。


```
// 基本動作
foreach

// 加算
c1 ++ c2  // 連結

// map演算
c.map
c.flatMap
c.collect

// 変換
c.toArray
c.toList
c.toIterable
c.toSeq
c.toIndexedSeq
c.toStream
c.toSet
c.toMap

// コピー
c.copyToBuffer
c.copyToArray

// サイズ
c.isEmpty
c.nonEmpty
c.size
c.hasDefiniteSize

// 要素取得
c.head    // 先頭の要素を返す。
c.last
c.headOption
c.lastOption
c.find(p: (A)=>Boolean) 渡した関数で最初にtrueになった要素のOption値を返す

// サブコレクション取得
c.tail    // 先頭以外を返す。headと対。長さ1のときは、空のコレクションが返る
c.init
c.slice
c.take(n) // 最初のn個
c.drop(n) // 最初のn個を除いた残り
c.takeWhile(p) // 先頭から p が true である限り (初めて p がfalseになる１つ前まで)
c.dropWhile(p) // 先頭から p が true である限りの部分を除いた残り
c.filter(p)    // p がtrueの要素を抽出。Booleanを返す関数オブジェクト(predicate)を渡す。
c.filterNot(p) // p がfalseの要素を抽出。
c.withFilter
c.distinct // (Seqのみ？ Seqから重複するitemを除く。unique的な)

// 分割
c.splitAt     // 先頭n個 と 残りに整理する
c.span        // 最初からpredicateがtrueである範囲と残りに分割する
c.partition   // predicate の結果で２つに分割する
c.groupBy     // 判定関数の結果で、Mapに整理する

// 要素条件演算
c.exists(p: (A)=>Boolean)  1つでも条件にあうものがあればTrue
(c.f.) c.contains(elem: A1)  一致するものが1つでもあればTrue (Seqのみ？)
c.forall
c.count

// fold演算？？？
c.foldLeft
c.foldRight
/:
:/
c.reduceLeft
c.reduceRight

// 特定 fold 演算 (numeric か comparable のみ)
c.sum
c.product
c.min
c.max

// 文字列演算
c.mkString
c.addString
c.stringPrefix

// view演算？？？
view
```

Seq

Iterable に加え index でアクセスできる。
```
s(2)  // 2番めの要素を取得 (先頭は 0 )

// 指定した条件を満たす最初の要素のindexを返す。見つからなければ -1 。
s.indexWhere(要素の条件式)
s.lastIndexWhere(要素の条件式)
// 指定した要素が最初に出てくるindexを返す。見つからなければ-1 。
s.indexOf(elem)
s.lastIndexOf(elem)

s.startsWith
s.endWith
s.indexOfSlice
```


配列 Array --- 単一型、ミュータブル(変更可能)

// String型、長さ3、中身は null, null, null
val greetStrings: Array[String] = new Array[String](3)
val greetStrings = new Array[String](3)  

// Array.applyメソッドがファクトリーメソッドになっている
val numNames = Array("zero", "one", "two") 

// 多次元配列

val a = Array.ofDim[Int](10, 9)
val b = Array.ofDim[Int](2, 3, 4)


Arrayは == で中身の比較ができない。(他のコレクションはできる)
a1.sameElements(a2)  // シンプルな配列（一次元配列）でのみ可能
sameElements は、null の場合に NullPointerException になってしまう。
java.util.Arrays.equals(a1, a2)
が、null の場合にも対応しており、楽。


リスト List --- 単一型、イミュータブル(変更不可)

初期化
val oneTwoThree = List(1,2,3)   // List.apply
val oneTwoTherr = 1 :: 2 :: 3 :: Nil
val thrill = "Will" :: "fill" :: "until" :: Nil
val nulllist = List()  // 空リスト
val nulllist = Nil     // 空リスト

val list = List.fill(10)("a")  // 同じ値が指定回数繰り返されるリスト

操作
thrill(2)   // 要素の取得。先頭の添え字は0。
thrill.head   // 先頭要素を返す
thrill.last   // 末尾要素を返す
thrill.init   // 末尾を除いた残りのリストを返す
thrill.tail   // 先頭を除いた残りのリストを返す
thrill.drop(2)   // 先頭の2要素を除いた残りのリストが返される
thrill.dropRight(2)   // 末尾の2要素を除いた残りのリストが返される

list1 :+ elem   // 末尾に elem を追加した新しいリストを返す

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


### 集合 Set

```
// 基本機能
contains(elem: A): Boolean
iterator: Iterator[A]
+= (elem: A): this.type
-= (elem: A): this.type


```

```
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
```


### Option型

```
Option[A] --- 値が返らないときがある場合によく使う。
    Some[A] --- 値が返ったとき
    None    --- 値がないとき

Option("aaa")  // オブジェクトを使って生成。nullだとNoneを返す。
Some("aaa")    // オブジェクトを使って生成。nullだと Some(null) を返す。
None           // 生成。というかオブジェクト。

opt.isEmpty
opt.isDefined
ops.nonEmpty

// OptionのSeq を中身のSeqにする。
optList = List[Option[Int]](Some(100), None, Some(200))
optList.flatMap(x=>x)   // List(100,200)
```


### マップ Map

これも scala.collection.{immutable,mutable} の２つがある。

Map型は抽象的なトレイト。Mapオブジェクトで生成は可能。
実際には、

HashMapもある。

```
import scala.collection.mutable.Map
val treasureMap = Map[Int, String]()

// 要素の追加
//  k -> v という書き方は、2要素タプル (k, v) を返す。
//  実際は全てのオブジェクトに備わっている ->演算子。
treasureMap += (1 -> "Go to island.")
treasureMap += (2 -> "Find big X on ground.")
treasureMap += (3 -> "Dig.")

// 取得
treasureMap(2)           // キーが無ければ例外
treasureMap.get(2)       // 値をOptionに入れて返す。キーがなければNone
treasureMap.contains(2)  // キーが存在するかどうかを Booleanで返す

// 要素を抜く
map -= key       // 自分自身(Map) を返す
map.remove(key)  // Option[V] を返す

// キー一覧を取得など
map.keys         // キー一覧を取得: Iterable[A]
map.keySet       // キー一覧を取得: Set[A]
map.values       // バリュー一覧を取得: Iterable[B]
```


イミュータブルMap
```
val romanNumeral = Map(
  1->"I", 2->"II", 3->"III", 4->"IV", 5->"V"
)

map - 3  // 要素を抜いた新しいMapを返す
map + (6 -> "VI")  // 要素を追加した新しいMapを返す
```

Map に対する Traversal 系の操作は、(k,v) のタプルが順に関数に渡される。
その場合、タプルをバラすのに以下のように書くのが、定石っぽい。
(partial function。引数１つでmatch１つからなる関数の省略形？)

```
val x = Map(1 -> "foo", 2 -> "bar")
x map { case (k,v) => s"$k is $v" }

// c.f. 真面目に書くとこんな感じになる
x map ( (t) => {
  val (k,v) = t
  s"$k is $v"
  })
```

Mapの種類

- AnyRefMap : 中身の一致(==)ではなく参照の一致(equals)によってキー同一性を行うMap

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


0 to 4      // 0,1,2,3,4
0 until 4   // 0,1,2,3
seq.indices  // そのseqを舐めるための添字のリスト
0 to 10 by 2 // 0,2,4,6,8,10


## Scalaの階層構造、型、Any, AnyVal, AnyRef, Unit, Null, Nothing, 同一比較

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

```
Any: 
    ==, != : オブジェクトの値(内容)が等しいかどうかを返す。 
             実態は equals()メソッド
    isInstanceOf[T], asInstanceOf[T]
AnyRef: 
    ==, != : オブジェクトの値（内容）が等しいかどうかを返す。
             自分自身がnullの場合はargもnullのときtrue。
             null以外の場合はjavaのequals()メソッドを呼び出す。
    eq, ne : インスタンスが同一かどうかを返す。Javaの「==」に相当。
    getClass(), 
    ##(), hashCode(), 
    synchronized[T](arg:T)
AnyVal: Java のネイティブ型に相当
```



Unit は型なし。()。 Java の void に相当。
Nothing: exit(i) の返り値や、常に例外が返るもの。値が戻らない。
null は Nullというクラスの値。AnyRefの全てのクラス(の変数)に代入できる。


### 等価性

TODO コップ本の30章をちゃんと読む

- Any の equals は eq と同じく参照等価性をテストする。
- Any の hashCode は オブジェクトのアドレスを元に作られる

それがいやだったら equals, hashCode メソッドをオーバーライドする。

```
override def equals(other: Any): Boolean = {    // other の型は Any で定義すること！
}
override def equals(other: Any): Boolean = other match {
  case that: Point => this.x == that.x && this.y == that.y
  case _ => false
}
```




## 列挙型、Enum

２つの方法がある

- Enumeration を継承したオブジェクトで定義
  - (メリ) 軽量？ (Enumerationのドキュメントより)
  - (メリ) 大小関係がある
  - (デメ) match式で、全ての条件を列挙できているかのチェックをやってくれない
- sealed class を使って定義
  - (デメ) 重い？
  - (メリ) match式で、全ての条件を列挙できているかのチェックをやってくれる

参考: [列挙型 (enum) が欲しいときの Enumeration と case object... - tnoda-scala](http://tnoda-scala.tumblr.com/post/106430183326/%E5%88%97%E6%8C%99%E5%9E%8B-enum-%E3%81%8C%E6%AC%B2%E3%81%97%E3%81%84%E3%81%A8%E3%81%8D%E3%81%AE-enumeration-%E3%81%A8-case-object)


### Enumeration を継承したオブジェクトで定義。

[Scala列挙型メモ(Hishidama's Scala Enumeration Memo)](http://www.ne.jp/asahi/hishidama/home/tech/scala/enumeration.html)

```scala
object E1 extends Enumeration {
  type E1 = Value    # これをやっておくと、importして使う際に便利。
  val Matsu, Take, Ume = Value   # Valueは呼び出される度に異なる値を出力する。
}

object E2 extends Enumeration(10) {
  val Matsu, Take, Ume = Value   # 指定した番号から始める例
}

object E3 extends Enumeration {
  val Matsu = Value(11)          # ID を個別に割り当てる例。
  val Take  = Value(22)
  val Ume   = Value(33)
}
object E4 extends Enumeration {
  val Matsu = Value("Matsu")     # 列挙子を個別に割り当てる
  val Take  = Value("Take")
  val Ume   = Value("Ume")
}
object E5 extends Enumeration {
  val Matsu = Value(11, "Matsu") 
  val Take  = Value(22, "Take")
  val Ume   = Value(33, "Ume")
}
object E6 extends Enumeration( "Matsu", "Take", "Ume" ) {
  val Matsu, Take, Ume = Value
}

// 使い方
val e = E1.Matsu

// 使い方２
import E1._
val e = Matsu
def f(e: E1) = println(e)   // typeの定義をしておくことで、変数の型指定に使える

e match {
  case Matsu => println("松")
  case Take => println("竹")
  case Ume => println("梅")
}
e match {
  case Matsu | Take => println("松か竹")
  case _ =>
}
```

### Enumeration を使わずにやる方法

参考: [ScalaのEnumerationは使うな - Scalaで列挙型を定義するには | Scala Cookbook](http://xerial.org/scala-cookbook/recipes/2012/06/29/enumeration/)


```
object DNA {
  // objectで定義するとsingletonになる
  case object A extends DNA(0)
  case object C extends DNA(1)
  case object G extends DNA(2)
  case object T extends DNA(3)
  case object N extends DNA(4)

  // DNAの文字列をすべて並べる。
  val values = Array(A, C, G, T, N)
  // 用途によって別の集合を定義することもできる
  val exceptN = Array(A, C, G, T)

  private val codeTable = Array(A, C, G, T, N, N, N, N)

  def complement(code:Int) : DNA = codeTable((~code & 0x03) | (code & 0x04))
}

// sealedを付けると、DNAを拡張したクラスはこのファイル内でしか定義できない
// abstractを付けると、DNAを拡張したクラスはA, C, G, T, N以外にないことを保証できるので
// match文がexhaustive(すべてのケースを網羅)になる
sealed abstrat class DNA(val code:Int) {
    // A, C, G, T, Nをcase objectとすると、クラス名を表示するtoStringが実装される
    val name = toString
    // DNAクラスには自由にメソッドを定義できる
    def complement = DNA.complement(code)
}


// 使い方
val a : DNA = DNA.G

a match {
  case DNA.A => ...
  case DNA.C => ...
  ...
}
```



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
// あまり推奨されない。
def myPrint(str:String) { ... }

// 1文だけならにょろかっこ省略可
def max(x: Int, y:Int): Int = if (x > y) x else y

// return文がなければ、計算された最後の値を返す
return ~(sum & 0xFF) + 1  // return はかっこで囲む必要はない
```

引数
```
// デフォルト引数 (あまり推奨はされていないようだ)
def myFunc(i1: Int = 10): String = ...
myFunc()    // i1 は 10 で呼ばれる
myFunc(30)  // i1 は 30 で呼ばれる

```



注:
def で作成されたものは厳密には、メソッドであり関数オブジェクトではない。
変数に代入したり、関数を引数に取る関数に渡したりする場合は、"_" を使う。

もしくは、関数の型であることが明示されている場所への代入は自動的に関数オブジェクトに変換される。

```
val fp = func _
val fp: Int=>Long = func    // "_" 不要
```



## パラメータなしメソッドと 空括弧メソッド

お約束として、(主にクラスのメソッドで)引数を取らずに副作用もないメソッドは、
引数リストのカッコを書かない。
そういうメソッドを呼び出す際もカッコを書かない。

逆に副作用のあるメソッドは、空括弧メソッドとし、
呼び出すときも空括弧をつけて呼び出すのがよい。

```
  def width() = this.width    // よろしくない
  def width = this.width      // good
  val w = obj.width   // 呼び出し。まるでメンバーを参照しているような形になる。

  def greet() = println("Hello, world")  // 引数なし
  def increment() = ...   // 副作用があるので、空括弧メソッド
  obj.increment()         // 使うときもからカッコをつける。(つけなくても動くが)
```

こうすることで、メンバフィールド と 
パラメタなしメソッドは見た目上区別がなくなるので、
使う側が、それがメンバで実装されているのかメソッドで実装されているのか、
意識する必要がなくなる。

更に、パラメタなしメソッドを、メンバフィールドでオーバーライドすることもできる。
逆も可。






## 関数リテラル

```
(引数:型, …) => 本体 : 戻り型

(n: Int) => { n + 1 } : Int
(n: Int) => { n + 1 }
(n: Int) => n + 1

(m:Int, n:Int) => { m + n }
(m:Int, n:Int) => m + n

() => { println(123) }
() => println(123)

// 代入先の変数の型（関数の引数の型）が分かっている場合は、
// 関数リテラルの引数の型を省略できる
var f = (n:Int) => n + 1
f = (n) => n + 1
f = n => n + 1

// また、引数を明示せず、関数本体でプレースホルダが使える
f = { _ + 1 }     //  プレースホルダ
f = _ + 1

var f = (a:Int, b:Int) => { a + b }
f = { _ + _ }

// 使わない引数がある場合、仮引数名に"_"とつけることができる
var f = (a:Int, _:Int, _:Int) => { a }
f = (a:Int, _, _) => { a }
f = (a, _, _) => { a }
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

c.f 名前渡し。

http://www.ne.jp/asahi/hishidama/home/tech/scala/def.html
関数を取る関数。関数がいつ評価されるか。
関数が渡るのか、関数を実行した結果が渡るのか。


## 呼び出し

```
max(3,5)
```

### 省略

- [Scalaメソッド定義メモ(Hishidama's Scala def Memo)](http://www.ne.jp/asahi/hishidama/home/tech/scala/def.html "Scalaメソッド定義メモ(Hishidama's Scala def Memo)")

```
// scalaでは、オブジェクトとメソッドの間のピリオドを省略できる
str.substring(1,3)   
str substring(1,3)

// 引数のないメソッドの場合、ピリオドの他に丸括弧も省略できる
obj.toString() 
obj.toString
obj toString()
obj toString

// 引数が1つのメソッドも丸括弧を省略できる (中置記法)
str.eq("abc")
str eq("abc")
str.eq "abc"   // これはできない
str eq "abc"

0 to 2              // (0).to(2)
Console println 10  // Console.println(10)
1 + 2               // (1).+(2)

// 末尾がコロン「:」で終わるメソッドでは、ピリオドを付けない場合は左右を入れ替える。
// ※ 演算子の結合性 コロンは右、それ以外は左。
list.+:("aa")
"aa" +: list   // リストの先頭に要素を追加した新しいリスト

// 引数1個の場合、丸括弧の代わりにとげ括弧を使うことができる
// （「値を渡す」というより「処理を渡す（記述する）」というニュアンスの時に使用する）
str.eq("abc")
str.eq{"abc"} // 以下の例は、本来あまりやらない(処理じゃないので)
str eq{"abc"}

list map { ... } とか
```

### 可変長引数としてSeqを渡す

`: _*` を使う。

参考: [可変長引数としてリストを渡す - A Memorandum](http://etc9.hatenablog.com/entry/20100519/1274285392 "可変長引数としてリストを渡す - A Memorandum")

```
def output(strs: String*){ ... } 
// 通常
output("hoge1", "hoge2", "hoge3")

// Seqを渡す
val seq = Seq[String]("hoge1", "hoge2", "hoge3")
output(seq: _*)
```

### apply, update メソッド

```
// 変数に括弧で囲んだ1つ以上の値を適用 -> applyメソッドが呼ばれる
myarray(2)  // myarray.apply(2) が呼ばれる。結果2番目の要素が返る。

// 括弧で囲んだ1つ以上の引数を伴う変数への代入 -> updateメソッドが呼ばれる
myarray(2) = "Hello"  // myarray.update(2, "Hello")
```



## PartialFunction

書きかけ
- isDefinedAt
- lift
- orElse

## 関数の合成

```
// 関数の合成。２つの関数を連鎖させた新しい関数を作る
// f1 の結果を引数にとり、f2 を実行する関数を返す。
// つまり x を渡すと f2(f1(x)) を実行して返すような関数を作る
  f1 andThen f2
  f2 compose f1

// c.f. 処理結果を踏まえた連鎖
// Option型を使うと、1つ目の処理がうまくいったときのみ、
// その結果を使って2つ目の処理を行うということができる
// (flatMap という名前が直感的ではない。Maybeモナド。名前はあまり気にするな)
f1: (A) => Option[B]
f2: (B) => Option[C]
val result: Option[C] = f1 flatMap f2
```

c.f. Option型
- flatMap
- map
- getOrElse


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
  // *最初の*処理として同じクラスの他コンストラクタを呼び出さないといけない。
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

  // TODO  これはクラスではなくオブジェクトにあるものか？
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

// 継承。親クラスの引数なしコンストラクタに連鎖する。
class クラス名 extends 親クラス { ... }   

// 親クラスの引数つきコンストラクタに連鎖させる場合
class クラス名 extends 親クラス(値, ...) { ... }

// トレイト (Javaのインターフェースのようなもの) をミックスイン
class クラス名 extends 親クラス with トレイト
class クラス名 extends 親クラス with トレイト1 with トレイト2
//   親クラスが無い場合、1つ目のトレイトはextendsを使う。
class クラス名 extends トレイト
class クラス名 extends トレイト1 with トレイト2

abstract class クラス名 { }  // 必ず他クラスで継承して使う
final class クラス名  { }    // これ以上継承させたくない
sealed class クラス名  { }  // 同一ソースファイル内では継承可

クラス本体に書くことがない場合は、{ } 省略可。
```


コンストラクタは(基本コンストラクタも補助コンストラクタも)継承されない。

```
class A(val v1:Int, val v2:Int) { ... }

// Aに少しだけ機能追加しようと思って、以下のようにしても
// Bのコンストラクタは引数を取れないし、
// Aの引数なしコンストラクタを呼ぼうとするのでコンパイルエラー
class B extends A { ... }  

// 真面目にこのようにするか
class B(v1: Int, v2:Int) exntends A(v1, v2) { Bでの追加機能... }  

// もし、このコンストラクタ引数の取り回しが面倒な場合は、
// 以下のように new するときにやる
val b = new A(1,2) { Bでの追加機能... }
val b = new A(1,2) with Bでの追加機能を実装したトレイト
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


scala-2.11 から。(まだ Experimental かも)
元のクラスが、SAM(Single Abstract Method、つまり1つの抽象メソッドを持つクラス)場合、
それを実装したインスタンスはもっと簡単に書ける糖衣構文がある (知らないと読めない...)

```
// 元の書き方
val thread = new Thread(new Runnable {
   def run() {
     println("hello world")
   }
})
// 変更後
val thread = new Thread(() => println("hello world"))
// 分解して書くとこんな感じ
val r: Runnable = () => println("hello world")
val thread = new Thread(r)
```

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

シングルトンオブジェクトが初期化されるのは、最初にアクセスされたとき。

## トレイト trait

トレイトとクラスの違い
    1. クラスパラメータ(基本コンストラクタに渡されるパラメタ)を持てない
    2. super が動的に決まる。？？？

トレイトの使いどころ
    1. シンインターフェースをリッチインターフェースに変える
       既に持っている最小限のメソッドを利用して、
       リッチインターフェースを作る。
    2. クラスへの積み重ね可能な変更
        線形化


### トレイトの定義

class の定義とほぼ一緒。違いは、

- コンストラクタで引数を持つことができない。
    - コンストラクタの処理は書ける
- 引数を持った補助コンストラクタ( def this(～) )を定義することもできない

```
trait トレイト名 extends 親トレイトまたは親クラス with 他トレイト ... {
    type 形名 = 型
    val 定数名 = 初期値
    var 変数名 = 初期値
    def メソッド名(引数...): 戻り型 = { 本体 }

    // 抽象メンバー
    type 形名
    val 定数名: 型
    var 変数名: 型
    def メソッド名(引数...): 戻り型 
}
```


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


## match式 (パターンマッチ)

参考: [Scala matchメモ(Hishidama's Scala match Memo)](http://www.ne.jp/asahi/hishidama/home/tech/scala/match.html "Scala matchメモ(Hishidama's Scala match Memo)")

基本構文
- マッチした最初のものだけが使われる
- match は値を返す

```
var n = 1
val s = n match {
  case 1 => "いち"
  case 2 => "に"
  case 3 =>              // 次のcaseが来るまでは一連の処理。最後の値が返る
    "み"
    "さん"
  case 0 =>              // `=>` の右側に何も書かなければ何もしない
  case _ => "たくさん"   // ワイルドカードパターン。なんにでもマッチ
                         // ワイルドカードパターンなくてもいい。
			 // マッチするのがなかったら例外 MatchError
}
```

`=>` の右辺で値を使わなくてよい場合

```
n match {   // 数値
  case 1 => "いち"
  case 2 => "に"
  case 4 | 9 | 13 => "不吉"  //  複数パターン。どれかに当たればマッチ
  case _ => "たくさん"
}

s match {  // 文字列
  case "abc" => 1
  case "def" => 2
}

a match {   // a: Array[Int]
  case Array(1,2,3) => 1
  case Array(4,5,6) => 2
}

t match {   // t: (Int, String)
  case (1,"abc") =>  11
  case (2,"abc") => 21
  case (1,"def") => 12
  case (2,"def") => 22
}

obj match {    // 値の一部の項目だけマッチしていればいい場合
  case (1, _) => "tup2-1"
  case (2, _) => "tup2-2"
  case (_, 3) => "tup2-3"
  case (_, _, _) => "tup3"
} 

lst match {    // 引数が可変になる場合 `_*` でその他を表せる。末尾のみ。
  case List(1, _*) => "one"
  case List(2, _*) => "two"
}

obj match {    // 型でのマッチング
  case _: String => "文字列"
  case _: Int    => "整数"
  case _: Set[_] => "集合"    // Set[Int]などとやっても、中の型は無視される
  case _         => "知らない"
}
```

マッチした値を取得する
```
obj match {    // obj が Any だとして、型ごとに処理を分ける。
  case s: String => s.length  // s は String型として扱える
  case a: Array[_] => a.length
  case l: List[_] => l.size
}

obj match {     // 中身の一部を取得 (タプル)
  case (1, s)    => "one " + s
  case (2, s)    => "two " + s
  case (_, s, _) => "tup3 " + s
}

obj match {    // 「@」を使うと、caseにマッチした値全体と、
               //  一部分を変数に入れたものが受け取れる。
  case t @ (_,b)   => t + "=" + b
  case t @ (_,_,c) => t + "=" + c
}

opt match {        // Option の中身を取り出すときの定石
  case Some(v) => v
  case _       => "default"
}
```

TODO
- コンストラクタパターン
- シーケンスパターン
- タプルパターン
- 型付パターン

パターンに変数(valでも)を書いた場合の注意
* 変数名が大文字で始まる単純名: 定数パターン。その値にマッチするか。
* 変数名が小文字で始まる単純名: 変数パターン。つまり何にでもマッチ。
* `変数名` とした場合: 定数パターン
* オブジェクト名.変数名とした場合(this.pi, obj.piなど): 定数パターン



## 繰り返し

while ( 条件式 ) { ... }

collection.foreach( 関数 )  //  返り値はない

for (arg <- args ) println(arg)   // 返り値はない


## 例外

```
// 投げる
throw new IlligalArgumentException()
throw new IlligalArgumentException("hogehgoe")
throw new IlligalArgumentException("hogehgoe", throwable)

// キャッチする
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

// 全ての例外をキャッチする
  case e: Throwable => ...
// NonFatal を使うのがおすすめ。
  import scala.util.control.NonFatal
  case NonFatal(e) =>  ...
  // _: VirtualMachineError | _: ThreadDeath | _: InterruptedException | 
  // _: LinkageError | _: ControlThrowable

// Exception の操作
ex.getMessage   // message 文字列
ex.toString     // Exceptionクラス名: message文字列

// stack trace 
ex.printStackTrace()   // 標準エラー出力へ

val sw = new StringWriter  // 文字列へ
e.printStackTrace(new PrintWriter(sw))
sw.toString

// 自分で例外を定義
class MyException(message :String = null, cause :Throwable = null) 
  extends Exception(message, cause)
```

### 代表的な例外

```
MatchError (scala, RuntimeException)
    match式で該当のものがなかった場合

IllegalArgumentException (java.lang, RuntimeException)
    不正な引数、または不適切な引数をメソッドに渡したことを示すためにスローされます。
    require(式) が満たされなかったとき

NoSuchElementException (java.util, RuntimeException)
    リクエストされている要素が存在しないことを示します。
    Mapにキーが存在しないとき
```

# main関数 コマンドライン引数

scalaプログラムのエントリポイントになるには、
mainメソッドを持つスタンドアロンシングルトンオブジェクトが必要。

object Summer {
  def main(args: Array[String]): Unit = {   // 引数は Array[String]。
    ...                                     // 結果型 Unit
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


## バイナリファイルの読み書き

FileInputStream, FileOutputStream を使う。

```
val file = new File(workdirFile, "out.bin")
var out: FileOutputStream = null
try {
  out = new FileOutputStream(file)  // 引数は文字列でも可
  out.write(bytes)
} finally {
  if ( out != null ) {
    out.close()
  }
}
```



## java.io.File クラス

ファイルパスとそれに対する操作ができる。

```
// 作り方
new File("./hoge.txt")
new File("dirname", "filename.txt")   // パスの連結

// 取得系メソッド
val str = f.getName()   // パスからファイル名部分のみを取得。いわゆるbasename
val str = f.getParent() // パスから親のパス部分のみを取得。いわゆる dirname
getParentFile, getPath
isAbsolute, getAbsolutePath, getAbsoluteFile, 
getCanonicalPath, getCanonicalFile

canRead, canWrite, canExecute

exists, isDirectory, isFile, isHidden
lastModified, length, 

list, listFiles,
listRoots,
getTotalSpace, getFreeSpace, getUsableSpace

// 操作系メソッド
setReadOnly, setWritable, setReadable, setExecutable
setLastModified, 

createNewFile
delete
deleteOnExit
mkdir, mkdirs
renameTo
createTempFile
```

# 外部コマンド、シェルコマンド

TODO どういう風にシェルの解釈がはいるか。
```
import scala.sys.process._

Process("ls").run   // 実行(非同期。終了を待たない)
Process("ls").!     // 終了コードを返す
Process("ls").!!    // 標準出力の結果を返す
Process("ls").lines    // 標準出力の結果を行ごとにリストとして返す

// 文字列でも可
"ls" run
"ps aux" #| "grep java" !            // パイプは #|演算子
"ps aux" #> new File("hoge.txt") !   // リダイレクト

// 引数を明示する場合  Seq[String] を使う
Seq("ps", "aux") !!
```

stderr の内容も取りたい場合はこう。
o,e は改行が除かれてくるっぽいので注意
```
val logger = ProcessLogger(
    (o: String) => println("out " + o),
    (e: String) => println("err " + e))
とか
val out = new StringBuilder
val err = new StringBuilder
val logger = ProcessLogger(
    (o: String) => out.append(o),
    (e: String) => err.append(e))
とかやって

"ls" ! logger
```

windows で動かす場合は、シェルの解釈に癖があり、ダブルクオートが落ちる場合がある
```
  val mylib_version = System.getProperty("os.name") match {
    case os if os.contains("Windows") =>
      Seq("awk", """/mylib/ {printf(\"[%s,%s]\", $5, $6); exit}""", "mylib.versions").!!.trim
    case _ =>
      Seq ("awk", """/mylib/ {printf("[%s,%s]", $5, $6); exit}""", "mylib.versions").!!.trim
  }
  "mylib" % "mylib" % mylib_version
```

# スレッド、並行処理など

参考: [今まで知らなかった 5 つの事項: java.util.concurrent 第 2 回](http://www.ibm.com/developerworks/jp/java/library/j-5things5.html "今まで知らなかった 5 つの事項: java.util.concurrent 第 2 回")

## 同期、待ち合わせの仕組み

### CountDownLatch

(Javaの機能。)
競馬の出走ゲート。Countが0になるまで待たせるための仕組み。
別スレッドで動いている何かの処理が終わるまで待つような場合に使える。

```scala
import java.util.concurrent.CountDownLatch
val latch = new CountDownLatch(1)
latch.await()   // 待つスレッド。カウントが0になるまで待つ。
latch.countdown()  // 待たせる側のスレッド。カウントを１つ減らす。
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

## URLencode,URLdecode

```
val encoded = java.net.URLEncoder.encode(raw, "UTF-8")
val decoded = java.net.URLDecoder.decode(encoded, "UTF-8")
```

## Config

JAVA の Propertiesクラスを使うのが一般的。
設定ファイルフォーマットは、以下の loadメソッドのところに記載。
- http://docs.oracle.com/javase/jp/8/docs/api/java/util/Properties.html

```
import java.util.Properties
import java.ioFileInputStream
val confFileName = "hoge.conf"
val prop = new Properties
prop.load(new FileInputStream(confFileName))
// FileInputSteram だとASCII以外受け付けてくれないかも
// Readを使うと大丈夫かも。実験してない。

prop.getProperty("key1")
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

## ディレクトリ構造

```
// ビルド定義ファイル
build.sbt
project/
  Build.scala

// ソースコード
src/
  main/
    resources/
      <メインの jar に含むデータファイル>
    scala/
      <メインの Scala ソースファイル>
      jp/co/mydomain.... と続く
    java/
      <メインの Java ソースファイル>
  test/
    resources/
      <テストの jar に含むデータファイル>
    scala/
      <テストの Scala ソースファイル>
    java/
      <テストの Java ソースファイル>

// ビルド成果物
target/                    // sbt clean をすると中身が消される
  resolution-cache/
  scala-2.10/
    classes/               // クラスファイルが格納
    test-classes/          // テストコードのクラスファイルを格納
    api/                   // scaladoc の出力
  streams/
  test-reports/            // テストの結果

  test-workdir/            // テスト時に一時的にファイルを置いたりするところ(独自)
```

こういうのはどこに置けばよいか

- 本番のコードで読み込みたいファイル
  - src/main/resources 直下                 // ※1
  - src/main/resources/jp/co/.... 以下      // ※1
- テストのコードで読み込みたいファイル → test/resources
  - src/test/resources 直下                 // ※1
  - src/test/resources/jp/co/.... 以下      // ※1
- テスト時に出力したり、一時的にファイルを操作したいとき
  - target/test-workdir/jp/co/.... 以下に作るのはどうだろうか。 ※2

※1: 後述の「リソースについて」を参照
※2: 後述の「テストでのファイルの出力」を参照

参考: ディレクトリ取得の方法
```
// カレントディレクトリの取得
new java.io.File(".").getCanonicalPath
System.getProperty("user.dir")

// パッケージ名の取得
getClass.getPackage.getName
val packagedir = getClass.getPackage.getName.replace('.', '/')

// パッケージパスも含めたクラス名の取得
getClass.getName
val classdir = getClass.getName.replace('.', '/')


// テストでなにかファイル出力したいときはこんな感じ
val classdir = getClass.getName.replace('.', '/')
val workdir = new File("target/test-workdir", classdir).toString

// workdir を掘っておく
val workdirFile = new java.io.File(workdir)
if ( ! workdirFile.exists ) {
  workdirFile.mkdirs()
}
```

## build.sbt

```
name := "study-scala-finagle-future"

version := "1.0"

scalaVersion := "2.11.8"

libraryDependencies += "com.twitter" %% "finagle-http" % "6.33.0"
libraryDependencies += "org.apache.kafka" %% "kafka" % "0.8.2.2" exclude("org.slf4j", "slf4j-log4j12")
libraryDependencies += "org.json4s" %% "json4s-native" % "3.3.0"

// 除外するときはこんな感じ
libraryDependencies += ("org.apache.kafka" %% "kafka" % "0.10.0.0"
  exclude("org.slf4j", "slf4j-log4j12")
  exclude("javax.jms", "jms")
  exclude("com.sun.jdmk", "jmxtools")
  exclude("com.sun.jmx", "jmxri")
  // exclude("org.slf4j", "slf4j-simple")
)

// 除外は、こうも書けるらしい
libraryDependencies +=
  "org.apache.zookeeper" % "zookeeper" % "3.4.9" excludeAll(
    ExclusionRule(name = "jms"),
    ExclusionRule(name = "jmxtools"),
    ExclusionRule(name = "jmxri")
    )
```

## sbt コマンド

```
compile

test
testOnly *テストクラス名   // 本来(packageの?)フルパス指定なので、'*'つける

dependencyTree  // ライブラリの依存関係のグラフが見られる
```

## リソースについて

プログラムやテスト中に必要なファイルをどう指定するか。
リソースを使うと実行環境によらず、クラスからの相対パスかプロジェクトトップからの絶対パスで呼び出せる。

src/main/scala や src/test/scala 以下に置いても、scalaファイル以外は無視されるようで、だめ。

```
val url1 = getClass.getResource("/simple_mdbm_1.txt")   // src/test/resources/ 直下に置いた場合
val url2 = getClass.getResource("simple_mdbm_2.txt")    // src/test/resources/ 以下に jp/co/... など同じディレクトリ構造で置いた場合
val s = Source.fromURL(url)
```

sbtは、以下のようにコピーしているらしい。(targetが実行環境？)

- src/main/resources/ 以下は、 target/scala-[scalaVersion]/classes 以下に
- src/test/resources/ 以下は、 target/scala-[scalaVersion]/test-classes 以下に

参考
[scala - How to access test resources? - Stack Overflow](http://stackoverflow.com/questions/5285898/how-to-access-test-resources "scala - How to access test resources? - Stack Overflow")


## テストでのファイルの出力

前提。
scalatestの各テストは、
カレントディレクトリがプロジェクトのトップディレクトリで動く。

テストの中でファイルを出力するときは、target/test-workdir/jp/co/..... 以下にしよう(独自)
```
val packagedir = getClass.getPackage.getName.replace('.', '/')
val outDir = new File("target/test-workdir/", packagePath)
outDir.mkdirs
val outputFile = new File(outDir, "output.txt")
val writer = new PrintWriter(outputFile)
writer.write(....)
writer.close
```

## 未整理

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

  markup { 
    """
      こういう書き方をすると、
      行頭のインデントをいい感じでのぞいてくれるようだ。
    """.stripMargin}

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

    // intercept は発生した例外を戻り値として返すので、
    // さらにそれをassertすることも可能
    val ex = intercept[NoSuchElementException] {
      Set.empty.head
    }
    asser( ex.message == "...." )

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
	assertResult(0) { Set.empty.size }      
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

## FeatureSpec

```scala
import org.scalatest.FeatureSpec
class SetSpec extends FeatureSpec {

  feature("The user can pop an element off the top of the stack") {
 
    scenario("pop is invoked on a non-empty stack") {
    }
 
    scenario("pop is invoked on an empty stack") {
    }

  }

}
```

## ScalaMock

- http://www.scalatest.org/user_guide/testing_with_mock_objects
- http://scalamock.org/quick-start/
- http://scalamock.org/api/index.html#org.scalamock.package


### テストへの組み込み方法

```scala
import org.scalatest.FlatSpec
import org.scalamock.scalatest.MockFactory

// クラスに MockFactory をextends してあげるひつようがある。
class ExampleSpec extends FlatSpec with MockFactory with ...  {

}
```

### モック的スタイル ( expectations-first )

全体の流れ
```scala
val mFunc = mockFunction[Int, String]    // Function Mock
val heaterMock = mock[Heater]            // Trait, interface Mock
// テストしたいオブジェクトをモックにつなげて生成
val coffeeMachine = new CoffeeMachine(heaterMock)  

// expects
mFunc expects (42) returning "Forty two" once

(mObj.isReady _).expects().returning(true)
(heaterMock.setPowerState _).expects(PowerState.On)
(heaterMock.setPowerState _).expects(PowerState.Off)
(mObj.func1 _).expects(*)   // wildcard
(mObj.func1 _).expects(~1.0)   // Epsilon Matching

(mObj.func1 _).expects().throws(new RuntimeException("what's that?"))


coffeeMachine.makeCoffee()  // 実行。expectどおりになるかをテスト
```

期待する関数がオーバーロードされている場合の指定
```
(m.overloaded(_: Int)).expects(10)
(m.overloaded(_: String)).expects("foo")
(m.overloaded[Double] _).expects(1.23)
(m.curried(_: Int)(_: Double)).expects(10, 1.23)
(m.polymorphic(_: List[Int])).expects(List(1, 2, 3))
(m.polymorphic[String] _).expects("foo")
``` 

> Overloaded method cannot be mocked if one of its parameters is a generic available to the trait. ・ Issue #93 ・ paulbutcher/ScalaMock
> https://github.com/paulbutcher/ScalaMock/issues/93

引数のマッチング
```
// 任意の関数を使ってチェック
// (例1)オブジェクトの中身をチェックしたいとき
(leaderBoardMock.addPointsForPlayer _) expects (where {
  (player: Player, points: Int) => player.id == 789 && points == 100
})

// (例2)引数間の大小を比較したいとき
mockedFunction expects (where { _ < _ }) // expects that arg1 < arg2
```

返す値
```
// 何も指定しないと null が返る

// 単純に値を返す場合、 returning を使う
(m.getPosition _).expects().returning(15.0, 10.0)
// 引数から計算した値を返す場合、 onCall を使う
m expects (*) onCall { _ + 1 }
m expects (*,*) onCall( (arg1: Int, arg2: Int) => arg1 * arg2 )

// 引数に 名前渡しが含まれていてそれを使いたい場合
// (1引数のonCall(Product=>A)を使う。その場合名前渡しの部分は Function0 になる
def getElse(i: Int)(f: => String): String = { ... }
(m.getElse(_:Int)(_: String)).expect(10, *)
  .onCall(_.productElement(1).asInstanceOf[() => String]())

// 例外を発生させる場合 throws を使う
m expects ("this", "that") throws new RuntimeException("what's that?")
```

呼び出し回数
```
// 何も指定しないと1回だけ呼ばれることを期待

// 回数を指定する場合
m1.expects(42).returns(42).repeat(3 to 7)
m2 expects (3) repeat 10

// エイリアス (http://scalamock.org/api/org/scalamock/CallHandler.html)
m1.expects("this", "that").once
m2.expects().returns("foo").noMoreThanTwice
m3.expects(42).repeated(3).times
```

呼び出し順序
```
// 指定しなければ順不同

// 順序指定する場合。inSequence を使う。
inSequence {
  m expects (1)
  m expects (2)
}

// 順序依存関係が2通りある場合。(例: 1と3はどちらが先でも可)
inSequence {
  m expects (1)
  m expects (2)
}
inSequence {
  m expects (3)
  m expects (4)
}

m(3)
m(1)
m(2)
m(4)

// こんな風に入れ子にもできる
(m.a _).expects()
inSequence {
  (m.b _).expects()
  inAnyOrder {
    (m.c _).expects()
    inSequence {
      (m.d _).expects()
      (m.e _).expects()
    }
    (m.f _).expects()
  }
  (m.g _).expects()
}
```


### スタブ的スタイル ( record-then-verify )

```scala
val m = stubFunction[Int, String]   // Function Stub
val heaterStub = stub[Heater]       // Trait, interface Stub
// テストしたいオブジェクトをスタブにつなげて生成
val coffeeMachine = new CoffeeMachine(heaterStub)

(heaterStub.isReady _).when().returns(true)  // スタブの挙動を決めてあげて

coffeeMachine.makeCoffee()   // 実際動かす

// どういう風に呼ばれたかを検証
(heaterStub.setPowerState _).verify(PowerState.On)  
(heaterStub.setPowerState _).verify(PowerState.Off)
```

verify は、そういう引数で呼ばれたのが指定回数(デフォルトは1回)であればよい。
それ以外の引数で呼ばれたのは何回あってもいい。


```
// 特定の引数で呼ばれた場合を記述
(m.func _).when(222).returns(true)

// 例外を返す場合
(m.func _).when(*).throws(new MyException())

// 渡された引数に応じた値を returnsする場合
(m.func _).when(*).onCall {
  arg: Int => arg + 1
}

```


### 未整理

```
val fakeDb = stub[PlayerDatabase] 

// configure fakeDb behavior 
(fakeDb.getPlayerById _) when(222) returns(Player(222, "boris", Countries.Russia))
(fakeDb.getPlayerById _) when(333) returns(Player(333, "hans", Countries.Germany))

// use fakeDb
assert(fakeDb.getPlayerById(222).nickname == "boris")
```


```
// Proxy mocks (trait や Java interface をモック)
//    org.scalamock.ProxyMockFactory を mix-in
val m = mock[Turtle]
m expects 'setPosition withArgs (10.0, 10.0)
m expects 'forward withArgs (5.0)
m expects 'getPosition returning (15.0, 10.0)

// Generated mocks (クラス、singleton/companion object をモック)
// そのクラスの方に、以下をmixする必要がある
//     クラス --- org.scalamock.annotation.mock annotation
//     コンパニオンオブジェクト付きクラス
//            --- org.scalamock.annotation.mockWithCompanion
//     シングルトンオブジェクト
//            --- org.scalamock.annotation.mockObject

// テストコードの方には GeneratedMockFactory を mix-in 
val m = mock[Turtle]
m.expects.forward(10.0) twice

val m = mockObject(Turtle)
m.expects.createTurtle

val m = mock[Turtle]
m.expects.newInstance('blue)   // 引数付きコンストラクタを使いたい場合？
m.expects.forward(10.0)
```

```
import org.scalatest.{ FlatSpec, PrivateMethodTester }

class PersonSpec extends FlatSpec with PrivateMethodTester {

  "A Person" should "transform correctly" in {
      val p1 = new Person(1)
      val transform = PrivateMethod[Person]('transform)
      assert(p2 === invokePrivate transform(p1))
    }
  }
}
```


# scaladoc

- [Scaladoc - Scaladoc for Library Authors - Scala Documentation](http://docs.scala-lang.org/overviews/scaladoc/for-library-authors.html "Scaladoc - Scaladoc for Library Authors - Scala Documentation")
- [Syntax - Scala Wiki - Scala Wiki](https://wiki.scala-lang.org/display/SW/Syntax "Syntax - Scala Wiki - Scala Wiki")
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

見出し:
=Heading=, ==Sub-Heading==, etc

リスト: (頭にスペース１つあけないと、効かない)

 - ordered lists  
 - hogehoge
   - level2

(1., i., I., A., a. が使えるらしい。)
 1. hoge
 1. fuga
    1. aaa
    1. bbb
       I. AAA
       I. BBB

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
    @throws expeption ...
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

# scalastyle

警告を止めたいとき。http://www.scalastyle.org/configuration.html
```
// scalastyle:off magic.number
... 
// scalastyle:on magic.number

1行なら
naughty()  // scalastyle:ignore
```

チェック項目のId http://www.scalastyle.org/rules-0.5.0.html
```
magic.number
method.length
parameter.number
no.whitespace.before.left.bracket
```

# ログ (Logging)

- Scala用ラッパーライブラリ: scala-logging
- 共通ログインターフェースライブラリ: SLF4J
- バックエンドライブラリ: logback

参考

- http://logback.qos.ch/manual/introduction_ja.html


## コードに書く側の仕組み

```
import com.typesafe.scalalogging.Logger
import org.slf4j.LoggerFactory

// logger_name の指定があれば、以下のように
val logger = Logger(LoggerFactory.getLogger("logger_name"))
// 一般的にはクラス名を書くことが多いようだ
// (階層になっているので後で設定で切り分けし易い)
val logger = Logger(LoggerFactory.getLogger(getClass))

// Logging, LazyLogging, StrictLogging というトレイトもあり。
// logger インスタンス変数が定義されます。
// logger_name はクラス名が自動で使われる？
class MyClass extends Logging {
  logger.debug("foo")
}

logger.trace("hoge")
logger.debug("foo")
logger.info("bar")
logger.warn("baz")
logger.error("baz")
```

遅延評価って言っているのは、
scala-logging では、
自動的に以下のようなコードに変換されるらしいので、
someHeavyFunc が呼ばれるのは、実際に出力されるとき。
つまり、infoを出力する設定になっていない場合は、 someHeavyFunc は評価されない。
```
logger.info("===" + someHeavyFunc + "===")
↓
if ( logger.isInfoEnabled ) {
  logger.info("===" + someHeavyFunc + "===")
}
```



## ログを出力する側の仕組み

### logback の設定ファイル

> http://logback.qos.ch/manual/configuration_ja.html#auto_configuration

- logback はクラスパス上でlogback.groovyというファイルを探します。
- 見つからなかったら、今度はクラスパス上でlogback-test.xmlというファイルを探します。
  (普通は src/test/resources 以下に配置)
- 見つからなかったら、今度はクラスパス上でlogback.xmlというファイルを探します。
  (普通は src/main/resources 以下に配置)
- 何も見つからなかったら、自動的にBasicConfiguratorを使って設定します。
  ロギング出力は直接コンソールに出力されるようになります。


### logback.xml

- property 変数みたいなもの
- appender 
  - 「どの場所にどういうフォーマットでログを出力するのか」を定義する
  - filterでどのログレベル(trace, debug, info, warn, error)のログを出すのか決める。
  - patternでログのフォーマットを決める
  - ローテーション、非同期、ファイルの圧縮もここで決める。
- logger
  - ロガー名とappender を対応づける？？？

### logback.xml の変数置換

値が書けるところには、シェル風の変数置換が書ける。

```
変数の展開
<root level="${ROOT_LOGLEVEL:-trace}">

変数のセットの方法(優先度高い順)
1. property xml要素で設定する
    xmlファイル中で設定
	<property name="ROOT_LOGLEVEL" value="info" />
    外部プロパティファイルから読み込み
	<property file="/aaa/bbb/ccc.conf" />
	そのファイルの中では、
	ROOT_LOGLEVEL=info
    外部ファイルの代わりに、クラスパス上のリソースを指定することも可
	<property resource="resource1.properties" />

2. システムプロパティ(java コマンドの -D オプション)で設定
    java -DROOT_LOGLEVEL="info" MyApp2

3. 環境変数
```



## ログを出力していることをテストする方法

参考
- [Logbackのログ出力内容をJUnitとMockitoでテストする方法 - Qiita](http://qiita.com/sifue/items/45ff10586ef609df1bc2 "Logbackのログ出力内容をJUnitとMockitoでテストする方法 - Qiita")
- [Checking Logback based Logging in Unit Tests | Autodidacticism](http://bloodredsun.com/2014/06/03/checking-logback-based-logging-in-unit-tests/ "Checking Logback based Logging in Unit Tests | Autodidacticism")

```
import ch.qos.logback.classic.spi.ILoggingEvent
import ch.qos.logback.classic.{Logger => LogbackLogger, Level}
import ch.qos.logback.core.Appender
import org.scalatest.FunSpec
import org.scalamock.scalatest.MockFactory
import com.typesafe.scalalogging.Logger
import org.slf4j.LoggerFactory

class Testee() {

  val logger = Logger(LoggerFactory.getLogger("Testee"))

  def method1(): Unit = {

    logger.error("TARGET 123")

    logger.error("TARGET 456")
  }

}

class ScalaLoggingTest extends FunSpec with MockFactory {

  it("scala logging でログが出力されることの確認") {

    val testee = new Testee

    val mockAppender = stub[Appender[ILoggingEvent]]
    (mockAppender.getName _).when().returns("MOCK")

    val testeeLogbackLogger = 
      LoggerFactory.getLogger("Testee").asInstanceOf[LogbackLogger]
    testeeLogbackLogger.addAppender(mockAppender)

    try {
      testee.method1()

      (mockAppender.doAppend _)
        .verify(where { (e: ILoggingEvent) =>
          e.getFormattedMessage.contains("TARGET 123") &&
            e.getLevel == Level.ERROR
        })

    } finally {
      testeeLogbackLogger.detachAppender(mockAppender)
    }

  }

}

```


# ベンチマーク sbt-jmh

https://github.com/ktoso/sbt-jmh

```
import org.openjdk.jmh.annotations._

@State(Scope.Thread)
class MyBenchmark {

  @Setup(Level.Iteration)
  def setup(): Unit = { ... }

  @Benchmark
  def benchHoge(): Unit = {
    ... 性能を測りたいコード ...
  }

  @TearDown(Level.Iteration)
  def teardown(): Unit = { ... }

}
```

流れ

- @Benchmark 指定したメソッドが1秒間、${t}スレッド並行で、猛烈に呼ばれる。 
  → 1イテレーション単位？
- 上記イテレーション単位が、ウォームアップ用に${wi}回、計測用に${i}回呼ばれる
  → 1fork？
- 上記1forkを、${f}回繰り返す

```
実行
$ sbt jmh:run -i 3 -wi 3 -f1 -t 1 benchmark.*
か、sbtの中で
> jmh:run -i 3 -wi 3 -f1 -t 1 benchmark.*

    i  : 計測回数
    wi : ウォーミングアップ回数
    f  : 全体（計測回数＋ウォーミングアップ回数）の試行回数
    t  : スレッド数
```

# feature

```
import scala.language.postfixOps   // 後置オペレーター
```

