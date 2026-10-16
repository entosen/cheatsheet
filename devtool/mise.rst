###########
mise
###########

概要
=====================

ランタイムバージョンマネージャー(Runtime Version Manager)の1つ。

- 多言語対応なので、1つ覚えれば済む
- asdf と同じようなツールだけど、こっちの方が高速


機能としては下記

- (Dev Tools) ツール・ランタイムのバージョン切り替え
- (Environments) 環境変数管理
- (Tasks) タスクランナー


ドキュメント

- `Dev tools, env vars, and tasks in one CLI | mise-en-place <https://mise.jdx.dev/>`__


インストール
=====================

mac & Linux::

  curl -fsSL https://mise.run | sh

mac brew::

  brew install mise


シェルに有効化処理を追加
========================


``.zshrc`` に下記を追加::

  eval "$(mise activate zsh)"



cheatsheet
=======================

::

  # ------------------------------------------------------------------------------
  # ツール バージョン管理 (mise use / install / ls)
  # ------------------------------------------------------------------------------

  mise install              # mise.toml に従い必要なバージョンを一括インストール

  # インストール = 設定ファイルを更新せずに特定のツールだけ事前ダウンロード
  mise install node@24.11.1
  mise install node@24
  mise install node

  mise registry             # 利用可能な言語・ツール一覧の確認
  mise ls-remote node       # install可能なバージョン一覧の確認
  mise plugins ls-remote    # asdf で使用可能な全プラグイン一覧を検索
  mise plugins add <plugin-name>   # プラグインを追加

  # use は仕様するバージョンを設定する。必要であれば install もされる
  mise use node@24          # ローカルのバージョン指定。カレントディレクトリの mise.toml に記録。
  mise use -g node@24       # グローバルのバージョン指定。~/.mise.toml に記録。
  mise use --shell node@24  # 現在のターミナルセッションのみ一時的に変更

  # 確認
  mise ls                   # インストール済み, 使用中, 要求されているツール一覧を表示
  mise ls --current         # 現在有効(要求されていて、かつ、install済み)なツール(行)のみを表示
  mise current              # 現在有効なツールのみを表示 (より簡潔)

  # アンインストール
  mise uninstall node@18    # 指定バージョンを削除
  mise prune                # 不要になった古いバージョンを一括削除

  # ------------------------------------------------------------------------------
  # 環境変数の制御 (mise env / set)
  # ------------------------------------------------------------------------------
  mise env                                # 現在適用されている環境変数一覧を表示
  mise set FOO=bar                        # .mise.toml に環境変数を保存
  mise unset FOO                          # .mise.toml から環境変数を削除

  # ------------------------------------------------------------------------------
  # タスクランナー (mise run)
  # ------------------------------------------------------------------------------
  mise run                                # 定義されているタスク一覧の表示・選択
  mise run <task>                         # 指定したタスクを実行(短縮形: mise r <task>)
  MISE_ENV=development mise run dev       # 開発環境設定(.mise.development.toml)を適用してタスク実行


  # ------------------
  # 以下未整理
  # -------------------
  mise which node        # どの実行ファイルを使うかを確認

  mise exec --

  mise run
  mise run dev

  mise env

  mise outdated
  mise upgrade node
  mise upgrade --bump node
  mise unuse node

  mise doctor

  

仕組み
======================

シェルのフックに入り込んで、cwd が変わったときに mise.toml を探索して、
適切に PATH 環境変数をセットすることで、ランタイムを切り替える。

XXenv みたいに shims 方式ではない。 (shims方式でやることもできるらしい) 。


フックが発火すると、mise はカレントディレクトリから親ディレクトリに向かって設定ファイルを探索する。

設定ファイルが見つかると、指定されたバージョンの実行ファイルが置かれているパス 
(例: ``~/.local/share/mise/installs/node/20.11.0/bin``) を割り出し、
現在のシェルの環境変数 PATH の先頭にそのパスを自動で割り込み挿入します。


スコープ
--------------

