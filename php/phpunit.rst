=====================
phpunit
=====================

実行方法::

    phpunit とか
    ./vendor/phpunit/phpunit/phpunit とかで呼び出す。

phpunit.xml が設定ファイル

::
    Usage: phpunit [options] UnitTest [UnitTest.php]
           phpunit [options] <directory>

    1つのテストクラスだけテスト実行したいとき
    phpunit <テストクラス名> 
        この形だと <テストクラス名>.php が存在する必要がある。
        たいてい tests/ ディレクトリ以下に収めたりするので、この形だとうまくいかない。

    phpunit <テストクラス名> <tests/ファイル名.php>
        こんな感じ。

    メソッドも絞りたいとき。 正規表現はメソッド名の途中にマッチ。
    phpunit --filter='<正規表現>' /path/to/test/AClassTest.php

