シェルスクリプト

```
if [ 条件 ] ; then
    ...
fi
```

testコマンド

    ファイル系
    -e File   存在すれば True


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

