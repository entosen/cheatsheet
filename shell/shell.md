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

