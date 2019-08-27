

リンク集
=============

- 公式(日本語)
    - https://www.elastic.co/guide/jp/elasticsearch/reference/current/index.html
- 公式(英語)
    - https://www.elastic.co/guide/index.html


基本概念
==========

- 基本概念 | Elasticsearchリファレンス [5.4] | Elastic
    - https://www.elastic.co/guide/jp/elasticsearch/reference/current/gs-basic-concepts.html

クラスタ 1つ以上のノード
ノード   1台のサーバー

```
elasticsearch  RDB
-------------  ----------
index          database
type           table
document       record,row
field          column
```



クラスタヘルス
=================

```
GET /_cat/health?v     # クラスタのヘルスチェック
GET /_cat/nodes?v      # ノードリストの取得
GET /_cat/indices?v    # インデックスのリスト
```

ドキュメントの取得と操作
==============================

```
GET /<Index>/<Type>/<ID>?pretty    # ID指定でドキュメントの取得
```

```
{
  "_index" : "customer",
  "_type" : "external",
  "_id" : "1",
  "_version" : 1,
  "found" : true,                       // 見つかったかどうか
  "_source" : { "name": "John Doe" }    // ドキュメントの内容
}
```

```
PUT
UPDATE
DELTE
```

Search API
================

## 基本的な形式


```
GET|POST /{index}/{type}/_search
```

GET,POST両方可。GETでもbodyを受け付けてくれる。

具体的には
```
# URIクエリパラメタで検索条件を指定
curl -XGET 'http://localhost:9200/blog/posts/_search?q=ad_id:114610308&pretty=true'

# リクエストボディで検索条件を指定
curl -XGET 'http://localhost:9200/doc_ad/type/_search?pretty=true' \
     -d '{"query" : {"term" : {"ad_id" : "1107081305"}}}' -H 'Content-Type: application/json'

# クエリJSONを外部ファイルから読み込ませることも (curlの機能)
curl -XGET 'http://localhost:9200/doc_ad/type/_search?pretty=true' \
     -d '@query.json' -H 'Content-Type: application/json'
```

対象のindex,typeの部分は、以下のような感じにも書ける。

- `/_search`
    すべてのインデックス内のすべてのタイプを対象に検索する
- `/blog/_search`
    blog インデックス内のすべてのタイプを対象に検索する
- `/blog,author/_search`
    blog と author インデックス内のすべてのタイプを対象に検索する
- `/b*,a*/_search`
    b から始まるインデックスと、a から始まるインデックス内のすべてのタイプを対象に検索する
- `/blog/posts/_search`
    blog インデックス内の posts タイプを対象に検索する
- `/blog,author/posts,users/_search`
    blog と author インデックス内の posts と users タイプを対象に検索する
- `/_all/posts,users/_search`
    すべてのインデックス内の posts と users タイプを対象に検索する


レスポンスの例

```
{
  "took" : 63,               // かかった時間（ミリ秒）
  "timed_out" : false,       // タイムアウトしたかどうか
  "_shards" : {              // 検索されたシャードの数と検索に成功/失敗したシャードの数
    "total" : 5,
    "successful" : 5,
    "failed" : 0
  },
  "hits" : {                 // 検索結果
    "total" : 1000,          // 検索基準に一致したドキュメントの数
    "max_score" : null,
    "hits" : [ {             // 検索結果の実際の配列（デフォルトで最初の10個のドキュメント） 
      "_index" : "bank",
      "_type" : "account",
      "_id" : "0",
      "sort": [0],
      "_score" : null,
      "_source" : {"account_number":0,"balance":16623,"firstname":"Bradshaw","lastname":"Mckenzie","age":29,"gender":"F","address":"244 Columbus Place","employer":"Euron","email":"bradshawmckenzie@euron.com","city":"Hobucken","state":"CO"}
    }, {
      "_index" : "bank",
      "_type" : "account",
      "_id" : "1",
      "sort": [1],
      "_score" : null,
      "_source" : {"account_number":1,"balance":39225,"firstname":"Amber","lastname":"Duke","age":32,"gender":"M","address":"880 Holmes Lane","employer":"Pyrami","email":"amberduke@pyrami.com","city":"Brogan","state":"IL"}
    }, ...
    ]
  }
}
```






## クエリ(query句)

https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html

クエリDSLは以下2つの種類の節(clauses)から構成される

- Leaf query clauses
    - あるフィールドが特定の値であるものを探す
    - (例) match, term, range
