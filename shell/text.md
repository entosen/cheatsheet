# テキスト処理


## 行を範囲で抜き出す cat, head, tail

サマリ

```
元 (seq 10)
|     head -n 3
|     |     head -n -3
|     |     |     tail -n 3
|     |     |     |     tail -n +3
|     |     |     |     |     sed -n '3,5p'
|     |     |     |     |     |     sed -n '0~3p'
|     |     |     |     |     |     |
1     1     1                             1
2     2     2                             2
3     3     3           3     3     3     3
4           4           4     4           4
5           5           5     5           5
6           6           6           6     6
7           7           7                 7
8                 8     8                 8
9                 9     9           9     9
10                10    10                10
```


```
        sed -n '/bbb/,/ddd/p'
        |
aaa        
bbb     bbb
ccc     ccc
ddd     ddd
eee        
aaa        
bbb     bbb
ccc     ccc
ddd     ddd
eee        
```





cat: ファイル内容を連結して出力

```
cat [OPTION]... [FILE]...

cat -n    # 行番号をつける
cat -v    # 非表示文字を ^- や M- をつけて出力する。でも見づらい。日本語出ない。
```

head: ファイルの先頭部分を出力

```
head [OPTION]... [FILE]...
    # デフォルトは各ファイルの先頭10行を出力する。
    # 複数ファイルの場合はファイルヘッダも挿入される。

    -n 20   
    --lines=20
	先頭から20行を出力。
	マイナスの場合(-n -20)は、末尾20行の前まで出力。
	-n -0 は、ファイル全体を出力。
    -c 20
    --bytes=20
	先頭から20バイト出力。末尾bは512B単位、kは1KB単位、mは1MB単位。
	マイナスの場合は、末尾から20バイトの前まで出力。
    
    -q  ファイルのヘッダを出力しない
```

tail: ファイルの末尾部分を出力

```
tail [OPTION]... [FILE]...
    # デフォルトは各ファイルの末尾10行を出力する。
    # 複数ファイルの場合はファイルヘッダも挿入される。

    -n 20   
    --lines=20
	末尾20行を出力。
    -n +20   
	先頭から20行目以降(20行目も含む)を出力
	
    -c 20
    --bytes=20
	末尾から20バイト出力。末尾bは512B単位、kは1KB単位、mは1MB単位。
    -c +20   
	先頭から20バイト目以降(20バイト目も含む)を出力
	

    -f   一旦EOFに到達しても終了せず続きを待ち続ける
```

sedで

```
# 11行目～20行目までを出力。
sed -n '11,20p'

# マッチした行以降を抜き出す
sed -n '/aaa/,$p'

# re1にマッチした行から、次にre2にマッチする行まで、(両端行含む) を処理する。それが複数回あれば全部。
# re1にマッチする行がなければ、全く処理されない。
# re2にマッチする行がなければ、最終行まで。
sed -n '/bbb/,/ddd/p'

# N行おきに出力。
sed -n '0~3p'    # 3で割ってあまりが0の行を出力
```

## マッチした行だけ表示

→ grep


## 複数行を1行にまとめる

sed Nコマンドの動作 （次の行を読み込んで、パターンスペースに追加）【Linuxコマンド】 : morituriのブログ
http://blog.livedoor.jp/morituri/archives/52036613.html


```
# 2行を1行にまとめる (カンマで連結)
sed 'N;s/\n/,/g;'

# 3行を1行にまとめる (カンマで連結)
sed 'N;N;s/\n/,/g;'
```

sed の N コマンドは、次の行を読み込んで、パターンスペースに追加。



## 特定の条件でカラムを抜き出す

特定のカラムを抜き出す

```
awk '{print $2,$1}'          # 2カラム目,1カラム目の順で出力。タブ区切り
awk -F ',' '{print $2,$1}'   # 入力ファイルのカラム区切り文字を指定で、同上
```

行の中の正規表現にマッチした部分を抜き出す

```
echo $input | perl -nle 'if(/.feserver(\d+)/){ print $1 }'

echo $input | sed -E 's/^.*\.feserver([0-9]+)\..*$/\1/'
    行頭から行末までマッチさせないと、だめ (置換だから)。
    マッチしない行はそのまま出力されてしまう。

echo $input | grep -E -o '\.feserver([0-9]+)\.'
    カッコの部分だけではなく、パターン全体を表示する
```

## カラムを整形する

各行を1要素として指定の全体幅に収まるように整形する。まず縦に並ぶ。
(ls の結果と同じかも。)

```
cat input.txt | column [-c <ページ幅>]

入力:
red aka
blue ao
green midori
white shiro
black kuro

出力(-c 50):
red aka		green midori	black kuro
blue ao		white shiro
```

既に空白でカラムが分かれているものを整形する。

```
cat input.txt | column -t [-s <デリミタ>]

入力:
red aka
blue ao
green midori

出力:
red    aka
blue   ao
green  midori
```


linux の column コマンドだと、
`--table-right` といったオプションがあって右寄せができたりするのだが、
Mac の column コマンドはない。Homebrew でも入れられるものはないっぽい。


## sort, uniq

### ソートしないで重複行を削除する

```
awk '!a[$0]++' file
```

- `a` は適当な名前の連想配列
- `$0` は行全体
- 条件: `a[$0] == 0` のときだけ
- 出力は省略されているので、`{print $0}` と同義。行全体を出力

サイズが巨大なものの、行のバリエーションが少ないときに有効。

### ソートしないで、出現数をカウントする

```
awk '{a[$0]++} END {for (k in a){print k":"a[k];}}'
```

## grep 


マッチの前後の行も表示
```
-B NUM     マッチした行の前 NUM 行も出力する (Before)
-A NUM     マッチした行の後 NUM 行も出力する (After)
-C NUM     マッチした行の前後 NUM 行も出力する (Context)

--group-separator=SEP    グループの区切り(＝出力されていない部分があることを示す)を指定。
                         デフォルトは --
--no-group-separator     グループの区切りをつけない
```

## wc 

## sed

参考

- [Man page of SED](https://linuxjm.osdn.jp/html/GNU_sed/man1/sed.1.html)

書式、オプション

```
sed 'スクリプト' [入力ファイル]...
sed -e 'スクリプト' -e 'スクリプト' ... [入力ファイル]   # 複数のスクリプト
sed -f スクリプトファイル [入力ファイル]...

    -n    自動出力しない。
    -r    正規表現を拡張正規表現を使う

    -i  --in-place   既存のファイルを上書き更新
```

コマンド

```
p     出力

s/foo/bar/

Q     これ以上入力を処理せず、直ちに終了する
```

アドレス範囲

```

```

典型的なケース

```
# foo を bar に出力
sed 's/foo/bar/g' 
```

## 複数ファイルの中身をまとめて置換

```
find . -type f -exec sed -i 's/DadControlAccount/DadControlDomainDiffer/g' {} +
```

## q

csv などを SQL でアクセスできる。
