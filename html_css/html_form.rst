

参考

- `ウェブフォームの構成要素 - ウェブ開発を学ぶ | MDN <https://developer.mozilla.org/ja/docs/Learn/Forms>`_
- `<form>: フォーム要素 - HTML: ハイパーテキストマークアップ言語 | MDN <https://developer.mozilla.org/ja/docs/Web/HTML/Element/form>`__




::

  <form action="/my-handling-form-page" method="post>
  <ul>
    <li>
      <label for="name">Name:</label>
      <input type="text" id="name" name="user_name" />
    </li>
    <li>
      <label for="mail">Email:</label>
      <input type="email" id="mail" name="user_email" />
    </li>
    <li>
      <label for="msg">Message:</label>
      <textarea id="msg" name="user_message"></textarea>
    </li>
    <li class="button">
      <button type="submit">メッセージを送信</button>
    </li>
  </ul>
  </form>


用語
-------------

フォームコントロール
入力欄のこと。 input, textarea, button, などなど。


form
-------------

- action: 送信先のURL(相対パス)
- method: "get", "post"

name

各入力欄(inputなど)には name を付ける。送信時の key-value ペアの key になる。

fieldset, legend
----------------------

::

  <form>
    <fieldset>
      <legend>Fruit juice size</legend>

      ...いろいろな input 要素など...

    </fieldset>
  </form>



fieldset は、form内の入力欄をまとめる。

用途

- style を付ける
- legend で説明を置く。fieldset を囲う線がいい感じで出せる。
- disable でフィールドセットの中身をまるっと無効にする
- form 属性を使うことで、fieldset を fromタグ外に置くことができる



legent は fieldset 要素の直下に置く。そのfieldsetのキャプション、説明文。

label
-------------

参照

- `<label>: ラベル要素 - HTML: ハイパーテキストマークアップ言語 | MDN <https://developer.mozilla.org/ja/docs/Web/HTML/Element/label>`__

``<label>`` 要素の意味

- 入力欄にフォーカス移動したときに、読み上げソフトがラベルを読み上げてくれたりする
- labelの部分をクリックすると入力欄自体をクリックした場合と同等の操作になる

``<label>`` と ``<input>`` の紐付け方

- ``<input>`` の id を、 ``<label>`` の for に指定する。
- ``<input>`` を ``<label>`` の内側に入れる。(この場合、id と for は必要ない)
- 複数のラベルを1つのinputに紐付けすることもできる
- ラベルを紐付けられるのは、 button, input(hiddenを除く), meter, output, progress, select, textarea



テキスト入力欄
-----------------------

参考

- `<input>: 入力欄（フォーム入力）要素 - HTML: ハイパーテキストマークアップ言語 | MDN <https://developer.mozilla.org/ja/docs/Web/HTML/Element/input>`__

type

- 単一行テキスト入力欄

  - text (規定値)
  - email

    - メールアドレス形式のvalidationあり
    - multiple 属性で、カンマ区切りで複数入力させることもできる
    - 端末によっては @ 入りの仮想キーボードを出す
    - ブラウザの補完で過去に入れたメアドが出る

  - password

    - 入力したものが ``****`` 表示になる

  - search

    - クリア用の(x)ボタンが表示される

  - tel

    - 仮想キーボードが電話番号用になったりする

  - url

    - URL形式のvalidationが入る

  - number

    - 浮動小数値のみのvalidation
    - 上下ボタンが付く。step で増加単位を指定可。
    - min, max 属性で制約を付けることができる
    
  - range

    - スライダー

  - 日付

    - datetime-local: 特定のタイムゾーン情報のない日付と時刻
    - month: 年と月
    - time: 時刻
    - week: 年の中の週番号

  - color: 色選択

    - 送信値は、小文字で6桁の16進数

value: 初期値

placeholder: 空のときに表示される内容


hidden
---------------

hidden: ユーザーには見えないが送信されるもの。::
  
    <input type="hidden" id="timestamp" name="timestamp" value="1286705410" />
    


テキストエリア textarea
------------------------------

::

  <textarea id="msg" name="user_message"></textarea>

textarea は開始タグと終了タグが必要。中身が初期値。


チェックボックス
--------------------

参考

- `<input type="checkbox"> - HTML: ハイパーテキストマークアップ言語 | MDN <https://developer.mozilla.org/ja/docs/Web/HTML/Element/input/checkbox>`__

::

  <fieldset>
    <legend>関心があるものを選んでください</legend>
    <div>
      <input type="checkbox" id="coding" name="interest" value="coding" checked />
      <label for="coding">コーディング</label>
    </div>
    <div>
      <input type="checkbox" id="music" name="interest" value="music" />
      <label for="music">音楽</label>
    </div>
  </fieldset>


