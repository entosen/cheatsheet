##################################################
テスト
##################################################

********************
testing
********************

概要
============

単体テストのフレームワーク。

参考

- `testing - Go 言語 <https://xn--go-hh0g6u.com/pkg/testing/>`__
- `Goのテストに入門してみよう！ | フューチャー技術ブログ <https://future-architect.github.io/articles/20200601/>`__
- `Golang testing 単体テストの書き方 - Qiita <https://qiita.com/ryu3/items/a2e39157bf1d55be149f>`__

ファイルの置き場

- 本体コードと同じディレクトリ、同じパッケージで、 ``foo_test.go`` というファイル名にする 

  - それにより、プライベート(小文字始まり)のメンバ・関数にもアクセス可能になる。

パッケージ内で関数名がぶつかったりする可能性があるので、
後述の testify/suite パッケージを利用するのもいい。


サンプルコード ::

    package hoge  // 普通は本体コードと同じにする

    import (
        "testing"
    )

    // テストコードは Test 始まり (TestHoge, Test_hoge はよいが、Testhoge はだめ)
    func TestAbs(t *testing.T) {
        got := Abs(-1)
        if got != 1 {
            t.Errorf("Abs(-1) = %d; want 1", got)
        }
    }

サブテスト::

    func TestFoo(t *testing.T) {
        // <setup code>
        t.Run("A=1", func(t *testing.T) { ... })
        t.Run("A=2", func(t *testing.T) { ... })
        t.Run("B=1", func(t *testing.T) { ... })
        // <tear-down code>
    }

DataProviderみたいなことは自前でやらないといけない::

    func TestAdd(t *testing.T) {
        type args struct {
            a int
            b int
        }

        // こんな感じでテストケースを列挙する
        tests := []struct{
            name string    // テスト名
            args args      // 入力
            want int       // 期待値
        }{
            {name: "fail", args: args{a: 1, b: 2}, want: 30},
            {name: "normal", args: args{a: 1, b: 2}, want: 3},
        }

        // tests をループしながら1つずつ t.Run を呼び出していく(階層的にサブテストになる)
        for _, tt := range tests {
            t.Run(tt.name, func(t *testing.T) {

                // Cleanup処理の登録
                // t.Fatalf でテストが失敗した場合でも Cleanup処理は呼び出される
                t.Cleanup(func() {
                    t.Log("cleanup!")
                })

                // t.Fatalf でテストが失敗しても defer の処理は呼び出される
                defer t.Log("defer!")

                if got := add(tt.args.a, tt.args.b); got != tt.want {
                    t.Fatalf("add() = %v, want %v", got, tt.want)
                }

                // t.Fatalf でテストが失敗した場合はそれ以降は呼び出されない。
                t.Log("after add() ...")
            })
        }
    }

スライスではなく map でテストケースを持たせる方法もあるが、順序がランダムになるのでお勧めしない。


正常になる場合と、エラーになる場合を、1つのテストケース型で表現する場合::

    func TestHoge(t *testing.T) {

            tests := []struct {
                    give    string
                    want    int64
                    wantErr interface{}
            }{
                    // nil, false を指定した場合は、エラーは発生しないこと期待
                    {"100", 100, nil},
                    {"100", 100, false},
                    // true を指定した場合は、なにかしらのエラーが発生(!=nil)を期待
                    {"xyz", 0, true},
                    // error型の値を指定した場合は、errors.Is で比較
                    {"xyz", 0, strconv.ErrSyntax},
                    {"128", 0, strconv.ErrRange},
                    // 関数を指定した場合は、その関数を使ってassertされる
                    {"xyz", 0, func(t *testing.T, gotErr error) {
                            var errNumError *strconv.NumError
                            assert.ErrorAs(t, gotErr, &errNumError)
                    }},
            }

            for _, tt := range tests {
                    t.Run(fmt.Sprintf(`give="%s"`, tt.give), func(t *testing.T) {

                            got, err := strconv.ParseInt(tt.give, 10, 8)

                            wantErrBool, ok := tt.wantErr.(bool)
                            if tt.wantErr != nil && !(ok && wantErrBool == false) {
                                    // エラーが返ってくることを期待するケース
                                    switch wantErr := tt.wantErr.(type) {
                                    case bool:
                                            assert.Error(t, err)
                                    case error:
                                            assert.ErrorIs(t, err, wantErr)
                                    case func(*testing.T, error):
                                            wantErr(t, err)
                                    default:
                                            t.Fatalf(`wantErrの指定が想定外: type=%T`, tt.wantErr)
                                    }
                            } else {
                                    // 正常(エラーが返ってこないことを期待するケース)
                                    assert.NoError(t, err, `ParseIntが想定外のエラーを返した`)

                                    assert.Equal(t, tt.want, got)
                            }
                    })
            }
    }



ネットで検索すると

- wantErr を bool 型にして、nilかどうかだけチェックしているもの
- wantErr を error型にして、同値性をチェックしているもの

があった。

想定どおりのエラーかどうかについては、Wrapを考慮したり、同値性か/同型なのか など、 結構複雑。

上のコードでとりあえず遭遇しそうなケースは対応できそう。



