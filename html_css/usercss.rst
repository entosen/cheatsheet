==========
UserCSS
==========

Chrome や Firefox で、User CSS を適用できる `Stylus`_ で使う UserCSS 形式についてまとめる。

.. _`Stylus`: https://github.com/openstyles/stylus


参考

- `UserCSS <https://github.com/openstyles/stylus/wiki/Usercss>`_
- `Writing styles <https://github.com/openstyles/stylus/wiki/Writing-styles>`_
- `Writing UserCSS <https://github.com/openstyles/stylus/wiki/Writing-UserCSS>`_


サンプル
========================

::

    /* ==UserStyle==
    @name         Example UserCSS style
    @namespace    github.com/openstyles/stylus
    @version      1.0.0
    @license      unlicense
    @preprocessor default
    @var color link-color "Link Color" red
    ==/UserStyle== */

    @-moz-document domain("example.com") {
      a {
        color: var(--link-color);
      }
    }


コメント
=====================

``/*``, ``*/`` のみらしい。

::

    /* この間がコメントして扱われる */

    /*
        複数行でもいいよ
        複数行でもいいよ
    */


``//`` は使えない。


Metadata
=======================

少なくとも ``@name``, ``@namespace``, ``@version`` は必須。 

あと公開するなら普通は ``@license`` もつける。

::

    /* ==UserStyle==
    @name         Google Dark
    @namespace    github.com/entosen/userscript
    @version      1.0.0
    @license      MIT
    @description  make Google Dark
    @author       My Name <my-email@my-site.com> (http://my-site.com)
    @homepageURL  https://github.com/entosen/userscript/
    @supportURL   https://github.com/entosen/userscript/issue
    @updateURL    https://raw.github.com/entosen/userscript/hoge/hoge.user.css
    ==/UserStyle== */


- ``@name`` と ``@namespace`` でユニークになるようにする
- ``@name``

  - 「どのサイトををどうする」ぐらいの意味は含めておくのがよいと思う
  - Stylus の管理画面の一覧に出る。
  - 変えると管理上別CSS扱いになるので、容易に変えられない。

- ``@namespace``

  - ユニークになりさえすれば良い
  - ドメインとか、githubのユーザーやリポジトリ、メールアドレスあたりでいいと思う
  - ::

        @namespace    github.com/openstyles/stylus

- ``@version``

  - セマンティックバージョンニング ( ``1.0.0`` みたいな)


- ``@license``

    - `SPDX License List <https://spdx.org/licenses/>`_ から書く


- ``@description``

  - 短い説明

- ``@author``

  - 下記のような感じで書く::

        @author My Name <my-email@my-site.com> (http://my-site.com)

  - email と URL は省略可

- ``@homepageURL``

  - 指定しておけば、管理画面などにリンクができる。

- ``@supportURL``

  - 指定しておけば、"Feedback" リンクができる

- ``@updateURL``

  - updateを確認しにいくURL
  - 指定するなら、rawで表示されるURLでないといけない
  - 指定しない場合、実際にインストールした際のURLが使われる
  - 指定しておくのが吉。(後述の「開発時のTips」)








適用先サイトの指定 @-moz-doument
===========================================


指定の仕方は4つ

- ``domain`` --- URLのドメイン部分が、指定のドメインおよびそのサブドメインなら適用。(プロトロルは含まない)
- ``url`` --- URL全体の完全一致 (プロトコル部分から)
- ``url-prefix`` -- URL全体の前方一致 (プロトコル部分から)
- ``regexp`` -- 正規表現


domain
------------

URLのドメイン部分(プロトコル部分、ポート部分は含まれない)にマッチ。
それが指定のドメインか、そのサブドメインだった場合に適用。

ワイルドカード的なものは使えない。

::

    @-moz-document domain("example.com")    /* --> www.example.com などのサブドメインが付いてもマッチする */
    @-moz-document domain("www.example.com")


url
---------------

URL(プロトコル部分から末尾まで)の完全一致。

::

    @-moz-document url("http://www.example.com/page.html")

ただし、アンカー( ``#`` )に関しては特殊扱いがある。::

    /* アンカーまで指定した場合は、そのアンカーまで一致しないとマッチしない */
    @-moz-document url("http://example.com/page.html#firstheading")
        → http://example.com/page.html にはマッチしない

    /* アンカーが指定されてない場合は、任意のアンカーがついてもマッチする */
    @-moz-document url("http://example.com/page.html")
        → http://example.com/page.html#firstheading にマッチする


url-prefix
------------------

URL(プロトロル部分から)の前方一致。

ワイルドカード的なものは使えない。

::

    @-moz-document url-prefix("http://www.example.com/")
    @-moz-document url-prefix("http://www.example.")
    @-moz-document url-prefix("http:")


regexp
--------------------

正規表現でマッチ

- URL全体にマッチしないといけない。前後に自動的に ``^``, ``$`` がつくと考える。
- ``@-moz-document regexp("...")`` のダブルクオートの中に書く場合は、
  もう一段ダブルクオート文字列としてのエスケープが必要になる。 (バックスラッシュが2つになる)。
  一方、Stylusエディタの "applies to" 欄に書く場合は、それは不要。
- ``/`` スラッシュはクオート不要
- ``.`` は本来はバックスラッシュエスケープすべき(でないと任意文字にマッチしてしまう)。
  だがたいていのケースではそれが問題になることは少ない。


::

    @-moz-document regexp("http://www\\.example\\.(com|de|org)/images/.*")
    @-moz-document regexp("https?://www\\.(example|test)\\.com/")

    /* 否定先読み */
    @-moz-document regexp("(?!https://(www\\.aaa\\.com|www\\.bbb\\.com|ccc\\.org)/).*")
    @-moz-document regexp("http://www\\.example\\.com/(?!members).*")



その他
--------

カンマで並べると or 結合::

    @-moz-document domain("images.example.com"),
                   domain('imagehost.com'),
                   url-prefix(https://example.com/images),
                   url(https://www.example.com/test.html) {
        ...
    }




開発時のTips
=================================

Stylus を使っている場合、Stylusのエディタを使ってもよいのだが、
使い慣れた vim などのエディタを使う場合は、下記のようにやる。


- github から clone したきて手元にある ``.user.css`` ファイルを、ブラウザに DnD 
- (再)インストール画面になる。一旦インストール。
- 管理画面になる。「自動リロード」を有効にすると、エディタの方を保存すると自動反映する。
- エディタで編集、動作確認、を繰り返す
- 決まったら、管理画面を閉じる (自動リロードは無効になる)

注

- 自動リロードは、インストール直後の管理画面でしか出ない
- CSS内で ``@updateURL`` をセットしておけば、この方法をやっても更新チェックはgitの方を見てくれる



