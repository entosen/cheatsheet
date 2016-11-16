# Windows バッチファイル チートシート


## 参考リンク

- [開発に役立つ，BATファイルの書き方・パターン集　（コマンドプロンプトの定石を体系的に学び，バッチ中級者になろう） - 主に言語とシステム開発に関して](http://language-and-engineering.hatenablog.jp/entry/20130502/PatternsOfMSDOSorBAT)


## 基本のテンプレ

```bat
@echo off



```

## 文法・お約束てきなこと

```
rem コメント


```

## 起動・呼び出し

```bat
rem start は、別プロセスで起動。終了を待たない。(Unix の & つけて実行みたいな感じ)
rem 第1引数は黒画面ウインドウのタイトルなので注意。
start "" "Paint.exe"
```

## 環境変数

```bat
rem 参照。 % で前後を囲う。
echo %Path%

rem 環境変数一覧の出力
set

rem セット
set AAA=BBB
```
