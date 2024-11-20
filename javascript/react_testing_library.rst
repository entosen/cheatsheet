===========================
React Testing Library
===========================



::

  import {render, screen} from '@testing-library/react'
  import userEvent from '@testing-library/user-event'
  import '@testing-library/jest-dom'

  import Fetch from './fetch'

  test('loads and displays greeting', async () => {
    // ARRANGE
    render(<Fetch url="/greeting" />)

    // ACT
    await userEvent.click(screen.getByText('Load Greeting'))
    await screen.findByRole('heading')

    // ASSERT
    expect(screen.getByRole('heading')).toHaveTextContent('hello there')
    expect(screen.getByRole('button')).toBeDisabled()
  })




参考
====================

- `React Testing Libraryの使い方 #React - Qiita <https://qiita.com/ossan-engineer/items/4757d7457fafd44d2d2f>`__
- `Common mistakes with React Testing Library の和訳 #react-testing-library - Qiita <https://qiita.com/kobanyan/items/126512ec3e8d76c538b3>`__
- `React Testing Library | Testing Library <https://testing-library.com/docs/react-testing-library/intro/>`__
- `Testing Library | Testing Library <https://testing-library.com/>`__


インストール
======================

::

  npm install --save-dev @testing-library/react @testing-library/dom @types/react @types/react-dom
  or
  yarn add --dev @testing-library/react @testing-library/dom @types/react @types/react-dom


レンダリング
====================

screen を使う場合::

  import {render, screen} from '@testing-library/react'

  render(<App />);

  screen.debug();
  const input = screen.getByLabelText('Username');

render の返り値を使う場合::

  {getByText, queryAllByRole} = render(<App />);
  const input = getByLabelText('Username');

  // 分割代入しない場合は view で受けるのがお行儀がよいらしい
  // const view = render(<App />);



screen を使う方法の方が新しいみたい。 
`DOM Testing Library v6.11.0 で追加 <https://github.com/testing-library/dom-testing-library/releases/tag/v6.11.0>`__

分割代入するのが大変だから。


デバッグ
==================

debug

::

  render(<RenderTest />);
  screen.debug(); // コンソールにレンダリング結果を出力

  もしくは getBy した結果を debug することも可


デフォルトではコンソール出力を 7000 (単位不明。バイト？) で打ち切ってしまう。
足りないようなら、下記のように DEBUG_PRINT_LIMIT 環境変数をセット。

::

  DEBUG_PRINT_LIMIT=30000 npm run test


Queries クエリ
====================


検索のタイプ
--------------

get, query, find の違い

- get は見つからなかった場合にエラーを投げる
- query は見つからなかった場合に null を返す。 (存在しないことを確認したいときに使ったり)
- find は非同期でRetry付き。待つ必要がある場合に使う。

All が付く付かないの違い

- All が付かないやつは、2つ以上見つかった場合にエラーを投げる
- All が付くやつは配列で複数返す。2つ以上見つかっても可。

==============  ============  ==============  ==============  ======================
Type of Query   0 Matches     1 Match         >1 Matches      Retry (Async/Await)
==============  ============  ==============  ==============  ======================
getBy...        Throw error   Return element  Throw error     No
queryBy...      Return null   Return element  Throw error     No
findBy...       Throw error   Return element  Throw error     Yes
getAllBy...     Throw error   Return array    Return array    No
queryAllBy...   Return []     Return array    Return array    No
findAllBy...    Throw error   Return array    Return array    Yes
==============  ============  ==============  ==============  ======================


container を第1引数で渡すか、バインド済みか
------------------------------------------------

第1引数に container を受け取るバージョン(testing/library/dom オリジナルのバージョン)と、
既に container がバインドされている(その分引数が1つ少ない)バージョンがある。

オリジナル::

  import {getByLabelText} from '@testing-library/dom'

  const container = document.querySelector('#app')
  const inputNode2 = getByLabelText(container, 'Username')  // 第1引数にcontainer


screen  既にバインドされたクエリ関数を持つオブジェクト

::

  import {render, screen} from '@testing-library/react'

  render(<RenderTest />);
  screen.getByLabelText('Username')



within() で、あるcontainerをバインド済みのクエリ関数を使うことができる

::

  import {within} from '@testing-library/dom'

  within(container).getByText('hello')   // withinすることでBind済みのクエリ関数が使える


TextMatch引数
------------------------

TextMatch引数に渡せるもの

