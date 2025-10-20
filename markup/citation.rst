====================================
引用の表現
====================================

引用、出典、参考文献 などを各markupでどのように表現するのがよいか。


HTMLで引用
-------------------

blockquoteタグ

::

  <div>
    <blockquote cite="https://www.huxley.net/bnw/four.html">
      <p>
        Words can be like X-rays, if you use them properly—they’ll go through
        anything. You read and you’re pierced.
      </p>
    </blockquote>
    <p>—Aldous Huxley, <cite>Brave New World</cite></p>
  </div>

- 引用元のURLは blockquote タグの cite 属性にセット
- 引用元のテキストでの表示は blockquote タグの外側直後に cite タグで置く





参考にしたサイト

- `<blockquote>: ブロック引用要素 - HTML | MDN <https://developer.mozilla.org/ja/docs/Web/HTML/Reference/Elements/blockquote>`_
- `<cite>: 引用元要素 - HTML | MDN <https://developer.mozilla.org/ja/docs/Web/HTML/Reference/Elements/cite>`_



reStructuredTextで引用
------------------------

ブロック引用
^^^^^^^^^^^^^^^^

reStructuredText では、まわりのテキストよりインデントが深いブロックが
ブロック引用になる。

ブロック末尾に ``--`` または ``---`` で始まる段落は、引用元を表す。


::

  This is an ordinary paragraph, introducing a block quote.

      "It is my business to know things.  That is my trade."

      -- Sherlock Holmes


参考

- https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#block-quotes


引用参照
^^^^^^^^^^^^^^

参考文献を示すような書き方。

::

  Here is a citation reference: [CIT2002]_.

  .. [CIT2002] 引用元の情報

ここにはリンクは書けないか？





Markdown で引用
-------------------

`gihyo.jp編集部におけるMarkdown記法 | gihyo.jp <https://gihyo.jp/article/2022/08/gihyojp-markdown>`_ では

::

  ### 本文見出し

  段落。段落。段落。段落。段落。段落。段落。

  > #### 引用文内見出し
  >
  > 引用。引用。引用。引用。引用。引用。引用。
  >
  > 引用。引用。引用。引用。引用。引用。引用。

  段落。段落。段落。段落。段落。段落。段落。


引用元を明示したい場合には::

  段落。段落。段落。段落。段落。段落。段落。

  > 引用。引用。引用。引用。引用。引用。引用。

  引用元：『書名』（技評太郎 著、技術評論社、2016；p. 20）

  段落。段落。段落。段落。段落。段落。段落。












