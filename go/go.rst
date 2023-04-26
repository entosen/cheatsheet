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
- 変数、関数のスコープは？

- errors.New(""), fmt.Errorf("xxxx")

- 予約語
https://golang.org/ref/spec#Keywords

- init関数


========================
基本
========================

-----------------
参考リンク
-----------------

- `A Tour of Go <https://go-tour-jp.appspot.com/welcome/1>`_


TODO リファレンスとか

- https://github.com/golang/go/wiki/SliceTricks
- https://golang.org/ref/spec#Slice_expressions


スタイルガイド

- `Uber Go Style Guide <https://github.com/uber-go/guide/blob/master/style.md>`_

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



ケツカンマ

- 付けられる
- 1行で書くは、gofmt が削除してしまうらしい
- 複数行の場合(閉じ括弧が次行にいく場合)は、カンマがないとエラーになる

::

    a := []int{1, 2, 3}
    a := []int{1, 2, 3,}  // 文法的にはOKだが、gofmtは最後のカンマを削除してしまう

    a := []int{1, 2, 3    // コンパイル時エラーになる
    }

    a := []int{1, 2, 3,   // これならOK。
    }


------------------------
デバッグとか
------------------------

表示::

    fmt.Print(i, j, c, python, java)
        // 各引数を文字列に直して、空白なしで連結して出力。最後改行しない。

    fmt.Println(i, j, c, python, java)
        // 各引数を文字列に直して、空白ありで連結して出力。最後改行する。

    fmt.Printf("Type: %T Value: %v\n", ToBe, ToBe)
        // 第1引数のフォーマット指定に従って出力する。最後改行しない。
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

厳密に言うと、定数には

- untyped なものと typed なものがある
- デフォルト型というのを持っている

詳しくは、下記を参照

- https://golang.org/ref/spec#Constant_expressions
- `Go の定数の話 - Qiita <https://qiita.com/hkurokawa/items/a4d402d3182dff387674>`__


型
==========================

型の分類
-------------

基本型(値型)::

    bool

    string

    int  int8  int16  int32  int64
    uint uint8 uint16 uint32 uint64 uintptr

    byte // uint8 の別名

    rune // int32 の別名
         // Unicode のコードポイントを表す

    float32 float64

    complex64 complex128

配列型::

    [5]int など

interface{}型::

    interface{}

関数型::

    func(x int, y int) int

参照型::

    // スライス
    []int

    // マップ
    map[string]int

    // チャネル
    chan int
    <-chan int
    chan<- int

ポインタ型::

    *int




ゼロ値(zero value)
初期値を与えずに宣言した場合の値


- 数値型(int,floatなど): 0
- bool型: false
- string型: "" (空文字列( empty string ))
- struct: 各フィールドがゼロ値の構造体
- 配列: 各要素がゼロ値の配列
- その他(ポインタ、スライス、マップ、関数、インタフェース、チャネル): nil


型変換
変数を別型の変数に代入しようとするときには必要。
C言語とは異なり、Goでの型変換は明示的な変換が必要です。
c.f. 右辺がリテラルだったらある程度型変換が効くっぽい。
::

    // 型名(変数)
    var i int = 42
    var f float64 = float64(i)
    var u uint = uint(f)


文字列 string と []rune と []byte
--------------------------------------

string型は文字列を表す。イミュータブル。

string型は基本バイト列(utf-8)。lenやインデックスはバイト単位。特に日本語を扱う場合に注意。

string型のリテラル::

    "abcde\n"
    "日本語"
    "\x41"         // "A"
    "\u0041"       // "A"
    "\U00000041"   // "A"

    // raw string literal (バックスラッシュを特殊解釈しない)
    `ab"cde"\n`     


rune型は1つの文字を表す。日本語のようなマルチバイトの文字も1つと扱う。

正確には「Unicodeコードポイントを表す特殊な整数型」。 32bit符号付き整数と同じ。

rune型のリテラル::

    'a'
    '日'


byte型は1バイトを表す。



操作::

    str := "あいうえお"
    bytes := []byte("あいうえお")   // string → []byte
    runes := []rune("あいうえお")   // string → []rune

    str := string(runes)            // []rune → string
    str := string(bytes)            // []rune → string

    len(s)                       // stringのバイト数
    utf8.RuneCountInString(s)    // stringの文字数
    len(bytes)                     // []byteの長さ、つまりバイト数
    utf8.RuneCount(bytes)          // []byteをruneとして解釈した文字数
    len(runes)                   // []runeの長さ、つまり文字数数

    s[1]    // byte型
    s[1:3]  // 文字列型? []byte型？ 開始位置(含む)、終了位置(含まない)

    // string型に range をした場合は、byteごとではなくruneごとで取れる
    for pos, runeValue := range s {
        ...
    }

    sNew := s1 + s2  // 文字列の連結
    sNew += s3
    
    // string.Builder で構築
    inport "strings"
    var builder strings.Builder
    builder.Grow(n)                   // あらかじめ n byte分確保
    builder.WriteString("ignition")   // string型を追加
    builder.Write(bytes)   // []byte型を追加
    builder.WriteByte(b)   // 1byte追加
    builder.WriteRune(r)   // 1rune追加
    builder.String()  // → string型を返す


ポインタ
---------------------

