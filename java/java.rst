############################
Java CheatSheet
############################


====================
基本事項
====================

文の終わりはセミコロン(;)


コメント
===================

::

  // 単一行コメント

  /* コメント */
  /*
    複数行
    コメント
  */

  /** ドキュメンテーションコメント */


mainメソッド
====================

基本の形::

  package to.msn.wings.selfjava.chap01

  import java.time.LocalDateTime;

  public class Hello {
    public static void main(String[] args) {
      LocalDateTime time = LocalDateTime.now();
      System.out.println(time);
    }
  }

簡単化(java 21から)::

  import java.time.LocalDateTime;

  void main() {
    LocalDateTime time = LocalDateTime.now();
    System.out.println(time);
  }

- TODO

====================
変数、データ型
====================

====================
演算子
====================


====================
制御構文
====================


=================================
オブジェクト指向構文
=================================





未整理
===================

ジェネリクス
-------------------

- `ジェネリクスの代入互換のカラクリ - プログラマーの脳みそ <https://nagise.hatenablog.jp/entry/20101107/1289124105>`__


=================================
Stream API
=================================

ラムダ式
-------------------

- `Javaラムダ式についてまとめてみた #java8 - Qiita <https://qiita.com/kenRp01/items/4045a7925340088bd7e3>`__
- `[Java] ラムダ式入門 #java8 - Qiita <https://qiita.com/xrdnk/items/7fcc349929685f029440>`__


Stream API
------------------

- `MapでStream APIを使う #Java - Qiita <https://qiita.com/megmogmog1965/items/414e71913ea080232396>`__

