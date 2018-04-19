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


## HTTP負荷テストツール

### vegeta

https://github.com/tsenart/vegeta

インストール

- https://github.com/tsenart/vegeta/releases から環境にあったバイナリをダウンロード
- 解凍・展開
- 必要なら PATH が通ったディレクトリなどに入れる


使い方

負荷をかける前の要チェックポイント

- `ulimit -a`
    - file descriptor数 (file descriptors) <--- 1プロセスあたりっぽい
    - プロセス数 (processes) 

コマンドの種類

```
# 負荷をかける (vegeta attack)
echo "GET http://localhost/" | ./vegeta attack -rate=50 -duration=5s > result.bin

# 結果をレポート (vegeta report)
vegeta report < result.bin

# 結果をダンプ (vegeta dump)
vegeta dump < result.bin
```

詳細は、開発元のgithub見て。

複数台で同時に負荷をかける方法

- かけたいQPSを台数で割る
- 各ホストで vegeta attack で上記QPSで負荷をかける。結果をファイルに保存
- 各ホストから結果のファイルをscpしてくる
- vegeta report で -inputs をカンマ区切りで全ホスト分指定



