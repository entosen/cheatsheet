シェルスクリプト

```
if [ 条件 ] ; then
    ...
fi
```

testコマンド

引数を評価して、終了コードで 0:TRUE, 1:FALSE を返す。

```
# 典型的な使い方
if [ $a -eq 100 ] ; then
    ...
else
    ...
fi



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

    -s  進捗とエラーを表示しない

    -i  レスポンスヘッダを表示する
    -v  通信のやり取りを詳細に表示する

    データの指定。ファイル名を指定する場合は @ファイル名
	--data <data>                 
	--data-binary <data>   
	--data-urlencode <data>   
```

