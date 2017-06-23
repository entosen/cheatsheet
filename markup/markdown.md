
## 参照

- [Daring Fireball: Markdown Syntax Documentation](https://daringfireball.net/projects/markdown/syntax)


## リンク

URLっぽい文字列を書くと、勝手にリンクしてくれる。

インライン

```
[an example](http://example.com/ "Title")  # タイトルあり
[This link](http://example.net/)           # タイトルなし

# 相対パスでもいけるっぽい。
```

リファレンス

```
定義
[foo]: http://example.com/
# 行頭がインデントされていても可
# コロンの後ろは空白を空けるのが正式

[foo]: http://example.com/  "Optional Title Here"   # タイトル付き
[foo]: http://example.com/  'Optional Title Here'
[foo]: http://example.com/  (Optional Title Here)

[id]: <http://example.com/>  "Optional Title Here"  # リンクを三角カッコでかこっても可

[id]: http://example.com/longish/path/to/resource/here
    "Optional Title Here"                           # タイトルを次の行に書くことも可

```

名前は、
- case insensitive。
- 空白を含めることも可

```
リンク

[link text][a]    # `a` で定義されているところにリンクする
[link text][A]    # 大文字小文字は区別されない！ この２つは同一。

[foo][]           # `foo` で定義されているところにリンクする
[Daring Fireball][]    # 名前に空白を含めることもできる
```