C言語と同じ感じ。ただしポインタ演算はない。

::

    var p *int   // int のポインタ型の変数を宣言
    i := 42
    p = &i       // 変数のポインタ
    *p           // ポインタ p を通して、i から値を読み出す
    *p = 21      // ポインタ p を通して、i へ値を代入する


構造体 struct
----------------------

::

    type Vertex struct {
        X int
        Y int
    }

アクセスの仕方 ドットを使う::

    v := Vertex{1, 2}
    v.X

    // ポインタを通してもアクセスできる
    p := &v   // struct へのポインタ
    (*p).X    // こうでもいけるが、
    p.X       // Goではこれでアクセスできる

structの初期値・structリテラル::

    var (
        v1 = Vertex{1, 2}   // フィールドを順に列挙
        v2 = Vertex{X: 1}   // フィールド名を指定し特定のフィールドを初期化
                            // それ以外のフィールドはゼロ値
        v3 = Vertex{}       // 全てのフィールドをゼロ値で初期化

        p = &Vertex{1, 2}   // &を付けると新しく割り当てられたstructへのポインタ
    )


配列 array、スライス slice
-------------------------------------

- 配列: 固定長
    
    - 配列の長さまで含めて型。長さが違えば別な型。

- スライス: 配列の一部への参照のようなもの

    - スライスはどんなデータも格納していない。
      単に元の配列の部分列(始点と終点で示される)を指し示す
    - スライスを変更すると、その元となる配列の対応する要素が変更される
    - 同じ元となる配列を共有している他のスライスは、それらの変更が反映される
    - ``a[low:high]``  lowは含む, highは含まない


配列::

    // 配列
    var a [2]string    // この時点では配列の各要素はゼロ値
    a[0] = "Hello"
    a[1] = "World"

    // 配列の初期化・配列リテラル
    primes := [6]int{2, 3, 5, 7, 11, 13}
    primes := [6]int{1: 3, 3: 7}  // インデックスと値を指定。指定が無い場合はゼロ値

    primes := [...]int{2, 3, 5, 7, 11, 13}   // 配列の長さを推論

スライス::

    // スライス
    // 既に存在する配列へのスライス
    var s []int = primes[1:4]  // [3 5 7]。 lowは含む, highは含まない
    
    // lowを省略した場合は0、highを省略した場合は配列の長さ
    a[0:6]
    a[:6]
    a[0:]
    a[:]

    // スライスリテラル
    // 同様の(無名の？)配列を作成し、それを参照するスライスを作成する
    q := []int{2, 3, 5, 7, 11, 13}
    q2 := []int{1: 3, 3: 7}  // インデックスと値を指定。指定されなかった箇所はゼロ値
    r := []bool{true, false, true, true, false, true}
    s := []struct {
        i int
        b bool
    }{
        {2, true},
        {3, false},
        {5, true},
        {7, true},
        {11, false},
        {13, true},
    }

    // 2次元配列みたいなの (c.f.配列ではできないのか？)
    // (スライスの中身の型がスライス)
    board := [][]string{
        []string{"_", "_", "_"},
        []string{"_", "_", "_"},
        []string{"_", "_", "_"},
    }


    // make を使ったスライスの生成
    // ゼロ値埋めされた無名の配列を作って、それを指すスライスを返す
    // 型と長さを指定
    a := make([]int, 5)  // len(a)=5
    // capも指定
    b := make([]int, 0, 5) // len(b)=0, cap(b)=5

- スライスの長さ ``len(s)`` は、それに含まれる要素の数です。
- スライスの容量 ``cap(s)`` は、スライスの最初の要素から数えて、元となる配列の要素数です。

再スライス::

    s := []int{2, 3, 5, 7, 11, 13}

    元の配列:  |  2 |  3 |  5 |  7 | 11 | 13 |
    s          |<--------------------------->|  len=6 cap=6 [2 3 5 7 11 13]
    s = s[:0]  ||............................|  len=0 cap=6 []
    s = s[:4]  |<----------------->|.........|  len=4 cap=6 [2 3 5 7]
    s = s[2:]            |<------->|.........|  len=2 cap=4 [5 7]

- 終点を前に縮めることはできる。その場合でもcapとして値は保存されている。
- 終点を cap までは後ろに伸ばすことができる。
  (capを超えて伸ばそうとしたときはエラーになる)
- 始点を後ろにするめることはできるが、前に戻すことはできない
  (マイナスのインデックスはエラーになる)

スライスの初期値は nil 。 (要素数0のsliceと厳密には異なるが、振る舞いとしてはほとんど一緒)

- nil スライスは、 0 の長さと容量を持っており、何の元となる配列も持っていない。
- nil スライスでも、range や append はきちんと動く

スライスへの要素の追加::

    // append で末尾に追加していく
    var s []int
    s = append(s, 0)
    s = append(s, 2, 3, 4)

- capを超えるような追加をした場合には、より大きいサイズの配列を割り当て直す。
  その場合、戻り値となるスライスは、新しい割当先を指す

スライスの連結::

    src1, src2 := []int{1, 2}, []int{3, 4, 5}
    dst := append(src1, src2...)   // この ``...`` が重要。引数として展開？
    // → [1, 2, 3, 4, 5]

