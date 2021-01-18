# シェルスクリプト

## リダイレクト

### ヒアドキュメント

コマンドへの標準入力となる。
(cat だとあんまりうれしくないけど)

```
cat << EOS   # EOS が単独で出てくる行までを入力内容とする
hoge
fuga
piyo
EOS          # 行頭から、前後に空白なども含んではだめ。

cat << EOS   # ""で囲った場合と同様の展開
cat << 'EOS' # ''で囲った場合と同様の展開(つまり、展開しない)

応用
cat << EOS myfile.txt > out.txt
...
EOS

    ↑この場合、コマンドライン引数とファイルディスクリプタどうなる？
```

基本的にインデントには対応していないので、普通に使うとインデントが崩れて読みにくい。

bash であれば、`<<-` を使うことで、
ヒアドキュメント中の行頭のハードタブを除いて出力してくれる。
(ただ、空白でなくタブなので、少々扱いづらい)

```
cat <<- EOS
>---    aaa
>---        bbb
>---EOS
↓
    aaa
        bbb
```

この方がいいかも

```
    cat << ____EOS | sed -E 's/^[[:space:]]+//' 
       hogehoge
       fugafuga
       aaaaaaaa
____EOS
```


## 終了ステータス・制御構造・条件分岐・ループ

TODO この辺、man bash にしたがって、PIPELINE, LISTS, ... のように整理したい。


### 終了ステータス

環境変数 `$?` に格納される。0～255。
(ただし128+n はシグナルn番で終了したとき用らしい)

- 0: 成功。TRUE
- 非0: 失敗。FLASE

```
true    # 常に成功(0)を返すコマンド
:       # 常に成功(0)を返すコマンド
false   # 常に失敗(1)を返すコマンド

! command args...  # commandの実行結果の否定を返すコマンド
```

```
cat hoge.txt        # 単一のコマンドは、その結果

output=`false`      # バッククオートでの変数代入時は、その中の終了ステータス。
                    # この場合 1
set output=`false`  # ただし set,export,local をつけると、setコマンドということになるので、
                    # この場合 成功(0)になってしまう。！注意！

```

パイプは基本的に前段が失敗したとしても、後段は必ず動く。
(逐次実行ではなく、並列で起動しているから)
パイプ連結のステータスコードは、必ず最後の段のコマンドの実行結果になる。

```
echo "hoge" | grep "hoge"    # grep の結果、マッチする行が存在したので $?=0   
echo "hoge" | grep "fuga"    # grep の結果、マッチする行がなかったので $?=1
cat not_exist.txt | wc -l    # cat がエラーだが、wc は実行され $?=0。STDERRに 0。
```

bash, zsh には、パイプの格段の終了ステータスを取得する変数が用意されている。
TODO



### 制御構造基本

if は後のコマンドの終了コードが 0:true, 非0:false で分岐する。
```
if [ 条件 ] ; then
    ...
elif [ 条件 ] ; then
    ...
else
    ...
fi
```

`&&`, `||` で連結

- && は前がTRUE(0)のときだけ、次のコマンドを実行
- || は前がFALSE(非0)のときだけ、次のコマンドを実行
- どちらも全体の終了ステータスは、最後に実行されたコマンドの結果

```
```


for は、in の後を１つずつ変数に入れて処理を実行。
中で continue, break コマンドが使える。
```
for var in aaa bbb ccc ddd ; do
    ... $var ...
done

for f in `ls -1 *.txt` ; 
for i in `seq 1 10` ; 
for i in {1..10} ;          # zshでは使える
```


while。条件を満たしている間は、中を繰り返し実行する。
中で continue, break コマンドが使える。
```
while [ 条件 ] ; do
    ...
done
```



### testコマンド、`[` コマンド

引数を評価して、終了コードで 0:TRUE, 1:FALSE を返す。

```
# 典型的な使い方
if [ $a -eq 100 ] ; then
    ...
else
    ...
fi
```

