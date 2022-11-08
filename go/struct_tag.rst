=======================================
go の struct のタグについて
=======================================

go のタグの基本・一般的なところ 
=======================================

サンプル::

    type User struct {
            ID     int    `label:"User ID" validate:"require"`
            Name   string `label:"User Name"`
    }

    type Book struct {
            Title  string `json:"title"`           // ベーシックな使い方
            Price  int    `json:"price,omitempty"` // ゼロ値の場合はこのフィールドを出力しない
            Author string `json:"-"`               // このフィールドは出力しない
    }


go の reflect パッケージは、タグ文字列をmapっぽく扱う方法を持っているので、普通はそれに従う。
(the conventional format。 `reflect.StructTag`_ 型)

.. _`reflect.StructTag`: https://pkg.go.dev/reflect#StructTag

- 普通は全体をバッククオートで囲んで raw string literal にする
- ``key:"value"`` の形

  - keyとvalueの間のコロンのまわりに空白を入れてはいけない

- key

  - keyは、印字可能文字。スペース、ダブルクオート、コロン は使えない

- value

  - value はダブルクオートで囲む。goの文字列リテラル同様の解釈がされる(エスケープ文字など)
  - value の中身・解釈方法までは StructTag は関知しない。
    (jsonのカンマ区切りなどは、jsonライブラリが独自に解釈している)

- 複数のキーを並べる場合

  - 空白区切りで並べる
  - 同じkeyは複数書けない (多分)


::

    By convention, tag strings are a concatenation of optionally space-separated key:"value" pairs. 
    Each key is a non-empty string consisting of non-control characters
    other than space (U+0020 ' '), quote (U+0022 '"'), and colon (U+003A ':').
    Each value is quoted using U+0022 '"' characters and Go string literal syntax.




タグを用いた機能を自前で実装
==============================================


サンプル::

    type S struct {
            F string `species:"gopher" color:"blue"`
    }

    s := S{}
    st := reflect.TypeOf(s)   // Type型
    field := st.Field(0)      // i番目のフィールドを取り出す。 StructField型

    field.Tag                 // StructTag 型。タグ文字列全体
    field.Tag.Get("color")    // タグから特定キーの値を取り出す
    field.Tag.Lookup("color") // タグから特定キーの値を取り出す。keyの存在チェックを厳密に



詳細

Type型::

    type Type interface {
        Name()       string
        PkgPath()    string
        Kind()       Kind
        NumField()   int
        Field(i int) StructField
        FieldByName(name string) (StructField, bool)
        ...
    }


StructField型。 Structの中の1つのフィールドを表す。 ::

    type StructField struct {
    	// Name is the field name.
	Name string

	// PkgPath is the package path that qualifies a lower case (unexported)
	// field name. It is empty for upper case (exported) field names.
	// See https://golang.org/ref/spec#Uniqueness_of_identifiers
	PkgPath string

	Type      Type      // field type
	Tag       StructTag // field tag string
	Offset    uintptr   // offset within struct, in bytes
	Index     []int     // index sequence for Type.FieldByIndex
	Anonymous bool      // is an embedded field
    }


StructTag型。 Structの中の1つのフィールドのタグ文字列を表す。 ::

    type StructTag string     // それ自体が文字列でタグ文字列全体に相当

    func (tag StructTag) Get(key string) string
        指定したキーの値を返す。
        キーが存在しない場合、空文字列。
        キー自体ないのか、キーがあり空文字列が指定されているかは区別できない。cf. Lookup()
        conventinal format でない場合、unspecified。

    func (tag StructTag) Lookup(key string) (value string, ok bool)
        指定したキーの値を返す。
        指定したキーが存在したら(値が空文字列であっても)、(その値, true)。
        キーが存在しない場合、("", false)。
        conventinal format でない場合、unspecified。









json
================

TOOD


validator
================

TODO


