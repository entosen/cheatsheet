======================
puppeteer
======================

概要
==============

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



tips
==============

WSLから動かす場合の設定
---------------------------

参考

- `Puppeteer doesn't run under WSL (Windows subsystem for Linux) · Issue #1837 · puppeteer/puppeteer · GitHub <https://github.com/puppeteer/puppeteer/issues/1837>`__

WSLから動かす場合追加の起動オプションが必要::

  --disable-gpu
  --disable-setuid-sandbox
  --single-process

Linuxやmacの人と共同で開発するような場合には、下記のようにするとよい(jest-puppeteer.config.js の場合の例)::

    const os = require('os');

    const headless = process.env.HEADLESS !== 'false';
    const launch = {
      args: [
        '--no-sandbox',
      ],
      headless: headless,
      devtools: true,
      ignoreHTTPSErrors: true
    };

    const isWSL = os.platform() == 'linux' && os.release().toLowerCase().indexOf('microsoft') != -1;
    if (isWSL) {
      launch.args.push('--disable-gpu');
      launch.args.push('--disable-setuid-sandbox');
      launch.args.push('--single-process');
    }

    module.exports = {
      launch: launch,
      exitOnPageError: false
    }



起動オプション
-------------------

puppeteer が chromium を起動する際のオプションを知りたい場合はこうする。

launch に下記をつける::

    executablePath: './printargs.sh'

printargs.sh::

    #!/bin/sh

    echo "$0" >&2
    for a in "$@" ; do
        echo "$a" >&2
    done

    exit 1

