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
- File > Settings > Editor > File Encodings >
    - Global Encoding, Project Encoding, を UTF-8 に
    - Default Encoding for properties files も UTF-8 に
- File > Settings > Build,Execution,Deployment > Build Tools > SBT
    - VM parameters に `-Dfile.encoding=UTF-8` を追加
    - Use auto-import を OFF に
- File > Settings > Editor > Color & Fonts > Font で、Consolas の 12 に。
- File > Settings > Apperance and Behavior > System Settings > Password
    - Do not save, forget password after restart

- Run > Edit Configuration > Defaults > SBT Task > VM Parameters >
    - `-Dfile.encoding=UTF-8` を追加


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

Right margin まわりの設定

- Editor > General > Appearance > Show right margin にチェック
- Editor > Code Style > Right margin (columns) を 80に。

その他

- ファイル末尾にかならず改行を入れる
    - Editor > General > Other > Ensure line feed at file end on Save にチェック


## code style の設定

> Copying Code Style Settings
> https://www.jetbrains.com/help/idea/2016.1/copying-code-style-settings.html?origin=old_help

code style の設定場所には以下のものがあるようだ

- default: IntelliJ の標準の設定
- Globalのカスタム設定: 名前をつけて保存できる。無意識でも設定を変えると"Default(1)" とかになっているはず。
  実体は `~/.Idea2016/config/codestyles` にある
- Projectの設定: カスタム設定をProjectの設定として保存できる。
  実体はプロジェクトの `.idea/codeStyleSettings`。


scala用設定。
Settings > Editor > Code Style > Scala > 

- クラスパラメーターの折り返し時、行頭からのインデントにする
  - Wrapping and... > Method Declaration parameters > Align when multilineのチェックを外す
- scaladoc の2行目移行の`*`の位置、1行目の1つ目の`*`の位置に揃える
  - ScalaDoc > Use scaladoc indent for leading asterisk のチェックを外す
- import文で `{ NameA, NameB, }` のように波括弧の内側に空白を開ける
  - Spaces > Other > Spaces after open and befor close braces in imports


## IdeaVim まわりの設定。

ホームディレクトリに `.ideavimrc` というファイルを置くと読み込んでくれる。
ただし Windows の場合は、環境変数HOME ではなく、
`C:\Users\(ユーザー名)\.ideavimrc` 決め打ちでしか読み込んでくれないようだ。

```
" Stop Bell
set visualbell
set noerrorbells
```

## scalariform を走らせるための設定

- Run > Edit Configuration > 追加 > SBT Task
    - Tasks: `compile test:compile`
    - before launch: `Build` が入っていたのを抜く


# 編集

## 置換

改行に置換(というか行を分割する)  

- IdeaVim では s/,/\r/ など、 \r が改行扱い。
- IJの置換で、"Regex" にチェックをいれた状態で、"\n" でいける。

# TODO

カーソル位置を表示するには？ 
    → 出てたわ
    でもこれ、半角全角考慮しない文字数っぽいので、半角文字数換算で出してほしい


# トラブルシュート

java のメソッドが見つからなくなった。

jdkのアップデートで発生。
File > Project Structure > SDKs > JDK home path を アップデートした最新のものに変更する。
C:\Program Files\Java\jdk1.8.0_73  とか。
