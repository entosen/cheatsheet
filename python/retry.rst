================================
リトライ処理を実現する
================================


下記のパッケージが使える。

- `retry · PyPI <https://pypi.org/project/retry/>`_
- `retrying · PyPI <https://pypi.org/project/retrying/>`_
- `tenacity <https://pypi.org/project/tenacity/>`_

どれも基本は似たような感じ。切り上げる条件や試行間隔、ログ出力などの柔軟性が違う感じ。

retry の場合の例::

    from retry import retry

    @retry(tries=3, delay=2)
    def make_trouble():
        '''Retry, raise error after 3 attempts, sleep 2 seconds between attempts.'''

