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


参考

- 第6章 Yum Red Hat Enterprise Linux 6 | Red Hat Customer Portal
https://access.redhat.com/documentation/ja-jp/red_hat_enterprise_linux/6/html/deployment_guide/ch-yum



検索

```
yum search string1 [string2] [...]  # パッケージ名とサマリーから検索。
                                    # 1件もヒットしなかったら詳細とURLから検索。
                                    # 必要なら --enablerepo='*' など。

yum list [all | glob_exp1] [glob_exp2] [...]
    glob がパッケージ名だけじゃなくて、バージョンにも引っかかってしまうな。
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

# あるファイルがどのpackageで入ったか
yum provides "*bin/top" 

# ある package で入ったファイルの一覧
rpm -ql <package-name>
```

リポジトリ

```
# 一覧、詳細
yum repolist [{all|enabled|disabled}]  # デフォは enabled
yum repolist -v [<リポジトリID>]

yum repoinfo <リポジトリID>

# yum コマンド実行時だけリポジトリの有効／無効を切り替える
yum --enablerepo=<リポジトリIDのglob> search,install,update等のコマンド 
yum --disablerepo=<リポジトリIDのglob> search,install,update等のコマンド 

# 定常的にリポジトリの有効/無効を切り替える
sudo yum-config-manager --enable <リポジトリID>
sudo yum-config-manager --disable <リポジトリID>


yum makecache
```

リポジトリに関するの設定ファイルは下記にある。
```
/etc/yum.conf
/etc/yum.repos.d/   (この中で .repo 終わりのファイルが読み込まれるっぽい)
```



主要リポジトリ

参考

- `CentOS で EPEL / IUS / Remi リポジトリを使う (CentOS-5.x / CentOS-6.x / CentOS-7.x)|Everything you do is practice <http://everything-you-do-is-practice.blogspot.com/2017/09/centos-epel-ius-remi-centos-5x-centos.html>`__
- `RHEL/CentOSから標準より新しいパッケージをインストールするためのレポジトリ4選(AppStream /RHECL/EPEL/IUS) | DevelopersIO <https://dev.classmethod.jp/articles/how-to-install-newer-packages-from-rhel-centos-with-appstream-rhscl-epel-ius/>`__

一覧

- CentOSデフォルト

    - base: OSリリース時の状態
    - updates: baseから更新があったパッケージが格納
    - extras: baseに含まれない便利なソフトウェア群。ベースコンポーネントのupgradeをしない。
    - centosplus: baseに含まれない便利なソフトウェア群。ベースコンポーネントのupgradeをする。 (デフォルトdisable)
    - contrib: packages by Centos Users。 (デフォルトdisable)
    - cr: continuous relese (デフォルトdisable)

- EPEL

    - https://fedoraproject.org/wiki/EPEL/ja
    - RHEL のアップストリームディストリビューションとして Fedora が存在し、
      より先進的な機能・パッケージが取り込まれています。 
      Extra Packages for Enterprise Linux (以下EPEL) は Fedora では提供されているが、
      RHEL では提供されていない一部のパッケージ群を
      RHEL からもりようできるようにするためのものです。
      https://dev.classmethod.jp/articles/how-to-install-newer-packages-from-rhel-centos-with-appstream-rhscl-epel-ius/
    - リポジトリ登録::

          sudo yum install epel-release

- Software collections(SCL)

    - https://www.softwarecollections.org/en/
    - /opt 以下にインストールされるのでバッティングしない。
      しかしそのため、PATHなどの設定が必要で、 scl コマンドや scl_source スクリプトが必要。
      pyenv みたいな感じ。
    - 参考

      - `ソフトウェアコレクション(SCL：Software Collections)とは？ – StupidDog's blog <https://stupiddog.jp/note/archives/1074>`__
      - `CentOS 7にSCLリポジトリーを追加する <http://www.tooyama.org/el7/scl.html>`__

    - Centos用のものには2つのリポジトリがある

      - centos-sclo-rh

        - Red Hat Software Collections 由来(Upstream)のSCLパッケージのみを提供

      - centos-sclo-sclo

        - CentOS Software Collections SIGのSCLパッケージを提供

    - sudo yum install centos-release-scl  (rh, scol 両方入る？)
    - sudo yum install centos-release-scl-rh
    - sudo yum install centos-release-scl-scol


- Remi

    - https://rpms.remirepo.net/
    - リポジトリ登録::
    
          # RHEL/CentOS-7.x
          wget http://rpms.famillecollet.com/enterprise/remi-release-7.rpm
          sudo rpm -Uvh remi-release-7*.rpm

- IUS

    - https://ius.io/
    - リポジトリ登録::

          # RHEL/CentOS 7
          sudo yum install \
          https://repo.ius.io/ius-release-el7.rpm \
          https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm





```
依存を調べる
yum deplist <pkg>

古いバージョン(新しいのも？)含めて表示する
yum --showduplicates list [<pkg>]


yum makecache fast


```




# apt (Debiun系)

```
apt list              # インストールできるすべてのパッケージ一覧
apt list --installed  # インストール済のパッケージ一覧

```


