=======================================
json
=======================================

サンプル
==================

json.Marshal の例::

    type ColorGroup struct {
            ID     int      `json:"id"`
            Name   string   `json:"name,omitempty"`
            Colors []string `json:"colors"`
    }
    group := ColorGroup{
            ID:     1,
            Name:   "Reds",
            Colors: []string{"Crimson", "Red", "Ruby", "Maroon"},
    }
    b, err := json.Marshal(group)  // ([]byte, error) が返る
    if err != nil {
            fmt.Println("error:", err)
    }
    os.Stdout.Write(b)

json.Unmarshal の例::

    var jsonBlob = []byte(`[
            {"name": "Platypus", "order": "Monotremata"},
            {"name": "Quoll",    "order": "Dasyuromorphia"}
    ]`)

    type Animal struct {
            Name  string `json:"name"`
            Order string `json:"order"`
    }

    var animals []Animal
    err := json.Unmarshal(jsonBlob, &animals)
    if err != nil {
            fmt.Println("error:", err)
    }

    fmt.Printf("%+v", animals)


::

    Field int                            // タグなしの場合のキー名はフィールド名と同じ
    Field int `json:"myName"`            // "myName" というキーで出力
    Field int `json:"myName,omitempty"`  
    Field int `json:",omitempty"`        // キー名はフィールド名と同じでよい、かつ、omitemptyを指定したい場合

    Field int `json:"-"`     // そのフィールドは出力されない
    Field int `json:"-,"`    // "-" というキーで出力したい場合

- 大文字始まりのフィールドがMarshalで出力される



スライスとマップが null になるか []{} になるか::

    nilスライス (宣言だけした状態, nilを代入しているケース)
         → null
    長さ0のスライス ([]string{} みたいな感じ)
         → [] 

    nilマップ (宣言だけした状態、nilを代入しているケース)
         → null
    要素数の0のマップ (map[string]string{} みたいな感じ)
         → {}

    サンプル
        type AAA struct {
            L1 []string
            L2 []string
            M1 map[string]string
            M2 map[string]string
        }
        a := AAA{
            L1: nil,
            L2: []string{},
            M1: nil,
            M2: map[string]string{},
        }
        b, _ := json.Marshal(a)
        fmt.Println(string(b))
        →  {"L1":null,"L2":[],"M1":null,"M2":{}}

omitempty について
========================

json.Marshal のときに効く。 Unmarshal ときは関係ない。

omitempty を付けたときにキーごと除かれるもの

- bool型のfalse
- 数値系の 0
- 空文字列(長さ0の文字列, "")
- ポインタの nil
- interface の nil

  - nil interface → 省略される
  - interface の中身が型付きのnil → 省略されない。キーが出力され、値はその型の MarshalJSON() による

    - interface の実体が構造体ポインタ型でnil であれば、値として ``null`` が出力される

- 長さ0の配列 ([0]int みたいなもの)

  - cf. 長さ0以外の配列 (例えば ``[3]int`` ) は省略されない。キーが出力され、値は ``{0,0,0}`` が出力される

- 空のスライス (nil、長さ0のスライス)

  - cf. 長さ0以外のスライス (例えば ``[]int{0,0,0}`` ) は省略されない。キーが出力され、値は ``{0,0,0}`` が出力される

- 空のmap (nil、要素数0のmap)

- cf. 中身が全部ゼロ値の構造体 → 省略されない。キーが出力され、値はその型の MarshalJSON() による

(参考) https://pkg.go.dev/encoding/json で "omitempty" を検索

::

    The "omitempty" option specifies that the field should be omitted from the encoding
    if the field has
        an empty value, defined as false, 0, a nil pointer, a nil interface value,
        and any empty array, slice, map, or string.



