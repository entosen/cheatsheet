===========================
SQLcl
===========================

sqlコマンド。 

sqlplus の代わりに使えて、sqlplusよりも便利。


commit, rollback
=========================

デフォルトでは下記の状態::

  SET AUTOCOMMIT OFF    --- コマンドごとには commit も rollback もしない
  SET EXITCOMMIT ON     --- 正常にsqlclを終了したとき(EXIT や ^D) に保留中の変更を commit


明示的に打つ::

  COMMIT
  ROLLBACK

  EXIT COMMIT
  EXIT ROLLBACK


``SET AUTOCOMMIT ON`` にすると INSERT/DELETE/UPDATE 文が正常に実行されると直ちにコミットされます。
デフォルト値は OFF です。

``SET EXITCOMMIT OFF`` にすると、sqlclを終了したときに保留中の変更をrollback。



spool
=========================


::

  項目                     stdout   stderr   spool     制御方法
  -------
  接続後のメッセージ        ◯       ×       ×         △   -s (silent) で出なくなる
  SQL> プロンプト           ◯       ×       ×         ×   不可
  直接入力したSQL文         ×       ×       選         ◯   set echo on でspool に出るようになる (default:off)
  @file.sql で実行した中見  選       ×       選         ◯   set echo on で両方に出るようになる
  &置換の旧新(old/new)      ◯       ×       ◯         ◯   set verify off   で stdout と spool 両方出なくなる
  SQLの結果                 ◯       ×       ◯         ◯   set termout off  で stdout に出なくなる。 spool には出る
  SQLの結果の件数           ◯       ×       ◯         ◯   set feedback off で stdout と spool 両方出なくなる
  エラーメッセージ          ×       ◯       ◯         △   whenever sqlerror



sqlformat
====================

TODO


ファイルに書かれたsqlを実行
====================================

::

  @file.sql

  -- 引数付き
  @file.sql 123 JP

  -- ファイル中では &1 &2 ... で参照する
  select * from t where id = &1 and country = '&2'


コマンドラインからも同様にできる::

  sql 接続 @file.sql
  sql 接続 @file.sql 引数1 引数2


@@ だと入れ子になっているときに、そのファイル基準で探しに行ってくれるらしい。

！注意！ ``&1``, ``&2`` などの位置パラメタに関しては、
``@`` で読み込む時点で ``set define on`` されていないとうまく値が渡らないぽい。



バッチ
=================

バッチに付けるおすすめ::

  sql -s  で起動時メッセージを減らす

  WHENEVER SQLERROR EXIT SQL.SQLCODE
  WHENEVER OSERROR EXIT 9

  SET ECHO OFF
  SET VERIFY OFF
  SET FEEDBACK OFF
  SET TERMOUT OFF
  SET DEFINE OFF

  SET PAGESIZE 0
  SET LINESIZE 32767

  SET TAB OFF
  SET SQLBLANKLINES ON




外部連携
===================

::

  pwd          カレントディレクトリを表示
  cd <dir>     カレントディレクトリを変更

  oerr ora 7445     oraエラーの詳細を表示

sqlcl内からシェルコマンドを実行する。

::

  HOST ls -l
  !ls -l

  パイプやリダイレクトもOK
  !ls -l | grep log
  !echo hello > test.txt

HOST の結果もSPOOLの対象になるので、ログ用途に便利。




履歴と編集
==============================

一応機能は用意されているが、いろいろ力不足な感じがするので、
外部のエディタで編集して、都度ペーストするという方が現実的かもしれない。



カーソル編集(インラインエディタ)
-----------------------------------------

::

  ↑/↓                カーソルが文末にあるときは、SQL1文単位で履歴を辿る。
                       カーソルが文中にあるときは、1行単位で移動。

  ←/→                左右に1文字

  ^R           現在のバッファを実行
  ^C           中止

  履歴に入ったあとは、viモードが使えるっぽい。でも動作があやしい。
     

ヒストリ
-------------------------

history::

  h              履歴を表示

  h 番号         番号の履歴をバッファに読み込む



バッファ編集
-------------------------

ラインエディタ的な編集。カーソル移動ができなかった時代の遺物。

バッファの内容表示::

  l       バッファ内のすべての行を表示。
          通常は直前に実行した1文が収まっている。ただし ; は含まれない。
          カレント行は最終行になる。
  (単独の ; でも同じ)

実行::

  r       バッファの内容を表示後、実行。カレント行は最終行になる。
  /       バッファの内容を表示せず、実行。カレント行はそのまま。

  実行してエラーが発生した場合は、エラー行がカレント行になる。

エディタで編集::

  ed            エディタでバッファを編集
  ed file名     ファイルをエディタで編集

  save file名   現在のバッファをファイルに書き出し
  get  file名   ファイル内容をバッファに読み込み

表示(カレント行の指定)::

  L            SQLバッファ内のすべての行を表示します。
  L n          行nを表示します。
  数字         行nを表示します。
  L *          カレント行を表示します。
  L n *        行nからカレント行までを表示します。
  L LAST       最終行を表示します。
  L m n        ある範囲(mからn)の行を表示します。
  L * n        カレント行から行nまでを表示します。


l以外のコマンドはバッファ内の1行にのみ影響する。(カレント行)。(アスタリスクがついている行)

削除::

  DEL          カレント行を削除します。
  DEL n        行nを削除します。
  DEL *        カレント行を削除します。
  DEL n *      行nからカレント行までを削除します。
  DEL LAST     最終行を削除します。
  DEL m n      ある範囲(mからn)の行を削除します。
  DEL * n      カレント行から行nまでを削除します。

カレント行の編集::

  A text       カレント行の末尾にテキストを追加します。
  C/old/new    カレント行内のoldをnewに変更します。
  C/text       テキストをカレント行から削除します。

  数字 text    行nをtextに置き換え

行追加、行変更::

  I text       1行追加。textという内容の1行をカレント行の下に追加します。
  0 text       先頭行に textという内容の1行を追加

  I            カレント行の後に1つ以上の行を追加します。空行かピリオド単独行が来るまで継続。
               (SQLclでは効かなかった)


バッファをクリア::

  CL BUFF      すべての行を消去します。





