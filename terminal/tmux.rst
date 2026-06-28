##################################
tmux
##################################

ターミナルマルチプレクサー

GNU screen みたいなやつ

================================
チートシート
================================

::

   % tmux             # 新しいsessionの開始

   PREFIX c           # 新しいwindowを追加

   PREFIX 0〜9        # N番のwindowに切り替え
   PREFIX n           # 次のwindowに切り替え
   PREFIX p           # 前のwindowに切り替え
   PREFIX l           # 直前に選択していたwindowに切り替え
   PREFIX PREFIX      # (個人設定) 直前に選択していたwindowに切り替え

   PREFIX %           # 左と右に分割
   PREFIX "           # 上と下に分割

   PREFIX 方向キー    # pane の切り替え
   PREFIX C-方向キー  # pane のリサイズ(1ずつ)
   PREFIX M-方向キー  # pane のリサイズ(5ずつ)

   PREFIX d           # 現在のclientをdetach
   % tmux ls          # sessionの確認
   % tmux a                  # attach
   % tmux a -t <session名>   # attach



===========================
用語・概念
===========================

::

                   Server


    +--------+     attach    +----------+
    | client |---------------| session  |
    +--------+ 1..*       1  +----------+
                                  | 1..*
                                  |
                                  | 1..*
                             +----------+
                             | window   |
                             +----------+
                                  | 1
                                  |
                                  | 1..*
                             +----------+
                             |  pane    |
                             +----------+


client
    sessionをattachしているターミナル。

session
    attach/detachの単位。1つ以上のwindowに紐付いている。

window
    windowはターミナル領域全体を占める。
    切り替える。1度に1つのwindowが見えている。

pane
    windowをいくつかに分割した1つ。
    1つのpaneが1つの仮想端末。


================================
インストール
================================

::

  brew install tmux
  touch ~/.tmux.conf


====================================================
プレフィックスキー PREFIX (個人的な設定)
====================================================

デフォルトは C-b になっている。
が、遠くて押しづらいのと、vimのキーバインドとかぶるので、 C-a に変える。
かつ、 C-a C-a で直前にいたwindowを選択、 C-a a でプロセスに C-a が渡るように設定する。

::

  set -g prefix C-a      # PREFIX を C-a にする
  bind a send-prefix     # C-a a でプロセスに C-a を送る
  bind C-a last-window   # C-a C-a で直前のウィンドウ
  unbind C-b             # デフォルトの PREFIX 関連のバインドを解除



====================================================
操作
====================================================


session
================

新しいセッション::

  % tmux                 # コマンドを省略した場合は new-session (new)

  % tmux new [-s <session-name>] [-n <window-name>]  # session名、window名を指定

既にsession内にいるときには new-session はエラーになる。

名前::

  PREFIX $                   # 現在のsessionの名前を変更


デタッチ・アタッチ・切り替え::

  PREFIX d       # デタッチ detach-client(detach)

  % tmux ls                 # session一覧の確認 list-session (ls)
  % tmux a -t <session>     # アタッチ (attach-session, attach, aでも可)
  % tmux a                  # デタッチされているsessionの中で一番最近まで使っていたものをアタッチ

  PREFIX s       # インタラクティブにsessionを切り替え (choose-tree -Zw)


window
================

新しいwindow::

  PREFIX c                   # new-window (neww)  新しいwindowでシェルを開始。
  % tmux neww                # 新しいwindowでシェルを起動
  % tmux neww vim main.c     # 新しいwindowでコマンドを実行することもできる

名前::

  PREFIX ,                   # 現在のwindowの名前を変更

カレントディレクトリがどうなるか::

  PREFIX c            →  cwd は sessionのcwdになる (*)
  PREFIX : neww       →  cwd は sessionのcwdになる 
  % tmux neww         →  cwd はこれを実行したシェルのcwdになる

  (*)これ面倒なので、設定でpaneのcwdで開くように設定する
    # 新規window, 新規pane は、現在のpaneのカレントディレクトリを引き継ぐようにする
    bind c new-window -c '#{pane_current_path}'
    bind '%' split-window -h -c '#{pane_current_path}'
    bind '"' split-window -v -c '#{pane_current_path}'


