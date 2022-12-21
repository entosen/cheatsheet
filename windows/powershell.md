
PowerShell Cheatsheet
=======================


```
# 使い方を見る (man)
help command

# alias
alias    # 現在のalias設定を表示

# which, where みたいなの (複数あるときは複数返る)
gcm command
gcm command | fl
Get-Command | Format-List

# 環境変数
# printenv みたいなの
Get-ChildItem env:
gci env:
gci env: | grep HOME
# echo みたいなの
$env:HOME    # string型で返る
gci env:HOME # DirectoryEntryオブジェクト (NameとValueがある)


# 現在位置
pwd
Get-Location

# カレントディレクトリを移動する (cd)
cd mydir           
chdir mydir
sl mydir
Set-Location mydir

# ls みたいなの
dir
ls



# ファイル操作

# ディレクトリ作成
ni foo -itemType Directory
New-Iterm foo -itemType Directory
```

TODO


```
Path環境変数への追加
$Env:Path += ";C:\Program Files\Internet Explorer\"   # 文字列連結。先頭の`;`は要素の区切りなので、必用に応じて付ける。
Set-Item Env:Path "$Env:Path;C:\Program Files\Internet Explorer\"


コメント
# 一行単位のコメントです。

<#
  複数行で記述する
  コメント表記です。
#>


継続行
    バッククオート

```
