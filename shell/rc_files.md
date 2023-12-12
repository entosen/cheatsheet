# シェルの rc ファイル

## ログインシェルとは、インタラクティブシェルとは

参考ドキュメント

- [ログインシェルとインタラクティブシェルと~/.bashrc達の関係 - Qiita](https://qiita.com/incep/items/7e5760de0c2c748296aa)


- ログインシェル かつ インタラクティブシェル
    - `ssh user@host`  (未確認)
    - `su - [user]`  (未確認)
    - `bash --login`  (未確認)
    - `zsh -l`  (未確認)
    - Cygwin のターミナル起動した場合
    - macOS Terminal.app 新規ウインドウ/タブ  (未確認)
    - tmux 新規ウィンドウ  (未確認)
- 非ログインシェル かつ インタラクティブシェル
    - `su [user]`  (未確認)
    - `bash`  (未確認)
    - `zsh`  (未確認)
- 非ログインシェル かつ 非インタラクティブシェル
    - `su user -c /path/to/command`  (未確認)
    - `bash -c /path/to/command`  (未確認)
    - `zsh -c /path/to/command`  (未確認)
    - `ssh user@host /path/to/command`  (未確認)
    - シェルスクリプト起動  (未確認)
- ログインシェル かつ 非インタラクティブシェル
    - `bash --loging -c /path/to/command`  (未確認)
    - `zsh -l -c /path/to/command`  (未確認)


ログインシェル、かつ、非インタラクティブシェルというのは、
厳密には存在するのかもしれないが、ほとんど登場しない。


判定方法

ログインシェルかどうかの判定方法

- `shopt` コマンドの変数 `longin_shell` (bash ？)
    - `if ! shopt -q login_shell ; then 非ログインシェル ; fi`

インタラクティブシェルかどうかの判定方法

- 環境変数`PS1` が設定されている (man bash より)
- シェル変数 `$-` に `i` が含まれている (man bash より)



## zsh の rc ファイル

```
                         ログイン    非ログイン   非ログイン  ログイン
			 対話          対話        非対話      非対話
/etc/zshenv                ○           ○           ○          ○

~/.zshenv                  ○           ○           ○          ○

/etc/zshprofile            ○           ×           ×          ?
 
~/.zshprofile              ○           ×           ×          ?

/etc/zshrc                 ○           ○           ×          ×

~/.zshrc                   ○           ○           ×          ×

~/etc/zlogin               ○           ×           ×          ?
                                                       
~/.zlogin                  ○           ×           ×          ?
```

「zsh の本」では、 zshprofile は使わず、zlogin の方を使っていた。

`zsh --sourcetrace` ってやると、読み込んでいるファイルが分かる。




## bash の場合

```
                         ログイン    非ログイン   非ログイン  ログイン
			 対話          対話        非対話      非対話
/etc/profile               ○           ×           ×          ○

~/.bash_profile            ○           ×           ×          ○
~/.bash_login              ○           ×           ×          ○
~/.profile                 ○           ×           ×          ○
    ↑この３つは最初に見つかったファイルだけが読み込まれる

~/.bashrc                  ×※         ○           ×          ×
    ※通常、.bash_profile の中で .bashrc を source するように書くので、
      実質、ログイン時にも読み込まれることになる

/etc/bashrc                ×※         ×※         ×
    ※通常、.bashrc の中で /etc/bashrc を source するように書くので、
    実質 .bashrc 同様読み込まれる。
```

tips

rc系のファイルを読み込まないオプション

```
--noprofile
    システム全体用の起動ファイル /etc/profile 、
    および個人用の初期化ファイル ~/.bash_profile, ~/.bash_login, ~/.profile のいずれも読み込みません。
--norc
    シェルが対話的動作を行う場合に、個人用初期化ファイル ~/.bashrc の読み込み・実行を行いません。
--rcfile
    対話的シェルとして起動された場合、 個人用の標準の初期化ファイル ~/.bashrc の代わりに file からコマンドを実行します 
```

bash -v って起動すると、読み込んでいる rc ファイルとかコマンドがわかる。