- name: 送信されるときのキー
- value: 送信されるときのバリュー。value を省略した場合は、規定値 ``on`` 。
- checked: 初期状態でチェックが入るようになる

送信について。

チェックしていないcheckbox のnameは送信されない。

同じ name で複数の checkbox をチェックした場合、送信内容はそれぞれ飛ぶ。 ::

  ...&interest=coding&interest=music&...

それがどう扱われるかはサーバ側の取り出し方による。
単純に連想配列に入れてしまうとキーが重複して最後のものしかとれなかったりする。
PHPだとキーを ``interest[]`` みたいにしないと複数値を扱えなかったらしい。
最近のものだとちゃんと複数個取り出せる手段が用意されているはず。


ラジオボタン
--------------------

::

  <fieldset>
    <legend>What is your favorite meal?</legend>
    <ul>
      <li>
        <label for="soup">Soup</label>
        <input type="radio" id="soup" name="meal" value="soup" checked />
      </li>
      <li>
        <label for="curry">Curry</label>
        <input type="radio" id="curry" name="meal" value="curry" />
      </li>
      <li>
        <label for="pizza">Pizza</label>
        <input type="radio" id="pizza" name="meal" value="pizza" />
      </li>
    </ul>
  </fieldset>



name の属性が同じであれば、同じグループのボタンであるとみなされ、
同じグループ内では1つしかチェックできない。

チェックされた name=value が送信される。

1つもチェックされていない場合、その name は送信されない。


セレクトボックス selectbox
-------------------------------

::

  <select id="simple" name="simple">
    <option>バナナ</option>
    <option selected>さくらんぼ</option>
    <option>レモン</option>
  </select>

デフォルトでは、optionの中身が送信時のvalueになる。別のものを指定したい場合は::

  <select id="simple" name="simple">
    <option value="banana">大きく美しい黄色いバナナ</option>
    <option value="cherry">ふくよかでジューシーなさくらんぼ</option>
    <option value="lemon">鋭くて力強いレモン</option>
  </select>

optgroup でドロップダウンをグループ分けして見やすくする::

  <select id="groups" name="groups">
    <optgroup label="果物">
      <option>バナナ</option>
      <option selected>さくらんぼ</option>
      <option>レモン</option>
    </optgroup>
    <optgroup label="野菜">
      <option>人参</option>
      <option>茄子</option>
      <option>馬鈴薯</option>
    </optgroup>
  </select>



ボタン button
-----------------

::

  <button type="submit">メッセージを送信</button>
  もしくは
  <input type="submit" value="メッセージを送信" />

type

- submit: (規定値)。action属性で指定した先に送信
- reset: フォームを規定値にリセット。 (UX的にはよろしくないらしい)
- button: 独自のボタンの作成に使用。デフォルトでは何も起こらないボタン。


name 属性を指定すると。 押したときに name=value も送られる。


画像ボタン 
-------------------

``<img>`` と同じように表示されるが、ユーザーがクリックすると送信ボタンのように動作する。

::

  <input type="image" alt="Click me!" src="my-img.png" width="80" height="30" />

画像ボタンを押して送信した場合、画像上のクリック位置(座標)が下記のように送信内容に含まれる。

- X 値のキーは name 属性の値の後ろに文字列 ".x" をつけたもの
- Y 値のキーは name 属性の値の後ろに文字列 ".y" をつけたもの
- ::

    http://foo.com?pos.x=123&pos.y=456


ファイルピッカー
-----------------

::

  <input type="file" name="file" id="file" accept="image/*" multiple />


その他
-----------------

meter:メーターバー::

  <meter min="0" max="100" value="75" low="33" high="66" optimum="0">75</meter>

progress: プログレスバー::

  <progress max="100" value="75">75/100</progress>


共通の属性
-----------------


- disabled: (規定値=false) 無効にする
- form: formタグの外側に置いた場合に、formと紐付けるため、form要素のidを指定する。





組み込みフォーム検証
=========================

- required: 何かしら入力されていないとだめ
- minlength, maxlength: テキストデータ(文字列)の最小・最大長
- min, max: 数値型の最小値・最大値
- type: データを数字にするか、メールアドレスにするか、その他のプリセットされた特定の型にするかを指定します。
- pattern: 入力データが正規表現に一致しないとだめ。自動で(部分一致じゃなくて)全体一致として扱われる。

これで何が起こるか

- 要素が妥当なとき

  - 要素が ``:valid`` 疑似クラスに一致する
  - ユーザーがデータを送信しようとしたとき(JavaScriptなどで特に止めようとしない限り)フォームを送信する

- 要素が不正なとき

  - 要素が ``:invalid`` 疑似クラスに一致する
  - ユーザーがデータを送信しようとしたとき、送信はせずにエラーメッセージを表示
