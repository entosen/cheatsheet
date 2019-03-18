# ulimit、システムのリソース上限など

## ulimit

シェルやそこから起動されるプロセスのリソース上限値を参照・設定する。

この値は環境変数のようにforkする際に子プロセスに引き継がれていく。
もちろんユーザーごと。

設定値には以下の２つの値がある

- hard limit
    - 一度設定すると？、root 以外のユーザが増やすことはできない
- soft limit
    - hard limit の値までは増やせる

```
    -S  soft limit を参照、操作する
    -H  hard limit を参照、操作する

    参照
    ulimit -a    (soft limit を表示)
    ulimit -S -a (soft limit を表示)
    ulimit -H -a (hard limit を表示)

    ulimit -S -n 10000  (ファイル数のsoft limitをセット)
    ulimit -H -n 10000  (ファイル数のhard limitをセット。root権限が必要)
```


### 稼働中プロセスの上限値を参照する

```
cat /proc/<PID>/limits

Max cpu time              unlimited            unlimited            seconds
Max file size             unlimited            unlimited            bytes
Max data size             unlimited            unlimited            bytes
Max stack size            10485760             unlimited            bytes
Max core file size        0                    unlimited            bytes
Max resident set          unlimited            unlimited            bytes
Max processes             64198                64198                processes
Max open files            1024                 4096                 files
Max locked memory         65536                65536                bytes
Max address space         unlimited            unlimited            bytes
Max file locks            unlimited            unlimited            locks
Max pending signals       64198                64198                signals
Max msgqueue size         819200               819200               bytes
Max nice priority         0                    0
Max realtime priority     0                    0
Max realtime timeout      unlimited            unlimited            us
```


### 設定の仕方

- ulimit 手動設定
- 起動スクリプト内で ulimit を実行
- ログイン時の設定を変更

### ulimitの値がデフォルトでいくつに設定されるか

ulimit は基本的にユーザーごとの設定なので、
ユーザのアカウントまわりの認証を担うPAMという仕組みでセットされる。


#### (PAM) 制限値の指定 

- /etc/security/limits.conf
- /etc/security/limits.d/90-nproc.conf
- /etc/security/limits.d/95-nofile.conf

サブディレクトリの方が優先ぽい。
サブディレクトリの中では番号どっちが優先なのか。

```
# nofile の設定の場合
*    soft nofile 65536
*    hard nofile 65536
root soft nofile 65536
root hard nofile 65536
```


#### (PAM) どのタイミングで反映されるか

どのタイミングで反映されるかについては、
/etc/pam.d/以下に各サービス別にファイルがあり、
そこに(もしくはincludeされているファイルの中に)以下の記述があれば、ulimitの反映が行われる
```
session    required     pam_limits.so
```

sshd経由でログインした場合 や sudo の際には、limit.conf に従って ulimit がセットされる。


ただし sshd なんかは limits.comf などを書き換えてもプロセスの再起動が必要なので注意。
(サービスのプロセスが起動するときに読まれるってことらしい)
```
sudo service sshd restart
```

ちなみに、ネットでは、以下のファイルに書くと反映すると書いてあるものがあったが、
会社のLinuxでは include される設定にはなっていなかったようなので、効かない。
(ディストリによる？)

- /etc/pam.d/common-session に追加
- /etc/pam.d/common-nonsession に追加




#### PAMを使わないデーモンの場合

デーモンなんかは、(とくにrebootで自動的に起動するようなデーモン)は PAM を通らないので、
上記の設定では効かない。
そういう場合は、起動スクリプト中に明示的に ulimit を書いたりするっぽい。
`/etc/initscript` に書くというのもあるっぽい。



### 各設定はどういう意味か

    TODO


