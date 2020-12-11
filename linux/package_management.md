# RPM

```shell
# インストール  -i(--install) 
# -v(--verbose), -h(--hash 進捗バーの表示)
rpm -ivh package-x.y.z.rpm
rpm -ivh http://package.example.com/package-x.y.z.rpm

# アップグレード  -U(--Upgrage)
rpm -Uvh package-x.y.z.rpm

# アンインストール  -e(--erase)
rpm -e package-x.y.z.rpm


# 検索 -q(--query)
## パッケージ情報の表示 -i(--info)
rpm -qi httpd24

## インストールされた一覧表示 -a(--all)
rpm -qa

## あるパッケージによって入ったファイル一覧 -l(--list)
rpm -ql httpd24
rpm -qc httpd24   # 設定系ファイルのみ -c(--config)
rpm -qf /bin/ls   # あるファイルがどのパッケージに含まれているか -f(--file)
```



# yum

書きかけ

会社のデフォルトの状態では、epel リポジトリは登録されていないっぽい。
以下で登録。
```
sudo yum install epel-release
```


一覧

```
yum list             # 利用可能とインストール済み
yum list installed   # インストール済み
yum list updates     # インストール済みでアップデート可能
yum list available   # 利用可能
yum list extras      # もう利用できないもの
```

```
yum info <package_name>
```

```
yum install <package>
yum groupinstall <package group>
yum clean packages
yum remove <package_name>


# ある package で入ったファイルの一覧
rpm -ql <package-name>
```

リポジトリ

```
# 一覧、詳細
yum repolist [{all|enabled|disabled}]  # デフォは enabled
yum repolist -v [<リポジトリID>]

# yum コマンド実行時だけリポジトリの有効／無効を切り替える
yum --enablerepo=<リポジトリID> search,install,update等のコマンド 
yum --disablerepo=<リポジトリID> search,install,update等のコマンド 
```


```
依存を調べる
yum deplist <pkg>

古いバージョン(新しいのも？)含めて表示する
yum --showduplicates list [<pkg>]


yum makecache fast


```
