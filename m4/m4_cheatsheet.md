参考
- [Super Technique 講座～m4 チュートリアル](http://www.nurs.or.jp/~sug/soft/super/m4.htm)
- リファレンス的なもの → [GNU macro processor:](http://www.bookshelf.jp/texi/m4/m4-ja.html)



入力のトークンへの分割

m4 は入力を読み込むと、それを以下の3種類のトークン(とコメント)に分割する。

- 名前(name)
    - アルファベット、数字、_(アンダースコア) を自由に並べたもののうち、先頭の文字が数字でないもの
    - 名前にマクロの定義が存在するときは、マクロの呼び出しとして認識され、 展開の対象となる
    - `foo`, `_tmp`, `name01`
- クオートされた文字列(quoted string)
    - クォートされた文字列（quoted string）は、 (デフォルトでは)引用符 `\`` と `'` に
      囲まれた文字列のうち、 
      文字列の内部で開始引用符`と終了引用符'の数が釣り合っているものです。 
    - クォートされた文字列（quoted string）のトークンとしての値は、 
      いちばん外側にある引用符を一対だけ取った文字列です。
      ```
          `'           → 空文字列
          `hoge'       → hoge
          ``hoge''     → `hoge'
      ```
    - クォートされた文字列は、マクロ展開されない
    - クォート記号を変えるには、changequote(開始クォート文字列,終了クォート文字列)
- その他単独の文字
    - 名前（name）とクォートされた文字列（quoted string）の構成要素にならない文字はすべて、
      それ自身で一つのトークンとなります。
    - 記号、空白、など
    - マクロ展開されない

- コメント
    - `#` から改行までの間
    - m4 の入力としては無視されるが、出力はされる。
    - コメントは入れ子にすることはできない。
    - コメント記号を変えるには、changecom(開始コメント文字列,終了コメント文字列)



マクロ呼出し

```
name                            # 引数を伴わないマクロ呼び出し。 × name()
name(arg1, arg2, ..., argn)     # 引数を伴うマクロ呼び出し
```

マクロを呼び出したくない場合 → クオートする

名前の切れ目じゃないところでマクロを呼び出したい場合 
```
indir(`X')Free86
```



マクロ定義

```
define(name [, expansion])
```

基本的にはクォートする。
クォートしないと、この定義自体が置換され、複数の定義ができる？
```
define(`hoge', `fuga')     # hoge を fuga に置換する。
```

引数を利用

```
define(`kv', `keyは$1、valueは$2)')
kv(apple, リンゴ)
kv(orange, みかん)
```

余分な引数は無視、足りない引数は空文字列になる。


$0 --- マクロ名
$# --- 引数の個数
$*
$@
それ以外の $ は、単に `$`文字として扱われる


```
undefine(name)
```


条件分岐


```
ifdef(NAME,IF-CASE,ELSE-CASE)
ifelse(比較対象Ａ,比較対象Ｂ,一致時に展開[,不一致時に展開])
```





dnl

--prefix-builtins


置換。 

トークンが前後に空白があいて(？)出現した場合は置換される。
置換は繰り返し行われる。無限ループに注意。






```
define(`hoge', `fuga')   # hoge を fuga に置換する
This is a hoge.          # これは hoge トークンとみなされるっぽい。
```

それ以上展開させない
define(`hoge', ``fuga'')

複数行

define(`hoge', `This
is
a
pen')
aaa hoge bbb


indir(`X')  --- 強制的に置換を行う。トークン前後に空白を置きたくない場合に。

```
define(`X',`W')
XFree86               # トークン`X'とは認識されない
indir(`X')Free86      # トークン`X'と認識される
```






undefine(`X')
pushdef( , )
popdef( )

include(`ファイル名')
sinclude(`ファイル名')



	

syscmd(shell-command)  --- コマンドの実行
esyscmd(shell-command)  --- コマンドの出力を読む
    ```
    define(`osname', `esyscmd(uname -o)')
    ```
sysval


コマンドライン




Cygwin の m4 だったら、
LC_CTYPE=ja_JP.utf-8 で、ファイルの文字コードがutf-8 であれば日本語も動いた。






虎の巻

```
define(`_aaa_', `1')
changequote({{{,}}})
ここは、どちらの場合も出力されます。
ifdef({{{_aaa_}}},{{{
ここは、defined場合に出力されます。
}}}, {{{
ここは、undefined場合に出力されます。
}}})
```

```
define(`os', `Windows')
changequote({{{,}}})
ここは、どちらの場合も出力されます。
ifelse(os, Linux, {{{
ここは、{{{os}}} が Linuxの場合に出力されます。
}}}, {{{
ここは、{{{os}}} が Linux 以外のときに出力されます。
}}})
```
