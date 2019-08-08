# コマンド例を書く際の標準的な書き方

## 書き方

いきなり例
```
usage: git [--version] [--help] [-C <path>] [-c <name>=<value>]
           [--exec-path[=<path>]] [--html-path] [--man-path] [--info-path]
           [-p | --paginate | -P | --no-pager] [--no-replace-objects] [--bare]
           [--git-dir=<path>] [--work-tree=<path>] [--namespace=<name>]
           <command> [<args>]
```


- 修飾なし
    - そのまま書いてあるとおりに入力すべきもの
- `<var>` もしくは斜体
    - プレースホルダ変数。実行者が適切に指定するもの。
- `[  ]`
    - 任意に指定。省略可
- `{ | }` `[ | ]`
    - 相互に排他的な引数
- `...`
    - 繰り返すことができる引数


## コマンドプロンプト

基本的に `$` で統一。

- 1行のコマンドを表示する場合、コマンドプロンプト（$記号）はオプションです。
- ただし、ページに複数行と1行の両方のコマンドが含まれる場合、一貫性を保つために、
  ページ上のすべてのコマンドにコマンドプロンプトを使用することをお勧めします。
- コマンドライン命令に入力行と出力行の組み合わせが含まれる場合、
  入力と出力に別々のコードブロックを使用することをお勧めします。


## 参考

- Documenting command-line syntax  |  Google Developer Documentation Style Guide  |  Google Developers
    https://developers.google.com/style/code-syntax
- コマンド構文の表記規則についてメモ - tasuwo blog
    http://tasuwo.github.io/blog/2015/03/18/biao-ji-gui-ze/
- コマンド構文規則
    http://publib.boulder.ibm.com/tividd/td/TRM/GC32-1320-00/ja_JA/HTML/cmdref18.htm



