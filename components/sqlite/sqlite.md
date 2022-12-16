
# SQLite



## スペシャルコマンド

Command Line Shell For SQLite
https://sqlite.org/cli.html


### 出力形式

```
.mode MODE ?TABLE?
.separator COL ?ROW?   # 区切り文字 (デフォルト "|")
.headers on|off        # ヘッダ行を出力するかどうか (デフォルト off)
```

MODE
```
list    区切り文字を挟んで1行で出力 (デフォルト区切りは"|") (デフォルト)
tabs    タブ区切りで出力 (mode list, separator "\t")
csv     カンマ区切りで出力。必要であればダブルクオートで囲う。

column   カラムをそろえて出力 (人が見やすい。ただし内容が省略される場合あり)
    デフォルトの幅は、max(10, カラム名, 1レコード目の値) で決まる。
    .width コマンドでカラム幅を指定できる。(0は上記デフォルトの動作)
	.width 12 6
	マイナス指定は右寄せ

line    カラム毎に行を分けて出力。レコードの区切りに空行。


html    html の <tr>,<th>,<td> 形式で出力
insert  INSERT文として出力
tcl     Tclのlist形式で出力？？？ デフォのseparator が "|" なので注意。

quote   SQLリテラルで出力 (3.16.0 以降 (多分))
    - 文字列はシングルクオート、文字列中のシングルクオートは2つにする
    - blob は16進数表記 x'abcd' 
    - NULL は "NULL"
```




### サンプル

```
.tables               # table一覧
.schema [<table名>]   # tableのschema表示
```