```
    # ファイル系
    -e File   存在すれば True (exists)

    -f File 	存在し，通常のファイルであれば真を返す (file)
    -d File 	存在し，ディレクトリであれば真を返す   (directory)
    -h File，-L File 	指定したファイルが存在し，シンボリック・リンクであれば真を返す
    -p File 	存在し，名前付きパイプであれば真を返す (pipe)
    -S File 	存在し，ソケットであれば真を返す       (socket)
    -b File 	存在し，ブロック・デバイスであれば真を返す (block)
    -c File 	存在し，キャラクタ・スペシャル・ファイルであれば真を返す (character)

    -r File 	存在し，読み取り可能であれば真を返す (read)
    -w File 	存在し，書き込み可能であれば真を返す (write)
    -x File 	存在し，実行可能であれば真を返す     (eXecute)
    -u File 	存在し，パーミッションにセット・ユーザーIDが付いていれば真 (user)
    -g File 	存在し，パーミッションにセット・グループIDが付いていれば真 (group)
    -k File 	存在し，パーミッションにスティッキ・ビットが付いていれば真 (???)

    -O File 	存在し，ファイルの所有者が現在実行しているユーザーであれば真を返す (Owner)
    -G File 	存在し，ファイルのグループが現在実行しているユーザーであれば真を返す (Group)

    -s File 	存在し，ファイル・サイズが1以上であれば真を返す (size)
    -t File 	指定したファイルが端末でオープンされていれば真を返す (terminal?)

    File1 -nt File2 	修正時刻が新しければ真を返す (newer than)
    File1 -ot File2 	修正時刻が古ければ真を返す (older than)
    File1 -ef File2 	デバイス番号とiノード番号が同じであれば真を返す (equal file?)

    # 文字列系
    文字列      指定した文字列が1文字以上であれば真を返す
    -n 文字列 	指定した文字列が1文字以上であれば真を返す
    -z 文字列 	指定した文字列が0文字（何もない）状態であれば真を返す

    文字列1 = 文字列2 	文字列1と文字列2が同じであれば真を返す
    文字列1 != 文字列2 	文字列1と文字列2が違ければ真を返す

    # 数値比較系
    数値1 -eq 数値2
    他に -ne -lt -le -gt -ge

    # 論理演算
    ! 条件式 	           NOT
    条件式1 -a 条件式2 	   AND
    条件式1 -o 条件式2 	   OR
```



### seq

TODO




### set -e オプション

これをつけないと、途中のコマンドがエラー(戻り値が非0)になっても、
シェルスクリプトは進む。

これをつけると、エラーになったところでシェルスクリプトは終了し、
exitcodeは、最後のコマンドの exitcode になる(当然非0)。

man bash より

> パイプライン(単一のコマンドも含む)、サブシェル、
> 波括弧で囲まれたコマンドリストのうちのどれか、
> が、非0で終了した場合、シェルスクリプトの処理をそこで打ち切る。
> 
> ただし失敗したコマンドが以下の場合は、例外的に打ち切らない。
> 
> - while,until の直後にあるコマンドリストの一部
> - if,elif に続く条件チェックのコマンド
> - `&&`, `||` で連結されるコマンドで、末尾以外のコマンド
> - パイプラインの最終段以外のコマンド
> - `!`コマンドで反転されることになっているコマンド


```
# 単純なコマンド
true
false                   # エラー終了
cat 存在しないファイル  # エラー終了

# 連結されたコマンド (エラーになったところで終了)
echo "one" ; false ; echo "three"     # false のところまで

# パイプは、最後のコマンド以外は無視される。
# パイプ連結は全体で１つのコマンド扱い。終了コマンドは最後のコマンド。
echo "one" | grep "hoge"  | wc -l       # 中段のgrep が非0だが、wc が実行され、次に進む
echo "one" | grep "one"  | grep "fuga"  # 末尾の grep が非0なので、パイプ全体として非0。エラー終了

# バッククオート。コマンド実行結果の代入
# バッククオートの中の実行結果が代入文の実行結果
output=`echo hogehoge`
output=`cat unknown_file`              # エラー終了
output=`echo "one" | grep "one"`
output=`echo "one" | grep "hoge"`      # エラー終了
output=`echo "one"; echo "two"`
output=`echo "one"; false ; echo "two"`   # エラー終了
# ただし、set や local コマンドにすると、エラーにはならない。中身は空
set output=`echo "one"; false ; echo "two"`
local output=`echo "one"; false ; echo "two"`

# 条件で連結
true && echo "hoge"     # echo は実行されて、この文の $? は 0。処理続行
false && echo "hoge"    # echo は実行されず、この文の $? は 1 だが、処理は続行
true || echo "hoge"     # echo は実行されず、この文の $? は 0。処理続行
false || echo "hoge"    # echo は実行されて、この文の $? は 0。処理続行

false || false          # エラー終了
true || false           # 正常。


# if文




# 関数の中でも `-e` は有効。returnではなく 全体がexitしてしまう
# (/bin/sh と bash で確認)
function sub(){
    echo "sub start"
    false
    echo "sub end"
}
echo "main start"
sub
echo "main end"
    === 結果===
    main start
    sub start

# subshell の中でも `-e` は有効。全体がexitしてしまう。
# (/bin/sh と bash で確認)
echo "main start"
(
    echo "subshell start"
    false
    echo "subshell end"
)
echo "main end"
    === 結果===
    main start
    subshell start


# 関数の結果
function sub() {
    return 1
}
echo "main start"
sub                      # ここで終了する
echo "main end"

# サブシェルの結果
echo "main start"
(
    exit 1               # ここで終了する。 
)
echo "main end"
```




