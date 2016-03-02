# リフレクション

## 参考

- Reflection - 概要 - Scala Documentation
  http://docs.scala-lang.org/ja/overviews/reflection/overview.html
- API document
  http://www.scala-lang.org/api/2.11.7/scala-reflect/#scala.reflect.package

## 概要

リフレクションでできること

1. 実行時リフレクション。
   実行時にランタイム型 (runtime type) やそのメンバをインスペクトしたり
   呼び出す能力。
2. コンパイル時リフレクション。
   コンパイル時に抽象構文木にアクセスしたり、それを操作する能力。
3. レイフィケーション (reification)。
   (1) の場合は実行時に、(2) の場合はコンパイル時に抽象構文木を生成すること。


実行時リフレクションでできること

- そのオブジェクトがどの型かがわかる
- 新しいオブジェクトを作成することができる
- そのオブジェクトのメンバにアクセスしたり呼び出したりできる


## ユニバース(Universe)

実行時リフレクションか、コンパイル時リフレクションかを選ぶ。
どちらも universe という同じインターフェースに抽象化されている。

- 実行時リフレクションのためには `scala.reflect.runtime.universe`
- コンパイル時リフレクションためには `scala.reflect.macros.Universe`


## 基本要素

- 名前(Name) : 名前を表現する。文字列の薄いラッパー
- シンボル(Symbol) : 名前と実体のバインディング。ミラーから子ミラーを得るために使う。
- 型(Type): シンボルの型情報
- ミラー(Mirror): インスタンスやメソッドを、リフレクション的に操作するための口を持ったもの。

### 名前 (Name)

http://www.scala-lang.org/api/2.11.7/scala-reflect/#scala.reflect.api.Names

- TermName: オブジェクトやメンバー(フィールド,メソッド、変数)の名前
- TypeName: クラス、トレイト、型メンバー(typeで書くやつ)の名前

得る方法
```
TermName("map")
"map": TermName   // 文字列リテラルからの暗黙の型変換を使って
```

メソッド

- decodedName: b_=, <init>  など
- encodedName: b_$eq, $lessinit$greater  など
- isTermName, isTypeName
- toTermName, toTypeName
- toString


### 型(Type)

得る方法
```
import scala.reflect.runtime.universe._

// 型記述？からtypeOfで得る
typeOf[List[Int]]
  // → scala.reflect.runtime.universe.Type = scala.List[Int]

// インスタンスから得る
// ( 型パラメタのcontext binding を利用することで T をうまいこと得る )
def getType[T: TypeTag](obj: T) = typeOf[T]
getType(List(1,2,3))
  // → scala.reflect.runtime.universe.Type = List[Int]

// 標準型
// http://www.scala-lang.org/api/2.11.7/scala-reflect/#scala.reflect.api.StandardDefinitions$DefinitionsApi
val intTpe = definitions.Int    // ひょっとすると IntTpe か？
など
```

演算

```
// サブタイプ関係 ( <:< )
class A
class B extends A
typeOf[A] <:< typeOf[B]  // false
typeOf[B] <:< typeOf[A]  // true
// c.f. weak_<:<

// 型の等価性 ( =:= ) (注！ == ではない！)
def getType[T: TypeTag](obj: T) = typeOf[T]
class A
val a1 = new A; val a2 = new A
getType(a1) =:= getType(a2)   // true

getType(List(1,2,3)) =:= getType(List(1.0, 2.0, 3.0))   // false
getType(List(1,2,3)) =:= getType(List(9,8,7))           // true

// メンバと宣言の照会
t.member(name): Universe.Symbol    // 名前を指定して取得
t.declaration(name): Universe.Symbol
t.members: Universe.MemberScope    // 全部取得。Traverseできる。
t.declaraions: Universe.MemberScope

typeOf[List[_]].member("map": TermName)
typeOf[List[_]].member("Self": TypeName)
```

### シンボル(Symbol)

http://www.scala-lang.org/api/2.11.7/scala-reflect/#scala.reflect.api.Symbols

シンボルは階層構造になっている。
(メソッドはクラスに所有され、クラスはパッケージに所有される)

- TypeSymbol (型シンボル): 型、クラス、トレイト、型パラメータ
  - ClassSymbol: クラスやトレイト
- TermSymbol (項シンボル): val, var, def, オブジェクトの宣言、パッケージや値のパラメタ
  - MethodSymbol: def の宣言
  - ModuleSymbol: シングルトンオブジェクトの宣言
