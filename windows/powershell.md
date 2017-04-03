
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


