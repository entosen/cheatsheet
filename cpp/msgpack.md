# msgpack

## msgpack-c

https://github.com/msgpack/msgpack-c

とりあえず、会社でよく使われている以下のバージョンで。

```
ports/msgpack-1.3.0_jp_1
ports/msgpack-devel-1.3.0_jp_1 (test)
```

include
```cpp
#include <msgpack.hpp>
// ヘッダファイルだけで、.so不要なので、Makefileには -L や -l は特に書かなくてよい
```


### pack

(ドキュメント: https://github.com/msgpack/msgpack-c/wiki/v1_1_cpp_packer )

#### 基本の形

pack の方法は大きく以下の2つ

- msgpack::packer を使う
    - 柔軟。階層構造のような複雑な構造でも、１つ１つpackしていきながら組み立てていける
    - C++だと表現しづらい、型が混じった array や map も組み立てられる
    - multiple toplevel objects なデータも作成できる
    - packされるフォーマットを指定していれる関数がある (最適なものではなくあえて大きい入れ物でいれることなどもできる)
- msgpack::pack を使う
    - pack1回で処理できるものであれば、こちらのほうが手間が少ない
    - 複雑な構造は作れない (`pack_array` や `pack_multi` は呼べない)
    - 一応複数回呼べば、multiple toplevel objects なデータも作れる
    
##### msgpack::packer を使うやり方

```cpp
    msgpack::sbuffer sbuf;  // バッファを用意 (後述)
    msgpack::packer<msgpack::sbuffer> pk(&sbuf);  // buffer につながった packer を用意

    // array 型
    pk.pack_array(3);
    pk.pack(std::string("Log message ... 1"));
    pk.pack(std::string("Log message ... 2"));
    pk.pack(std::string("Log message ... 3"));

    // map型
    pk.pack_map(2);
    pk.pack(std::string("x");
    pk.pack(3);
    pk.pack(std::string("y");
    pk.pack(3.1415);

    // sbuf.data(); // char *
    // sbuf.size(); // size_t
```

上記以外にも、format を指定して入れるような関数がいろいろある。
→ https://github.com/msgpack/msgpack-c/wiki/v1_1_cpp_packer の "Pack Manually" を参照。

##### msgpack::pack を使うやり方

```cpp
    // packしたいもの
    std::vector<std::string> vec;
    vec.push_back("Hello");
    vec.push_back("MessagePack");

    // pack
    msgpack::sbuffer sbuf;  // バッファを用意
    msgpack::pack(sbuf, vec);

    // sbuf.data(); // char *
    // sbuf.size(); // size_t
```

#### pack でどのクラスがどのタイプにパックされるか

msgpack::pack と msgpack::packer::pack は、
代表的な型については、ほとんど直感どおりMsgPack に pack してくれる。

ドキュメント
- 対応表: https://github.com/msgpack/msgpack-c/wiki/v1_1_cpp_adaptor

```
bool型       → bool
整数型       → integer
double型     → float

std::map     → map   // 上記ドキュメントには Map → array となっているが、map 型にpackされる

std::vector  → array
std::pair    → array

std::string  → string    // 長さを持っているので、途中に'\0' があっても大丈夫
char*        → string    // 終端の'\0' は含まない。
                          // 当然だが、途中に '\0' があるとそこまでになるので注意。
                          // pack_str(size); pack_str_body(cp, size) を使えば、途中に '\0' が入っても大丈夫

std::vector<char>   → bin   // 長さを持っているので、途中に '\0' を含んでも大丈夫。

// 標準で string 型にpackされるやつを、強制的に bin型にpackするには、
// pack_bin(size); pack_bin_body(cp, size); を用いるか、
// std::vector<char> data(str.begin(), str.end());  こんな感じで vector<char> に変換してpackする。
```

自作クラス

```cpp
class myclass {
private:
    std::string m_str;
    std::vector<int> m_vec;
public:
    // 以下のどれかを定義しておくことで、クラスを一発でpackすることができる。
    MSGPACK_DEFINE_ARRAY(m_str, m_vec);  // MSGPACK_DEFINE されたものは Array型にpackされる。
                                         // メンバ変数名は入らない(Map型ではない)ので注意
    MSGPACK_DEFINE_MAP(m_str, m_vec);    // MSGPACK_DEFINE されたものは Map型にpackされる。
                                         // メンバ変数名がキーとして入る
    MSGPACK_DEFINE(m_str, m_vec);        // MSGPACK_USE_DEFINE_MAP が define されているかに依る。
                                         // (msgpack.hpp 読み込み前に定義されている必要あり)
};

void pack_myclass() {
    myclass c1;
    // メンバ変数をセット

    msgpack::sbuffer sbuf;
    msgpack::pack(sbuf, c1);
}
```


#### バッファ

packer を使う場合も、packを使う場合も、
出力用の領域として、以下の関数を持つインスタンスを渡す。

```cpp
write(const char*, std::size_t);
```

通常は msgpack::sbuffer を使うことが多い

```cpp
msgpack::sbuffer sbuf;
sbuf.data();    // → char * 
sbuf.length():  // → size_t
```

その他
- std::stringstream も使えるけど、data() と length() を取得するのに、一度 std::string にしないといけないので面倒？
- msgpack::vrefbuffer --- 参照を利用して高速。でも気をつけて扱う必要がある。
- msgpack::zbuffer --- 書き出すと同時に圧縮してくれる
- msgpack::fbuffer --- c-style の `FILE*` をラップ






### unpack

(ドキュメント: https://github.com/msgpack/msgpack-c/wiki/v1_1_cpp_unpacker)

#### 基本の形

以下２つの形

- unpackしたいデータが手元に揃っている
    - → msgpack::unpack を使う
- unpackしたいデータが順次送られてくるような場合(そろっているかどうか不明)
    - → msgpack::unpacker を使う


##### msgpack::unpack を使う方法

```cpp
void some_function(const char* data, std::size_t len) {

    msgpack::unpacked unpacked;
    msgpack::unpack(unpacked, data, len);
	// 注: unpack は１つの topleve 要素以下しか処理しない。
	//     複数の toplevel 要素がある場合は後述の方法を使う。

    msgpack::object = unpacked.get();  
	// 注: object型は unpack内のメモリ領域を参照しているので、
	//     object型が生きている間は unpacked型も生きていないといけない。

    // object からの取り出し方は後述。
}

```

##### msgpack::unpacker を使う方法

```cpp
// The size may decided by receive performance, transmit layer's protocol and so on.
std::size_t const try_read_size = 100;

msgpack::unpacker unp;

// Message receive loop
while (/* block until input becomes readable */) {
    unp.reserve_buffer(try_read_size);
    // unp has at least try_read_size buffer on this point.

    // input is a kind of I/O library object.
    // read message to msgpack::unpacker's internal buffer directly.
    std::size_t actual_read_size = input.readsome(unp.buffer(), try_read_size);

    // tell msgpack::unpacker actual consumed size.
    unp.buffer_consumed(actual_read_size);

    msgpack::unpacked result;
    // Message pack data loop
    while(unp.next(result)) {
        msgpack::object obj(result.get());
        // Use obj
	// object からの取り出し方は後述。
    }
    // All complete msgpack message is proccessed at this point,
    // then continue to read addtional message.
}
```


###### multiple toplevel data を unpack で扱う場合

unpackでやる場合

```cpp
void some_function(const char* buffer, std::size_t len) {
    std::size_t off = 0;

    while (off != len) {
        msgpack::unpacked result;
        unpack(result, buffer, len, off);
        msgpack::object obj(result.get());
        // Use obj
	// object からの取り出し方は後述。
    }
}
```


#### msgpack::object から値の取り出し

##### convert で丸っと

基本的なデータ構造 (数値型、文字列型、Array、Map、およびその入れ子など) は、以下のように convert 一発で可能。
```cpp
    map<string,int> data;
    obj.convert(data);
```

自作のクラスに `MSGPACK_DEFINE` をつけて pack したものも、convert で一発で可能。

```cpp
    MyClass c1;   // MSGPACK_DEFINE が定義されているクラス
    obj.convert(c1);
```

それ以外の型を convert1発で取り出したい場合は、adaptorクラスを書く。



##### マニュアルで抽出

参考
- https://github.com/msgpack/msgpack-c/wiki/v1_1_cpp_adaptor
- [c++でmsgpackを使ってみる - ludwig125のブログ](http://ludwig125.hatenablog.com/entry/2017/11/22/234335)


TODO 例えば arrayやmap の要素にいろいろな型が含まれているもの。

以下のような操作で取り出すことはできそう。


object の type を調べる。 (
```
obj.type 
    msgpack::type::NIL
    msgpack::type::BOOLEAN
    msgpack::type::POSITIVE_INTEGER
    msgpack::type::NEGATIVE_INTEGER
    msgpack::type::FLOAT
    msgpack::type::STR
    msgpack::type::BIN
    msgpack::type::ARRAY
    msgpack::type::MAP
    msgpack::type::EXT


obj.via.array
    size
    ptr[0]
    ptr[1] 

as とか
```




あと、`array` object を `vector<msgpack::object>` に convert というのはできるっぽい
```
    msgpack::object obj;   // いろんな型を含んだ array 。 [ 123, "abc", false, 3.14 ] みたいな
    
    std::vector<msgpack::object> v1;
    obj.convert(v1);
```




### adaptor

TODO 