## 変数展開

### 変数名

- 変数名に使える文字列は、[A-Za-z0-9_] 。ただし先頭は数字以外。
- 大文字小文字は区別される。

### 位置パラメータ

TODO

位置パラメータを上書きする方法
```
set -- 111 222 333
```

### 空白を含む扱い

```
VALUE_B="hoge     fuga"
$VALUE_A=$VALUE_B         # 空白5つがちゃんと保持される。
```

TODO どういうとき空白が詰まる？


### デフォルト値 +α

```
# なければ代わりにデフォルト値を返す
${FOO-aaa}   # FOOが未使用であれば、 aaa 値を返す (代入はしない)
${FOO:-aaa}  # FOOが未使用か空文字列であれば、 aaa 値を返す (代入はしない)

# 上に加えて、代入もしてしまう
${FOO=aaa}   # FOOが未使用であれば、FOOにaaaを代入し、aaaを返す。
${FOO:=aaa}  # FOOが未使用か空文字列であれば、FOOにaaaを代入し、aaaを返す。


# ある場合は代わりにデフォルトの値を返す
${FOO+aaa}   # FOOが未使用であればそのままの値。それ以外がセットされていれば aaa を返す
${FOO:+aaa}  # FOOが未使用か空文字であればそのままの値。それ以外がセットされていれば aaa を返す

if [ -n "${HOGE+x}" ]; then ...   # HOGEが未使用であることのチェック？意味あるか？


# ない場合はエラー終了
${FOO?FOO is not set}   # FOOが未使用であれば 'FOO is not set' を表示してエラー終了
${FOO:?FOO is not set}  # FOOが未使用か空文字であれば 'FOO is not set' を表示してエラー終了

% echo ${HOGE:?not set}
zsh: HOGE: not set

% echo ${HOGE:?}        # メッセージが指定されていない場合、デフォルトのメッセージが使われる
zsh: HOGE: parameter not set
```


### Word-Splitting 空白や改行を含む変数展開

/bin/sh, bash と zsh で、変数展開時の区切り文字の扱いが異なる。

```
output=`ls -l`    
    # 変数には改行文字も含めてそのまま入っている 
    # (最後の最後の改行だけは抜かれているかも。
echo "$output"
    # 変数全体が1つの引数として渡される。つまり echo の引数の個数は1。
    # よって、結果は複数行の形のまま出力される
echo $output
    # /bin/sh, bash は、展開時に区切り文字(空白・改行など)によって
    # 複数の引数に分けられる。echo の引数はたくさんになる。
    # よって、echoの結果、間に空白文字１つが挟まって1行で出力される。
    #
    # zsh は、この場合でも、分割しない。"$output" と同じく複数行が出力される。
    # zsh で bash相当の展開をしたい場合は $=output とやる。
```

参考
- bash: https://www.gnu.org/software/bash/manual/bashref.html#Word-Splitting


## 算術演算

### シェルの置換で (Arithmetic Expansion)

シェルの機能での算術演算は以下の形がある

- `((expression))` : 式の結果が
- `$((expression))` : 算術式を評価してその結果に置換



詳しくは man bash で "Arithmetic Expansion" および "ARITHMETIC EVALUATION"。

整数だけでなく、小数でもOKっぽい？？？一部？？？

10進数表現だけ？？

```sh
$(( ...算術表現... ))

# 算術展開の中では変数展開の`$`は不要
a=5
b=3
c=$((a + b))   # 空白をあけているが、あけなくてもOK。
echo $c        # → 8

# カッコ含め複雑な式も書ける
$(((10 + b / 2) * 3 + c ** 2 ))
```