- Compound query clauses
    - leaf query や他の compound query をラップして、組み合わせる (例) bool, dis_max
    - もしくは、leaf query や他の compound query の振る舞いを変える (例) constant_score


スコア (ほんとか？)

1. 各クエリを実行
1. 各クエリのスコアを加算
1. マッチしたクエリ数をかける
1. 全クエリ数で割る


query context と filter context

- query context --- このドキュメントはクエリに、どれぐらいマッチしているか
    - マッチするかどうかの他に、スコアを計算する(スコアに影響する)
    - queryパラメタに渡された場合
- filter context --- このドキュメントはクエリに、マッチしているかどうか
    - 答えは Yes/No の2択。スコアを計算しない(スコアに影響しない)
    - スコアを計算しないので速い。キャッシュもする。
    - データをフィルタするときに使う。例えば
        - "timestamp" がある範囲に入っているかどうか
        - "status" が "published" かどうか
    - filterパラメタに渡された場合
        - boolクエリの filterパラメタやmust_notパラメタ
        - constant_scoreクエリのflterパラメタ
        - filter aggregation

```
GET /_search
{
  "query": {   // query context
    "bool": {  // query context
      "must": [
        { "match": { "title":   "Search"        }},
        { "match": { "content": "Elasticsearch" }}
      ],
      "filter": [   // filter context
        { "term":  { "status": "published" }},
        { "range": { "publish_date": { "gte": "2015-01-01" }}}
      ]
    }
  }
}
```

(tips) スコアに影響させる条件は query節に入れて、影響させない条件は filter節に入れる。


### Compound query

leaf query や他のcompound query をラップして、

- 結果およびスコアを結合する
- 振る舞いを変える
- filter contextに変える



#### bool

https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html


- must
    - ドキュメントに必ず現れなければならない(must)条件。スコアにも影響する。(query context)
- filter
    - ドキュメントに必ず現れなければならない(must)条件だが、スコアには影響しない。(filter context)
- should
    - ドキュメントに現れるべき(should)条件。(query context)
    - 必ずしも現れなくてもよいっぽい。現れればスコアが上がる。
    - 複数書いた場合はOR結合と書いてあるドキュメントがあるが、微妙に違うかも。
      全部の条件を満たさなくてもスコアの高いものが返る？
      1つもマッチしなかったらスコアがつかないので返らないのでOR結合のように見えるだけ？
    - c.f. minimum_should_match
- must_not
    - ドキュメントに現れてはならない(must not)条件。スコアには影響しない。(filter context)
    - 複数書いた場合、どれか1つにでもマッチしたら、結果から除外される。(多分)


```
POST _search
{
  "query": {
    "bool" : {
      "must" : {
        "term" : { "user" : "kimchy" }
      },
      "filter": {
        "term" : { "tag" : "tech" }
      },
      "must_not" : {
        "range" : {
          "age" : { "gte" : 10, "lte" : 20 }
        }
      },
      "should" : [
        { "term" : { "tag" : "wow" } },
        { "term" : { "tag" : "elasticsearch" } }
      ],
      "minimum_should_match" : 1,
      "boost" : 1.0
    }
  }
}
```

上記のように、must, filter, must_not, should には、
直接単一の子要素も含められるし、配列にして複数の子要素も含められるっぽい。



#### boosting

- positive (必須)
    - 満たされないといけない条件
- negative (必須)
    - これにマッチした場合は、negative_boostの値がスコアにかけ算される
    - これにマッチしても結果から排除されるわけではない (c.f. bool の must_not )
- negative_boost (必須)
    - 0.0～1.0 の値

```
GET /_search
{
    "query": {
        "boosting" : {
            "positive" : {
                "term" : {
                    "text" : "apple"
                }
            },
            "negative" : {
                 "term" : {
                     "text" : "pie tart fruit crumble tree"
                }
            },
            "negative_boost" : 0.5
        }
    }
}
```

↑apple社にマッチさせたいので、果物のリンゴに関連する語と一緒に出現した場合はスコアを下げる。


#### constant_score

filterクエリをラップし、それに固定のスコアを与える。

```
GET /_search
{
    "query": {
        "constant_score" : {
            "filter" : {
                "term" : { "user" : "kimchy"}
            },
            "boost" : 1.2     // 省略可。省略した場合は 1.0。
        }
    }
}
```

#### dis_max

