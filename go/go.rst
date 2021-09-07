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

基本型
-------------

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


文字列
---------------------

::

    "abcde\n"

    // raw string literal (バックスラッシュを特殊解釈しない)
    `ab"cde"\n`     

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
    
    - 配列の長さまで含めて型

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

スライスの初期値は nil 。

- nil スライスは、 0 の長さと容量を持っており、何の元となる配列も持っていない。

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

    // この状態では中身は nil 
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
    

変数レシーバとポインタレシーバ

- 変数レシーバー

    - 変数のコピーがメソッドに渡る。(なので、変更しても元の変数には影響を与えない)
    - 変数レシーバのメソッドは、変数からでも、ポインタからでも呼び出せる

        - コンパイラが ``p.Abs()`` を ``(*p).Abs()`` と解釈してくれる

- ポインタレシーバー

    - 内容の更新をする場合には、ポインタレシーバにしないといけない
    - 内容のコピーをしたくない場合も、ポインタレシーバーにする
    - ポインタレシーバのメソッドは、変数からでも、ポインタからでも呼び出せる

        - コンパイラが ``v.Scale(10)`` を ``(&v).Scale(10)`` と解釈してくれる

- c.f. 上記の解釈はレシーバーに限った話で、引数ではそうは解釈されない
  (ポインタにはポインタを渡す必要がある)


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

インターフェース型のゼロ値は nil ？

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
- 2つ目の変数vは、ループの旅に定義されるのではなく、
  ループに先立ち定義された1つが使い回される。
  vの要素のポインタを返したりする場合、その中身がループで変わっていくので注意。

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
error型(interface)を返すのが標準っぽい。::

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


errorの作り方
---------------------

error interface を満たす値の作り方。

errors.New()。(内部的には ``*errorString`` 型というのになっている) ::

    errors.New("some message")

    // 下記だと Printf の構文が使える
    fmt.Errorf("math: square root of negative number %g", f)


独自のエラー型を定義::

    type SyntaxError struct {
        msg    string // description of error
        Offset int64  // error occurred after reading Offset bytes
    }

    func (e *SyntaxError) Error() string { return e.msg }


error を内包した独自interfaceを定義して、そこから作るってこともある。::

    // net.Error の例
    type Error interface {
        error
        Timeout() bool   // Is the error a timeout?
        Temporary() bool // Is the error temporary?
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

errorの実際の型によって処理を分ける::

    if err := dec.Decode(&val); err != nil {
        if serr, ok := err.(*json.SyntaxError); ok {
            line, col := findLine(f, serr.Offset)
            return fmt.Errorf("%s:%d:%d: %v", f.Name(), line, col, err)
        }
        return err
    }

TODO switch で分かれる例も。



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


代表的な作り方 ``fmt.Error("%w", err)`` では下記のような形になっている::

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
