## 文字列リテラル

複数行の文字列をインデントを崩さずに書く方法

```
s = textwrap.dedent("""\
	Hello, world
	    この行はインデントされている
	ほげほげ
	""")
```

## 文字列型のようなもの str型 bytes型

(python3)

参考
- [Unicode HOWTO — Python 3.7.4 ドキュメント](https://docs.python.org/ja/3/howto/unicode.html)
- [組み込み型#テキストシーケンス型 — Python 3.7.4 ドキュメント](https://docs.python.org/ja/3/library/stdtypes.html#str)
- [組み込み型#バイナリシーケンス型 — Python 3.7.4 ドキュメント](https://docs.python.org/ja/3/library/stdtypes.html#binaryseq)

まず、おさらい

- Unicode (TODO UCS とかいうのもあったはず)
    - 文字セット。0 から 0x10FFFF に文字を割り振っている。コードポイント。`U+265E` と表記したりする。
	- `a (U+0061)`, `b (U+0062)`, `{ (U+007B)`, `あ (U+3042)`, `漢 (U+6F22)`
- Unicode文字列、コードユニット列
    - (概念的)コードポイントの列
- 文字エンコーディング、エンコーディング、符号化
    - Unicode 文字列をバイト列として翻訳する規則
	- UTF-8
	    - コードポイントが 128 未満だった場合、そのまま1バイト
	    - コードポイントが 128 以上の場合、128 から 255 までのバイトからなる、2、3 または 4 バイトのシーケンス

Python3では、
- str型は Unicode文字列。
- bytes型、単純なバイナリ列。


ソースコードの文字エンコーディングを指定
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-    <-- こんな感じで指定する。
```

```
# リテラル
s = 'abcdeあ漢字\n'   # <class 'str'> 'abcdeあ漢字' len=8

b = b'abcde\x41\n'    # <class 'bytes'> b'abcdeA\n' len=7
b = b'abcdeあ漢字\n'  # × bリテラルには ascii 文字しか書けない。 \x?? は解釈してくれる。\u???? は解釈されない。
```

ファイルから読み込み
```
# -------------------------------
# str型に読み込み
# -------------------------------
with open('input_utf8.txt', 'r') as f:
    a = f.read()
    # <class 'str'> 'abcdeあ漢字\n' 9

with open('input_eucjp.txt', 'r', encoding='euc-jp') as f:     # utf-8以外はファイルのエンコーディングを指定する必要がある
    a = f.read()
    # <class 'str'> 'abcdeあ漢字\n' 9

# -------------------------------
# bytes型に読み込み
# -------------------------------
with open('input_utf8.txt', 'rb') as f:
    a = f.read()
    # <class 'bytes'> b'abcde\xe3\x81\x82\xe6\xbc\xa2\xe5\xad\x97\n' 15

with open('input_eucjp.txt', 'rb') as f:
    a = f.read()
    # <class 'bytes'> b'abcde\xa4\xa2\xb4\xc1\xbb\xfa\n' 12
```

ファイルに出力
```
# -------------------------------
# str型の出力
# -------------------------------
a = "abcdeあ漢字\n"
with open('output_utf8.txt', 'w') as f:
    f.write(a)
    # テキストモードでファイルを開いた場合、f.writeに渡すのは str型じゃないといけない

# 出力のエンコーディングを指定する場合はこんな感じ
with open('output_eucjp.txt', 'w', encoding='euc-jp') as f:
    f.write(a)

print(a)      # 標準出力にはこれで出力できる

# -------------------------------
# bytes型の出力
# -------------------------------
b1 = b'abcde\xe3\x81\x82\xe6\xbc\xa2\xe5\xad\x97\n'
b2 = b'abcde\xa4\xa2\xb4\xc1\xbb\xfa\n'

# バイナリモードでファイルを開いた場合、f.writeに渡すのは bytes-like objectじゃないといけない
with open('output_bin.txt', 'wb') as f:
    f.write(b1)
    f.write(b2)

sys.stdout.buffer.write(b1)  # これでbytesをそのまま出力できる
print(b1)   # --> b'abcde\xe3\x81\x82\xe6\xbc\xa2\xe5\xad\x97\n'
            #     bリテラル表記で出力されてしまう。
```

str型、bytes型をファイルのように扱う
```
f = io.StringIO("some initial text data")                  # 'r' モードでopenしたものに近い
f = io.BytesIO(b"some initial binary data: \x00\x01")      # 'rb' モードでopenしたものに近い
```

str型 <--> bytes型 相互変換 (ついでに整数値とも)
```
# bytes --> str
b'\x80abc'.decode("utf-8", "strict")    # そのバイト列を utf-8 として解釈して str化
                                        # 第2引数: strict, replace, ignore

# str --> bytes
s.encode('utf-8')                       # その文字列を utf-8 でエンコードした結果のバイト列を返す


# 整数値 -->  str
chr(57344)   # その整数に対応するコードポイントの文字(str型 1文字)
# str --> 整数値
ord('\ue000')  # その文字に対応するコードポイント値(整数)
```


bytes型に対しても、str型が持っているようなテキスト処理が行える。
ただし、引数に渡すものも bytes 型を渡す必要がある。
```
b.split(b'\n')
```

## パッケージ管理、環境

### virtualenv

参考ドキュメント

- [Pythonの仮想環境を構築できるvirtualenvを使ってみる - Qiita](http://qiita.com/H-A-L/items/5d5a2ef73be8d140bdf3)

```
# 事前準備
sudo easy_install virtualenv

# 仮想環境の作成
mkdir /path/to/PythonTest
virtualenv --no-site-packages /path/to/PythonTest

# その仮想環境を使いたいとき (おそらくPATHなど必要な環境変数がセットされる)
source /path/to/PythonTest/bin/activate

# 仮想環境終了 (環境変数などを元に戻す)
deactivate
```

### パッケージ管理, pip

```
pip 
python -m pip
py -m pip          # windwos の場合、これがおすすめ。どのバージョンのpythonにpipするかわかりやすい

py -m php -V       # どのpythonバージョンのpipが起動するか確認


py -m pip freeze               # インストールされているパッケージ一覧を表示
py -m pip list                 # インストールされているパッケージ一覧を表示。微妙に違うらしい。

// インストール
py -m pip install パッケージ
py -m pip install パッケージ==バージョン番号
py -m pip install -r requirement.txt    # テキストファイルに書かれたパッケージを一括でインストール

// アンインストール
py -m pip uninstall パッケージ 

// 検索
py -m pip search 検索ワード
```



## デコレータ

関数デコレータの場合で説明。メソッドも同じ。クラスの場合もほぼ同じ(関数をクラスに読み替える)

参考
- 8. 複合文 (compound statement) — Python 3.9.4 ドキュメント#関数
https://docs.python.org/ja/3/reference/compound_stmts.html#function
- Pythonのデコレータを理解するための12Step - Qiita
https://qiita.com/_rdtr/items/d3bc1a8d4b7eb375c368


デコレータ ＝ 関数をラップして、同名の関数名に入れたもの。

デコレータの書き方には2種類ある
```
# ---------------------------------
# 引数を取らないデコレータ
# ---------------------------------
@decorator1
def func(a):
    ...

    ↓ これとほぼ同じ

func = decorator1(func)

この形のデコレーターは、関数を受け取って別の関数を返す関数
例
def decorator1(func):
    def new_func(*args, **argv):
	# なにかしら追加の処理
	return func(*args, **argv)  
    return new_func

# ---------------------------------
# 引数を取るデコレータ
# ---------------------------------
@decorator2("arg1", "arg2")
def func(a)
    ...
    ↓ これとほぼ同じ

func = decorator2("arg1", "arg2")(func)

この形のデコレータは、呼び出した結果引数無しのデコレータを返す関数？？
```
