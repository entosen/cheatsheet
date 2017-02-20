
## 参考ドキュメント

- [Rubyist Magazine - プログラマーのための YAML 入門 (初級編)](http://magazine.rubyist.net/?0009-YAML)

## コメント

```
# 行末までコメント
```


## インデント

タブを使わず空白のみで。

通常は空白２つ。



## 構造(基本)

リスト

- 「`-`」のあとには半角スペース

```
--- # ブロック形式
- Casablanca
- Spellbound
- Notorious
--- # インライン形式、またはフロー形式
[milk, bread, eggs]
```

連想配列

- コロン「`:`」のあとに半角スペースを 1 つ以上入れてください

```
--- # ブロック
name: John Smith
age: 33
--- # インライン
{name: John Smith, age: 33}
```


## 構造(複合)

```
# リストの値にハッシュ
- {name: John Smith, age: 33}
- name: Mary Smith
  age: 27

# ハッシュの値にリスト
men: [John Smith, Bill Jones]
women:
  - Mary Smith
  - Susan Williams

# リストの値にリスト
- aaa
-
  - b1
  - b2
  -
    - b3.1
    - b3.2
- ccc
# → rubyの表記で書くと ["aaa", ["b1", "b2", ["b3.1", "b3.2"]], "ccc"] の構造

# ハッシュの値にハッシュ
A: aaa
B:
  B1: bbb1
  B2: bbb2
C: ccc
```


