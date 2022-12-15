



```
pip install beautifulsoup4
```

サンプル
```
import requests
from bs4 import BeautifulSoup

res = requests.get('http://quotes.toscrape.com/')
soup = BeautifulSoup(res.text, 'html.parser')

```


ドキュメント

- 本家
    - [Beautiful Soup Documentation — Beautiful Soup 4.4.0 documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#css-selectors)
- 本家(日本語)
    - [kondou.com - Beautiful Soup 4.2.0 Doc. 日本語訳 (2013-11-19最終更新)](http://kondou.com/BS4/)



find系

find
find_all

```
soup.find('title')   # (最初の)title要素
find_all('a')        # a要素全部

find_all('div', {'class': 'quote'})  # class="quote" の div要素全部
```


select系

CSSセレクターを使って抽出

select_one   1つ
select       全部

```
select('div.quote small.author')
```

テキストの抜き出し
