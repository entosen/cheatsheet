

クラスを探す  Ctrl+N


# コード編集

```
画面分割 --- :vsp 。Window > Editor Tabs > Split Vertically 。 
```

# git関連

「9:Version Control」というので操作できる。

```
git status, add, commit, diff : 
    "Local Changes"タブ

git log, Network Graph : 
    "Log"タブで見れる。

git fetch : VCS > Git > Fetch
git push : VCS > Git > Push
git pull : VCS > Git > Pull

git branch, checkout, fetch, push, merge は？
```


# sbt関連

```
sbt compile             --- Build > Make Project  (Ctrl+F9)
そのファイルだけビルド  --- Build > Compile...    (Ctrl+Shift+F9)
sbt run

sbt test
    --- いまのところ、左カラムのProjectタブから
        テストコードのソースファイルを選択し、右クリックから Run 。
	2回目以降は、右上のRunボタンでいける。

sbt doc  --- Tools > Generate Scaladoc
```

それ以外のsbtタスクの実行
Run ＞ Edit Configurations ＞ プラスボタン ＞ SBT


依存ライブラリの追加  
build.sbt に追記したら(そのままではだめで)、
右縁の"SBT"タブを開き、"Refresh" を押す。



# 設定

- 行番号を常に表示
  - 「settings」→「Editor」→「General」「Appearance」の「Show Line Numbers」
- (新規作成ファイルの)改行コードを Unix に。
  - Setting ＞ Editor ＞ Code Style ＞ Line separator (for new file) を "Unix and OS X" に。
  - 合わせて、以下のgitの設定もしておくといい。

```
git config --global core.eol lf 
git config --global core.autocrlf false
```


# 編集

## 置換

改行に置換(というか行を分割する)  

- IdeaVim では s/,/\r/ など、 \r が改行扱い。
- IJの置換で、"Regex" にチェックをいれた状態で、"\n" でいける。

# TODO

カーソル位置を表示するには？ 
    → 出てたわ
    でもこれ、半角全角考慮しない文字数っぽいので、半角文字数換算で出してほしい


