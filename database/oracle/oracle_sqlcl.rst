===========================
SQLcl
===========================

sqlコマンド。 

sqlplus の代わりに使えて、sqlplusよりも便利。


commit, rollback
=========================

基本的に自動ではcommitしない。

明示的に打つ::

  COMMIT;
  ROLLBACK;

  もしくは
  EXIT;




spool
=========================


::

  項目                     stdout   stderr   spool     制御方法
  -------
  接続後のメッセージ        ◯       ×       ×         △   -s (silent) で出なくなる
  SQL> プロンプト           ◯       ×       ×         ×   不可
  入力したSQL文             ◯       ×       ◯         ◯   set echo off     で stdout と spool 両方出なくなる (default:off)
  &置換の旧新(old/new)      ◯       ×       ◯         ◯   set verify off   で stdout と spool 両方出なくなる
  SQLの結果                 ◯       ×       ◯         ◯   set termout off  で stdout に出なくなる。 spool には出る
  SQLの結果の件数           ◯       ×       ◯         ◯   set feedback off で stdout と spool 両方出なくなる
  エラーメッセージ          ×       ◯       ◯         △   whenever sqlerror



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


