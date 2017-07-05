

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

