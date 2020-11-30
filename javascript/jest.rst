========================
Jest
========================


`Jest · 🃏快適なJavaScriptのテスト <https://jestjs.io/ja/>`__


設定ファイル
====================

- package.jsonのjestフィールドにJSONで設定
- jest.config.jsを用意して、JavaScriptで設定


出力の調整
----------------

::

    --verbose  テストファイルごとの結果ではなく、テストファイル内の各テストケースごとの結果を表示
    --silent   console.log()やconsole.error()などを非表示


使い方::

    npm test -- --silent=false --verbose


テスト対象
--------------

::

    testRegex [string | array<string>]
        Default: (/__tests__/.*|(\\.|/)(test|spec))\\.[jt]sx?$

        - 拡張子が .js, .jsx, .ts, .tsx
        - 場所が (OR)
            - __tests__ 以下に格納されたファイル
            - 拡張子を除いたファイル名が .test, .spec で終わる
                (hoge.test.js, hoge.spec.tsx, など)
            - 拡張子を除いたファイル名が test, spec
                (test.js, spec.tsx など)

    roots [array<string>]
        探す対象をこれ以下に限定


TODO カバレッジ


テストコード
=====================

サンプル::

    const sum = require('./sum');

    test('adds 1 + 2 to equal 3', () => {
      expect(sum(1, 2)).toBe(3);
    });


テストの構造
======================

テスト関数
--------------

::

    test('テストの説明', () => {
        ...
    });

it は test の別名で、全く同じ。


setup と Teardown
------------------------

下記の関数を、ファイルグローバルや各describeに定義できる。

::

    beforeEach    // 各テスト前
    afterEach    // 各テスト後
    beforeAll    // ファイル(もしくはdescript)の最初
    afterAll     // ファイル(もしくはdescript)の最後

    beforeEach(() => {
      ...
    });

{before,after}Eachが指すのは、"各test" 。
子要素に describe があったとしても、"各describe" ではなく "各describeの中の各テスト" に対し呼ばれる。

各テストに対して複数のレベルの beforeEach, afterEach が適用される場合、
外側の beforeEach の方が先に呼ばれる (外側の afterEach の方が後に呼ばれる)。

TODO ファイルスコープの変数は、複数のテストで共用されてしまうか？


describe
-----------------------

describe で、テスト(および befor\*, after\* )をグループにまとめることができる。::

    describe('グループの説明', () => {
        beforeEach(() => { ... });
        test('test1', () => { ... });
        test('test2', () => { ... });
        ...など...
    });

    // describe を入れ子にすることも可能
    describe('group1', () => {
        describe('group1-1', () => {
            test('goup1-1-1', () => {...});
        });
    });


いわゆるデータプロバイダ的なこと
---------------------------------------

(test.each だけでなく、describe.each も同様に可能)

test.each(table)(name, fn, timeout)

- table は通常2次元配列

::
    test.each([
      [1, 1, 2],     // 1つ目のテスト
      [1, 2, 3],     // 2つ目のテスト
      [2, 1, 3],
    ])('.add(%i, %i)', (a, b, expected) => {
      expect(a + b).toBe(expected);
    });

テスト名の中の ``%`` がprintfと同様に(一パラメータで)置換される::

    %p - pretty-format.
    %s- String.
    %d- Number.
    %i - Integer.
    %f - Floating point value.
    %j - JSON.
    %o - Object.
    %# - テストケースのインデックス。
    %% - %文字そのもの


test.each`table`(name, fn, timeout)

-  ``｜`` を区切り文字として要素に分割
-  1行目はキー名を表す行
- テスト関数の引数はオブジェクトで渡される
- テスト名の中の ``$キー名`` で置換される

::

    test.each`
      a    | b    | expected
      ${1} | ${1} | ${2}
      ${1} | ${2} | ${3}
      ${2} | ${1} | ${3}
    `('returns $expected when $a is added $b', (obj) => {
      expect(obj.a + obj.b).toBe(obj.expected);
    });


テスト絞ったり飛ばしたりする
-------------------------------------

コメントアウトするよりも、下記のように skip, only を使う方が、
テスト結果にも表示されるのでベター。

test や describe には skip, only がつけられる。::

    // .skip をつけたテストはスキップされる
    test.skip('テストの説明', () => { ... });

    // ファイルの中で .only が付いたものだけをテストする
    test.only('テストの説明', () => { ... });

    // テストはこれから書くという意味
    test.todo('テストの説明', () => { ... });



並列実行
------------------

基本的に、ファイルの中の各テストは直列に動く。

``test.concurrent`` を使うと並行にも動かせるらしい。 (実験的)




Matcher
================

https://jestjs.io/docs/ja/expect

::

    expect(  ).toBe(  )
              .toBeTruthy()

    expect(2 + 2).toBe(4);   // Object.is ？？？ 
    expect(data).toEqual({one: 1, two: 2});   // オブジェクトや配列を再帰的に比較

    await expect( async関数  ).resolves.toBe(  )   # 頭にも await つけないといけない。



一部のテストだけ実行する
==============================


一部のファイルだけ実行する

::
    # ファイル名やパスで実行するファイルを限定する
    jest my-test ...
    jest path/to/my-test.js ...

    # path/to/fileA.js と path/to/fileB.jsに関連したテストを実行する:
    jest --findRelatedTests path/to/fileA.js path/to/fileB.js

    # 除外
    jest --testPathIgnorePatterns=hogehoge

test を test.only にすると、そのファイルの中ではそのテストだけが実行されるようになる。

::
    test.only('this will be the only test that runs', () => {
        expect(true).toBe(false);
    });


TOOD -t オプション

非同期なコードのテスト
===========================

非同期処理が終了してから次のテストに行きたいので、
Jestに非同期処理が終了したことを知らせる必要がある。

TODO JavaScript の非同期処理をもうちょっとちゃんと分かってからまとめる。



jest-puppeteer
=========================

https://jestjs.io/docs/ja/puppeteer

jest の設定に下記を追加::

    {
      "preset": "jest-puppeteer"
    }

browser, page, context が、グローバル変数として用意される。
window, document もか？

https://github.com/smooth-code/jest-puppeteer#api

pageとかはテストファイルごとに生成されているらしい。

jestの実行環境はファイルごとに独立しているので、
逆を言うと同じファイル内は同一の実行環境になります。
そのため、globalオブジェクトに生えている変数や関数を変更すると、
同じファイルの他のテストに影響を与えることがあります。



headless=false(＝ヘッドあり)で実行した場合に、
テスト後もpageを開いたままにする方法。デバッグモードに入る方法。

```
await jestPuppeteer.debug();
```