- 文字列
- 正規表現
- 関数 ``(content?: string, element?: Element | null) => boolean``

::

  <div>Hello World</div>

  // Matching a string:
  screen.getByText('Hello World')                 // デフォルトは、完全一致、case-sensitive
  screen.getByText('llo Worl', {exact: false})    // 部分一致。case-insensitive
  screen.getByText('hello world', {exact: false}) // 部分一致。case-insensitive

  // Matching a regex:
  screen.getByText(/World/)          // substring match, デフォルトで case-sensitive
  screen.getByText(/world/i)         // substring match, ignore case
  screen.getByText(/^hello world$/i) // full string match, ignore case
  screen.getByText(/Hello W?oRlD/i)  // substring match, ignore case, searches for "hello world" or "hello orld"

  // Matching with a custom function:
  screen.getByText((content, element) => content.startsWith('Hello'))


さらに追加の情報をoptions引数に渡せる

- exact: boolean

  - (default) true: 完全一致、case-sensitive
  - false: 部分一致、case-insensitive
  - 正規表現と関数のときは無視される

- normalizer: 関数 ``(string) => string``

  - 指定なしの場合: 先頭末尾の空白除去、連続空白を1つに。
  - 指定した場合はデフォルトのNormalizerとの差し替えになるので、
    たいていは、デフォルトNormalizerを少し改造したようなものにする。::

        screen.getByText('text', {
          normalizer: getDefaultNormalizer({trim: false}),
        })

        screen.getByText('text', {
          normalizer: str =>
            getDefaultNormalizer({trim: false})(str).replace(/[\u200E-\u200F]*/g, ''),
        })




検索関数
---------------------------

https://testing-library.com/docs/queries/about/


getByRole
^^^^^^^^^^^^^^^^

HTMLの role属性、Accessible Name(アクセシブル名), Accessible Description(アクセシブル説明) で検索する。
どれもアクセシビリティ関連で使われる値。

- role属性。

  - `WAI-ARIA ロール - アクセシビリティ | MDN <https://developer.mozilla.org/ja/docs/Web/Accessibility/ARIA/Roles>`__
  - 明示的に付けなくても暗黙的に(勝手に)付いていることがある。
    基本的に明示的には付けないものっぽい。
  - 暗黙的に付く role の一覧

    - `a table of HTML elements with their default and desired roles <https://www.w3.org/TR/html-aria/#docconformance>`__

      - この表は、HTML要素、暗黙的に付くrole、明示的に付ける場合の許容されるrole の一覧

    - `Testing LibraryのgetByRoleで指定できる属性一覧 #React - Qiita <https://qiita.com/tondemonai7/items/3f7ed9bd6af1e0c3dfb7>`__

- Accessible Name

  - `Accessible name (アクセシブル名) - MDN Web Docs 用語集: ウェブ関連用語の定義 | MDN <https://developer.mozilla.org/ja/docs/Glossary/Accessible_name>`__
  - name属性とは別。音声読み上げソフトが読み上げる文字列らしい。
    子のテキストエレメントだったり、alt とか placeholder とかから自動的に取られるっぽい。
  - `Accessible Name and Description Computation 1.1 <https://www.w3.org/TR/accname-1.1/>`__
  - `What is an accessible name? - TPGi <https://www.tpgi.com/what-is-an-accessible-name/>`__

- Accessible Description

  - `Accessible description (アクセシブル説明) - MDN Web Docs 用語集: ウェブ関連用語の定義 | MDN <https://developer.mozilla.org/ja/docs/Glossary/Accessible_description>`__
  - table の caption だったり、input要素のvalueだったり。


確認方法

- Chromeの開発ツール > 要素 > アクセシビリティ > Name,役割
- テストで。 logRoles(container); ログ出力


option がいっぱいあるので、詳細はリファレンスを見て。

