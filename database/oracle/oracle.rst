

初期設定
------------------------------

::

  -- プロンプト系
  set time on

  -- SET SQLPROMPT "SQL> "
  -- SET SQLPROMPT '_USER@_CONNECT_IDENTIFIER> '   -- ちと長い。


  -- 日付時刻フォーマット
  ALTER SESSION SET nls_date_format = 'YYYY/MM/DD HH24:MI:SS';
  ALTER SESSION SET nls_timestamp_format = 'YYYY/MM/DD HH24:MI:SS';


  SET PAGESIZE 100
  SET LINESIZE 300
  SET NUMWIDTH 11
  SET TAB OFF       -- タブをスペースに
  SET WRAP OFF      -- 折り返し禁止
  SET SQLblanklines on

  -- セッションスキーマを変える
  ALTER SESSION SET CURRENT_SCHEMA = other_schema;


接続先確認
-------------------------------

::

  -- ログインユーザー
  SELECT USER FROM dual;

  -- 接続先確認
  SELECT
    sys_context('USERENV','SESSION_USER')        AS session_user,   -- ログインユーザー
    sys_context('USERENV','CURRENT_SCHEMA')      AS current_schema, -- 現在のセッションスキーマ
    sys_context('USERENV','DB_NAME')             AS db_name,
    sys_context('USERENV','SERVICE_NAME')        AS service_name,
    sys_context('USERENV','CON_NAME')            AS container_name,
    sys_context('USERENV','HOST')                AS host_name
  FROM dual;


テーブルとかいろんな一覧
------------------------------

シノニム::

  -- 自分が所有しているシノニム
  SELECT synonym_name, table_owner, table_name, db_link FROM user_synonyms
  ORDER BY table_owner, table_name, synonym_name;

  -- 自分がアクセス可能なシノニム (自分所有＋PUBLIC＋権限あり)
  SELECT owner, synonym_name, table_owner, table_name, db_link FROM all_synonyms
  ORDER BY owner, table_owner, table_name, synonym_name;

  -- すべてのシノニム(DBA権限)
  SELECT owner, synonym_name, table_owner, table_name, db_link FROM dba_synonyms
  ORDER BY owner, table_owner, table_name, synonym_name;



DBLink::

  -- 自分が所有している DB Link 一覧（一般ユーザー）
  SELECT db_link, username, host, created FROM user_db_links;
  -- 自分がアクセス可能な DB Link 一覧（権限あり）
  SELECT owner, db_link, username, host FROM all_db_links;
  -- すべての DB Link 一覧（DBA権限）
  SELECT owner, db_link, username, host FROM dba_db_links;


MView
--------------------

MView::

  SELECT mview_name, refresh_method, refresh_mode, last_refresh_type, last_refresh_date, staleness
  FROM user_mviews
  ORDER BY mview_name;

  SELECT owner, mview_name, refresh_method, refresh_mode, last_refresh_type, last_refresh_date, staleness
  FROM all_mviews
  ORDER BY owner, mview_name;

  SELECT owner, mview_name, refresh_method, refresh_mode, last_refresh_type, last_refresh_date, staleness
  FROM dba_mviews
  ORDER BY owner, mview_name;

更新ジョブ::

  select owner, job_name, enabled, next_run_date, last_start_date, last_run_duration
  order by owner, JOB_NAME;

  EXEC DBMS_SCHEDULER.DISABLE('JOB_HOGEHOGE');

  EXEC DBMS_MVIEW.REFRESH('M_HOGEHOGE', 'C');

  EXEC DBMS_SCHEDULER.ENABLE('JOB_HOGEHOGE');



権限系
-------------------------------

確認::

  alter session set nls_date_format='YYYY/MM/DD HH24:mi:SS';
  SET PAGESIZE 100
  SET LINESIZE 300
  SET NUMWIDTH 11

  column username format a30;
  column account_status format a30;
  column grantee format a30;
  column granted_role format a30;

  SELECT username, account_status, created
  FROM dba_users
  WHERE username IN ('USER1', 'USER2');

  SELECT grantee, granted_role
  FROM dba_role_privs
  WHERE grantee IN ('USER1', 'USER2')
  ORDER BY grantee, granted_role;

アカウント作成(CREATE_USER)::

  DEFINE USERNAME = USER1
  DEFINE PASS     = TempPass1234_
  CREATE USER &USERNAME IDENTIFIED BY "&PASS" PASSWORD EXPIRE;
  GRANT ROLE1, ROLE2 TO &USERNAME;





アカウントロックの解除方法
-------------------------------


確認::

  SELECT USERNAME, ACCOUNT_STATUS FROM DBA_USERS WHERE USERNAME = 'FOO';

  +--------+--------------+
  |USERNAME|ACCOUNT_STATUS|
  +--------+--------------+
  |FOO     |OPEN          |
  +--------+--------------+
  
  - OPEN             正常
  - LOCKED(TIMED)    パスワードの繰り返し入力ミスのため、ロック。何日かすると外れる。

LOCK解除::

  ALTER USER FOO ACCOUNT UNLOCK;
  
