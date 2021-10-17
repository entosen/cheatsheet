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

- 本体コードと同じディレクトリ、同じパッケージで、 foo.go というファイル名にする 

  - それにより、プライベート(小文字始まり)のメンバ・関数にもアクセス可能になる。


サンプルコード ::

    import (
        "testing"
    )

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




実行方法::

    got test -v 


    TODO



名前::

    実際値 got
    期待値 want

    複数テストケースをループさせるとき
        テストケースのリスト  tests
        テストケースの1つ     tc,  tt


アサーション、Assertion
============================

testing には assertion は用意されていない。
代わりに自前で比較・エラー通知をする。

::

    t.Fatal    # その時点でその(単一の)テストは中止される
    t.Error    # これが呼ばれても、テストは実行される

    t.Fatalf, t.Errorf



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
=====================

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
        setMock func(*mock.MockFoo)
    }{
        {
            name: "test1",
            setMock: func(m *mock.MockFoo) {
                mc.EXPECT().SUT('aaa').Return("hoge", nil)
            },
        }
    }


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


Matcher
--------------

::

    // mockのメソッドがどういう引数で呼ばれるか
    m.EXPECT().Bar(gomock.Eq(99)).Return(101)
               ^^^^^^^^^^^^^^^^^^

	.Put("a", 1)                      // 期待する引数をそのまま書いてもよい
	.Put("b", gomock.Eq(2))           // gomock.Eq() を使ってもよい

        .Bar(gomock.Any())                // なんでもいい場合。


return
-----------------

::

    .Return(101)   // 単純に固定の値を返せばよいとき

    // 渡された引数に応じた値を返したいとき
    .DoAndReturn(func(s string, i int) int {
            return (引数に応じた式など)
        })


呼ばれる回数
-----------------

デフォルトでは1回きっかり。


::

    TODO
    .Times(2)     // 2回きっかり
    .AnyTimes()   // 何回呼ばれてもよい。呼ばれなくてもよい。 (0回以上)

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


