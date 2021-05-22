::

    #####################
    見出し1
    #####################

    *********************
    見出し2
    *********************

    見出し3
    ===========

    見出し4
    -----------

    見出し5
    ^^^^^^^^^^^

    見出し6
    """""""""""

#######
TODO
#######

- package とは
- 変数のスコープは？


========================
基本
========================

-----------------
参考リンク
-----------------

- `A Tour of Go <https://go-tour-jp.appspot.com/welcome/1>`_


TODO リファレンスとか


-----------------
Hello, World
-----------------

::

    package main

    import "fmt"

    func main() {
        fmt.Println("Hello, 世界")
    }

::

    package main

    import (
        "fmt"         // カンマ不要
        "math/rand"
    )

    func main() {
        fmt.Println("My favorite number is", rand.Intn(10))
    }


--------------------
基本の書き方
--------------------

コメント::

    // one line comment

    /* comment */
    /*
        line1
        line2
    */


文

- 行末にセミコロンとかは不要

インデントはタブ文字が標準らしい。

main() 関数から始まる。
スクリプト言語みたいに、地の文に処理は書けない？？？

------------------------
デバッグとか
------------------------

表示::

    fmt.Println(i, j, c, python, java)

    fmt.Printf("Type: %T Value: %v\n", ToBe, ToBe)
        %T ???
        %v ???

名前
=========================

- 大文字始まり

    - 外部のパッケージから参照できる。公開された名前 (exported name)

- 小文字始まり

    - 公開されていない名前

公開/非公開は、「パッケージ外」が境界？


変数
==========================

宣言が必要。宣言してから使う。

var
変数を宣言する。
地の文(packageの文脈) or 関数内で書ける

:=
関数内で書ける (地の文では書けない)


var::

    var i int
    var i int, msg string     // こういうのもいけるか？
    var c, python, java bool  // bool型の3つの変数を宣言


初期化子(initializer)付きvar::

    var i, j int = 1, 2

    // 初期化子が与えられた場合、型を省略できる
    // 変数の型は初期化子から決定(推論)される
    var c, python, java = true, false, "no!"

factordスタイル::

    var (
        i int = 1             // カンマは不要
        b bool = false
        name string = "Joe"
    )

``:=``::

    k := 3
    c, python, java := true, false, "no!"


定数(const)::

    const Pi = 3.14

    // これもいけるか？
    const a, b = 3, 4

    const (

    )

定数は、文字(character)、文字列(string)、boolean、数値(numeric)のみで使える。

数値の定数は、高精度な値。リテラルのまま扱っているようなもの？？？


型
==========================

基本型::

    bool

    string

    int  int8  int16  int32  int64
    uint uint8 uint16 uint32 uint64 uintptr

    byte // uint8 の別名

    rune // int32 の別名
         // Unicode のコードポイントを表す

    float32 float64

    complex64 complex128


ゼロ値(zero value)
初期値を与えずに宣言した場合の値


- 数値型(int,floatなど): 0
- bool型: false
- string型: "" (空文字列( empty string ))


型変換
変数を別型の変数に代入しようとするときには必要。
C言語とは異なり、Goでの型変換は明示的な変換が必要です。
c.f. 右辺がリテラルだったらある程度型変換が効くっぽい。
::

    // 型名(変数)
    var i int = 42
    var f float64 = float64(i)
    var u uint = uint(f)




関数, Function
==========================

関数定義::

    func add(x int, y int) int {
        return x + y
    }

    // 引数なし、戻り値なし
    func main() {
        fmt.Println(add(42, 13))
    }

    // 引数同じ型の連続は最後の1つだけでも可
    // 複数の引数を返す
    func swap(x, y string) (string, string) {
        return y, x
    }

    // 使うとき
    a, b := swap("hello", "world")


Named return values

戻り値の型に名前をつけると、

- 関数の冒頭でその変数が定義されたことになる
- return には返す値を書かなくていい (naked return)
- 短い関数の場合のみの利用にとどめろ

::

    //                   ↓ここ
    func split(sum int) (x, y int) {  
        x = sum * 4 / 9  // 定義済みなので := ではなく = で代入できる
        y = sum - x
        return           // この場合 return には値を並べない
    }

呼び出し方::

    TODO




フロー制御
=========================

forとかifの ( ) 丸括弧 は不要。 { } 中括弧は必要。

for::

    sum := 0
    for i := 0; i < 10; i++ {  // i の スコープは for の中だけ。
        sum += i
    }

    // 初期化と後処理の記述は任意
    sum := 1
	for ; sum < 1000; {
		sum += sum
	}

    // セミコロンも省略可。 while はないので、これを使う
    sum := 1
	for sum < 1000 {
		sum += sum
	}

    // 条件もなくすと無限ループ
    for {
        ...
    }


if::

    if x < 0 {
        ...
    } else if x < 10 {
        ...
    } else {
        ...
    }

    // 条件中に簡単な文も書けるが、
    // そこで宣言した変数のスコープは if,else の中だけ。
    if v := math.Pow(x, n); v < lim {
		return v
	}


switch

- 自動では fall through しない。(breakはいらない)
- fallthroughさせたい場合は、？？？
- case は定数である必要はない。式でも関数呼び出しでもよい。
- switchに渡す値は整数である必要はない

::

    switch os := runtime.GOOS; os {
	case "darwin":
		fmt.Println("OS X.")
	case "linux":
		fmt.Println("Linux.")
	default:
		// freebsd, openbsd,
		// plan9, windows...
		fmt.Printf("%s.\n", os)
	}


条件のないswitchは、 switch true と書くことと同じです。 
if, else if が長く続く条件分岐の代わりに使える。::

	t := time.Now()
	switch {
	case t.Hour() < 12:
		fmt.Println("Good morning!")
	case t.Hour() < 17:
		fmt.Println("Good afternoon.")
	default:
		fmt.Println("Good evening.")
	}


defer

- defer に渡した関数の実行を、呼び出し元の関数の終わり(returnする)まで遅延させる
- defer に渡した関数の各引数はすぐに評価される

::

    func main() {
        defer fmt.Println("world")

        fmt.Println("hello")
    }

defer を複数回使った場合

defer はスタックに積まれる。LIFO(last-in-first-out)で実行される。



package, import
==========================

こっちの方が好ましいらしい::

    import (
        "fmt"         // カンマ不要
        "math/rand"
    )

こうも書けるけど::

    import "fmt"
    import "math"

