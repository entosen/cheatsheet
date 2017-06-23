

## map

配列の要素それぞれに、ある処理を適用する

```
# 関数を適用
@chars = map(chr, @numbers);    # 対応する文字に変換する

# ラムダ関数を適用
my @squares = map { $_ * $_ } @numbers;   # それぞれの2乗

# () を返すとその要素は出ない。要素数が減る。
my @squares = map { $_ > 5 ? ($_ * $_) : () } @numbers
my @squares = map { $_ * $_ } grep { $_ > 5 } @numbers   # 上と同じ

# 結果をハッシュにする
%hash = map { get_a_key_for($) => $_ } @array;
```

tips
```
# inputの各要素のある部分のみを抜き出す
my @result = map { m/logs=(\w*)/ } @input;
my @result = map { $_ =~ m/logs=(\w*)/ } @input;
    # 正規表現マッチはリストコンテキストで評価されると、($1, $2, ...) のリストを返すから
    # マッチしてない場合は、空リスト() が返され、その要素は結果に含まれない(要素数が減る)
```



## ファイル分割、モジュール

```
# ファイル名 Hoge.pm
package Hoge.pm

sub func1 {
}
sub func2 {
}

1;    # <-- 忘れやすいので注意。
```



## コマンドライン引数、getopt

- [Perlでコマンドラインオプションの解析に Getopt::Long を使う時、絶対に忘れてはいけない引数 - たごもりすメモ](http://tagomoris.hatenablog.com/entry/20120918/1347991165)
- [Perl スクリプトでのコマンドラインオプション処理](https://emptypage.jp/notes/getopt-on-perl.html)


```perl
use Getopt::Long qw(:config posix_default no_ignore_case gnu_compat);

# コマンドライン引数を受ける変数を用意しておく。
# 指定なしの場合のデフォルト値もセット。
my $opt_all = 0;
my $opt_debug = 0;

GetOptions(
    "all" => \$opt_all,
    "debug|d" => \$opt_debug    # `|` で複数候補が書ける
    );

@ARGV  # オプションを評価した後の残りの引数が入っている。
```


引数を取らないオプション

0か1で扱うのがスタンダードらしい。
```
"all" => \$opt_all
"debug" => \$opt_debug
```

引数を取るオプション

`--aaa hoge` でも `--aaa=hoge` でも、どちらでも可。

```
"aaa=s"   # 文字列を取る
"aaa=i"   # 整数値を取る
```



与え方と設定

TODO

