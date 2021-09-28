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


概要
==========

インストール::

    go get github.com/golang/mock/gomock
    go get github.com/golang/mock/mockgen

mockの生成

- mock を固めて入れる mock ディレクトリを作っておくのがいい

::

    mockgen -source=sample.go -destination mock/mock_sample.go


mockを使ったテストの実装

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
testcase に含めるのがいいと思う。



MockやStubの指定の仕方
============================

::

    TODO
