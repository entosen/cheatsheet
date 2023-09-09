===========================
ssh
===========================



known_hosts まわり
=============================

::

    ssh-keygen -F <hostname>     # (Find) known_hosts から hostname に属するhostkeyを表示する
    ssh-keygen -R <hostname>     # (Remove) known_hosts から hostname に属するhostkeyを削除する
    ssh-keygen -H                # (Hash) known_hosts を Hashed形式化する