切り替え::

  PREFIX 数字        # N番のwindowを切り替え (select-window -t :=0)
  PREFIX '           # 番号を指定してwindowを切り替え。10番以上を指定するときなど。
  PREFIX n           # 次のwindowに切り替え  (next-window)
  PREFIX p           # 前のwindowに切り替え  (previous-window)
  PREFIX l           # 直前にいたwindowに切り替え (last-window)

  PREFIX M-n         # Move to the next window with a bell or activity marker.
  PREFIX M-p         # Move to the previous window with a bell or activity marker.

  PREFIX w           # Choose the current window interactively.


window順の変更::

  PREFIX .           # window位置を変更。番号指定。行き先が空いていないとダメ。

  # swap-window (swapw)  windowの位置を交換。
  # swap-window [-d] [-s src-window] [-t dst-window]

    -s を省略した場合、マークしたpaneがあればそのwindow、なければ current window 。
    -d を省略した場合は？ TODO

  # move-window (movew)

kill::

  PREFIX &           Kill the current window.


pane
===================

分割してpaneの作成::

  PREFIX "           Split the current pane into two, top and bottom. (split-window)(splitw)
  PREFIX %           Split the current pane into two, left and right. (split-window -h)



切り替え::

  PREFIX Up, Down
         Left, Right
              矢印でpaneを切り替え

  PREFIX ;    直前にいたpaneに切り替え


  C-o         Rotate the panes in the current window forwards.
  M-o         Rotate the panes in the current window backwards.
  z           Toggle zoom state of the current pane.
  {           Swap the current pane with the previous pane.
  }           Swap the current pane with the next pane.

  C-Up, C-Down
  C-Left, C-Right
              Resize the current pane in steps of one cell.
  M-Up, M-Down
  M-Left, M-Right
              Resize the current pane in steps of five cells.

  m           Mark the current pane (see select-pane -m).
  M           Clear the marked pane.


  x           Kill the current pane.

  !           現在のペインを新しいウィンドウに独立させる


ターゲット
=======================

``-t`` オプション (場合によっては ``-s`` オプション) で、ターゲットを指定できる。
target-client, target-session, target-window, target-pane のいずれか。

target-client
----------------

client pty名で指定する。

例えば、 ``/dev/ttyp1`` または ``ttyp1`` 。

未指定の場合、現在使われているclient。

client一覧は ``list-clients`` (``lsc``) コマンドで分かる。


target-session 
-------------------

下記の順でチェックされる

1. ``$`` を前置したセッションID。
2. セッションの完全一致名 （list-sessions, ls コマンドで表示される名前）。
3. セッション名の先頭部分。たとえば「mysess」は「mysession」というセッションに一致する。
4. セッション名に対して glob(7) パターンとして照合される。

セッション名の先頭に「=」を付けた場合は、完全一致のみが受け付けられる

一致するセッションが 1 つだけ見つかった場合は、それが対象セッションとして使用される。

複数一致した場合はエラーとなる。

セッションが省略された場合、

- 利用可能であれば現在のセッションが使用され、
- それが存在しない場合は、直近で使用されたセッションが選択される。


target-window
--------------------

target-window (or src-window or dst-window) は ``session:window`` の形式で指定する。
session の解釈規則は target-session と同じで、
window は下記の順でチェックされる

1. 下記に示す特別なトークン。
2. window番号 (window index) 例: "``mysession:1``"は ``mysession`` のウィンドウ 1番。
3. ウィンドウ ID。例: ``@1`` 。
4. ウィンドウ名の完全一致。 例: "``mysession:mywindow``"。
5. ウィンドウ名の先頭一致。 例: "``mysession:mywin``"。
6. ウィンドウ名に対する glob(7) パターン。

セッションと同様に、「=」を前置すると完全一致のみが行われる。

ウィンドウ名が空の場合、