スライス操作::

    // 要素を除く
    src := []int{1, 2, 3, 4, 5}
    i := 2
    dst := append(src[:i], src[i+1:]...)   // [1, 2, 4, 5]

    dst = src[:i+copy(src[i:], src[i+1:])]  // これでもいけるらしいが よくわからん

TODO copy


Map, マップ
------------------------------

- キーの型には、比較演算子で比較ができるもの
- 順序は保持されない

::

    // マップ型の書き方
    var m map[string]int    // map[キーの型]値の型

    // この状態では中身は nil。空のmapと nil map は異なるので注意。
    // nilマップはキーを持っておらず、キーを追加することもできない。
    // (要素数の取得(0)、キーの存在チェック、キーの削除は可能らしい。)

    // 空で初期化
    m = map[string]int{}

    // makeで初期化(キーを追加できる状態にする) 要素数0。
    m = make(map[string]int)
    m = make(map[string]int, 10)  // あらかじめ容量を確保した状態で初期化

    // マップリテラル
    var m = map[string]int{
        "one": 1,
        "two": 2,
        "three": 3,
    }

mapの操作::

    // 要素の参照(のコピー)
    i := m["Three"]
    // キーが存在しない場合は、要素型のゼロ値が返る

    // キーが存在するかどうか
    elem, ok := m["Five"]  // キーあり: elem=その値のコピー, ok=true
                           // キーなし: elem=要素の型のゼロ値, ok=false
    
    // 要素の挿入、更新
    m["Three"] = 3

    // 要素の削除 
    // キーがなくても怒られない
    delete(m, "three")


mapリテラルで、要素の型が単なる型名だった場合、リテラル要素から型名を省略できる::

    type Vertex struct {
        Lat, Long float64
    }

    // 正式な書き方
    var m = map[string]Vertex{
        "Bell Labs": Vertex{40.68433, -74.39967},
        "Google":    Vertex{37.42202, -122.08408},
    }

    // 要素の型が単なる型名だった場合、リテラル要素から型名を省略できる
    var m = map[string]Vertex{
        "Bell Labs": {40.68433, -74.39967},
        "Google":    {37.42202, -122.08408},
                 // ↑ここの Vertex が省略可
    }


関数も変数
-----------------------

::

    // 関数型
    var someFunc func(float64, float64) float64

    // 関数リテラル
	hypot := func(x, y float64) float64 {
		return math.Sqrt(x*x + y*y)
	}

    // ちなみに普通の関数定義
    func hypot(x, y float64) float64 {
		return math.Sqrt(x*x + y*y)
    }


関数型の変数のゼロ値は nil 。
    


channel, チャネル
------------------------------

キューみたいなデータ構造。複数の go ルーチン間での受け渡しを想定している。

::

    var ch0 chan int     // 変数 ch は int 型のチャネル
    var ch1 <-chan int   // 受信専用チャネル
    var ch2 chan<- int   // 送信専用チャネル

制限無しチャネルは、送信専用チャネルや受信専用チャネルに代入できる::

    ch1 = ch0  // OK
    ch2 = ch0  // OK
    ch0 = ch1  // NG
    ch0 = ch2  // NG
    ch2 = ch1  // NG
    ch1 = ch2  // NG

::

    ch := make(chan int)       // 生成。capacity  0
    ch := make(chan int, 10)   // 生成。capacity 10

    ch <- 5    // チャネルに送信
    i := <-ch  // チャネルから受信
    i, ok := <-ch    // チャネルから受信(クローズ判定付き)
                     // オープン中、closeされてもデータが残っている場合 ok==true
                     // closeされてデータがない場合 i==ゼロ値, ok==false

    close(ch)

    len(ch)    // チャネル内のデータの個数
    cap(ch)    // チャネルのバッファサイズ


capacity 0 のチャネルを unbuffered channel、
capacity >0 のチャネルを buffered channel と呼ぶ。

待つ(ブロックする)場合は下記

- 送信側
  
  - capacity 0 の場合: 受信側が準備できていない(向こう側にいない)チャネルへの送信
  - capacity >= 1 の場合: バッファ内に空きがないチャネルへの送信

- 受信側

  - capacity 0 の場合: 送信側が準備できていない(向こう側にいない)チャネルへの送信 
  - capacity >= 1 の場合: バッファ内が空のチャネルからの受信


capacity 0 でも、送信側・受信側双方が準備完了したら(そこにたどり着いたら)
値を受け渡すことができる。
そうなるまでブロックすることになるが。
(糸電話みたいなイメージ)

capacity が1以上でバッファに空きがあるなら、値を放り込んで、待つことなく先に進める。
(メッセージ受け渡し用の箱(キュー)があるイメージ。ロッカーみたいな。)

全ての Goルーチンが待ち状態になると、デッドロックと判断されPanic。

closeされたチャネルについて

- 送信すると Panic 
- 受信すると、バッファ内に既にたまっているデータは受信できる。それ以降は ゼロ値。(Panicにはならない)



クローズの検知のみをやりとりする場合、
型は ``struct{}`` にするのが定石(サイズ0だから)