- NoSymbol: owner がないことを表すときやデフォルト値に使用される

メソッド

- (Symbol)
  - name, fullName
  - isConstructor
  - isAbstruct, isFinal, isJava, isPackage, 
  - isPrivate, isProtected, isPublic, 
  - isClass, isMethod, isModule, isModulueClass, isTerm, isType
  - companion
  - (TypeSymbol)
    - isAbstructType, isContravariant, isCovariant
    - (ClassSymbol)
      - isFinal, isPrivate, isProtected, isAbstractClass
      - baseClasses
      - typeParamas
    

得る方法

- Type の memberメソッドや declaraion メソッド

シンボル変換

member は、Symbol のインスタンスを返すので、
それを MethodSymbol に変換する必要がある。

- asClass, asMethod, asModule, asTerm, asType

```scala
import scala.reflect.runtime.{universe => ru}
class C[T] { def test[U](x: T)(y: U): Int = ??? }  // こういうクラスがあったとして

val testMember = ru.typeOf[C[Int]].member(ru.TermName("test"))
  // → scala.reflect.runtime.universe.Symbol = method test

testMember.asMethod
  // → scala.reflect.runtime.universe.MethodSymbol = method test
```


### ミラー(Mirror)

大きく2種類
- クラスローダーミラー: 
  (staticClass/staticModule/staticPackage メソッドを使って) 
  名前をシンボルへと翻訳する。
- invokerミラ:
  (MethodMirror.apply や FieldMirror.get といったメソッドを使って)
  リフレクションを用いた呼び出しを実装する。

実行時ミラー

- クラスローダーミラー: (ReflectiveMirror型)
- invokerミラー:
  - InstanceMirror: インスタンスのミラー
  - MethodMirror: インスタンスのメソッドのミラー
  - FieldMirror: インスタンスのフィールドのミラー
  - ClassMirror: クラスのミラー(コンストラクタのミラーを作成するのに使う)
  - ModuleMirror: シングルトンオブジェクトのミラー

得る方法

- クラスローダーミラーは、決め打ちで取得
- 既にあるミラーから、reflect, reflectMethod, reflectField などに Symbol を渡して呼ぶことで、
  Symbol に対応するミラーが得られる。

コンパイル時ミラー

コンパイル時ミラーは名前からシンボルを読み込むクラスローダミラーだけが使われる。
(あとまわし)




## サンプルコード (実行時)

```
import scala.reflect.runtime.{universe => ru}

// クラスローダーミラーの取得。ほぼお約束
val m = ru.runtimeMirror(getClass.getClassLoader)

// あるインスタンスのメソッドを呼びたい。
// class C { def x = 2 }     // こういうクラスがあったとして
val im = m.reflect(new C)   // InstanceMirror の取得
val methodX = ru.typeOf[C].declaration(ru.TermName("x")).asMethod  // MethodSymbol を作って
val mm = im.reflectMethod(methodX)   // method mirror の取得
mm()                                 // メソッドの実行

// あるインスタンスのフィールドを操作したい。
// class C { val x = 2; var y = 3 }  // こういうクラスがあったとして
val im = m.reflect(new C)    // InstanceMirror の取得
val fieldX = ru.typeOf[C].declaration(ru.TermName("x")).asTerm.accessed.asTerm  // TermSymbolを作って
val fmX = im.reflectField(fieldX)    // FieldMirror の取得
fmX.get
fmX.set(3)
```







==================================================
java の リフレクションを利用した古いやり方
うーん。うまくフィールド名が取れなかったりして、よくわからない...。

クラスの取得

val c = classOf[クラス名]     // クラス名から
val c = obj.getClass()        // インスタンスから
// java.lang.Class[T] 型
→ http://docs.oracle.com/javase/jp/8/docs/api/java/lang/Class.html


メンバーの取得
c.CanonicalName  // クラス名が取れる。
c.GetName

c.getClasses()   // メンバークラス、インターフェースの取得

c.getDeclaredFields()   // 全てのフィールド。Field[] 型
c.getFields()           // public なフィールド。Field[] 型

c.getDeclaredMethods()  // 全てのメソッド。継承されたものは含まれない。 Method[] 型
c.getMethods()          // public なメソッド。継承されたもの含む。Method[] 型

Field型
    f.getName()         // フィールド名を返す

c.getFields.map(_.getName)