実行方法::

    go test -v 


    TODO
    テストを指定する場合 (ディレクトリを指定 ＋ -runで正規表現指定)
        go test -run ^TestHoge$ ./internal/hogedir/... 
                     テスト関数名(正規表現)

        (suiteの中の1テストを指定する場合)
        go test -run '^TestFooSuite$' -testify.m '^(TestDesignPrefetcherImpl_Prefetch)$' ./internal/hogedir/... 
                                                  テストメソッド名(正規表現)
                      suite.Runをしている関数名(正規表現)




名前::

    入力値 give
    実際値 got
    期待値 want
    エラーが発生することを期待 wantErr  (bool だったり、error型で同値性を調べたり)

    複数テストケースをループさせるとき
        テストケースのリスト  tests
        テストケースの1つ     tc,  tt


アサーション、Assertion
============================

testing には assertion は用意されていない。
代わりに自前で比較・エラー通知をする。

::

    // テストを失敗させる
    t.Fail()     # テスト失敗報告。テストは継続
    t.FailNow()  # テスト失敗報告。その時点でその(単一の)テストは中止される

    // メッセージを出力する
    t.Log(args ...any)                   # 引数それぞれを出力
    t.Logf(format string, args ...any)   # 引数を Sprintf的に解釈して出力

    // テストをスキップ報告。その時点でその(単一の)テストは中止
    t.SkipNow()


    // 複合
    t.Error, t.Errorf   # Log,Logf を呼んで、Fail
        t.Error(args ...any)
        t.Errorf(format string, args ...any)

    t.Fatal, t.Faitalf  # Log,Logf を呼んで、FailNow   
        t.Fatal(args ...any)
        t.Fatalf(format string, args ...any)

    t.Skip, t.Skipf     # Log,Logf を呼んで、SkipNow
        t.Skip(args ...any)
        t.Skipf(format string, args ...any)



これだといろいろ不便なので、 testify/assert を使うことが多い。


Helper()
--------------

テスト結果には、デフォルトで、アサーション関数(t.Failとか)を呼んだ位置が出力される。

各テストの共通処理を関数にくくり出したり、
アサーション関数を自作した場合は、
t.Fail() をした場所ではなく、その関数の呼び出し元の位置を表示したい。

その場合、共通関数の方の冒頭で、t.Helper() を呼べばよい。



Tips
============================

Goは、単純なstruct同士なら、中身を比較してくれる。

ただし、{slice, map, 関数}、それらをを含む struct は単純な ``!=`` では比較できない。

その場合は ``reflect.DeepEqual(a, b)`` を使う。


********************
gomock
********************

interface を元にmockを作成しテストを実行する。

参考

- `golang/mock: GoMock is a mocking framework for the Go programming language. <https://github.com/golang/mock>`__
- https://pkg.go.dev/github.com/golang/mock/gomock

概要
==========

インストール::

    # この変の違いがまだよくわからん...。

    go install github.com/golang/mock/mockgen@v1.6.0

    go get github.com/golang/mock/gomock
    go get github.com/golang/mock/mockgen


go では基本的に interface しか mock化できないっぽい。

本体コード::

    type Foo interface {
      Bar(x int) int
    }

    func SUT(f Foo) {
     // ...
    }

テストコード::

    func TestFoo(t *testing.T) {
      ctrl := gomock.NewController(t)

      // Assert that Bar() is invoked.  
      // 指定回数モックが呼び出されたとこを検証するために呼び出す。
      defer ctrl.Finish()

      m := NewMockFoo(ctrl)   // mockgen によってこの関数が用意される

      // Asserts that the first and only call to Bar() is passed 99.
      // Anything else will fail.
      m.
        EXPECT().
        Bar(gomock.Eq(99)).
        Return(101)

      SUT(m)
    }

mockの生成
=========================================

案1 同じディレクトリにmockファイルを作る
-------------------------------------------------

うちのチームではこっちを採用することになった。

ディレクトリ構成::

    cmd/
    internal/
        hoge/
            foo.go
            mock_foo.go        <--  mock/ 以下に同じパス・ファイル名で作るのがよさそう

::

    //go:generate mockgen -source=$GOFILE -destination=mock_$GOFILE -package=$GOPACKAGE



案2 大きくmockディレクトリを作る
----------------------------------------

mock を固めて入れる mock ディレクトリを作っておくのがいい::

    cmd/
    internal/
        hoge/foo.go
    mock/                  <-- ここ
        hoge/foo.go        <--  mock/ 以下に同じパス・ファイル名で作るのがよさそう

    たいていは、別な mock ディレクトリ以下に、
    本体と同じディレクトリ・ファイル名で格納するっぽい。

生成

自前でコマンド打つ場合。::

    mockgen -source=hoge/foo.go -destination mock/hoge/foo.go
    mockgen -source=hoge/foo.go -destination mock/foo.go

