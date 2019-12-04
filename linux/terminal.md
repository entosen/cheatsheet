
## console_codes

いわゆるエスケープシーケンス

参考
- [ANSI escape code - Wikipedia(en)](https://en.wikipedia.org/wiki/ANSI_escape_code)
- man 4 console_codes
- [console_codes - スペシャルファイル (デバイス)の説明 - Linux コマンド集 一覧表](https://kazmax.zpp.jp/cmd/c/console_codes.4.html)

### ウィンドウタイトルを変更

OSC というグループの機能でできる。
ST のところは本来は、`ESC \` だが、xterm は BEL(`\a`, `\007`) でもいける。

```
ESC ] 0 ; txt ST 	アイコン名とウインドウタイトルを txt に セットする。
ESC ] 1 ; txt ST 	アイコン名を txt にセットする。
ESC ] 2 ; txt ST 	ウインドウタイトルを txt にセットする。
```

- ウインドウタイトル --- ウインドウが表示されているときのタイトル
- アイコン名 --- ウインドウが最小化されているときのタイトル
- putty の場合は、設定に Window ＞ Behaviour > Separate window and icon titles があり、
    - off --- 最小化したときにもウインドウタイトルが使われる
    - on  --- 最小化したときにはアイコン名が使われる

ウィンドウタイトルを変更するシェルスクリプト
```
title="hogehoge"
printf "\033]0;$title\a"
```

TODO 日本語は行ける？


## GNU screen と tmux

### 違い

参考

- [tmuxに慣れてみる: tmuxとGNU screenの違いなど](https://rcmdnk.com/blog/2015/01/02/computer-tmux-screen/) 
  の図がわかりやすい。


ほとんど同じ。
分割した場合に違いがある。
分割の考え方が違う。

screen は、分割した中に、表示する仮想端末を選択する。

- セッション
    - 分割の設定(１つ)
    - 仮想端末(１つ以上)
    - 分割の各領域と仮想端末の紐づけ
      ( `^A n` とか `^A p` で切り替えるのはこの紐づけ)

tmux は、切り替えの単位(window)の中を分割する。

- セッション
    - window ( `^b n` とか `^b p` で切り替える単位)
	- 分割
	    - 仮想端末

自分の使い方だと screen の方が好きかも。

### GNU screen

#### チートシート

```
a           ^a を送信
?           現在のキーバインドを表示

c ^c        新規window作成
:number 数字      現在のwindowを数字に移動する

0～9        window切り替え
^a          直前のwindowに切り替え
n sp ^n     次の番号のwindowに切り替え
p ^p        前の番号のwindowに切り替え
'           指定の番号のwindowに切り替え
"           window一覧から選択して切り替え

A           windowのタイトルを設定する
w ^w        タイトル一覧をステータス行に表示

C           端末のクリア[
Z           端末のリセット

z ^z        サスペンド
d           デタッチ

S           横切り分割 曰
Q           分割解除。現在のwindowのみを表示。
tab         分割のフォーカスを移動
```

#### window番号を 1 始まりにする。

参考

- [GNU Screen - ArchWiki#Start_at_window_1](https://wiki.archlinux.org/index.php/GNU_Screen#Start_at_window_1)
- [GNU Screen - ArchWiki(日本語)#ウィンドウ1から起動](https://wiki.archlinuxjp.org/index.php/GNU_Screen#.E3.82.A6.E3.82.A3.E3.83.B3.E3.83.89.E3.82.A61.E3.81.8B.E3.82.89.E8.B5.B7.E5.8B.95)

```
bind c screen 1
bind ^c screen 1
bind 0 select 10                                                            
screen 1
```

ただし、これだと `C-a c` でやる場合は大丈夫だが、`screen vim prog.c` とかでやると 0 にできてしまう。
0番に何かダミーのwindowを指定しておくか？

### tmux
