======================
puppeteer
======================

Chrome, Chromium をコントロールするためのAPIライブラリ。

    Puppeteer is a Node library which provides a high-level API 
    to control Chrome or Chromium over the DevTools Protocol.
    Puppeteer runs headless by default,
    but can be configured to run full (non-headless) Chrome or Chromium.


参考ドキュメント

- 公式 `GitHub - puppeteer/puppeteer: Headless Chrome Node.js API <https://github.com/puppeteer/puppeteer>`__



サンプル::

    const puppeteer = require('puppeteer');

    (async () => {
      const browser = await puppeteer.launch();
      const page = await browser.newPage();
      await page.goto('https://example.com');
      await page.screenshot({path: 'example.png'});

      await browser.close();
    })();


この辺全部 async 関数かも。完了を待つには await が必要になるかも。

::

    page.goto(url) : url を開く
    page.click(id) : 要素をクリック

    page.waitForSelector(elem): その要素ができるまで待つ
    page.waitForNavigation( ): 
    page.waitForFunction( ):

    page.on('request', func) で、特定の条件で関数を起動することができる。

        request, response 
        error, pageerror

        page.setRequestInterception(true) をやっているからかもしれない。

    page.evaluate(`JS文字列`)
        pageのJSでこの文字列を評価する

    page.screenshot({path: 'a.png'});
        スクリーンショットを撮る

    window.scrollTo( )
