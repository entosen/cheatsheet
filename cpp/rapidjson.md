
# rapidjson


## 基本。エンコードとデコード

```cpp
#include "rapidjson/document.h"
#include "rapidjson/writer.h"
#include "rapidjson/stringbuffer.h"

using namespace rapidjson;

int main() {
    // 入力・デコード
    const char* json = "{\"sv\":\"hoge\", \"iv\":123, \"dv\":999.999 }";
    Document d;
    d.Parse(json);

    assert(d.IsObject());  // Documentクラスは Objectタイプの Value でもある。

    // 出力・エンコード
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    d.Accept(writer);
    std::cout << buffer.GetString() << std::endl;

    return 0;
}
```


## そもそもJSONとは

```
{
    "hello": "world",        // 文字列
    "t": true,               // 真偽値  true/false は小文字でないといけない
    "f": false,              // 真偽値 
    "n": null,               // null
    "i": 123,                // 数値 (整数) 10進表記に限る。2進,8進,16進表記はできない。
    "pi": 3.1415,            // 数値 (実数) 。 1.0e-10  という表記もできる
    "a": [1,2,3,4],          // array
    "o": { "apple": "red", "lemon": "yellow" }   // object。 キーは文字列に限る
}
```

## Value のタイプ

こんなイメージ

```
Value
    Nullタイプ                 // null
    Boolタイプ                 // true, false
    Numberタイプ               // 123, -1, 0.456, -3.1415, 999999999999999
	(整数型)
	    Int
	    Uint
	    Int64
	    UInt64
	Double
    Stringタイプ               // "hoge", "this is a string"
    Arrayタイプ                // [1,2,3,4]
    Objectタイプ               // { "apple": "red", "lemon": "yellow" }
```


タイプをチェックする。

rapidjson の場合、解釈は厳密。
例えば、"123" は、文字列タイプとしてしか解釈しない。(IsNumberはfalseになる)
1 を Boolタイプとしては解釈しない。

ただし、`123` は IsDouble は false だが、GetDouble はエラーにならずに動作する。

```
v.IsNull()

v.IsBool()

                123  -123   3000000000  -3000000000  5000000000   123.000
v.IsNumber()     T    T       T            T           T            T
v.IsInt()        T    T       F            F           F            F     // 整数値 かつ int32_t で表現可能な範囲ならTure
v.IsUint()       T    F       T            F           F            F     // 整数値 かつ uint32_t で表現可能な範囲ならTure
v.IsInt64()      T    T       T            T           T            F     // 整数値 かつ int64_t で表現可能な範囲ならTure
v.IsUInt64()     T    F       T            F           T            F     // 整数値 かつ uint64_t で表現可能な範囲ならTure
v.IsDouble()     F    F       F            F           F            T     // 実数値ならTrue

v.IsString()
v.IsArray()
v.IsObject()

v.GetType()
static const char* kTypeNames[] = 
    { "Null", "False", "True", "Object", "Array", "String", "Number" };
kTypeNames[v.GetType()]
```

### Value を作る

```
// Value の コンストラクタで作る
Value v;          // null type
Value b(true);    // bool
Value i(-123);    // int
Value u(123u);    // unsigned
Value d(1.5);     // double
Value o(kObjectType);  // object
Value a(kArrayType);   // array
```

Valueの中身をセットする。typeも変える。
```
Value v;     // この時点では null type

v.SetInt(10); 
v.SetObject();
v.SetArray();

v = 10; 
```




### 各タイプで可能な操作

#### null, boolean, string, 整数, 小数

```
// nullタイプ
// get系できない。v.IsNull() だけ。

// booleanタイプ
v.GetBool();    // bool

// stringタイプ
v.GetString():  // string型

// 整数値
v.GetInt()
v.GetUint()
(int)v

// 小数型
v.GetDouble()
```

#### 文字列
```
// ゲット
s.GetString();    // 何型？

// コピーしてセット
Document document;
Value s;
s.SetString(buffer, len, document.GetAllocator());
s.SetString(buffer, document.GetAllocator());  // \0を含まないならこれでもOK

// 参照をセット
Value s;
s.SetString("hoge");
s = "hoge";            // これも同様
```

#### array型

```
Value v0 = a[0];     // 0始まり
Value v1 = a[1];     // 0始まり
Value v2 = a[2];     // 0始まり

for (Value::ConstValueIterator itr = a.Begin(); itr != a.End(); ++itr)
    printf("%d ", itr->GetInt());

a.Empty()   // bool
a.Capacity()   // SizeType = unsigned
```


#### Objectタイプ

```
// 狙ったキーの値を取得

// この方法は2回Lookupするので、効率が悪い。
if (v.HasMember("apple")) {
    v2 = v["abble"];
}

// こっちの方法の方がよい
Value::ConstMemberIterator itr = v.FindMember("hello");
if (itr != v.MemberEnd())
    printf("%s\n", itr->value.GetString());


// イテレーション
for (Value::ConstMemberIterator itr = document.MemberBegin();
    itr != document.MemberEnd(); ++itr)
{
    printf("Type of member %s is %s\n",
        itr->name.GetString(), kTypeNames[itr->value.GetType()]);
}

// メンバーの追加
Value contact(kObjet);
contact.AddMember("name", "hoge", document.GetAllocator());
contact.AddMember("married", true, document.GetAllocator());


// メンバーの削除
TODO

```