- 次に未使用のインデックス (適切であれば。 例: new-window や link-window コマンド）
- そうでなければ、そのセッションの現在のウィンドウが選択される。

以下の特別なトークンを用いて、特定のウィンドウを指定できる。
各トークンには 1 文字の代替表現がある。

::

  トークン            意味
  {start}       ^    最も小さい番号のウィンドウ
  {end}         $    最も大きい番号のウィンドウ
  {last}        !    直前（以前に現在だった）ウィンドウ
  {next}        +    番号順で次のウィンドウ
  {previous}    -    番号順で前のウィンドウ


target-pane
--------------

session と window は名前を持つことができるが、pane は名前を持つことができない。
なので、番号(index)かIDで指定する。

target-pane（または src-pane、dst-pane）はペイン ID (``%123``) を指定するか、
target-window と同様の形式に、ピリオドとペインインデックスまたは
ペイン ID を追加した形式を取る。例::

  mysession:mywindow.1
  mysession:mywindow.@123

ペインインデックスが省略された場合は、
指定されたウィンドウ内の現在アクティブなペインが使用される。

ペインインデックスには、以下の特別なトークンを使用できる。::

  トークン                意味
  {last}            !    直前（以前にアクティブだった）ペイン
  {next}            +    番号順で次のペイン
  {previous}        -    番号順で前のペイン
  {top}                  最上部のペイン
  {bottom}               最下部のペイン
  {left}                 最も左のペイン
  {right}                最も右のペイン
  {top-left}             左上のペイン
  {top-right}            右上のペイン
  {bottom-left}          左下のペイン
  {bottom-right}         右下のペイン
  {up-of}                現在のペインの上にあるペイン
  {down-of}              現在のペインの下にあるペイン
  {left-of}              現在のペインの左にあるペイン
  {right-of}             現在のペインの右にあるペイン

  「+」および「-」トークンにはオフセットを続けることができる。
     例:
       select-window -t:+2

その他
------------------

さらに、target-session、target-window、target-pane は、
トークン "``{mouse}``"（代替表現 "``=``"）のみで構成することもできる。

これは、直近のマウスイベントが発生した
セッション・ウィンドウ・ペインを指定するためのものである
（MOUSE SUPPORT セクションを参照）。

また、"``{marked}``"（代替表現 "``~``"）を指定することで、
マークされたペインを指定できる
（select-pane -m を参照）。


セッション、ウィンドウ、ペインにはそれぞれ一意な ID が割り当てられる。

- セッション ID は「$」、
- ウィンドウ ID は「@」、
- ペイン ID は「%」で始まる。

これらの ID は tmux サーバ内で一意であり、
セッション・ウィンドウ・ペインの存続期間中は変更されない。
ペイン ID は、TMUX_PANE 環境変数として
ペインの子プロセスに渡される。
ID は「session_id」「window_id」「pane_id」というフォーマット
（FORMATS セクションを参照）や、
display-message、list-sessions、list-windows、
list-panes コマンドを使って表示できる。




キーバインド
===================

::

  list-keys -T prefix     # prefix 関連のキーバインド一覧を表示


===================
以下未整理
===================

::

  ---

  (全体的)
  C-b         Send the prefix key (C-b) through to the application.

  ?           List all key bindings.

  :           Enter the tmux command prompt.

  ~           Show previous messages from tmux, if any.

  (client)
  d           Detach the current client.
  C-z         Suspend the tmux client.


  (session)
  $           Rename the current session.
  (           Switch the attached client to the previous session.
  )           Switch the attached client to the next session.



  (copy mode)
  [           Enter copy mode to copy text or view the history.
  ]           Paste the most recently copied buffer of text.
  Page Up     Enter copy mode and scroll one page up.

  (buffer)
  #           List all paste buffers.
  =           Choose which buffer to paste interactively from a list.
  -           Delete the most recently copied buffer of text.

  (TODO)
  .           Prompt for an index to move the current window.
  D           Choose a client to detach.
  L           Switch the attached client back to the last session.
  f           Prompt to search for text in open windows.
  i           Display some information about the current window.
  o           Select the next pane in the current window.
  q           Briefly display pane indexes.
  r           Force redraw of the attached client.
  s           Select a new session for the attached client interactively.
  t           Show the time.
  M-1 to M-7  Arrange panes in one of the seven preset layouts: even-horizontal, even-vertical, main-
         horizontal, main-horizontal-mirrored, main-vertical, main-vertical-mirrored, or tiled.
  Space       Arrange the current window in the next preset layout.






  コマンド

  コマンド実行方法::

    # キーに割り当てる
    bind-key C set-option -g status-style bg=cyan

    # tmux のコマンドプロンプト
    PREFIX :
    set-option -g status-style bg=cyan

    # シェルから
    tmux set-option -g status-style bg=cyan

    # ~/.tmux.conf
    set-option -g status-style bg=cyan



