==========================
Rosseta
==========================

Rosetta は、特定のアーキテクチャのプログラムコードを持つバイナリを、
別のアーキテクチャに適宜変換することでバイナリの互換性を維持するAppleの技術。 

現行の Rosetta 2 は、x86_64 (Intel Mac用) バイナリを
arm64 (Apple Silicon Mac) 上で動かすことができる。



チートシート
====================================

各種確認
------------------

今の動作しているアーキテクチャの確認 (``uname -m``)::

  % uname -m
  arm64

  % arch -x86_64 uname -m 
  x86_64


実行ファイルがどちらか確認::

  # === file コマンド ===
  % file /usr/bin/uname
  /usr/bin/uname: Mach-O universal binary with 2 architectures:
      [x86_64:Mach-O 64-bit executable x86_64] [arm64e:Mach-O 64-bit executable arm64e]
  /usr/bin/uname (for architecture x86_64):	Mach-O 64-bit executable x86_64
  /usr/bin/uname (for architecture arm64e):	Mach-O 64-bit executable arm64e

  # === lipo -info コマンド ===
  % lipo -info /usr/bin/uname
  Architectures in the fat file: /usr/bin/uname are: x86_64 arm64e


ユニバーサルバイナリのどれ(どちら)を起動するか指定する (``arch``)::
-----------------------------------------------------------------------

概要

- 引数なしで arch コマンドを使用すると、マシンのアーキテクチャタイプを表示
- ユニバーサルバイナリで選択されたアーキテクチャを実行

::

  # 表示
  arch

  # アーキテクチャを選択して実行
  arch -x86_64 

  arch [-32] [-64] [[-arch_name | -arch arch_name]...] [-c] [-d envname]...
          [-e envname=value]... [-h] prog [args ...]


  アーキテクチャの指定
    -x86_64            # ハイフンにつつけて arch_name 
    -arm64

    -arch x86_64       # 互換性のため -arch オプションも使える

  環境変数関係
    -c                  環境変数をクリアして(引き継がずに)実行
    -d envname          環境変数から指定の変数を削除して実行
    -e envname=value    環境変数を追加して実行

  arch_name
    i386     32-bit intel
    x86_64   64-bit intel
    x86_64h  64-bit intel (haswell)
    arm64    64-bit arm
    arm64e   64-bit arm (Apple Silicon)



解説
==============

参考情報

- `M1 Mac の環境構築メモ | 株式会社エムケイシステム TECH BLOG <https://blog.mksc.jp/contents/apple-silicon/>`_
- `Universal Binary - Wikipedia <https://ja.wikipedia.org/wiki/Universal_Binary>`_


ユニバーサルバイナリとは
-----------------------------

1つのバイナリファイル中に、複数のアーキテクチャのバイナリが含まれている。

::

  % file /bin/bash

  /bin/bash: Mach-O universal binary with 2 architectures: [x86_64:Mach-O 64-bit executable x86_64] [arm64e:Mach-O 64-bit executable arm64e]
  /bin/bash (for architecture x86_64):	Mach-O 64-bit executable x86_64
  /bin/bash (for architecture arm64e):	Mach-O 64-bit executable arm64e



Rosetta 2
-------------

x86_64 のエミュレーター。

arm64 → x86_64 バイナリの呼び出し(exec?)も、
x86_64 → arm64 バイナリの呼び出し(exec?)も、両方サポートされてる。

なので、この辺がシームレスなので、使う側としては、
いちいちアーキテクチャを意識して指定するということはほとんどないと思う。
(コマンドが存在すればいいので。それが x86_64 か arm64 かは問わないことが多いので)。


ユニバーサルバイナリの中のどれが動くか

- 通常は、プロセッサタイプに一番近いアーキテクチャをOSが自動的に選択する。

  - 未エミュレーション時は、物理プロセッサに一番近いもの
  - 既エミュレーション時は、エミュレーションしているプロセッサに一番近いもの
    (=つまり arch の選択は子プロセスに引き継がれる) (ソース見つからず。実験した限りはそう)

- そうじゃないアーキテクチャを使いたい場合には、 arch コマンドを使って指定する


Homebrewとの関係
------------------------------

brew コマンドはシェルスクリプトで、ユニバーサルバイナリではない。

下記のようにすると arm64版の brew と x86_64版の brew を両方併存させることができる::

  # 正確には Homebrew のサイトのインストールスクリプトを参考に

  # arm64版をインストール
  % /bin/bash -c "$(curl....install.sh)"
  → /opt/homebrew/bin/brew

  # x86_64版をインストール
  % arch -x86_64 /bin/bash -c "$(curl....install.sh)"
  → /usr/local/bin/brew

この2つのbrewはディレクトリが分かれて別個に存在する。
tapの設定やインストール済みの一覧も別個に管理される。
それぞれインストールされるディレクトリも異なる(と思う)。

起動の仕方。

brewコマンドはシェルスクリプトであり、ユニバーサルアプリではない(そもそもパスが異なる)ので、
OSの自動選択は効かない。
ユーザーが明示的にどちらを動かすか(パスで)選ぶ必要がある。

なお、brew list などの表示系はそのときのアーキテクチャによらず呼び出せるが、
brew install などの変更系は、それぞれ期待するアーキテクチャで起動されていないとエラーになった気がする。

- arm64版は、arm64の環境でないエラーになる
- x86_64版は、x86_64(エミュレーション中)の環境でないとエラーになる

::

  # arm64 brew 
  % brew install foo

  # x86_64 brew
  % arch -x86_64 /usr/local/bin/brew install foo

方針

- 原則arm64のバイナリを使う
- brew はarm64版とx86_64版を両方インストールして、
  arm64 brew では提供されてないものを入れたいときは、x86_64 brewを使う
- PATH 環境変数を /opt/homebrew/bin → /usr/local/bin の優先順位にすることで、arm64 brewが優先的に実行されるようにする
- ややこしいので、 arm64 brew と x86_64 brew の両方で、同じものをインストールしないように注意する 
