# シェルスクリプト

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


デフォルト値
```
# なければ代わりにデフォルト値を返す
${FOO-aaa}   # FOOが未使用であれば、 aaa 値を返す (代入はしない)
${FOO:-aaa}  # FOOが未使用か空文字列であれば、 aaa 値を返す (代入はしない)

# 上に加えて、代入もしてしまう
${FOO=aaa}   # FOOが未使用であれば、FOOにaaaを代入し、aaaを返す。
${FOO:=aaa}   # FOOが未使用であれば、FOOにaaaを代入し、aaaを返す。
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




## 未整理


ls 
    -S     ファイルサイズでソート



pushd
popd
dirs
    -c  クリア
    -v  縦表示



# 文字列操作

シェルスクリプトで、正規表現で文字列中の一部を抜き出す

```
echo $input | sed -E 's/^.*\.feserver([0-9]+)\..*$/\1/'
    行頭から行末までマッチさせないと、だめ

echo $input | grep -E -o '\.feserver([0-9]+)\.'
    こんな感じか？ パターンのところだけ出力してくれる
    試していない。
```


# 時刻

```
# 今の時刻
date                   # Fri Sep 30 13:31:25 JST 2016
date +%s               # Unixtime で出力
date +%Y%m%d-%H%M%S    # YYYYMMDD-HHMMSS 形式で出力

# 指定時刻
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

# 標準入力を変換 (各行を -d 指定して実行した効果)
echo '2016/01/01' | date -f -
```

# プロセス

pstree
```
pstree -ap

    引数なしでも、全ユーザーのプロセスを表示してくれる。
    Thread もPIDで管理されているようで、表示してくれる。{ } で囲んで表示。
    -a  起動時のコマンドライン引数を表示
    -p  PIDも表示。
    -l  長く
```

# ネットワーク

wget

```
wget -nv -O - --save-headers 'http://entosen.tokyo:8080/status.html'
    -q    エラー時も何も出さない
    -nv   エラー時にはそれを出力する
    なし  進捗バーのようなものを出す

# POST
wget -nv -O - --save-headers --post-data 'data.......' 'http://entosen.tokyo:8080'
```

curl 

```
curl http://www.example.com/

    -s, --silent                 進捗とエラーを表示しない
    -sS, --slient --show-error   進捗は表示しないが、エラーは表示する (おすすめ)

    -I  レスポンスヘッダだけを出力する。body は出力されない。
    -i  bodyに加えて、レスポンスヘッダを出力する
    -v  通信のやり取りを詳細に表示する(リクエストヘッダ、レスポンスヘッダ、ボディ)

    データの指定。ファイル名を指定する場合は @ファイル名
	--data <data>                 
	--data-binary <data>   
	--data-urlencode <data>   
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