算術式表現

使える演算子と結合順 (man bash から)
```
演算子
   id++ id--
	  variable post-increment and post-decrement
   ++id --id
	  variable pre-increment and pre-decrement
   - +    unary minus and plus (単項のプラスとマイナス。いわゆる符号)
   ! ~    logical and bitwise negation
   **     exponentiation べき乗
   * / %  multiplication, division, remainder
   + -    addition, subtraction
   << >>  left and right bitwise shifts
   <= >= < >
	  comparison
   == !=  equality and inequality
   &      bitwise AND
   ^      bitwise exclusive OR
   |      bitwise OR
   &&     logical AND
   ||     logical OR
   expr?expr:expr
	  conditional operator
   = *= /= %= += -= <<= >>= &= ^= |=
	  assignment
   expr1 , expr2
	  comma

数値
    123    # 十進数
    0777   # 先頭が0である定数は 8進数
    0xff   # 0x, 0X 始まりは 16進数
    5#22   # 5進数で10。→ 12

```


## getopt

参考
- [bash によるオプション解析 - Qiita](http://qiita.com/b4b4r07/items/dcd6be0bb9c9185475bb "bash によるオプション解析 - Qiita")

だいたい以下の方法がある

- ビルトインコマンドの `getopts` を使う。 → ロングオプション使えない
- コマンド版の `getopt`
    - gnu版(Linuxに最初から入っているのはこれ)。 → ロングオプションも使えるし、空白など含んでもきちんと扱える。
    - 従来版(MacOSXに最初から入っているのはこれらしい)。 → 貧弱で、いろいろ制限がある。
- 自前で処理する。 

基本的に gnu版の getopt が入っているなら、それを使うのが一番よい。

### gnu版 getopt

拡張版や enhanced版とも呼ばれる。

- getopt (enhanced) のマニュアルの日本語訳
    - [getoptのヘルプ・マニュアル／リナックスコマンド](http://www.linux-cmd.com/getopt.html "getoptのヘルプ・マニュアル／リナックスコマンド")

拡張版であれば、引数に空白を含んでいても適切に扱える。

コマンドの書式

```
(従来版の動作になる)
getopt optstring parameters             

(拡張版の動作になる)
getopt [options] [--] optstring parameters
getopt [options] -o|--options optstring [options] [--] parameters
```

拡張版のサンプル
```
#!/bin/sh

function usage_and_exit() {
    local exitcode="$1"
    echo "Usage: $0 [-a] [-d dir] item..." >&2
    exit "$exitcode"
}

if !  OPT=`getopt -o 'ad:' -l 'alpha,delta:' -- "$@"`
then
    usage_and_exit 1   # 指定外のオプションが入力された場合もここ。
fi
eval set -- "$OPT"     # 従来版では setに渡していただけだが、拡張版では eval する。

# debug ここから
i=1
for a in "$@" ; do
    echo "[$i]:$a"
    i=$((i + 1))
done
# debug ここまで

while true
do
    case "$1" in
        -a | --alpha) FLAG_A=1
            shift
            ;;
        -d | --delta) VALUE_D=$2
            shift 2     # 引数とるやつは shift 2
            ;;
        --) shift
            break
            ;;
        *)
            echo "Internal error!" >&2  # 基本ここには入ることないはず。
            exit 1
            ;;
    esac
done


echo "FLAG_A=$FLAG_A"
echo "VALUE_D=$VALUE_D"
echo "\$#=$#"
i=1
for a in "$@" ; do
    echo "[$i]:$a"
    i=$((i + 1))
done
```

従来版のサンプル(ロングオプション使えない。空白などがきちんと扱えないので注意！)
```
#!/bin/sh

function usage_and_exit() {
    local exitcode="$1"
    echo "Usage: $0 [-a] [-d dir] item..." >&2
    exit "$exitcode"
}

set -- `getopt 'ad:' "$@"`
if [ $? -ne 0 ] ; then
    usage_and_exit 1
fi

# debug ここから
i=1
for a in "$@" ; do
    echo "[$i]:$a"
    i=$((i + 1))
done
# debug ここまで

for OPT in "$@"
do
    case $OPT in
        -a) FLAG_A=1
            shift
            ;;
        -d) VALUE_D=$2
            shift 2     # 引数とるやつは shift 2
            ;;
        --) shift
            break
            ;;
    esac
done


echo "FLAG_A=$FLAG_A"
echo "VALUE_D=$VALUE_D"

echo "\$#=$#"
i=1
for a in "$@" ; do
    echo "[$i]:$a"
    i=$((i + 1))
done
```



### getopts

ビルトインコマンドなので、早い？ 空白を含んでいても扱える。
ロングオプションは使えない。

コマンド書式
```
getopts optstring name [args]
```



## ユニットテスト、単体テスト

shunit2 というのと bats というのがメジャーっぽい。

shunit2 の Assertion の書き方がクオートしないといけないのが少し気持ちわるいのと、
bats の方が、表示が洗練されているし、コマンドの出力・exitcodeの取得も楽そう。

### bats

ドキュメント: [sstephenson/bats: Bash Automated Testing System](https://github.com/sstephenson/bats)

```sh
#!/usr/bin/env bats

@test "addition using bc" {
  result="$(echo 2+2 | bc)"       # 中括弧の中の各行が全てassertion。/bin/sh -e の様に失敗するとそこで止まる。
  [ "$result" -eq 4 ]
}

@test "addition using dc" {
  result="$(echo 2 2+p | dc)"
  [ "$result" -eq 4 ]
}

# エラーになるような動作をチェックしたい場合は runコマンドを使う
# STDERR も含め $output に入るっぽい。
@test "invoking foo with a nonexistent file prints an error" {
  run foo nonexistent_filename
  [ "$status" -eq 1 ]
  [ "$output" = "foo: no such file 'nonexistent_filename'" ]
}
```





## カレントディレクトリ系

### カレントディレクトリとディレクトリスタック

イメージとしてはこんな感じ。
```
% dirs -v
0       dirA      # +0 -3 <-- cwd 。 スタックトップが cwd 。
1       dirB      # +1 -2 
2       dirC      # +2 -1
3       dirD      # +3 -0
```

スタックのトップ、つまり一番上で見えている部分が cwd というイメージ。

### cd

cd は cwd を変更する。言い換えると ディレクトリスタックのトップを変更する。スタックの長さは変わらない。

```
cd         # $HOMEに cwd を変える
cd -       # 直前にいたディレクトリに cwd を変える
cd dir1    # dir1 に cwd を変える
           # スラッシュで始まる場合は絶対パス
	   (cdpathに `.` が含まれていない場合) cwd直下の dir1、cdpathを順に
	   (cdpathに `.` が含まれている場合) cdpath直下のdir1を順に
cd old new   # cwd の一部を置換する。 (oldの部分をnewに置換する)    (zshのみ？)

```

### pushd,popd,dirs

```
pushd dir1        # スタックに dir1 を積む。結果 cwd が dir1 になる。 スタックの長さは +1 。
pushd             # スタックの先頭２つを入れ替える。  スタックの長さは変わらない。
                  # スタックが空だった場合は、pushd $HOME の動作になる。スタックの長さは +1 。

pushd {+|-}n      # ディレクトリスタックを(nがトップに来るように)ローテートする

popd              # ディレクトリスタックの先頭を消す。cwdは新しい先頭のものになる。スタックの長さは -1
popd {+|-}n       # ディレクトリスタックのn番目を消す。(popd +0 以外では)cwdは変わらない。スタックの長さは -1

cd {+|-}n         # ディレクトリスタックのn番目を取り出し、cwd(つまり先頭)を書き換える。スタックの長さは -1 

dirs
    -c  クリア
    -v  縦表示(番号付き)
    -p  縦表示(番号なし)

dirs dir1...     # スタックをクリアし指定したディレクトリで書き換える。最後にcwdを乗せる。
```


# ファイル系

## ls 

```
    -S     ファイルサイズでソート

    --full-time   ファイルの時刻の秒も表示
```

## tree

```

--charset=C   罫線をASCII文字で書く。
```


## find 

更新時刻関係

`-mtime` , `-atime` , `-ctime` (日数指定)

- `-daystart` をつけない場合、24時間単位。now から24時間ごとに区切る。
    - 直近24時間 を 0 日目、そこから24時間ごとに N 日目 としていく。
- `-daystart` をつけた(前に置いた)場合、暦日単位。0時で区切る。
    - now を含む暦日を 0日目、そこから暦日ごとに N 日目 としていく。
- `-daystart` の効果はそれより後ろにしか効かない。なので前に置く。

```
N   --- N日目のみ
-N  --- N日目より若いファイル(N日目を含まない)
+N  --- N日目より古いファイル(N日目を含まない)
```

例
```
-daystartなし
                                                                8時
                                                                now
                                                                 |
0時         0時         0時         0時         0時         0時  V      0時
-|---+-------|---+-------|---+-------|---+-------|---+-------|---+-------|
     |   4日前   |   3日前   |   2日前   |   1日前   |   0日前   |
<------(+2)----------------->|<---(2)--->|<--------(-2)--------->


-daystartあり
                                                                8時
                                                                now
                                                                 |
0時         0時         0時         0時         0時         0時  V      0時
-|---+-------|---+-------|---+-------|---+-------|---+-------|---+-------|
             |   4日前   |   3日前   |   2日前   |   1日前   |0日|       |
<--------------(+2)----------------->|<---(2)--->|<----(-2)------>
```

`-mmin` , `-amin` , `-cmin` (分単位) 

now から60秒単位。

`-daystart` と組み合わせることもでき、その場合は、その日の24:00:00が基準になる。
(あまり使わないかも)

```
-newer <file>                # あるファイルのmtimeより新しいもの。 -anewer, -cnewer もある

-newermt '20150806 10:59'    # date の -d オプションの形式
-newermt '2016-04-25'        # こうでもよい。省略したところは 0 が埋まる
! と組み合わせて、範囲指定もできる。
-newermt '20150806 10:59' ! -newermt '20150806 14:00'
```

というか、結構難しいから、必ず -ls で確認しろ。


-ls は後ろに書かないとダメ



# バイナリ操作

od
hexdump
xxd



1バイトずつ16進表記に変換して出力するスクリプト

```perl
#!/usr/local/bin/perl

use strict;
use warnings;

while(1) {
    my $input;
    read(STDIN, $input, 1) || last;
    my $byte = unpack("C", $input);
    printf "%02x ", $byte;
}
print "\n";
```

# 時刻

```
date -d STRING は display つまり表示
    +FORMAT が出力のフォーマット
date -s STRING は set つまり設定

# 今の時刻を表示
date                   # Fri Sep 30 13:31:25 JST 2016

# 指定時刻を表示
date -d '2015/04/25'
date -d '30 days'      # 30日後。day でも days でもいい。'30days' でもいい。
                       # month, year, hour, minute, second
                       # month は 月の末日の方は注意
date -d '1 day ago'    # 1日前。ago をつけると過去方向
date -d '-3 days'      # マイナスも過去方向
date -d tomorrow       # tomorrow, yesterday, week, fortnight

date -d '2013/09/04 12:17:00'  # 日時で指定
date -d '@1382282400'  # unixtimeで指定

date -d '2015/04/25 1 month'   # 組み合わせ。

# 特定のフォーマットで出力 (-d STRING との組み合わせも可)
date +%s               # Unixtime で出力
date +%Y%m%d-%H%M%S    # YYYYMMDD-HHMMSS 形式で出力


# 標準入力を変換 (各行を -d 指定して実行した効果)
echo '2016/01/01' | date -f -
```

## ntp

```
# 時刻が大幅にずれたときは、ntpd が時刻合わせを諦めてしまうので、
# 以下で強制的に同期させる
cat /etc/ntp.conf     # ntp サーバのIPアドレスを確認
sudo ntpdate NTPサーバ

# ntpd がいつの間にかいなくなったときは、以下で再開
sudo /etc/init.d/ntpd restart
ntpq -p     # 確認
```


# 虎の巻

## true になるまで繰り返し実行

運用のスクリプトなどで、最大で指定時間まで、
一定時間ごとにコマンドを実行し、条件が満たされるまで待つ。

```
function wait_until_true() {
    # usage: wait_until_true max_wait_ces command
    local max_wait_sec=$1
    shift

    local deadline
    local now
    deadline=`date +%s -d "$max_wait_sec secs"`

    echo -n "Waiting for '$@' " >&2
    sleep 1
    while true ; do
        echo -n "." >&2
        if eval "$@" ; then
           echo >&2
           return 0
        fi
        sleep 1

        now=`date +%s`
        if [ $now -gt $deadline ] ; then
           echo >&2
           return 1
        fi
    done
}
```

# 未整理



