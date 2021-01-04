=========================
PDFjam
=========================

概要
==============

- PDFjam

  - https://ctan.org/tex-archive/support/pdfjam
  - texliveってやつに含まれている
  - 内部で `pdfpages`_ というのを使っている

.. _`pdfpages`: https://ctan.org/pkg/pdfpages

制限

- pdfjamで出力されるpdfファイルは、全てのページが同じサイズ・向きに限られる。

インストール方法::

    sudo apt install texlive-extra-utils

ドキュメント

- ``pdfjam --help``
- それと pdfpages のオプションが使えるので、それについては下記参照

  - http://ftp.jaist.ac.jp/pub/CTAN/macros/latex/contrib/pdfpages/pdfpages.pdf


使い方
==============

基本、入力ファイル、ページ指定、出力ファイル::

    pdfjam [OPTION [OPTION] ...] [SRC [PAGESPEC] [SRC [PAGESPEC]] ...]

    # 入力ファイル(複数可) と 出力ファイルを指定する。
    # 2つのpdfを連結した結果が出力される。
    pdfjam file1.pdf file2.pdf --outfile myNewFile.pdf

    # ページ指定
    pdfjam file1.pdf '{},2-' file2.pdf '10,3-6' --outfile myNewFile.pdf

        3,5,6,8    1ページずつ指定
        4-9        範囲指定
        -9         最初から9ページ目まで
        4-         4ページ目から最後まで
        -          全ページ
        {}         空ページを挿入

        ページ指定なしの場合は全ページになる (この点pdfpagesと違う？)

    # 複数ファイルのページ指定はちょっと癖ある
    file1 file2 file3 1-7
        各ファイルの1-7ページが処理される
    file1 file2 2- file3 1-7
        file1 と file2 は2ページ目以降、file3 は 1-7ページが処理される

    パイプする場合、/dev/stdin や /dev/stdout を使う。
    `-` はページ指定になるため。
    入力ファイルが1つも指定されていないときは /dev/stdin を読み込む



    # それぞれ出力 (--batch と --suffix)
    pdfjam --batch --suffix 2up --nup 2x1 --landscape file1.pdf file2.pdf
        # → file1-2up.pdf, file2-2up.pdf が出力される

    # --outfile にディレクトリを指定した場合も、それぞれ出力になる？
    pdfjam --suffix 2up --nup 2x1 --landscape file1.pdf file2.pdf --outfile OutDir


N-up::

    --nup 3x2     # 縦に3つ、横に2つに並べる
                  # pdfpages のオプションでページを流す向きや、表紙の扱いなどを指定できる

    特に指定がなければ、マージンやパディングはされない。
    縦横比は保持したまま、指定の個数をタイル上に並べて、
    出力サイズ・向きにおさまる最大のサイズに拡大縮小される。

    --delta '10mm 20mm'    # 横のタイルとの間隔、縦のタイルとの間隔

    --noautoscale true     # もとのサイズを保持する

    
出力のサイズ、向きを変える::

    --a4paper
    --a3paper

    --landscape     横向き
    --no-landscape  縦向き

    デフォルトは --a4paper --no-landscape ?

その他オプション::

    --frame true
        (nupやscaleする前の)ページの外側に枠線をつける
    --scale 0.95
        (nupなどした後の全体)ページの拡大縮小する
    
Tips

- 基本的に上下左右の中央に置かれ、フィットするように拡大縮小される



