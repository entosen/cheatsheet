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





