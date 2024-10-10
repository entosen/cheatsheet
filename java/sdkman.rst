=========================
sdkman
=========================

使い方

- `Usage | SDKMAN! the Software Development Kit Manager <https://sdkman.io/usage>`__

::

    sdk <subcommand> [candidate] [version]

        candidate は java, maven, scala, groovy, などなど

    sdk version   # 確認

    # install可能リスト
    sdk list         # candidate の一覧
    sdk list java    # candidate=java での version の一覧。
                     # install済みか、use中かの印も。

    sdk install <candidate> [version]    # インストール
    sdk uninstall <candidate> <version>  # 削除 

    sdk default <candidate> [version]   # 使うバージョンを選択。永続。たぶんどこかに保存。
    sdk use <candidate> <version>       # 使うバージョンを選択。現在のshell(と子孫シェル？)のみ

    sdk env init       # .sdkmanrc を作成する
    sdk env install    # .sdkmanrc に記述されているツールキットをすべてインストールする
    sdk env            # .sdkmanrc に記述されているツールキットに切り替える (現在のshellと子孫シェル)
    sdk env clear      # defaultで指定されているバージョンに切り替える

    sdk current [candidate]    # 現在 use しているやつの表示





参考
======

- 本家 `Home | SDKMAN! the Software Development Kit Manager <https://sdkman.io/>`_


インストール
================

::

    curl -s "https://get.sdkman.io" | bash

やっていること

- ``~/.sdkman`` ディレクトリを作り、その中に sdkman をインストールする
- ``~/.zshrc`` の末尾に下記を追記::

    #THIS MUST BE AT THE END OF THE FILE FOR SDKMAN TO WORK!!!
    export SDKMAN_DIR="$HOME/.sdkman"
    [[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"

ドットファイルを別管理している場合などは、手動で下記のように編集する。

.zprofile::

    if [ -e ~/.sdkman ] ; then
        export SDKMAN_DIR="$HOME/.sdkman"
    fi

.zshrc::

    [[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"


これにより、現在のシェルに ``sdk`` 関数が追加される。


仕組み
=======

sdkコマンド自体は、シェル関数として存在。
そのシェルのPATHやJAVA＿HOME環境変数をセット・切り替えすることで、狙ったバージョンを動かす。

c.f. nodenv や goenv のような shims 方式ではない。

なので、.zshrc などを経由しない、Dockからの起動とかだとうまく動かなそうに思う。

- インストールされた実体は、 ``$SDKMAN_DIR/candidates/<candidate>/<version>`` 以下に入る。
- ``<candidate>/current`` がuseしている version へのシンボリックリンクになっている。
- PATH環境変数の先頭に ``$SDKMAN_DIR/candidates/java/current/bin`` が追加される。
- 同様の感じで、JAVA_HOME, binary_input, zip_output あたりの環境変数をうまいことセットしてくれる

おそらく

- sdkman-init.sh 呼んだときに、各default のバージョンが PATH などの環境変数にセットされる
- sdk use をしたときには、その指定したバージョンが PATH などの環境変数にセットされる


sdkman_auto_env について
------------------------------

``.sdkman/etc/config`` に ``sdkman_auto_env=true`` を書いておくと、
``.sdkmanrc`` が置いてあるプロジェクトディレクトリに移動した際に、 
``sdk env`` をしなくても自動的に.sdkmanrcで指定したJDKを使用するようになる。

仕組み。
``sdkman_auto_env=true`` にすると、PROMPT_COMMAND 環境変数にsdkman_auto_env を入れる。
PWD != SDKMAN_OLD_PWD のときに、.sdkmanrc の存在をチェックし、あれば sdk env を実行するっぽい。

ref. https://github.com/sdkman/sdkman-cli/discussions/1200






