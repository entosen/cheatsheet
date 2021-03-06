
## ホストの指定

```python
execute(タスク, host=ホスト名)
execute(タスク, hosts=[ホスト名, ...])
# 注: execute の戻り値は、ホスト名をキーとして辞書
```

run() や sudo() は、host, hosts などのホスト指定は受け付けない。


## オペレーション

ドキュメント

- [オペレーション - Fabric ドキュメント](http://fabric-ja.readthedocs.io/ja/latest/api/core/operations.html)

### 基本

```
run(*args, **kwargs)
例
run("ls /var/www/")
run("ls /home/myuser", shell=False)
output = run('ls /var/www/site1')
run("take_a_long_time", timeout=5)
```

sudo もほぼほぼ同様の挙動・オプションが使えるので、読み替える。


### エラー時の挙動、出力 

- 標準の動き
    - 実行しようとするコマンドを出力
    - 実行コマンドの出力(STDOUT,STDERRがマージされて)出力
    - 0以外のexitcodeになった場合 abort
- warn_only=True
    - 標準との違いは、0以外のexitcodeになった場合 abortせず warning を出すだけで処理継続
- quiet=True
    - 実行しようとするコマンドを出力しない
    - STDOUT, STDERR も出力しない。
    - 0以外のexitcodeになった場合も何も出さずに処理継続


例)

```
=== 標準での失敗ケース ===
[localhost] run: /home/hogehoge/tmp/170705_fabric_test/testcommand 1
[localhost] out: これは STDOUT に出力される1
[localhost] out: これは STDERR に出力される1
[localhost] out: これは STDOUT に出力される2
[localhost] out: これは STDERR に出力される2
[localhost] out: これは STDOUT に出力される3
[localhost] out: これは STDERR に出力される3
[localhost] out:


Fatal error: run() received nonzero return code 1 while executing!

Requested: /home/hogehoge/tmp/170705_fabric_test/testcommand 1
Executed: /bin/bash -l -c "/home/hogehoge/tmp/170705_fabric_test/testcommand 1"

Aborting.

=== warn_onlyでの失敗ケース ===
[localhost] run: /home/hogehoge/tmp/170705_fabric_test/testcommand 1
[localhost] out: これは STDOUT に出力される1
[localhost] out: これは STDERR に出力される1
[localhost] out: これは STDOUT に出力される2
[localhost] out: これは STDERR に出力される2
[localhost] out: これは STDOUT に出力される3
[localhost] out: これは STDERR に出力される3
[localhost] out:


Warning: run() received nonzero return code 1 while executing '/home/hogehoge/tmp/170705_fabric_test/testcommand 1'!

=== quietでの失敗ケース ===
(なにも表示されない。)
```

### 戻り値

戻り値は、STDERR,STDOUTをマージした結果(一般的には複数行の、単一の文字列)
この文字列は、通常の文字列の属性以外に `failed` `succeeded` などの追加の属性を持つ。

```
output = run('...コマンド...')
print output          # STDOUT,STDERRの結果が取れる。これやらなくても自動で出力はされる(quiet=True時以外)
output.return_code    # exitcode を返す
output.succeeded      # exitcode が 0 なら True
output.failed         # exitcode が 非0 なら True
output.command        # 要求したコマンド。(例) `testcommand 1`
output.real_command   # 実際に実行したコマンド。(例) `/bin/bash -l -c "testcommand 1"`
```

run,sudo は、標準だと stdout と stderr を結合した文字列を戻り値とする。
stdout と stderr を別々に取り出したい場合は、以下のようにする。

```
ret = run("cmd", pty=False, combine_stderr=False)   # この２つを両方Falseにしないと交じる
str(ret)      # → stdout のみ取れる
ret.stderr    # → stderr のみ取れる
```


## 環境, env

参考ドキュメント

- [環境辞書、 env - Fabric ドキュメント](http://fabric-ja.readthedocs.io/ja/latest/usage/env.html)
- [fab オプションと引数 - Fabric ドキュメント](http://fabric-ja.readthedocs.io/ja/latest/usage/fab.html)

### 既存の設定

TODO

### 独自の設定を追加

単なる辞書なので、独自の設定を追加することも可能。(ただし、名前の衝突には注意)。

設定をグローバル変数ではなく env に入れることのメリットは、
fabの起動時の `--set` コマンドラインオプションでセットすることができる。
ただし、スクリプト内でのセットの方が優先されるので注意。

ベストプラクティスとしては以下のような感じになると思う。

```python
from fabric.api import task, env

if 'my_threshold' not in env:
    env.my_threashold = 75

@task
def check(th=env.my_threashold):
    if a > th:
	...
```

```sh
% fab check                          # th は 75
% fab --set my_threashold=60 check   # th は 60
% fab check:th=50                    # th は 50
```