select::

    L:      // このforを抜けるためには ``break L`` とする。breakだけではselectしか抜けない。
        for {
            select {
            case e1 := <-ch1:
                // ch1 からの受信が成功した場合の処理
            case e2, ok := <-ch2:
                // ch2 からの受信が成功した場合の処理(2変数バージョン)
            case ch3 <- e3:
                // ch3 へ送信が成功した場合の処理
            case ch4 <- ch5:
                // ch5 から ch4 へ送信が成功した場合の処理
            default:
                // case節の条件が成立しなかった場合の処理
                // default 節をつけた場合、ブロックしない。
                // default 節を付けない場合、どれかのcaseが成立するまでブロックする
            }
        }



Enum
-------------------

他の言語の Enum に相当するのはないので、下記のように const をつかって対応。::

    type Color int

    const (
        Red Color = iota
        Blue
        Yellow
    )


型についていろいろ
================================

TODO

- type した場合、別な型ということになる。メソッドも引き継がれない



type 構文
--------------------

type構文。Defined type ::

    // type <defined type> <underlieing type>

    type MyKey int

    type UserData stuct {
        Name string
        Age  int
    }

- type構文によって作った型は、完全に別な型ということになる。メソッドも引き継がれない

  - 元の型とも別な型
  - 同じ元の型から作った2つの新しい型も、それぞれ別の型扱い

- type構文によって作った型は defined type と呼ばれる。

  - 実は int とか string も defined type らしい。TODO


alias構文 (エイリアス構文) ::

    type NewTypeName = OldTypeName

- エイリアスの場合、別名で同じ型を表すだけなので、
  同じ型として扱われるし、メソッドも同じように使える。
- 主にリファクタリング目的。
  型の名前を変えるようなリファクタリングを徐々にやりたい場合に、
  一旦両方の名前で使えるようにするなど。

参考

- `go言語1.9で追加予定の新機能 型エイリアス - Qiita <https://qiita.com/weloan/items/8abbb4003cfa1031a9e9>`__




Assignability (代入可能)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

参考

- https://golang.org/ref/spec#Assignability
- `Goの型同一性を理解する <https://zenn.dev/syumai/articles/77bc12aca9b654>`__

x が T に Assignable (代入可能) とは、下記のどれか1つを満たす場合

- x の型が T に等しい
- xの型V と T が、同一の underlying types を持っており、かつ、少なくとも V か T が defined type でない。
  
  - defined type というのは ``type`` で定義した型ということ::

        ``type [defined type] [underlying type]`` 

  - 加えて、言語仕様上特別に(?)、int,floatなどの数値型、string型も defined type ということになっている

- Tがinterface型で、xがTを implement している (そのinterfaceを満たしている＝必要なメソッドを持っている)
- x が双方向チャネル値で、Tがチャネル型で、xの型V と T が同一の要素型を持っており、かつ、少なくとも V か T が defined type でない
- x が nil で、Tが ポインタ、関数、スライス、マップ、チャネル、インターフェースのどれか
- x が untyped constant で、Tの値によって表現可能(representable)


Representability (定数がある型で表現可能)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

https://golang.org/ref/spec#Representability


Comparable 比較可能, Ordered 順序可能, Equality 等価性
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

https://golang.org/ref/spec#Comparison_operators

まず、比較するにあたっては、 x は yの型 に Assignable、もしくは、 y は xの型に Assignable でなければならない。
(違ったら invalid operation でコンパイルエラー)

用語

