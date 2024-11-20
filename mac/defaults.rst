


::

  defaults domains                    ドメイン一覧を表示
  defaults domains | tr , '\n'        見やすく

  defaults find <word>                ドメイン名, キー, および値を検索

  defaults read                       全表示
  defaults read <domain>              そのドメインの全キー表示
  defaults read <domain> <key>        そのドメインのそのキー表示
  defaults read-type <domain> <key>   そのドメインのそのキーの型を表示
  
  defaults write <domain> <key> <value>  値のセット

    defaults write com.companyname.appname "Default Color" '(255, 0, 0)'

  defaults write <domain> <plist>        plist形式で値のセット。それまでのkeyは削除される。

    defaults write com.companyname.appname '{ "Default Color" = (255, 0, 0);
                                            "Default Font" = Helvetica; }'

  defaults delete <domain>            そのドメインを削除
  defaults delete <domain> <key>      そのドメインのそのキーを削除

  # 一般的にはそのアプリを再起動しないと設定が反映しないので、
  # 下記のように killall するか、GUIでアプリを一旦終了して再度起動する
  killall Dock


データ構造は、 domain - key - 値 。

Windows のレジストリみたいなもの。

実体は ``~/Library/Preferences/`` フォルダ以下の plist ファイル。

- ファイルがドメインに相当。

  - <domain> のところは下記が書ける。

    - ドメイン名

      - (例) ``com.apple.dock``

    - ``-app アプリケーション名``  

      - (例) ``-app TextEdit``

    - ``-globalDomain``, ``-g``, ``NSGlobalDomain``

      - どのアプリにも共通の設定。
      - 実体は .GlobalPreferences.plist

    - ファイルのパス

      - (例) ``~/Library/Containers/(中略)/com.apple.TextEdit.plist``
      - ``.plist`` はあってもなくても認識される

- <key> がファイルの中のキー
- <value> がそれに紐付く(型と)値::

    <value> is one of:
      <value_rep>        (文字列表記で型も含めて表現する)

        '"aaa"'                                文字列
        '(255, 0, 0)'                          配列
        '{"key1" = "v1"; "key2" = "v2"}'       ディクショナリ
        '< 54637374 696D67 >'                  バイナリデータ 16進表記

      -string <string_value>
      -data <hex_digits>
      -int[eger] <integer_value>
      -float  <floating-point_value>
      -bool[ean] (true | false | yes | no)
      -date <date_rep>
      -array <value1> <value2> ...
      -array-add <value1> <value2> ...
      -dict <key1> <value1> <key2> <value2> ...
      -dict-add <key1> <value1> ...

    


  
