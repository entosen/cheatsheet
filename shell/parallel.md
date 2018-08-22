# GNU parallel

## インストール

```
# 会社のインストールコマンドで
xinst install -br test gnu_parallel (古い。1.1.0 が 20151022 相当)

# Homebrew
brew install parallel

# Cygwin 
TODO
```


## 並列実行するジョブの指定

dry-run
```
--dry-run オプションでどういう風に実行されるか確認できる。
--dry, --dryrun でも可。
```

並列実行する引数リストの指定
```
parallel echo ::: aaa bbb ccc
    → echo aaa
       echo bbb
       echo ccc

parallel ::: 'ls bin' 'ls libs'   # コマンド自体もリストとしてもよい
    → ls bin
       ls libs

# 複数の ::: を渡すと、その掛け合わせ
parallel echo ::: aaa bbb ccc ::: yyy zzz
    → echo aaa yyy
       echo aaa zzz
       echo bbb yyy
       echo bbb zzz
       echo ccc yyy
       echo ccc zzz

parallel wc -l :::: argfile(s)  # ファイルから入力(1行ごとに並列実行)

parallel wc -l < argfile    # 標準入力から(リダイレクト)
ls -1 | parallel wc -l      # 標準入力から(パイプ)
parallel -a argfile wc -l   # 指定したファイルから



```

引数の置き換え
```
parallel 'find {} -name "README*"' ::: ~/vendor/julia ~/vendor/vector
parallel 'echo {1} {2}' ::: aaa bbb ccc ::: xxx yyy

    {1},{2},...   --- N番目(Nカラム目)の引数

    {.}   --- 拡張子を除いた引数
    {/}   --- ファイル名だけを抽出
```




## 出力


出力するタイミング

```
--group  (デフォルト) 各ジョブの出力は一旦バッファされ、ジョブ終了時にすぐに出力。
         その際は、stdout、stderr の順。

-k       デフォルトと似ているが、ジョブが終了した順ではなく、入力の順で出力。

--line-buffer   行単位で即座に。(CPUを他より多く使う)。行が交じることはない。
--lb

--ungroup  バッファしない。即座に出力。
-u         各ジョブの出力は(行の途中でさえ)ごちゃまぜになる。
           --tag との併用不可。
```

出力に付加
```
--tag     各出力行の先頭にどのジョブから出たかを出力。
          -u と併用付加。
```