- comparable 比較可能 ( ``==``, ``!=`` )
- ordered 順序可能 ( ``<``, ``>``, ``<=``, ``>=``

ルール

- bool値同士は比較可能。true同士とfalse同士が等しいと判定される
- 整数値(int, int64など)整数値同士は比較可能 かつ ordered 。
- 浮動小数点値(float32, float64)同士は比較可能 かつ ordered 。
- 複素数値同士は比較可能 であり、2つの複素数の実部と虚部が共に等しい場合に等しいと判定される
- 文字列値同士は比較可能 かつ ordered 。byte-wiseの辞書順で。
- ポインタ値同士は比較可能 であり、「どちらも同じ変数を指している場合」と「どちらもnilである場合」に等しいと判定される。
  (中身が同じでも違う変数を指していれば、違うと判定される)
- チャネル値同士は比較可能 であり、「どちらも同様のmake文から作られている場合」と「どちらもnilである場合」に等しいと判定される
- インターフェース値同士 は比較可能 であり、「どちらも同じdynamic type・等しいdynamic valueを持つ場合」と「どちらもnilである場合」に等しいと判定される
- 非インターフェース型の型Xの値xと、インターフェース型Tの値tは、
  「型X(同士)が比較可能 であり、かつ、XがインターフェースTを実装している場合」に比較可能 である。
  「tのdynamic type が X と同じであり、ｔのdynamic valueがx等しい場合」に等しいと判定される
- 構造体型はすべてのフィールドが比較可能である場合にそれ自身も比較可能となり、それぞれの対応するnon-blankなフィールドの値が等しい場合に2つの構造体値が等しいと判定される
- 配列型は、その配列の基底型が比較可能である場合にそれ自身も比較可能となり、全ての配列要素が等しい場合に2つの配列値は等しいと判定される
- ポインタ、チャネル、インターフェースは nil とも比較可能
- スライス、マップ、関数値は比較可能ではない。しかし特殊ケースとして、nil とは比較可能



関数, Function
==========================

TODO

- 関数の中に関数を書けるか？


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


TODO

- たぶん、関数のオーバーロードはできない


メソッド
==========================

- Goにはクラスの仕組みはないが、型にメソッドを定義できる。
- メソッドは特別なレシーバ( receiver )引数を関数に取ります
- レシーバは、 func キーワードとメソッド名の間に自身の引数リストで表現します


::

    type Vertex struct {
        X, Y float64
    }

    // メソッドの定義(変数レシーバ)
    func (v Vertex) Abs() float64 {
        return math.Sqrt(v.X*v.X + v.Y*v.Y)
    }

    // メソッドの定義(ポインタレシーバ)
    // 内容の変更を伴う場合はこうしないとだめ。
    // 内容を更新することが多いため、こちらの方が一般的。
    func (v *Vertex) Scale(f float64) {
        v.X = v.X * f
        v.Y = v.Y * f
    }

    // メソッドの呼び方 (ドットでつなげて呼び出す)
    v := Vertex{3, 4}
    p := &v

    v.Abs()  // → 5
    p.Abs()  // 変数レシーバーメソッドをポインタから呼び出すこともできる

    // ポインタレシーバーの場合、変数からでもポインタからでも呼び出せる
    v.Scale(10)    // v の内容が {30, 40} になる
    p.Scale(10)   
    

値レシーバ(value receiver)とポインタレシーバ(pointer receiver)

- 値レシーバー

    - 値のコピーがメソッドに渡る。(なので、変更しても元の値には影響を与えない)
    - 値レシーバのメソッドは、値からでも、ポインタからでも呼び出せる

        - コンパイラが ``p.Abs()`` を ``(*p).Abs()`` と解釈してくれる

- ポインタレシーバー

    - 内容の更新をする場合には、ポインタレシーバにしないといけない
    - 内容のコピーをしたくない場合も、ポインタレシーバーにする
    - ポインタレシーバのメソッドは、変数からでも、ポインタからでも呼び出せる

        - コンパイラが ``v.Scale(10)`` を ``(&v).Scale(10)`` と解釈してくれる

- c.f. 上記の解釈はレシーバーに限った話で、引数,返り値ではそうは解釈されない
  (ポインタにはポインタを渡す必要がある)


メソッドの呼び出し::

                     値レシーバーのメソッド      ポインタレシーバーのメソッド

      値型             ○呼び出せる               ○呼び出せる(自動解釈)

      ポインタ型       ○呼び出せる(自動解釈)     ○呼び出せる 


c.f. 引数,返り値::

                     値型の引数に      ポインタ型の引数に

      値型             ○渡せる          ×渡せない

      ポインタ型       ×渡せない        ○渡せる 


インターフェースを満たすかの判定、インターフェースからのメソッド呼び出し::

                     値レシーバーのメソッド      ポインタレシーバーのメソッド

      値型             ○持っているとみなす       ×

      ポインタ型       ○持っているとみなす       ○持っているとみなす


埋め込み(embedded)フィールドの持つメソッドについて::

                                      値レシーバー(T)のメソッド   ポインタレシーバー(*T)のメソッド

      値型として埋め込み          s    ○持っているとみなす         ×
      type s struct{T}
                                 *s    ○持っているとみなす         ○持っているとみなす


      ポインタ型として埋め込み    s    ○持っているとみなす         ○持っているとみなす
      type s struct{*T}
                                 *s    ○持っているとみなす         ○持っているとみなす


どちらがいいのか。

https://github.com/golang/go/wiki/CodeReviewComments#receiver-type

- map, func, chan はポインタレシーバーを使うな
- メソッドでresliceやreallocateしないスライスは、ポインタレシーバーを使うな
- メソッドがレシーバーを変更する場合、ポインタレシーバーでなければならない
- sync.Mutexなどの同期フィールドを持っているstructの場合、
  コピーを避けるために、ポインタレシーバーでなければならない
- 大きいstructやarrayの場合、ポインタレシーバーが効率的。どれぐらいの大きさかって？
  それらを全てメソッドの引数で渡すと想定したときに、多いと感じるようであれば大きいと考える。
- Can function or methods, either concurrently or when called from this method,
  be mutating the receiver?
  A value type creates a copy of the receiver when the method is invoked,
  so outside updates will not be applied to this receiver.
  If changes must be visible in the original receiver, the receiver must be a pointer.
- レシーバーがstruct,array,sliceで、その要素に変更される何かへのポインタを持っている場合、
  ポインタレシーバーが好ましい。(読み手に意図を伝えやすくする観点から)
- レシーバーが自然な値型だけを含む小さいarrayやstructで、
  かつ変更されるフィールドがなく、ポインタも含まない場合、
  もしくは、単にstringやintなどの基本型の場合、
  値レシーバーが意味を持つ。
  値レシーバーはゴミの量を減らす可能性がある。ただし、まずプロファイリングをやってから選択しろ。
- 1つの型にポインタレシーバーと値レシーバーを混ぜるな。どちらかに統一。

  - (自分注釈) `tour of go <https://go-tour-jp.appspot.com/methods/8>`__ でも混在させるなと言っている。

- 最後に、迷っているなら、ポインタレシーバーを使っておけ



struct型だけでなく、任意の型にメソッドが定義できる

- レシーバを伴うメソッドの宣言は、その型(レシーバの型)が同じパッケージにある必要がある
- そのため、下記の様に package 内で type 定義しないといけない

::

    type MyFloat float64

    func (f MyFloat) Abs() float64 {
        if f < 0 {
            return float64(-f)
        }
        return float64(f)
    }




TODO

- 裸の関数とメソッドは同名でも区別されるよね？ 別な


interface, インタフェース
----------------------------------

interface(インタフェース)型は、
メソッドのシグニチャ(名前,引数型,返り値型)の集まりで定義します。

interface型の変数には、それらのメソッドを実装済みの型の値であれば代入することができる。

あるinterfaceを満たす型を実装するというのは、必要なメソッドを実装するだけ。
Java みたいに ``implements`` みたいな明示的な宣言は不要。

インターフェース型のゼロ値は nil。

Goだと、interface型の型名に -er って付けるのが一般的？ Abser, Stringer

::

    type Abser interface {
        Abs() float64
    }

    // MyFloat型は Abs() float64 を持っている
    type MyFloat float64

    func (f MyFloat) Abs() float64 {
        if f < 0 {
            return float64(-f)
        }
        return float64(f)
    }

    // *Vertex型は Abs() float64 を持っている
    type Vertex struct {
        X, Y float64
    }

    func (v *Vertex) Abs() float64 {
        return math.Sqrt(v.X*v.X + v.Y*v.Y)
    }

    var a Abser

    f := MyFloat(-math.Sqrt2)
    a = f    // f つまり MyFloat型は Abser interface を満たすので代入可
             // a の中身は (f, MyFloat) みたいな感じ
    a.Abs()  // MyFloat型の Abs() を呼び出す(※2)

    v := Vertex{3, 4}
    a = &v   // &v つまり *Vertex型は Abser interface を満たすので代入可
             // a の中身は (&v, *Vertex) みたいな感じ
    a.Abs()  // *Vertex の Abs() を呼び出す(※2)

    a = v    // v つまり Vertex型は Abser interface を満たしていないの代入できない(※1)

(※1)
インターフェースが実装されているかどうかに関しては、
メソッド定義のレシーバが変数型かポインタ型かは区別される。
なので、普通は、メソッドの実装の際に、変数型にするかポインタ型にするかは統一する。

(※2)
インターフェース型の値は (値, 型) ようなもの。
型がわかっているので、その型のメソッドが呼ばれる


interface定義の中に、別のinterfaceを埋め込むことができる::

    type BaseInterface interface {
        func1()
        func2()
    }

    type SecondInterface interface {
        BaseInterface
        func3()
    }

    // SecondInterface を満たすには、
    // func1(), func2(), func3() を持っていないといけない。




nilの変数をinterfaceに代入した場合::

    var p *Vertex    // *Vertex型だけど初期化されていないので nil 
    var a Abser = p  // a の中身は (nil, *Vertex) みたいな感じ
                     // この場合。a 自体は nil ではない
    a.Abs()          // *Vertex の Abs() が v = nil として呼ばれる。
                     // なので nil でも対応できるように実装するのが一般的らしい

interface型変数がそもそもnilの場合::

    var a2 Abser  // a2 はそもそも nil
    a2.Abs()      // ランタイムエラー 


empty interface ＝ どんな型でも取れる変数 ::

    var i interface{}
    i = 42          // 代入可
    i = "hello"     // 代入可

interfaceの中身の型判定、型アサーション::

    var i interface{} = "hello"

    // 1つの返り値の場合、型が合わなかったらパニック
    s := i.(string)

    // 2つの返り値の場合、
    // 型があっていたら、v=interfaceの中身の値, ok=true
    // 型が違っていたら, v=その型のゼロ値, ok=false
    v, ok := i.(string)    // "hello", true
    v, ok := i.(float64)   // 0.0, false

interface の型スイッチ::

    switch v := i.(type) {    // ``(type)`` って書くのがポイント！
    case T:
        // ここでは変数 v の型は T型
    case S:
        // ここでは変数 v の型は S型
    default:
        // no match; ここでは変数 v の型は i と同じインターフェース型・値
    }


ある値が、あるinterfaceを満たしているか(あるメソッドが実装されているか)を調べるのも、
上の型アサーション、型switch を使ってできそう。


お作法として、interface は

GoのInterfaceの作法 "Accept Interfaces, Return structs" - y-zumiの日記
https://y-zumi.hatenablog.com/entry/2019/07/28/035632

> 「一般的にGoのInterfaceは、構造体などの値を実装するpackageではなく値を使用するpackageに属します。
> 値を実装しているpackageは、通常はポインターや構造体型を返す必要があります。





Stringer

fmt.Println などで表示させたい場合

::

    // fmt パッケージ(と、多くのパッケージ)では、
    // 変数を文字列で出力するためにこのインタフェースがあることを確認します。
    type Stringer interface {
        String() string
    }


Error

エラー値の基底クラスみたいなもの？

このインターフェースを実装して(継承するみたいな感じ)、独自エラー型を作れば、
型スイッチとかエラー種類ごとの分岐がかける？

::

    type error interface {
        Error() string
    }

io.Reader

::

    func (T) Read(b []byte) (n int, err error)




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


for(スライスやmapの要素をループ)::

    var pow = []int{1, 2, 4, 8, 16, 32, 64, 128}
    for i, v := range pow {
		...
	}


    // 不要なら _(アンダーバー) に代入して捨てることができる
    for i, _ := range pow
    for _, value := range pow
    // 1つの変数だけ指定した場合は、インデックスのみが入る
    for i := range pow

- 1つ目の変数は、インデックス(もしくはキー)
- 2つ目の変数は、値の **コピー**  (v は宣言されているし。)。
  なので v を変更しても元のスライスの中身は変更されない。
  vのポインタを返すようなケースも注意。
- 2つ目の変数vは、ループの度に定義されるのではなく、
  ループに先立ち定義された1つが使い回される。
  vの要素のポインタを返したりする場合、その中身がループで変わっていくので注意。

ラベル。2重ループから一気に抜ける場合とか::

    label1:
	for i := 0; i < 9; i++ {
            for j := 0; j < 9; j++ {
                if j == 3 {
                    break label1
                }
            }
	}

- ラベルの直後にあるスコープにラベルが付くイメージ。

  - なので、この場合forの前に書かないといけない。
  - 抜けるからといって、 ``for { }`` の後に書くのは間違い



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
- fallthroughさせたい場合は？

  - 同じ処理をする条件が複数あるという場合なら、caseに条件をカンマ区切りで複数書ける。
  - fallthrough って書けば、次のcaseに fallthrough する？？？

- case は定数である必要はない。式でも関数呼び出しでもよい。
- switchに渡す値は整数である必要はない

::

    // TODO これちょっと応用編だな
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



エラー処理, error
==========================

参考
--------

- `Error handling and Go - The Go Blog <https://blog.golang.org/error-handling-and-go>`__

error interface
---------------------

関数からエラーを返す場合は、下記のように、
2つ目の返り値(もしくは値を返さない関数の場合は唯一の返り値)で、
error型(interface)を返すのが標準っぽい。(※1) ::

    func Open(name string) (file *File, err error)

呼び出し側でのエラー処理としては、err != nil で分岐するのが標準っぽい。::

    f, err := os.Open("filename.ext")
    if err != nil {
        log.Fatal(err)
    }
    // do something with the open *File f

error interface の定義。stringを返す Error() メソッドを持って入れば満たす。::

    // cf. https://golang.org/pkg/builtin/#error
    type error interface {
      Error() string
    }

logとかfmt.Print系とかは、error型の表示の仕方を知っているのでそのまま渡せば良い
(多分、内部で Error() を呼んでいる)

::

    log.Fatal(err)
    fmt.Println(err)



関数が独自エラーを返す場合でも、戻り型は error 型にすること！
----------------------------------------------------------------

(※1) 関数が独自エラーを返す場合でも、戻り型は error 型にすること！
(独自エラー型にしてはダメ。バグのもと)。

戻り型以外でも、エラー値を一時的な変数に入れる場合なども、 独自エラー型に入れてはいけない。
変数に入れずに直接 return nil するか、どうしても一時変数に入れたいなら error 型に入れること！

- https://go.dev/doc/faq#nil_error
- `Goのnilについて - Carpe Diem <https://christina04.hatenablog.com/entry/2017/06/07/231030>`__

  - nilは型を持つ
  - interfaceの場合のみ、型もnilでないと ``xxx == nil`` はfalse


独自型の nil を interface 型に入れると nil 判定がうまくされないから。

::

    type MyError struct{}

    func (e MyError) Error() string {
        return "some error"
    }

    func MyErrorFunc() *MyError {   // <---- これダメ！！！
        return nil  // nilリテラルを返す。*MyError 型の nil になってしまう
    }

    func Wrapper() error {
        return MyErrorFunc()  // nilを返している（ただし型は*MyError）
    }

    func main() {
        err := Wrapper()  // interface型（error）のnilだけど、nil内部の型は*MyError
        fmt.Println(reflect.ValueOf(err))  // <nil>
        fmt.Println(reflect.TypeOf(err))  // *main.MyError

        if err == nil {
            fmt.Println("no error")  // 通らない
        }
    }


errorの作り方
---------------------

error interface を満たす値の作り方。

errors.New()。(内部的には ``*errorString`` 型というのになっている) ::

    errors.New("some message")


fmt.Errorf ::

    // 下記だと Printf の構文が使える
    fmt.Errorf("math: square root of negative number %g", f)

    // %w を使うと、errorをWrapしたerror (Wrapped Error) を作れる
    fmt.Errorf("funcHoge returns Error: %w", err)



独自のエラー型を定義::

    type SyntaxError struct {
        msg    string // description of error
        Offset int64  // error occurred after reading Offset bytes
    }

    func (e *SyntaxError) Error() string { return e.msg }


error を埋め込んだ独自interfaceを定義して、そこに合うように作るってこともある。::

    // net.Error の例
    type Error interface {
        error
        Timeout() bool   // Is the error a timeout?
        Temporary() bool // Is the error temporary?
    }

errorをWrapしたerror (Wrapped Error) を独自定義::

    // Error() string に加えて、
    // Unwrap() error を実装する

    // fmt.Errorf が返す wrapError 構造体の定義
    type wrapError struct {
            msg string
            err error
    }
     
    func (e *wrapError) Error() string {
            return e.msg
    }
     
    func (e *wrapError) Unwrap() error {
            return e.err
    }


エラー処理
------------------------

nil と比較::

    f, err := os.Open("filename.ext")
    if err != nil {
        log.Fatal(err)
        // return, 異常終了するなど。
    }
    // do something with the open *File f

エラーの同値性::

    こういう風に定義されているエラーがある場合は、エラーの同値性を調べる

        // 例 io/io.go
        var EOF = errors.New("EOF")
        var ErrClosedPipe = errors.New("io: read/write on closed pipe")
        var ErrNoProgress = errors.New("multiple Read calls return no data or error")
        var ErrShortBuffer = errors.New("short buffer")
        var ErrShortWrite = errors.New("short write")
        var ErrUnexpectedEOF = errors.New("unexpected EOF")

    if err == io.EOF { ... }

    if errors.Is(err, io.EOF) { ...  }   // Go 1.13 からのエラーのWrapを考えると、こちらが推奨


errorの実際の型によって処理を分ける::

    エラーごとに専用型が用意されている場合、型でエラーの種類が分かって、中身は追加の情報という感じ。

    === json の Decode の例 ===
    type SyntaxError struct {
            Offset int64 // error occurred after reading Offset bytes
            // contains filtered or unexported fields
    }

    type UnmarshalTypeError struct {
	Value  string       // description of JSON value - "bool", "array", "number -5"
	Type   reflect.Type // type of Go value it could not be assigned to
	Offset int64        // error occurred after reading Offset bytes
	Struct string       // name of the struct type containing the field
	Field  string       // the full path from root node to the field
    }

    if err := dec.Decode(&val); err != nil {
        if serr, ok := err.(*json.SyntaxError); ok {
            line, col := findLine(f, serr.Offset)
            return fmt.Errorf("%s:%d:%d: %v", f.Name(), line, col, err)
        }
        return err
    }


    === os.Open の例 ===
    type PathError struct {
        Op   string
        Path string
        Err  error
    }

    switch e := err.(type) {
    case *os.PathError:
        if errno, ok := e.Err.(syscall.Errno); ok {
            switch errno {
            case syscall.ENOENT:
                fmt.Fprintln(os.Stderr, "ファイルが存在しない")
            case syscall.ENOTDIR:
                fmt.Fprintln(os.Stderr, "ディレクトリが存在しない")
            default:
                fmt.Fprintln(os.Stderr, "Errno =", errno)
            }
        } else {
            fmt.Fprintln(os.Stderr, "その他の PathError")
        }
    default:
        fmt.Fprintln(os.Stderr, "その他のエラー")
    }


    // Go 1.13 からのエラーのWrapを考えると、こちらが推奨
    var perr *os.PathError
    if errors.As(err, &perr) {
        fmt.Fprintf(os.Stderr, "file is \"%v\"\n", perr.Path)
    }


Error() メソッドの返り値（文字列）を解析する::

    バッドノウハウっぽい。最後の手段





Wrapされたエラー
-------------------------------

Go 1.13 (17 October 2019) から、error の wrap という仕組みが入った。

参考

- `Working with Errors in Go 1.13 - The Go Blog <https://blog.golang.org/go1.13-errors>`__
- `errors · pkg.go.dev <https://pkg.go.dev/errors#example-package>`__


ある error を内包する error。 「Wrapしている」

たとえば、ライブラリからエラーが返ってきた場合に、
それに追加の情報(渡した引数とか)を付与した形で返したいときがある。
そういうときに使う。

数珠つなぎに何重にもwrapすることもできる。


代表的な作り方 ``fmt.Errorf("%w", err)`` では下記のような形になっている::

    type wrapError struct {
            msg string
            err error
    }

    func (e *wrapError) Error() string {
            return e.msg
    }

    func (e *wrapError) Unwrap() error {
            return e.err
    }


これ以外でも、下記の Unwrap() メソッドを持っていれば、別なerrorをwrapしているとみなされる::

    Unwrap() error   // 内包するエラーを返す


``errors.Is``   値との比較::

    var ErrNotFound = errors.New("not found")

    // 従来の書き方。 err が wrap されていると満たさない
    if err == ErrNotFound {
        // something wasn't found
    }

    // wrapに対応した新しい書き方
    if errors.Is(err, ErrNotFound) {
        // something wasn't found
    }


``errors.As``   型との比較::

    // 従来の書き方。 err が wrap されていると満たさない
    if e, ok := err.(*NotFoundError); ok {
        // e.Name wasn't found
    }

    // wrapに対応した新しい書き方
    var e *QueryError
    if errors.As(err, &e) {
        // err が QueryError もしくはそれをwrapしたものであれば成り立ち、
        // e に値がセットされる
    }


``errors.Unwrap`` ::

    w := errors.Unwrap(err)
    // err を1段階wrapする。
    // err が Unwrap() メソッドを持っていない場合は nil が返る


wrapしたエラーの作り方::

    fmt.Error("..... %w .....", errOrig)
    // %w があると errOrig をwrapしたものが返る
    // メッセージ (Error()で返る値は %w -> %v に読み替えてできるもの)






TODO
errors.Is, errors.As の動作を拡張する、Is,As メソッド





mod
=====================

下記のエラーがでたとき::

    fatal: 'origin' does not appear to be a git repository

下記で直る::

    go clean -modcache
    go get -u
