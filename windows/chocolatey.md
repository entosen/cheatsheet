# chocolatey 

chocolatey
https://chocolatey.org/

インストール方法

- 管理者権限でコマンドプロンプトを起動
- https://chocolatey.org/install にあるコマンドを入力。
- (結果) システム環境変数に `C:\ProgramData\chocolatey\bin` が追加される


なお chocolatey コマンドは管理者権限のコマンドプロンプトから叩くのがいい。

chocolatey コマンド

```
# インストール済みのパッケージ一覧を表示
choco list -localonly
choco list -lo

# パッケージのインストール
choco install <packageName>...

# インストール済みパッケージのアップデート
choco update <packageName>...
choco update all

# アンインストール
choco uninstall <packageName>...

# パッケージリポジトリ関係
choco list                  # パッケージ一覧の表示(時間がかかる)
choco list <packageName>    # パッケージの検索
```