Disjunction max query (分離 最大 クエリ)

bool の should と似ていて、少なくとも1つの条件にマッチしたドキュメントを返す。
ただし、その際のスコアは、各クエリのうち最も大きいものが採用される。(tile_breakerが0.0の場合)

- queries (必須。配列)
- tie_breaker (オプション。0.0～1.0の値。デフォルト 0.0)
    - (MAXの条件のスコア) + tie_breaker * (その他の条件のスコア)


```
GET /_search
{
    "query": {
        "dis_max" : {
            "queries" : [
                { "term" : { "title" : "Quick pets" }},
                { "term" : { "body" : "Quick pets" }}
            ],
            "tie_breaker" : 0.7
        }
    }
}
```

使いどころ

- [Bool Query と Dis Max Query の違い - Carpe Diem](https://christina04.hatenablog.com/entry/2016/03/23/052609)

```
{"index": {"_id": "1"}}
{"title": "Quick brown rabbits", "body": "Brown rabbits are commonly seen."}
{"index": {"_id": "2"}}
{"title": "Keeping pets healthy", "body": "My quick brown fox eats rabbits on a regular basis."}
```

上記に対し、"brown fox" というtermで検索した場合、
単語が複数のフィールドに分かれて出現する1より、同じフィールドに両方出てくる2の方のスコアを高くしたい。

- bool の should を使うと、マッチするフィールド数が多い1の方がスコアが高くなってしまう。
- dis_max を使うと、最もスコアのよい成績のフィールドが採用されるので2の方がスコアが高くなる。


#### function_score

スコアを補正する。

- [Function score query | Elasticsearch Reference \[7.3\] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-function-score-query.html)

```
GET /_search
{
    "query": {
        "function_score": {
            "query": { "match_all": {} },
            "boost": "5",
            "random_score": {}, 
            "boost_mode":"multiply"
        }
    }
}
```

複数の条件を同じ重みではなく、重みを変えたりできる。
```
GET /_search
{
    "query": {
        "function_score": {
          "query": { "match_all": {} },
          "boost": "5", 
          "functions": [
              {
                  "filter": { "match": { "test": "bar" } },
                  "random_score": {}, 
                  "weight": 23
              },
              {
                  "filter": { "match": { "test": "cat" } },
                  "weight": 42
              }
          ],
          "max_boost": 42,
          "score_mode": "max",
          "boost_mode": "multiply",
          "min_score" : 42
        }
    }
}
```

TODO 結構、量があるので別で調査する。


### Full text query

Analizerで処理されたテキストフィールドを検索する。

ドキュメントをインデクシングする際に使ったのと同じAnalizerで、
クエリ文字列も処理される。
単語分解やストップワードの除外等されることがあるため注意。

- intervals
    - 一致する用語の順序と近接度をきめ細かく制御できるフルテキストクエリ。
- match
    - あいまい一致およびフレーズまたは近接クエリを含む全文クエリを実行するための標準クエリ。
- match_bool_prefix
    - prefixクエリとして一致する最後の用語を除き、各クエリをtermクエリとして一致するboolクエリを作成します。
- match_phrase
    - matchクエリに似ていますが、完全一致フレーズまたは単語の近接マッチに使用されます。
- match_phrase_prefix
    - match_phraseクエリにmatch_phraseますが、最後の単語でワイルドカード検索を行います。
- multi_match
    - matchクエリのマルチフィールドバージョン。
- common
    - 特殊なクエリで、一般的でない単語を優先します。
- query_string
    - コンパクトなLucene クエリ文字列構文をサポートし、単一のクエリ文字列内でAND | OR | NOT条件と複数フィールド検索を指定できます。
      上級ユーザーのみ。
- simple_query_string
    - ユーザーに直接公開するのに適した、単純で堅牢なquery_string構文のバージョン。


```
// "message"フィールドに this, is, a, test のいずれかが含まれている (OR結合)
{ "match" : { "message" : "this is a test" } }

// すべて含まれているものを検索(AND結合)
{ "match" : { "message" : {"query": "this is a test", "operator": "and" } } }

// score の下限を指定
{ "match" : { "message" : { "query" : "to be or not to be", "cutoff_frequency" : 0.001 } } }
```

※
Analyzer によって単語分解やストップワードの除外等されることがあるため、
上記以外の部分語にもマッチする（しない）可能性がある。
上記では、「a」はストップワードとして除外される。

```
{ "simple_query_string" : {
    "query": "\"fried eggs\" +(eggplant | potato) -frittata",
    "fields": ["title^5", "body"],
    "default_operator": "and"    // デフォルトは "or"。andの方が一般的なのでたいてい付ける。
} }
```


### Geo queries

TODO 

### Joining queries

TODO

### Match all query

最もシンプルなクエリ。全てのドキュメントにマッチし、それらに _score 1.0 をつける。

```
{"match_all": {}}
{"match_all": { "boost" : 1.2 }}

{"match_none": {}}  // 逆で、絶対にドキュメントにマッチしない。
```

### Span queries

TODO

### Specialized queries

TODO

### Term-level queries

(Analyserを通したテキストではなく)構造化データ(JSON)そのものを検索する。

https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.html

「term」を利用すると、（検索時に）analyzer により分解されない
※ ただし、indexing 時にはanalyzer が走っている可能性があることに注意


```
// "user"というフィールドに値を持つものを検索
{"exists": { "field": "user" }}

// 少々違っていてもマッチする
{ "fuzzy": { "user": { "value": "ki" } } }

{ "fuzzy": {
    "user": {
        "value": "ki",
        "fuzziness": "AUTO",
        "max_expansions": 50,
        "prefix_length": 0,
        "transpositions": true,
        "rewrite": "constant_score"
    }
} }


// ID指定でドキュメントを検索する
{"ids" : { "values" : ["1", "4", "100"] } }


{ "prefix": { "user": { "value": "ki" } } }
{ "prefix": { "user": "ki" } }  // 省略版

{ "range" : { "age" : { "gte" : 10, "lte" : 20, "boost" : 2.0 } } }
    gt, gte, lt, lte
{ "range" : { "timestamp" : { "gte" : "now-1d/d", "lt" :  "now/d" } } }
{ "range" : { "timestamp" : { "time_zone": "+01:00", "gte": "2015-01-01 00:00:00", "lte": "now" } } }

{ "regexp": {
    "user": {
        "value": "k.*y",
        "flags" : "ALL",
        "max_determinized_states": 10000,
        "rewrite": "constant_score"
    }
} }


// 文字列を含むものを検索。正確な文字列マッチ。空白や大文字小文字も正確に検索する
{ "term": { "user": "user01"} } 
{ "term": { "user": { "value": "Kimchy", "boost": 1.0 } } }

// 少なくとも1つの文字列を含むものを検索。正確な文字列マッチ。
{ "terms" : { "user" : ["kimchy", "elasticsearch"] } }
{ "terms" : { "user" : ["kimchy", "elasticsearch"], "boost" : 1.0 } }  // boost がつく位置が他と違うので注意

// TODO terms_set

// ワイルドカード
{ "wildcard": {
    "user": {
        "value": "ki*y",
        "boost": 1.0,
        "rewrite": "constant_score"
    }
} }
```








## query句以外


"_source": ["field1", "field2"]
    全フィールドではなく一部のフィールドのみを返す。SQL の select 句みたいなの。



ページング

size と from パラメタ


from は 0 から始まる。

```
GET /_search?size=5 
GET /_search?size=5&from=5 
GET /_search?size=5&from=10
```

```
{
  "query": { "match_all": {} },
  "from": 10,
  "size": 10
}
```


TODO

```
q=*   // 全ドキュメント
sort=account_number:asc


{
  "query": { "match_all": {} },
  "sort": [
    { "account_number": "asc" }
  ]
}
```


Analysisモジュール
=====================

日本語は分かち書きしないので、トークナイズが必要

```
               適合率                  再現率
形態素解析    高い(マッチ度が高い)  低い(検索漏れが多くなる)
N-gram        低い                  高い
```


Analyzer

- Char filter: 文字レベルの加工処理。除外や正規化。(0個以上)
- Tokenizer: トークナイズ方法を定義。 (1個)
- Token filters: トークンに対して加工処理。除外や正規化。(0個以上) 

フィールド単位でAnalyzerを設定できる。

インデックス時と検索時のクエリ文字列処理で使用される。

インデックス側のアナライザーとサーチ側のアナライザーは基本的には同じもを使用しますが、違うものを使用することも可能。


確認
```
% curl -XGET 'localhost:9200/{インデックス名}/_analyze?analyzer={アナライザー名}&pretty=true' -d '{解析対象文字列}'
```



TODO


"explain": true

Nestedデータ型とObjectデータ型

