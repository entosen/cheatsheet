# 表示

ソースコードタブの色

  文字色白: 変更なし
  文字色青: 変更あり
  文字色緑: 新規追加
  背景灰: mainコード
  背景緑: テストコード



# ショートカット

前提  
Windows上で、IdeaVim を使っているので、それ前提で。

## 画面全体の表示

ツールWindows
  Alt+1 で Project
  Alt+2 で Favorites
  Alt+3 で Find 
  ... など
  番号が出ているのでわかる。


## 検索(Find)と移動(Navigate)

現在のファイル内を検索

プロジェクト全体から検索(Unixでいうgrep的な),
    Edit > Find > Find in Path,  Ctrl+Shift+F
    → Alt+3 の Find タブに結果が出る。


クラスを探す  Ctrl+N


## 実行 Run

ファイルをコンパイル
  Projectタブからファイルを選択し、Ctrl+Shift+F9
ファイルを実行
  Projectタブからファイルを選択し、Ctrl+Shift+F10


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

- (scala用) クラスパラメーターの折り返し時、インデントを4に。
  http://kxbmap.hatenablog.com/entry/2015/02/26/031541
  - Settings > Editor > Code Style > Scala > 
      - Other > Alternate Indentation for constructor args and parameter declarationsをチェックして4spacesに
      - Wrapping and... > Method Declaration parameters > Align when multilineのチェックを外す


Editor Tab まわりの設定

- Editor > General > Editor Tabs
  - "Hide tabs if there is no space" は嫌いなので、チェックを外す
  - "Hide file extension in editor tabs" チェックを入れてみる
  - "Mark modified tabs with asterisk" チェックを入れてみる
      - 効いてない？一度ついてもすぐ消えてしまう。
  - "Show tabs in single row" を外してみる
      - これ外して、複数行になっている側のウィンドウに C-W H で移れなくなった...。C-W C-W は効く。
      - IdeaVim に Bug 上がってた。
  	Ctrl-w + h doesn't alway work (window navigation to the left window) : VIM-795
  	https://youtrack.jetbrains.com/issue/VIM-795
  - "When closing active editor" は "Activate most recently opened tab" にしてみる。


# 編集

## 置換

改行に置換(というか行を分割する)  

- IdeaVim では s/,/\r/ など、 \r が改行扱い。
- IJの置換で、"Regex" にチェックをいれた状態で、"\n" でいける。

# TODO

カーソル位置を表示するには？ 
    → 出てたわ
    でもこれ、半角全角考慮しない文字数っぽいので、半角文字数換算で出してほしい


