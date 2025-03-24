============================
reStructuredText Cheatsheet
============================

reStructuredText および sphinx の独自記法をまとめる

参考・リファレンス
************************

- `reStructuredText マークアップ仕様 — Docutils documentation in Japanese ドキュメント <https://docutils.sphinx-users.jp/docutils/docs/ref/rst/restructuredtext.html>`_
`reStructuredText ディレクティブ — Docutils documentation in Japanese 0.12 ドキュメント <https://docutils.sphinx-users.jp/docutils/docs/ref/rst/directives.html>`_
- `reStructuredText — Sphinx documentation <https://www.sphinx-doc.org/ja/master/usage/restructuredtext/>`__

概要
*************

テキストでも十分に見やすいことを重視しているので、
インデントやリストの番号など、結構厳密になっている。


見出し・セクション
********************

::

    #####################
    見出し1
    #####################

    *********************
    見出し2
    *********************

    見出し3
    ===========

    見出し4
    -----------

    見出し5
    ^^^^^^^^^^^

    見出し6
    """""""""""

* 記号を上下もしくは下に並べて装飾する。 ``= - ` : ' " ~ ^ _ * + # < >``
* 同じ記号でも、下だけと、上下両方は、別物扱い
* 特に順序は決まっておらず、登場した順に大きな見出しになる
* 全部で6レベル作ることができる。(6レベルしか作ることができない)

どの記号を使うか

* Python のドキュメンテーションスタイルガイドでは上の例が推奨
* sphinx のドキュメントでは下記の例が推奨::

    =====================
    セクション(レベル１)
    =====================

    レベル２
    ========

    レベル３
    --------

    レベル４
    ^^^^^^^^



インライン
*************

::

    *強調*             --- emタグ。斜体。
    **強い強調**       --- strongタグ。太字。
    `翻訳文`           --- siteタグ。斜体。  ???
    ``リテラル(等幅)`` --- ttタグ。等幅。

注意点

- インライン記法の前後には半角スペースか改行が必要
- インライン記法内にインライン記法は書けない
- 対象文字列の最初と最後に半角スペースは入れられません。 `* foo*` はNG。

インライン記法(ロール)

::

  :emphasis:`強調`
  :strong:`強い強調`
  :literal:`make html`
  :sub:`Sphinx`     下付き
  :sup:`Sphinx`     上付き
  :title:`Sphinx`   タイトル



早見表
**************

紛らわしい記述の早見表です。

::

  .. hogehoge::      --- ディレクティブ

  .. _hogehoge:                            --- 内部ハイパーリンクターゲット
  .. _`hogehoge`:                          --- 内部ハイパーリンクターゲット

  .. _ヤフー: https://www.yahoo.co.jp/     --- 外部ハイパーリンクターゲット
  .. _`ヤフー`: https://www.yahoo.co.jp/   --- 外部ハイパーリンクターゲット
  .. __: https://www.yahoo.co.jp/          --- 外部ハイパーリンクターゲット(無名)
  __ https://www.yahoo.co.jp/              --- これも。外部ハイパーリンクターゲット(無名)

  .. This is a comment                     --- 上記の形に合わなければ、コメント

コメント
****************

コメント::

  .. This is a comment
  ..
     _so: is this!
  ..
     [and] this!
  ..
     this:: too!
  ..
     |even| this:: !



ディレクティブ
********************

ディレクティブの一般的な形としてはこんな形::

  .. function:: foo(x)
                foo(y, z)
     :module: some.module.name

     Return a line of text input from the user.


- ディレクティブ名

  - function のところ。 ピリオドピリオド空白 名前 コロンコロン 。

- 引数

  - コロンコロンの後に続く。

- オプション
  
  - 空行を入れずに
  - フィールドリストの形式
  - インデントはディレクティブ名と揃える

- コンテンツ

  - 空行を入れて
  - インデントはディレクティブ名と揃える


リンク・参照
***************

ハイパーリンク参照
===================

名前付きハイパーリンク参照::

    この `ヤフー`_ はポータルサイトです。

    .. _`ヤフー`: https://www.yahoo.co.jp/

- 1行目が「名前付きハイパーリンク参照」
- 2行目が「ハイパーリンクターゲット」
- 名前に対応するターゲットがページのどこかに存在してないといけない
- 前後に空白を空けないといけないっぽい
- 名前に空白や記号を含まない場合は、バッククオートを省略できる


無名ハイパーリンク参照::

    ニュースサイトは `Yahoo!ニュース`__ 。

    .. __: https://news.yahoo.co.jp/
    もしくは
    __ https://news.yahoo.co.jp/

- 無名の場合は、参照とターゲットが出現順序で対応付けられる。個数が一致していないといけない。


ハイパーリンクターゲット
=============================

- 外部ハイパーリンクターゲット(コロンの後ろがURL)::

    .. _`Yahoo!知恵袋`: https://chiebukuro.yahoo.co.jp/

- 内部ハイパーリンクターゲット(コロンの後ろが空)

  - その直後の要素にアンカーを貼る::

      .. _`ほげほげについての説明`:

      ほげほげとは、こうこうこういうものである。

  - その直後の外部ハイパーリンクのエイリアスを作る::

      .. _`Yahoo! Japan Travel`:
      .. _`Yahoo!トラベル`: https://travel.yahoo.co.jp/

  - 連続する内部ハイパーリンクは連鎖する。つまり全て同じところを指す::

      .. _`ヤフーファイナンス`:
      .. _`Yahoo! JAPAN Finance`:
      .. _`Yahoo!ファイナンス`: https://finance.yahoo.co.jp/

- 間接ハイパーリンクターゲット(コロンの後ろがハイパーリンク参照)::

    .. _`Yahoo!映画`: eiga_
    .. _eiga: https://movies.yahoo.co.jp/

- 暗黙ハイパーリンクターゲット

  - セクションタイトル、脚注および引用によって自動的に生成される



埋め込み型
================

::

    See the `Python home page <http://www.python.org>`_ for info.

    See the `Python home page <http://www.python.org>`__ for info.

1つ目は↓と全く同じ::

    See the `Python home page`_ for info.

    .. _`Python home page`: http://www.python.org




リスト
*************

箇条書きリスト(bullet)と列挙リスト(enumerated list)
====================================================

- 前後に空行が必要
- 箇条書きリストは ``* + -`` で始める
- 列挙リストは、以下のメンバーと書式の組み合わせ

  - メンバーは 1,2,3,... / A,B,C,...Z / a,b,c,...,z / I,II,III,IV,... / i,ii,iii,iv,... / ``#`` など
  - 書式は ``1.``, ``(1)``, ``1)``

- 子リストは
  
  * インデントは、親の記号の後のテキストの開始位置に合わせる。ベースライン。
  * 前後に空行が必要

- 子リストに限らず、
  インデントを守っていれば任意のブロック要素をいくらでも書ける

  - ただし、複数段落になるアイテムが1つでもあると、
    全てのアイテムが段落扱いになり、``<p>`` で囲まれてしまう。


::

    - aaa
    - bbb

      - 子リスト。インデントはここ。
      - 子リスト。
        単一段落として折り返す場合は、インデントはここ。

      1. aaa
      2. bbb

    #. 自動で番号を振る
    #. 自動で番号を振る


複数段落も含められる

:: 

    - あああああああああ
      あああああああああ

      アイテム1の2段落目
    - アイテム2


定義リスト
=====================

::

    term 1
        Definition 1.

    term 2
        Definition 2, paragraph 1.

        Definition 2, paragraph 2.

    term 3 : classifier
        Definition 3.

    term 4 : classifier one : classifier two
        Definition 4.

- 用語と説明の間には空行を入れない (c.f. 入れると引用ブロックになってしまう)


フィールドリスト
=======================

::

    :gcc: 4.4.7-3.el6
    :make: 3.81-20.el6
    :openssl-devel: 1.0.0-27.el6_4.2
    :bzip2-devel: 1.0.5-7.el6_0


整形済みブロック系
*************************

リテラルブロック
========================

行末の ``::`` のあと、1行空け、インデントする。

::

    ::

        ここにコードなどを書く。
        ここにコードなどを書く。
        ここにコードなどを書く。

    もしくは、このようにしてもいい ::

        ここにコードなどを書く。
        ここにコードなどを書く。
        ここにコードなどを書く。


- ``::`` の前に空白を空けると、 ``:`` は表示されない
- ``::`` の前に空白がない場合、 1つの ``:`` が表示される

ソースコードハイライト
===========================

sphinxのみ。

::

  .. code-block:: python

     import os
     import sys
     from blockdiag.utils import images, unquote, urlutil, uuid, XY
     class Base(object):
         basecolor = (255, 255, 255)
         textcolor = (0, 0, 0)
         fontfamily = None
         fontsize = None
         style = None

対応している言語のリストは ``pygmentize -L`` 。


テキストブロック
***********************

引用ブロック
=======================

1行あけ、インデントする

::

    彼の発言は以下のようなものである。
        
        彼の発言。
        うんたらかんたら。

        複数段落も書ける。


警告メッセージなど
=========================

::

  .. note::
     :collapsible: closed

     段落。段落。
     ほげほげ。

::

  .. attention::     注意 (赤 (!))
  .. error::         エラー (赤 (x))
  .. hint::          ヒント (緑 (?))
  .. important::     重要 (オレンジ (炎))
  .. note::          注釈 (青 (鉛筆))
  .. tip::           Tip (緑 (i))
  .. warning::       警告 (オレンジ (!))

  .. caution::       注意 (オレンジ (稲妻))
  .. danger::        危険 (赤 (稲妻))

  .. seealso::       参考 (緑(i))

  .. admonition:: title      

::

  :collapsible:            --- 折り畳み可。初期状態 open (default)
  :collapsible: open       --- 折り畳み可。初期状態 open
  :collapsible: close      --- 折り畳み可。初期状態 close


テーブル
***********************

グリッドテーブル::

    +------------------------+------------+----------+
    | Header row, column 1   | Header 2   | Header 3 |
    +========================+============+==========+
    | body row 1, column 1   | column 2   | column 3 |
    +------------------------+------------+----------+
    | body row 2             | Cells may span        |
    +------------------------+-----------------------+


シンプルテーブル::

    ====================  ==========  ==========
    Header row, column 1  Header 2    Header 3
    ====================  ==========  ==========
    body row 1, column 1  column 2    column 3
    body row 2            Cells may span columns
    ====================  ======================


csvテーブル::

    .. csv-table:: Frozen Delights!
       :header: "Treat", "Quantity", "Description"
       :widths: 15, 10, 30

       "Albatross", 2.99, "On a stick!"
       "Crunchy Frog", 1.49, "If we took the bones out, it wouldn't be
       crunchy, now would it?"
       "Gannet Ripple", 1.99, "On a stick!"

listテーブル::

    .. list-table:: Frozen Delights!
       :widths: 15 10 30
       :header-rows: 1

       * - Treat
         - Quantity
         - Description
       * - Albatross
         - 2.99
         - On a stick!
       * - Crunchy Frog
         - 1.49
         - If we took the bones out, it wouldn't be
           crunchy, now would it?
       * - Gannet Ripple
         - 1.99
         - On a stick!

フィールドリストも表の代わりに使えるかも。


画像
******************

::

  .. image:: picture.png

::

  .. figure:: images/sphinx-logo.jpg

     Sphinx のロゴ             --- キャプション

     ホルスの目と呼ばれる古代エジプトのシンボルをモチーフとしています  --- 以下説明文
  

ページ構成
***************************

(sphinxのみ)

::

  .. toctree::

     purpose
     procedure
     verification

- ``.rst`` 拡張子は不要
- 相対パス。スラッシュで始めるとプロジェクトルートからの絶対パス。
- 各ファイルにはセクションがないといけない


sphinx のドキュメント構造は、セクション(の深さ)で決まる。
ディレクトリ構造とは別なので注意。
toctreeはファイルの読み込み順序を決めている感じ。

各ファイルのセクションの種類(記号や登場順序)は、そのファイルの中だけで有効。
toctreeで関係づけられたファイルは、toctree がある位置の子セクションとして読み込まれる。



