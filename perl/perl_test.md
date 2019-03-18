
Test::More

ドキュメント
http://perldoc.jp/docs/modules/Test-Simple-0.99/lib/Test/More.pod

ファイルの拡張子は `.t` が一般的。
`t/` というディレクトリに入れるのが一般的。

```
#!/usr/bin/perl
use strict;
use warnings;

use Test::More tests => 4;  # テストの数を書く
# use Test::More "no_plan"; # テストの数を書くのが面倒な場合は "no_plan" を使う



# 以下、「説明」の引数は省略可

require_ok( 'Some::Module' );

ok(式, 説明);            # true であることをテスト

is( s1, s2, 説明 );            # s1 と s2 が一致することをテスト
isnt( s1, s2, 説明 );          # s1 と s2 が一致しないことをテスト

like("abcde", qr/^a/, 説明);     # 正規表現に一致することをテスト
unlike("abcde", qr/^a/, 説明);   # 正規表現に一致しないことをテスト
                                 # 第2引数は正規表現のリファレンス
```




-----------------

prove っていうのは、あるディレクトリ配下にある `.t` をまとめて実行してくれるやつ

perl t/hoge.t 
ってやってもいいけど、
prove -vlr t
ってやるとまとめて実行してくれる
