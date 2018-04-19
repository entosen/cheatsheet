# ネットワーク

## wget

```
wget -nv -O - --save-headers 'http://entosen.tokyo:8080/status.html'
    -q    エラー時も何も出さない
    -nv   エラー時にはそれを出力する
    なし  進捗バーのようなものを出す

# POST
wget -nv -O - --save-headers --post-data 'data.......' 'http://entosen.tokyo:8080'
```

## curl 

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


