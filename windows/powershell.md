
PowerShell Cheatsheet
=======================


```
# 使い方を見る (man)
help command

# alias
alias    # 現在のalias設定を表示

# which みたいなの
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


# カレントディレクトリを移動する (cd)
cd mydir           
chdir mydir
sl mydir
Set-Location mydir

# ls みたいなの
dir
ls
```


