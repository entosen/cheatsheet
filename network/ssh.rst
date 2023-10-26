===========================
ssh
===========================



known_hosts まわり
=============================

::

    ssh-keygen -F <hostname>     # (Find) known_hosts から hostname に属するhostkeyを表示する
    ssh-keygen -R <hostname>     # (Remove) known_hosts から hostname に属するhostkeyを削除する
    ssh-keygen -H                # (Hash) known_hosts を Hashed形式化する


(注) ポートが異なれば別ホストとして扱われる。表記法は下記::

    ポート番号が付かない場合 (デフォルトの22番ポートを意味する)
    hoge.example.com

    ポート番号が付く場合は角括弧で囲む
    [host.example.com]:443

ref. sshd(8)
