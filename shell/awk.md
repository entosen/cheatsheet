# awk


## 実行方法

```
awk 'パターン-アクション' [file]...
awk -f プログラムファイル名 [file]...
```



## 基本

```
パターン {アクション}
...

例)
/abc/ { print }     # 正規表現にマッチする行を出力
{ print $2 }        # パターンはなくてもよい。その場合、全ての行にコマンドが実行される
```

## フィールド

フィールドとは、いわゆるカラム。

デフォルトでは、spaceとtab 。

参考 → FS, FPAT, RS, OFS, ORS


## パターン

```
空のパターン   全ての入力行にマッチ

BEGIN
END
BEGINFILE
ENDFILE

# 比較演算子
$1 == 'hoge"
$2 > 80

# 正規表現
/^S/    # 'S'で始まる行
```

パターンの組み合わせ

```
# 論理演算子 (&& || !)
pattern1 && pattern2
# 三項演算子
pattern1 : pattern2 : pattern3
```


パターンの範囲

```
pattern1,pattern2    # パターン1が出現してからパターン2が出現するまで
/Tanaka/,/Sasaki/
```

## アクション

```
print          # 行を出力
print $3       # 行の3カラム目だけを出力
print $3,$1    # 行の3カラム目,1カラム目を出力

printf

変数に代入
aaa = "hoge"
line += 1


制御
if (式) 文
if (式) 文 else 文
while (式) 文
do 文 while (式)
for (式; 式; 式) 文
for (変数 in 配列) 文
break
continue
next
exit
exit 式
{ 文の並び }    # 改行、もしくは ';' 
```

## 式



## 変数


配列

添字は内部では文字列として扱われる
```
a[1] = 10
a[2] = 20
a['foo'] = "abc"

m[1][2] = 100    # 多次元配列。gawk4.0以降
```

特別な変数

```
$1, $2, ...    現在の入力レコードにおいてn番目のフィールド
$0             現在の入力レコード全体

FS       入力フィールドの区切り文字。定義しない場合、空白文字の連続？
    TODO例
FPAT     フィールドを区切る正規表現？
RS       入力レコードの区切り文字。定義しない場合、改行。
OFS      出力フィールドの区切り文字。定義しない場合、スペース。
ORS      出力レコードの区切り文字。定義しない場合、改行。

ARGC
ARGV

FILENAME   現在の入力ファイル名
NR         現在のレコード番号。複数ファイルの場合は通しての番号
FNR        現在のファイルのレコード番号
NF         現在のフィールド数

RSTART
RLENGTH

SUBSEP

IGNORECASE

ENVIRON     環境変数を保持する配列

```

関数

```
注: 文字位置などは 1始まり。

index(STRING, TARGET)
    pos = index("123456789", "1")    → 1
length(STRING)
match(STRING, REGEXP)    1始まり。見つからなければ 0
split(STRING, ARRAY,FILD_SEPARATOR)
    split("2015-04-01\t12:34:56", time, "[-\t:]+")
patsplit(STRING, ARRAY, REGULAR_EXPRESSION)     gawk4.0から
sprintf(FORMAT, EXPRESSION1, ...)
sub(REGEXP, REPLACEMENT_STRING, TARGET_VALUE)  → 戻り値は置換した数
    str = "ABC123ABC"
    sub(/ABC/, "abc", str)  → str は "abc123ABC" になる
    sub(/ABC/, "&zzz", str) → str は "ABCzzz123ABC" になる。&はマッチした文字を表す。
gsub(REGEXP, REPLACEMENT_STRING, TARGET_VALUE)   最初の1つだけじゃなく全部置換する
substr(STRING, P, LENGTH)   P 文字目から LENGTH文字分の部分文字列を返す
```

## tips

```

```

