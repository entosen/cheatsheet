



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
  