ファイルにコメントに書いておいて、自前でやる場合::

    該当ファイルにこんなコメントを書いておく。
    -distination の指定は、そのファイルが置いてある場所基準に書けばよいっぽい。

        //go:generate mockgen -source=$GOFILE -destination ../mock/foo.go

    Makefileにこんな感じで入れておいて使う
        mockgen:
            rm -rf mock/*      # ← ソースファイルが消えていた場合にmockも消えるように
            go generate ./...


mockを使ったテストの実装
========================================

::

    type Foo interface {
      Bar(x int) int
    }

    func SUT(f Foo) {
     // ...
    }

::

    func TestFoo(t *testing.T) {
      ctrl := gomock.NewController(t)

      // Assert that Bar() is invoked.  
      // 指定回数モックが呼び出されたとこを検証するために呼び出す。
      defer ctrl.Finish()

      m := NewMockFoo(ctrl)   // mockgen によってこの関数が用意される

      // Asserts that the first and only call to Bar() is passed 99.
      // Anything else will fail.
      m.
        EXPECT().
        Bar(gomock.Eq(99)).
        Return(101)

      SUT(m)
    }

testcase を作ってループさせる場合は、
mockオブジェクトを受け取って、expectなどをセットする無名関数を
testcase に含めるのがいいと思う。::

    testcases := []struct{
        name string
        mockSetupper func(*mock.MockFoo, *mock.MockBar)
    }{
        {
            name: "test1",
            mockSetupper: func(mockFoo *mock.MockFoo, mockBar *mock.MockBar) {
                mFoo.EXPECT().SUT('aaa').Return("hoge", nil)
                mBar.EXPECT().BAR(1).Return("hoge", nil)
            },
        }
    }


モックの返り値に別のモックを渡すようなケースもあるので、
mockSetupper は、全てのモックを受け取って一度に設定するような感じの方がよさそう。


MockやStubの指定の仕方, gomock
====================================

internal/hoge/foo.go::

    package hoge

    type Foo interface {
         Bar(x int) int
    }

    func SUT(f Foo) {
        // ...
    }


mock/hoge/foo.go (自動生成)::

    package mock_hoge

    func NewMockFoo(ctrl *gomock.Controller) *MockFoo {
        ...
    }

- package 名は、もともとのものの前に ``mock_`` が付く
- モックを生成する関数は interface 名の前に ``NewMock`` が付く


モックを使う::

    import (
        "testing"

        "github.com/golang/mock/gomock"

        // 作ったモックをimport
        mock_hoge "example.com/go-mock-sample/mock/hoge"
    )

    func TestSample(t *testing.T) {

        ctrl := gomock.NewController(t)
        // ↓これをやることで、モックが指定回数呼ばれたことをassertion
        defer ctrl.Finish()
     
        m := mock_hoge.NewMockFoo(ctrl)

        // Bar(99) が1回だけ呼ばれることをassert、それ以外は fail になる。
        m.
            EXPECT().
            Bar(gomock.Eq(99)).
            Return(101)

        SUT(m)
    }


スタブ

モックの場合とほぼほぼ同じ。

最後に ``.AnyTimes()`` を呼んでおけば、何回呼ばれてもassertionにならない。
(つまりスタブになる)

::

    m.
      EXPECT().
      Bar(gomock.Eq(99)).
      DoAndReturn(func(_ int) int {
        time.Sleep(1*time.Second)
        return 101
      }).
      AnyTimes()





モックの指定の仕方
=============================

参考

- `【Go言語】 gomock モックメソッドの指定方法まとめ | ramble - ランブル - <https://ramble.impl.co.jp/3235/>`__


基本
-----------------

::

    MockObject.EXPECT().期待するメソッド(引数1, 引数2, ...).Return(戻り値1, 戻り値2, ...)

Matcher
--------------

::

    // mockのメソッドがどういう引数で呼ばれるか
    m.EXPECT().Bar(gomock.Eq(99)).Return(101)
               ^^^^^^^^^^^^^^^^^^

	.Put("a", 1)                      // 期待する引数をそのまま書いてもよい
	.Put("b", gomock.Eq(2))           // gomock.Eq() を使ってもよい

        .Bar(gomock.Any())                // なんでもいい場合。


::

    gomock.Any()   // なんでもいい
    gomock.Eq(x)   // 一致(equalityをチェック)
    gomock.Len(i)  // その引数が特定のlenを持っていたらマッチ
    gomock.Nil()   // == nil であればマッチ

    gomock.InAnyOrder([]int{1, 2, 3})   // スライスが順不同で一致していればマッチ

    gomock.AssignableToTypeOf(s)   // ある型に代入可能可能であればマッチ
        var s fmt.Stringer = &bytes.Buffer{}
        AssignableToTypeOf(s).Matches(time.Second) // returns true
        AssignableToTypeOf(s).Matches(99) // returns false


Matcherの否定/ 組み合わせ ::

    gomock.Not     Not(Eq(5))
    gomock.All     All(Not(Eq(3), Not(Eq(5)))




アクション
-----------------

::

    .Return(101)   // 単純に固定の値を返せばよいとき

    // 渡された引数に応じた値を返したいとき
    .DoAndReturn(func(s string, i int) int {
            return (引数に応じた式など)
        })

.Do

DoAndReturn の、「戻り値」が不要な場合に使う。 

::

    // - クロージャーにしておいて、変数をセットする。 (他のモックの返り値や判定で使う)
    calledString := ""
    mockIndex.EXPECT().Put(gomock.Any(), gomock.Any()).Do(func(key string, _ interface{}) {
            calledString = key
    })

    // - テストをその場で失敗させる
    mockIndex.EXPECT().Put("nil-key", gomock.Any()).Do(func(key string, value interface{}) {
        if value != nil {
            t.Errorf("Put did not pass through nil; got %v", value)
        }
    })


.SetArg 。 ポインタ引数に代入したい場合

::

    mockIndex.EXPECT().Ptr(gomock.Any()).SetArg(0, 7)
        0番目の引数(*int型) の中身を 7 に変える


TODO これ .Do でも同じことできそうな気がするがどうなんだろうか。

- .SetArg の実装コードを見ると、ポインタだけでなく、引数がスライスやマップでも動くっぽい。
- メソッドの引数が多い場合だと、.Do でやると無名関数の記述が大変になるかも。




TODO

- .NillableRet()

呼ばれる回数
-----------------

デフォルトでは1回きっかり。


::

    TODO
    .Times(2)     // 2回きっかり
    .AnyTimes()   // 何回呼ばれてもよい。呼ばれなくてもよい。 (0回以上)
    .MaxTimes(10)  // (0回)～10回
    .MinTimes(3)   // 3回～ (無限)

呼ばれる順番
-----------------

デフォルトでは、呼ばれる順番は問わない。

順序を指定する場合::

    // InOrder を使う方法
    gomock.InOrder(
        mockObj.EXPECT().SomeMethod(1, "first"),
        mockObj.EXPECT().SomeMethod(2, "second"),
        mockObj.EXPECT().SomeMethod(3, "third"),
    )

    // After を使う方法
    firstCall := mockObj.EXPECT().SomeMethod(1, "first")
    secondCall := mockObj.EXPECT().SomeMethod(2, "second").After(firstCall)
    mockObj.EXPECT().SomeMethod(3, "third").After(secondCall)


独自Macher (TODO)
-----------------------

- 独自Matcher
- 他のMatcherに委譲する独自マッチャー


WantFormatter
GotFormatter


********************
testify
********************

golang でテストをより記述しやすくするためのパッケージ。

- assert 系の関数が用意されている


aseert
=================

https://pkg.go.dev/github.com/stretchr/testify/assert

::

    import (
      // ... 他の必要なパッケージ
      "github.com/stretchr/testify/assert"
    )

    func TestSomething(t *testing.T) {
      var a string = "Hello"
      var b string = "Hello"
      assert.Equal(t, a, b, "The two words should be the same.")
    }

    // assert に t をいちいち渡すのが面倒な場合
    func TestSomething(t *testing.T) {
      assert := assert.New(t)    # <-- 注目
      var a string = "Hello"
      var b string = "Hello"
      assert.Equal(a, b, "The two words should be the same.")
    }



::

    assert.Equal(t, expented, actual)

    assert.Panics(t, func(){ GoCrazy() })





    // assert.NoError, assert.Error
    // これは単に nil interface かそうでないかを判定 cf. assert.Nil, NotNil より狭い)
    // エラー判定の場合、一般的に interface error を != nil で判定するので、
    // エラーかどうかの判定をする場合にはこちらを使った方がよい。
    actualObj, err := SomeFunction()
    if assert.NoError(t, err) {
        assert.Equal(t, expectedObj, actualObj)
    }
    actualObj, err := SomeFunction()
    if assert.Error(t, err) {
        assert.Equal(t, expectedError, err)
    }

    // こちらは、error型以外の、一般的な値が nil である/でない ことをチェックする場合に使う。
    assert.Nil(t, obj)
    assert.NotNil(t, obj)
        (nil interface か、
         objが{pointer, function, map, slice, channel, interface} の何らかの型でその中身がnil)


出力されるメッセージ
--------------------------

例::

    === RUN   Test_Sample
        sample_test.go:1039:
                    Error Trace:    sample_test.go:1039
                    Error:          これはFailのfailureMessageです。
                    Test:           Test_Sample
                    Messages:       これはFailのmsgAndArgsです。
        sample_test.go:1042:
                    Error Trace:    sample_test.go:1042
                    Error:          Not equal:
                                    expected: 1
                                    actual  : 2
                    Test:           Test_Sample
                    Messages:       これはEqualのmsgAndArgsです。
    --- FAIL: Test_Sample (0.00s)
    FAIL


assert が出力する文言は2つ。Error と Messages 。


- Error (FailureMessage)

  - 通常は、失敗した理由(どういう比較をしたかがわかるようなもの)、および、渡された値を表示する。(ref. 後述)

- Messages (msgAndArgs)

  - テストコードから渡されたものがそのまま表示される。
  - FailureMessage の方には、値しか出ない(変数名は出ない) ので、それを補足するようなものがよさそう。


他の言語のテストライブラリだと、渡した変数名なんかも出してくれたりするけど、
その辺 Go は不親切な感じがする。


Fail と FailNow
^^^^^^^^^^^^^^^^^

一番プリミティブなものは、Fail と FailNow。 ::

    // Fail はテスト失敗を通知する。テストは継続
    func Fail(t TestingT, failureMessage string, msgAndArgs ...interface{}) bool

    // FailNow はテスト失敗を通知し、そこでテストは中止
    func FailNow(t TestingT, failureMessage string, msgAndArgs ...interface{}) bool

これらは

- 比較はせずにテストを失敗させるだけ。
- failureMessage → 結果の Error のところになる
- msgAndArgs → 結果の Messages のところになる


assert には testing.Log に相当する、ただメッセージを出すだけの関数は用意されていない。

ただ、メッセージを出したいだけの場合は、 t.Log, T.Logf を使う。


それ以外のいろいろな比較関数
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

比較関数と、失敗した場合の failureMessage::

    func Equal(t TestingT, expected, actual interface{}, msgAndArgs ...interface{}) bool

            // 数値を比較した場合
            Not equal:
            expected: 1
            actual  : 2
        
            // 文字列を比較した場合 Diff も出してくれる。複数行の文字列の場合に便利
            Not equal:
            expected: "02jsn2keav9p9"
            actual  : "dg5env7tq49ad"

            Diff:
            --- Expected
            +++ Actual
            @@ -1 +1 @@
            -02jsn2keav9p9
            +dg5env7tq49ad

    func Greater(t TestingT, e1 interface{}, e2 interface{}, msgAndArgs ...interface{}) bool

            "1" is not greater than "2"

    func True(t TestingT, value bool, msgAndArgs ...interface{}) bool

            Should be true






これらは、

- 比較・判定をし、満たしていない場合は中でFailを呼ぶ
- failuerMessage  は自動で作成してくれる

  - たいていは expected と actual の中身を表示してくれる

- msgAndArgs は渡されたものがそのままFailに渡る


msgAndArgs
^^^^^^^^^^^^^^^

assert の各関数は、追加の引数として、msgAndArgs を取れる。

標準の testing と違い、assert の msgAndArgs は個数によって下記のように動作する

- 0個 → 表示なし
- 1つ → そのオブジェクトを表示
- 2つ以上 → Sprintf 的に解釈して表示

なので、 ``Equal`` と ``Equalf`` のように2つずつ関数が用意されているが、
実質的な違いはない。


assert関数の自作
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

assert のコードを真似して作ればよいと思う。

- https://github.com/stretchr/testify/blob/v1.7.4/assert/assertions.go

基本的には、

- t.Hepler() を呼ぶ

  - エラーがあった箇所の表示を、
    Failを呼んだ行ではなく、この関数の呼び出し元にしたい場合、
    t.Helper() を呼べばよい。

- 比較して、満たしていなかったら assert.Fail を呼ぶ。

    - もしくは 既存のassert関数を利用してもよい。 failuerMessage の内容が分かりやすいかは気をつける。
    - FailNow()を呼ぶことはないはず。そのテストを途中で終わるかどうかは呼び出し側の判断。関数内の以降の判定をしない場合は return すればよい。

- 成功した場合は true、失敗した場合は false を return する

::

    func NearlyEqual(t *testing.T, expected, actual int, msgAndArgs ...interface{}) bool {

        t.Helper()

        diff := actual - expected
        if diff <= -3 || diff >= 3 {
            return assert.Fail(
                t,
                Sprintf("Not nealy equal, expected: %v, actual: %v", expected, actual),
                msgAndArgs...)
        }

        return true
    }



suite
================

https://github.com/stretchr/testify#suite-package


go test は、関数ベースでできている。(ファイル内のTest始まりの関数をどんどん呼んでいく)。

suite は、他の言語のテストフレームワークのように、テストクラスみたいな考え方。

SetUp/TearDown的なことも可能になる。

::

    import (
        "testing"
        "github.com/stretchr/testify/suite"
    )

    // Suite を1つ用意する
    type ExampleTestSuite struct {
        suite.Suite         // お約束
    }

    // お約束。go test からのcallをSuiteにつなげるためにこれが必要。
    func TestExampleTestSuite(t *testing.T) {
        suite.Run(t, new(ExampleTestSuite))
    }

    // 各テストは、Suite のメソッドとして実装する
    // receiver変数名、パッケージ名とかぶりそうだけど、こうするのが定番らしい。
    func (suite *ExampleTestSuite) TestExample() {
        assert.Equal(suite.T(), 2, 1+1)
    }


アサーションのやり方::

    // suite.T() で *testing.T が取れるので、下記のように assert パッケージを使う
    assert.Equal(suite.T(), 2, 1+1)

    // suiteで用意されている各assertion関数が、suiteのメソッドとしているのでそれを使う。
    // しかも T を指定する必要も無い
    suite.Equal(2, 1+1)


suite の中でさらにサブテストをするとき::

    for name, tc := range testcases {

        suite.Run(name, func() {...})

        // cf. Tの場合。
        t.Run(name, func(t *tesing.T) {...})
    }




``suite.Suite`` を埋め込んだ struct に、なんらかのメンバ変数を持たせることも可能。




*************************
httptest
*************************

- https://pkg.go.dev/net/http/httptest

goで書かれた http serverのコードをテストする
( ``ServeHTTP(w ResponseWriter, r *Request)`` の挙動をテストする)
ためのユーティリティ。

::

    import "net/http/httptest"


サーバを立ち上げずにテスト
==================================

::

    myHandler := NewMyHandler()  // テストしたいHandler

    // テストの入力。戻り値は *http.Request
    req := httptest.NewRequest("GET", "/hello", nil)

    // いろいろ記憶することができる http.ResponseWriter の実装
    rec := httptest.NewRecorder()

    // テスト対象のHandlerをコール
    myHandler.ServeHTTP(rec, req)

    assert.Equal(t, http.StatusOK, rec.Code)
    assert.Equal(t, "body期待値", rec.Body.String())

    // 上記以外の項目は rec.Result() で *http.Response を取得して比較する
    resp := rec.Result()
    assert.Equal(t, "application/json", resp.Header.Get("Content-Type"))


- httptest.NewRequest は http.NewRequest で作るのとどう違うのか？

  - そもそも http.NewRequest は、httpクライアントとしてリクエストを投げるときに使うものだから、
    サーバが受ける Request を生成するものではない？ という使い分けだと思う。
  - 多分 http.NewReqeust で作ってしまうと、いろいろ足りないものがありそう。

    - 送信元IPとか
    - Content-Length とか？？



(注) go の http server が受け取る ``r *http.Request`` での Host 関連のフィールドについて。

- Host名(http通信上の ``Host:`` ヘッダ)は、r.Host に入り、r.Header には入らない(除かれる)
- r.URL は、http通信の1行目 ``GET /hoge/fuga?foo=bar HTTP/1.0`` みたいな部分をパースしたものなので、
  r.URL.Host は空になっている

なので、その想定に合わせて、httptest のリクエストも作らないといけない。

httptest.NewRequest は、 ``r.Host`` が ``example.com`` で作られるので、
変更する場合は、 ``r.Host = "hoge.com"`` などとしないといけない。
( ``r.Header.Set("Host", "hoge.com")`` は間違い )



サーバを立ち上げてテスト
==================================

指定した Handler をローカルにサーバを起動する。

やろうと思えば ``http.HandleFunc("/", h); http.ListenAndServe(":8080", nil)`` 
みたいにやればできなくはないが、ポートが空いていなかったらとか、
起動前に通信をしてしまうとテストが失敗してしまうとか、終了はどうするかとか、いろいろめんどう。
そこを楽にしてくれる。

ただ、上の「サーバを立ち上げずにテスト」で足りるような気はする。

::

    myHandler := NewMyHandler()  // テストしたいHandler

    // ローカルにサーバを起動。ローカルの空いている適当なポートで起動する。
    testServer := httptest.NewServer(myHandler)
    defer testServer.Close()

    // 実際に起動したサーバにhttpリクエストを投げ、結果を受け取る。
    // testServer.URL で、起動している Method, host名, ポート番号 を含んだ文字列が返る。
    req, _ := http.NewRequest("GET", testServer.URL+"/hello", nil)
    resp, _ := client.Do(req)
    respBody, _ := ioutil.ReadAll(resp.Body)

    assert.Equal(t, http.StatusOK, resp.StatusCode)
    assert.Equal(t, helloMessage, string(respBody))

- ``httptest.NewTLSServer(myHandler)`` とすれば https で起動する


スタブサーバを立ち上げて、httpクライアント部分のテスト
==========================================================

上の「サーバを立ち上げてテスト」の応用で、スタブサーバを立ち上げて、
httpクライアント部分のテストをすることもできるが、
この用途だと正直、httpmock とかの方がやりやすいと思う。

::

  h := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintln(w, "Hello, client")
  })

  ts := httptest.NewServer(h)
  defer ts.Close()

  // テスト対象のコード(http client になっている)の実行。
  // 向き先はなんとかして上で立てたサーバに向くようにする必要がある。

  // 結果のアサーション

  // 想定どおりにリクエストが飛んだかの確認は、このやり方だと難しそう


*************************
httpmock
*************************

httpクライアントになっている部分のテストのための、スタブサーバを用意するためのライブラリ。
本体コードが使う、外部のリソースをシミュレーションする。

httpmock は、標準のhttp通信ライブラリを差し替えて(横取りして)、レスポンスを返す。

横取りするので、http通信を行っている本体コードの方を書き換える必要がない。
(interface化して差し替えたり、向き先を変えたりする必要がない。)

実際にサーバが起動/Listenしているわけではないっぽい。おそらくだが、別goルーチンも動いていないのでは？

"mock" と言いつつ、呼ばれたことの assertion はできない。いわゆるスタブに近い。

- https://github.com/jarcoal/httpmock
- https://pkg.go.dev/github.com/jarcoal/httpmock

インストール::

    go get github.com/jarcoal/httpmock

簡単な使い方::

    import "github.com/jarcoal/httpmock"

    func TestFetchArticles(t *testing.T) {

      // Activate を呼ぶことで、http通信ライブラリが差し替えられる
      httpmock.Activate()
      defer httpmock.DeactivateAndReset()

      // Exact URL match
      httpmock.RegisterResponder("GET", "https://api.mybiz.com/articles",
        httpmock.NewStringResponder(200, `[{"id": 1, "name": "My Great Article"}]`))

      // Regexp match (could use httpmock.RegisterRegexpResponder instead)
      httpmock.RegisterResponder("GET", `=~^https://api\.mybiz\.com/articles/id/\d+\z`,
        httpmock.NewStringResponder(200, `{"id": 1, "name": "My Great Article"}`))

      // do stuff that makes a request to articles

      // get count info
      httpmock.GetTotalCallCount()

      // get the amount of calls for the registered responder
      info := httpmock.GetCallCountInfo()
      info["GET https://api.mybiz.com/articles"]             // number of GET calls made to https://api.mybiz.com/articles
      info["GET https://api.mybiz.com/articles/id/12"]       // number of GET calls made to https://api.mybiz.com/articles/id/12
      info[`GET =~^https://api\.mybiz\.com/articles/id/\d+\z`] // number of GET calls made to https://api.mybiz.com/articles/id/<any-number>
    }

サーバの準備(実際にはライブラリの差し替え
===============================================

::

    httpmock.Activate()
    defer httpmock.DeactivateAndReset()

    // もし、本体コードが、標準のhttp通信ライブラリ (http.DefaultClient) ではなく
    // 別のものを使っている場合は下記のように明示的に指定して差し替える。
    httpmock.ActivateNonDefault(someHTTPClient)
    defer httpmock.DeactivateAndReset()


httpmock.RegisterResponder で、URL に Responder を紐付ける
==============================================================

::

    func RegisterResponder(method, url string, responder Responder)

        // 普通のURL、もしくはパス
        //     クエリパラメタ(?以降)が含まれている場合は、その順番は保持される(区別される)

        httpmock.RegisterResponder("GET", "http://example.com/",
          httpmock.NewStringResponder(200, "hello world"))

        httpmock.RegisterResponder("GET", "/path/only",
          httpmock.NewStringResponder("any host hello world", 200))

        // =~で始まれば正規表現
        httpmock.RegisterResponder("GET", `=~^/item/id/\d+\z`,
          httpmock.NewStringResponder("any item get", 200))

    
    func RegisterRegexpResponder(method string, urlRegexp *regexp.Regexp, responder Responder)
        // regexp.Regexp で指定


    func RegisterResponderWithQuery(method, path string, query interface{}, responder Responder)
        // RegisterResponder と違って、クエリの順序を問わずにマッチする

        path の部分を ``=~`` 始まりにすることはできない。
        query として取りうるのは、
        - url.Values
        - map[string]string
        - string, a query string like "a=12&a=13&b=z&c" (see net/url.ParseQuery function)

        例
          expectedQuery := net.Values{
            "a": []string{"3", "1", "8"},
            "b": []string{"4", "2"},
          }
          httpmock.RegisterResponderWithQueryValues(
            "GET", "http://example.com/", expectedQuery,
            httpmock.NewStringResponder("hello world", 200))

          // requests to http://example.com?a=1&a=3&a=8&b=2&b=4
          //      and to http://example.com?b=4&a=3&b=2&a=8&a=1


    func RegisterNoResponder(responder Responder)
        // 他のルールにマッチしない場合の Responder を指定する。
        // デフォルトは、httpmock.ConnectionFailure がセットされている。



マッチのアルゴリズム

- https://pkg.go.dev/github.com/jarcoal/httpmock#readme-algorithm

下記の順で探しにいく::

    http://example.tld/some/path?b=12&a=foo&a=bar (original URL)
    http://example.tld/some/path?a=bar&a=foo&b=12 (sorted query params)
    http://example.tld/some/path (without query params)
    /some/path?b=12&a=foo&a=bar (original URL without scheme and host)
    /some/path?a=bar&a=foo&b=12 (same, but sorted query params)
    /some/path (path only)


Responder
===================

Responder はこういう形::

    type Responder func(*http.Request) (*http.Response, error)


基本的には、下記の ``New*Responser`` などを利用する::

    func NewStringResponder(status int, body string) Responder
        httpmock.NewStringResponser(200, `Some Response`)
        httpmock.NewStringResponder(200, httpmock.File("body.txt").String())
        Content-Typeはセットされない


    func NewBytesResponder(status int, body []byte) Responder
        httpmock.NewBytesResponder(200, httpmock.File("body.raw").Bytes())
        Content-Typeはセットされない


    func NewErrorResponder(err error) Responder
        エラーを返すResponder。 (nil, err)を返す。
        httpのエラーレスポンスではなく、そもそも通信がうまく行かなかった系の挙動に相当。


    func NewJsonResponder(status int, body interface{}) (Responder, error)
    func NewJsonResponderOrPanic(status int, body interface{}) Responder
        body にはJSON Marshal(encode)可能なオブジェクトや構造体を渡す。
        Content-Typeは "application/json" にセットされる

        httpmock.NewJSONResponderOrPanic(200, &MyBody)
        httpmock.NewJsonResponderOrPanic(200, httpmock.File("body.json"))
            // httpmock.File は Marshall() メソッドをごまかしてくれるので、
            // JSON 文字列をファイルに書いておけば、それをそのまま送信してくれる
        httpmock.NewJsonResponderOrPanic(200, `{"a": 1, "b": 2}`)
            // これはうまく行かないらしい。さらにJSON Marshalがかかるため。
            // NewStringResponce で作って、そこに Content-Type を足す、独自のResponderを作るのがいい。


    func NewXmlResponder(status int, body interface{}) (Responder, error)
    func NewXmlResponderOrPanic(status int, body interface{}) Responder
        Content-Type は "application/xml" にセットされる

        httpmock.NewXmlResponderOrPanic(200, &MyBody)
        httpmock.NewXmlResponder(200, httpmock.File("body.xml"))
            // httpmock.File は Marshall() メソッドをごまかしてくれるので、
            // JSON 文字列をファイルに書いておけば、それをそのまま送信してくれる
        httpmock.NewJsonResponderOrPanic(200, `<data><item>a</item></data>`)
            // これはうまく行かないらしい。さらにXML Marshalがかかるため。
            // NewStringResponce で作って、そこに Content-Type を足す、独自のResponderを作るのがいい。


    func NewNotFoundResponder(fn func(...interface{})) Responder
        // 一般的には RegisterNoResponder() と組み合わせて、
        // マッチするルールが無かった場合に、処理をさせる場合に使う。

        // fn の引数は、マッチしなかったルート情報が渡る。
        // fn は t.Fatal や t.Log を渡すことを意図しているっぽい。
        // ログする必要がなければ fn は nil でもいい。
        // fn が panic せずに return した場合、リクエスト側には
        // (nil, "Responder not found for GET http://foo.bar/path") ようなものが返る。
        // (使いどころが分からん。デバッグ用？)


    httpmock.InitialTransport.RoundTrip
        // これを指定すると、もともとの http client にパスバックし、本当にhttp通信を行う。
        httpmock.RegisterNoResponder(httpmock.InitialTransport.RoundTrip)


    httpmock.ConnectionFailure
        常に (nil, NoResponderFound) を返す Responder。
            NoResponderFound は変数で、デフォルトでは errors.New("no responder found") になっている。
        マッチするものがなかった場合に使われる


    func ResponderFromResponse(resp *http.Response) Responder
        常に固定の http.Response を返す Responder を作る。
        
    func ResponderFromMultipleResponses(responses []*http.Response, fn ...func(...interface{})) Responder
        呼ばれるごとに返すものを変えていくResponder。
        呼ばれるごとにリストの順で返していく。
        リストの長さ以上に呼ばれた場合は、fn が呼ばれ、その後エラーが返る。

          httpmock.RegisterResponder("GET", "/foo/bar",
            httpmock.ResponderFromMultipleResponses(
              []*http.Response{
                httpmock.NewStringResponse(200, `{"name":"bar"}`),
                httpmock.NewStringResponse(404, `{"mesg":"Not found"}`),
              },
              t.Log),
          )


注意: resp.body は、繰り返し読まれても大丈夫なようにしないといけない。(下記のどれかをやる)

- resp を NewStringResponse, NewBytesResponse で作る
- resp.body を NewRespBodyFromString, NewRespBodyFromBytes で作る


独自のレスポンダーを書く場合::

    httpmock.RegisterResponder("GET", url,
        func(req *http.Request) (*http.Response, error) {
            resp, err := httpmock.NewJsonResponse(200, mockedResponse)
            if err != nil {
                return httpmock.NewStringResponse(500, ""), nil
            }
            return resp, nil
        },
    )

    中では、下記の New*Response 関数を使うと楽。
    (New*Responder と対応しているので、動作・使い方はそちらを参照)
        func NewStringResponse(status int, body string) *http.Response
        func NewBytesResponse(status int, body []byte) *http.Response
        func NewJsonResponse(status int, body interface{}) (*http.Response, error)
        func NewXmlResponse(status int, body interface{}) (*http.Response, error)

    上記を使わずに独自で http.Response を組み立てる場合、
    body は、下記の関数で作らないといけない。

        func NewRespBodyFromBytes(body []byte) io.ReadCloser
            httpmock.NewRespBodyFromBytes(httpmock.File("body.txt").Bytes())

        func NewRespBodyFromString(body string) io.ReadCloser
            httpmock.NewRespBodyFromString(httpmock.File("body.txt").String())


正規表現のプレイスホルダーの部分を取り出して、使うこともできる::

    httpmock.RegisterResponder("GET", `=~^https://api\.mybiz\.com/articles/id/(\d+)\z`,
      func(req *http.Request) (*http.Response, error) {
        // Get ID from request
        id := httpmock.MustGetSubmatchAsUint(req, 1) // 1=first regexp submatch
        return httpmock.NewJsonResponse(200, map[string]interface{}{
          "id":   id,
          "name": "My Great Article",
        })
      },
    )

    func GetSubmatch(req *http.Request, n int) (string, error)
    func GetSubmatchAsFloat(req *http.Request, n int) (float64, error)
    func GetSubmatchAsInt(req *http.Request, n int) (int64, error)
    func GetSubmatchAsUint(req *http.Request, n int) (uint64, error)
    func MustGetSubmatch(req *http.Request, n int) string
    func MustGetSubmatchAsFloat(req *http.Request, n int) float64
    func MustGetSubmatchAsInt(req *http.Request, n int) int64
    func MustGetSubmatchAsUint(req *http.Request, n int) uint64


メソッドチェーンでResponderを修飾::

    func (r Responder) Delay(d time.Duration) Responder
        dだけ待ってから r を呼び出すようににする
        httpmock.NewStringResponder(200, "{}").Delay(100*time.Millisecond)

    func (r Responder) Once(fn ...func(...interface{})) Responder
        1回だけ呼び出し可能にする
        それ以上呼ばれたときは fn を呼んで、その後エラーを返す。
        httpmock.NewStringResponder(200, "{}").Once(t.Log)

    func (r Responder) Times(n int, fn ...func(...interface{})) Responder
        n回だけ呼び出し可能にする
        それ以上呼ばれたときは fn を呼んで、その後エラーを返す。
        httpmock.NewStringResponder(200, "{}").Times(3, t.Log)

    func (r Responder) Then(next Responder) (x Responder)
        呼ばれるごとに、順にResponderが呼ばれるようにする。
        A := httpmock.NewStringResponder(200, "A")
        B := httpmock.NewStringResponder(200, "B")
        C := httpmock.NewStringResponder(200, "C")
        httpmock.RegisterResponder("GET", "/pipo", A.Then(B).Then(C))

    func (r Responder) Trace(fn func(...interface{})) Responder
        呼び出される度にログ出力するようにする
        httpmock.NewStringResponder(200, "{}").Trace(t.Log)