- ローカルスコープ (``mise use``)

  - 書き込み先: カレントディレクトリの ``.mise.toml``
  - 影響範囲: そのディレクトリ(およびサブディレクトリ)内のみ

- グローバルスコープ (``mise use -g``)

  - 書き込み先: ``~/.config/mise/config.toml``
  - 影響範囲: ローカル設定が存在しないすべての場所

- 現在のシェルだけに適用 (``mise shell``) 

  - ファイルには一切書き込まず、現在のシェルセッション内だけ一時的にバージョンを変更
  - ::

      mise shell node@18        # 現在のシェルだけに適用
      mise shell --unset node   # 元に戻す場合


優先順位
-----------------

1. ``mise shell`` (最優先)
2. カレントディレクトリの ``.mise.toml``
3. 親ディレクトリを遡って見つかった ``.mise.toml``
4. グローバル ``~/.config/mise/config.toml`` 


設定ファイル名
-----------------------

ローカル用の設定ファイル

- ``.mise.toml``
- ``mise.toml``
- ``.tool-versions`` (asdf 互換)
- ``.node-version`` / ``.python-version`` などの各種専用ファイル

グローバル用の設定ファイル

- ``~/.config/mise/config.toml`` (標準)
- ``~/.config/mise.toml``
- ``~/.mise.toml``





設定ファイル .mise.toml
==============================

::

  [tools]
  node = "22"
  python = "3.13"

  [env]
  NODE_ENV = "development"

  [tasks.build]
  run = "npm run build"



インタラクティブな環境でどうするか？
=========================================

シェルスクリプトの中はプロンプトフックが効かないため、
シェルスクリプト内で cd するようなケースでは、別途対応が必要。


(方法1) mise en-env を eval
-------------------------------

``eval "$(mise en-env)"`` を実行すると、
そのディレクトリの ``.mise.toml`` を読み込んで
現在のシェルの PATH や環境変数を即座に適用します。

::

  #!/bin/bash
  cd /path/to/my-project

  eval "$(mise en-env)"    # フック時相当の動作

  node -v                  # my-project 指定のバージョンのnodeが起動する。


(方法2) mise exec (または mise x) を使う
---------------------------------------------

サブプロセスとして mise 経由でコマンドを実行する方法です。
スクリプト全体の環境を汚さず、特定コマンドだけ指定のバージョンで動かしたい場合に便利です。

::

  #!/bin/bash

  # -- で区切った配下のコマンドを、cd 先の指定バージョンで実行
  cd /path/to/my-project
  mise exec -- node -v
  mise exec -- npm run build

  # 省略形 (mise x) も可能
  mise x -- python main.py


(方法3) 事前に Shims モードを有効にしておく
-----------------------------------------------

``~/.zshrc``::

  export PATH="$HOME/.local/share/mise/shims:$PATH"

スクリプト::

  #!/bin/bash
  cd /path/to/my-project

  # シムが自動的に .mise.toml を読み込んで適切なバージョンを呼び出す
  node -v



Shimsモードにしていないのに、PATHにshimsが入っている件
===========================================================

はまったのでメモ。

mise の動作には2パターンある。

- PATH 切り替えモード ( ``mise activate zsh`` )
- shims モード ( ``mise activate zsh --shims`` )


PATH 切り替えモードにしていた場合にも、PATH環境変数にshims用のパスが入る。::

  ``~/.local/share/mise/shims``

不自然に感じるが、これは意図したもの。
lazyなツールやない場合に自動インストールするためにshimsも有効にしてある。

shimsモードは、shimsでの動作のみを有効にするもの (PATH切り替え動作は無効) 。

常に shimp モードで動かすためには、下記のsettingsを加える。::

  mise settings set activate_shims=false

参考

- ``mise activate` adds shims directory to path · jdx/mise · Discussion #12924 <https://github.com/jdx/mise/discussions/12924>`__
- https://mise.jdx.dev/dev-tools/shims.html#activate-shims
- https://mise.jdx.dev/configuration/settings.html#activate_shims