::

  const inputNode = getByRole('textbox', { name: 'Username'}


  screen.getByRole("heading")             // h1〜h6全部マッチ
  screen.getByRole("heading", {level:1})  // h1 のみマッチ



getLabelText
^^^^^^^^^^^^^^^^^^^

label文字列で対応する入力要素を検索::

  <label for="username-input">Username</label>
  <input id="username-input" />

    const inputNode = screen.getByLabelText('Username')
    const inputNode = screen.getByLabelText('Username', {selector: 'input'}) // 要素で絞り込む

getByPlaceholderText
^^^^^^^^^^^^^^^^^^^^^^


Placeholder文字列で入力要素を検索::

  <input placeholder="Username" />   フォーム未入力のときに入力欄に薄く現れる文字列

  const inputNode = screen.getByPlaceholderText('Username')

getByText
^^^^^^^^^^^^^^^^^^^^^^


テキストノードやbuttonのvalue値で要素を検索::

  <a href="/about">About ℹ️</a>
  テキストノードだけじゃなく、submitやbuttonのvalue属性にもマッチする
  <input type="submit" value="Send data" />

    const aboutAnchorNode = screen.getByText(/about/i)
    const aboutAnchorNode = screen.getByText(/about/i, {selector: 'a'})

  デフォルトで script, style ノードは無視される。 → ignore オプション


getByDisplayValue
^^^^^^^^^^^^^^^^^^^^^^


input, textarea, select の各入力値(value値)で検索::

  <input type="text" id="lastName" />
  // 入力欄に Norris と入力

    const lastNameInput = screen.getByDisplayValue('Norris')

getByAltText
^^^^^^^^^^^^^^^^^^^^^^


alt属性で要素を検索::

  <img alt="Incredibles 2 Poster" src="/incredibles-2.png" />

    const incrediblesPosterImg = screen.getByAltText(/incredibles.*? poster/i)

  altを取りうる要素: <img>, <input>, <area>

getByTitle
^^^^^^^^^^^^^^^^^^^^^^


title属性で要素を検索::

  <span title="Delete" id="2"></span>  // title属性

  <svg>
    <title>Close</title>  // svg の title ノードも対象
    <g><path /></g>
  </svg>

    const deleteElement = screen.getByTitle('Delete')

getByTestId
^^^^^^^^^^^^^^^^^^^^^^

data-testid で検索::

  <div data-testid="custom-element" />

    const element = screen.getByTestId('custom-element')


(力技) querySelector でやっちゃう
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


::

  const foo = container.querySelector('[data-foo="bar"]')

  querySelector はマッチしたものの最初の1つを返す。

    ".myclass"  // クラス
    "div.user-panel.main input[name='login']"

https://developer.mozilla.org/ja/docs/Web/API/Document_Object_Model/Locating_DOM_elements_using_selectors



おすすめの順序
--------------------

https://testing-library.com/docs/queries/about/#priority

#. Accessible

  #. getByRole
  #. getByLabelText
  #. getByPlaceholderText
  #. getByText
  #. getByDisplayValue

#. Semantic

  #. getByAltText
  #. getByTitle

#. Test IDs

  #. getByTestId


設計思想的に、内部の情報ではなくて、
ユーザーに実際に見えているものでテストするほうがよいという考え方なので、
こんな順序になっている。


Testing Playground Chrome 拡張
-------------------------------------

`Testing Playground - Chrome ウェブストア <https://chromewebstore.google.com/detail/testing-playground/hejbmebodbijjdhflfknehhcgaklhano>`__

開発ツールのDomインスペクタで要素を選ぶと、それを抽出できるおすすめのクエリを教えてくれる。



webサイトで動く、 testing-playground.com もある

https://testing-playground.com




アサーション関数
=============================

https://github.com/testing-library/jest-dom

- toBeDisabled  (input要素が？)disabledかチェック
- toBeEnabled   (input要素が？)disabledじゃないことをチェック
- toBeEmpty
- toBeEmptyDOMElement   DOMの中身が空かチェック
- toBeInTheDocument     DOMの中身に対象があるかチェック
- toBeInvalid           input要素などが invalid かチェック
- toBeRequired          input要素などが requires かチェック
- toBeValid             input要素などが invalid でないことをチェック
- toBeVisible           要素が目に見える状態かチェック
- toContainElement      要素を子要素として持っているかチェック
- toContainHTML         要素を子要素として持っているかチェック
- toHaveAttribute       
- toHaveClass           対象のclassを持っているかチェック
- toHaveFocus           focus状態かチェック
- toHaveFormValues      formの値をチェック
- toHaveStyle           対象のstyleをチェック
- toHaveTextContent     中の文字要素をチェック
- toHaveValue           inputなどのvalueをチェック
- toHaveDisplayValue
- toBeChecked           チェック状態かチェック
- toBePartiallyChecked
- toHaveDescription



イベントの発火
====================




userEvent

  type



fireEvent


userEvent の方が fireEvent より好ましいらしい。





