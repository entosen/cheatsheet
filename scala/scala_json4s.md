# Json4s チートシート

## 参考ドキュメント

- [json4s/json4s: A single AST to be used by other scala json libraries](https://github.com/json4s/json4s)
- [JSON4Sの日本語Readme 私訳](https://gist.github.com/takuya71/4025974)
- [json4s/JsonDSL.scala at 3.4 ・ json4s/json4s](https://github.com/json4s/json4s/blob/3.4/ast/src/main/scala/org/json4s/JsonDSL.scala)
- [json4s/JsonAST.scala at 3.4 ・ json4s/json4s](https://github.com/json4s/json4s/blob/3.4/ast/src/main/scala/org/json4s/JsonAST.scala)
- [json4s/MonadicJValue.scala at 3.4 ・ json4s/json4s](https://github.com/json4s/json4s/blob/3.4/core/src/main/scala/org/json4s/MonadicJValue.scala)
- [json4s/JsonAstSpec.scala at 3.4 ・ json4s/json4s](https://github.com/json4s/json4s/blob/3.4/tests/src/test/scala/org/json4s/JsonAstSpec.scala)


## データ構造

Json4s ではJSONのデータ構造を、Json AST というデータ構造(DOMみたいなもの)で扱う。

参考: [json4s/json4s: A single AST to be used by other scala json libraries] 。特に図。

```scala
sealed abstract class JValue
case object JNothing extends JValue // 'zero' for JValue
case object JNull extends JValue
case class JString(s: String) extends JValue
case class JDouble(num: Double) extends JValue
case class JDecimal(num: BigDecimal) extends JValue
case class JInt(num: BigInt) extends JValue
case class JBool(value: Boolean) extends JValue

case class JObject(obj: List[JField]) extends JValue
  // toStringすると → JObject(List( (k1,v1), (k2,v2), ... ))  
case class JArray(arr: List[JValue]) extends JValue
  // toStringすると → JArray(List( v1, v2, ... ))

type JField = (String, JValue)
```

注: JField は JValue ではない。



### Json文字列 ←→ AST

```scala
scala> import org.json4s._
scala> import org.json4s.native.JsonMethods._

// パース
val json = parse(""" { "numbers" : [1, 2, 3, 4] } """)   // JObject

// 文字列に出力
compact(render(json))  // 1行の文字列に出力
pretty(render(json))   // 人が見やすい形の複数行の文字列に出力
```


### データ構造の構築

プリミティブな値、Seq、Taple2[String, A] がそれぞれ、
JSONのプリミティブ値、JArray、JObjectになる。
(正確には、必要となったタイミングで AST に暗黙の型変換される)

まっさらからやる場合
```
import org.json4s.JsonDSL._

// === Json Array ===
val json = List(1,2,3)      // Seq → JSON配列
// 型がまざっているときは JsonAST.concat 使う
val arr2 = JsonAST.concat("aaa", 2, "ccc")

// === Json Object ===
val f1 = ("name" -> "joe")  // (String, JValue) のタプル → JField
val obj = ("name" -> "joe") ~ ("age" -> 35)  // JField を '~' でつなぐとJObject
※ 同じキーのFieldを連結しても、両方とも存在してしまう。

// 単一のJField でも必要に応じて JObject に暗黙に変換されるが、
// あえて明示的に JObject にしたい場合は、 以下のようにする
val objSingle: JObject = ("name", "joe")
val objSingle = ("name", "joe"): JObject

// 一度に作らなくても、以下のように追加していける
val arr2 = arr ++ "aaa"   // TODO 未検証
val obj2 = obj ~ ("gender" -> "male")  // DSLオブジェクトの場合
val obj2 = obj merge ("gender" -> "male")  // ASTオブジェクトの場合 TODO 未検証

// 入れ子で階層的なデータ構造も作れる
val obj = 
  ("name" -> "joe") ~
  ("age" -> 22) ~
  ("father" -> ("name" -> "fred") ~ ("age" -> 48) ) ~
  ("friends" -> List(
    ("name" -> "bob") ~ ("age" -> 20),
    ("name" -> "alice") ~ ("age" -> 21)
  ))

// JNothing という値は、なかったことになる。
// ある条件のときだけ値を入れるようなときに便利
val a1 = JsonAST.concat(
  "aaa",
  123,
  if ( a > 5 ) 999 else JNothing )

val obj1 = 
  ("name" -> "Joe") ~
  ("height" -> 180) ~
  if ( gender == "M" ) ("weight" -> 65) else JNothing
```

### データ構造の追加・変更・一部削除

#### merge を使う。(追加。変更) 

- [json4s/Merge.scala at 3.4 ・ json4s/json4s](https://github.com/json4s/json4s/blob/3.4/ast/src/main/scala/org/json4s/Merge.scala)
- [json4s/MergeExamples.scala at 3.4 ・ json4s/json4s](https://github.com/json4s/json4s/blob/3.4/tests/src/test/scala/org/json4s/MergeExamples.scala)

構造・名前を再帰的に照らしあわせて行って、
- object1 merge object2 ==> mergeFields
  + どちらかにしか存在しない名前のfieldは採用
  + 同じ名前のfield は それぞれの値をmerge
- arr1 merge arr2 ==> mergeVals
  + arr1 の後ろに、arr2の中でarr1に出現しない要素を追加したもの
- JNothing merge x ==> x
- x merge JNothing ==> x
- 上記以外(値と値とか、値とObj、値とArray、ObjとArry) ==> 右辺に書いたものを採用

```
scala> val lotto1 = parse("""{
         "lotto":{
           "lotto-id":5,
           "winning-numbers":[2,45,34,23,7,5,3],
           "winners":[{
             "winner-id":23,
             "numbers":[2,45,34,23,3,5]
           }]
         }
       }""")

scala> val lotto2 = parse("""{
         "lotto":{
           "winners":[{
             "winner-id":54,
             "numbers":[52,3,12,11,18,22]
           }]
         }
       }""")

scala> val mergedLotto = lotto1 merge lotto2

scala> pretty(render(mergedLotto))
res0: String =
{
  "lotto":{
    "lotto-id":5,
    "winning-numbers":[2,45,34,23,7,5,3],
    "winners":[{
      "winner-id":23,
      "numbers":[2,45,34,23,3,5]
    },{
      "winner-id":54,
      "numbers":[52,3,12,11,18,22]
    }]
  }
}
```

#### replace を使う。(変更、削除)

[json4s/MonadicJValue.scala at 3.4 ・ json4s/json4s](https://github.com/json4s/json4s/blob/3.4/core/src/main/scala/org/json4s/MonadicJValue.scala)

```
定義
def replace(l: List[String], replacement: JValue): JValue
```

- object の l で指定されるFieldの値を replacement に置換した新しいObjectを返す。
- l で指定したFieldが存在しない場合は、そのまま
- l で指定した経路が Object でない場合も そのまま

```
obj2 = obj.replace(List("father", "weight"), 85)
obj2 = obj.replace("father" :: "weight" :: Nil, 85)
```

TODO JNothing に置換したら、そのField を消せるか？


#### 下の方にあるArrayの内容をいじる

replace と Seq操作を組み合わせる

TODO



### データ構造を再帰的に辿って複数の値に同様の処理を行う

```
/*
mapField --- 再帰的に辿って、Fieldを操作した新しい json構造を返す
transformField --- mapFieldの partial function 版(つまりマッチしないところはそのまま)
map --- 再帰的に辿って、値を操作した新しい json構造を返す
transform --- map の partial function版(つまりマッチしないところはそのまま)
*/

json.mapField {
  case ("age", JInt(x)) => ("age", JInt(x+1))
  case x => x
}

json.transformField {
  case ("age", Jint(x)) => ("age", JInt(x+1))
}

json.map {
  case Jint(x) => Jint(x+1)
  case x => x
}

json.transform {
  case Jint(x) => Jint(x+1)
}

/*
removeFiled --- 条件に合うFieldを除いた新しい json構造を返す
remove --- 条件に合う値を除いた新しい json構造を返す
*/

json.removeField {
  case ("age", _) => true
  case _ => false
}

json.remove { _ == JNull }
```



## 値を取得する

###  "LINQ" style

```
for {
  JObject(child) <- json
  JField("age", JInt(age))  <- child
} yield age
```

### XPath + HOFs

[json4s/MonadicJValue.scala at 3.4 ・ json4s/json4s](https://github.com/json4s/json4s/blob/3.4/core/src/main/scala/org/json4s/MonadicJValue.scala)

`\ String型` は直下(ただしそこがJArrayだった場合、JArrayでなくなるまでは再帰的に下る)から、そのkeyをもつフィールドの値を返す。
結果が１つだったら、その値を、
複数だったら JArrayとして返す

`\ Class型` は、直下(ただしそこがJArrayだった場合、JArrayでなくなるまでは再帰的に下る)から、その型の値を抜き出して返す。
JObjectだったら、直下のFieldで値の型が指定クラスのもの、
(JArrayだったら、再帰)
自身が値だった場合には、マッチしない。
１つでも複数でも List型で返る。


`\\ String型` は再帰的に そのkeyを持つFieldを探す。
結果が１つだったら、その値を、
複数だったら、JObjectとして返す

`\\ Class型` は再帰的にその型の値を返す (JFieldの値、JArrayの要素値)。
１つでも複数でも List型で返る。

```
json: JObject =
  ("person" ->
    ("name" -> "Joe") ~
    ("age" -> 35) ~
    ("spouse" ->
      ("person" ->
        ("name" -> "Marilyn") ~
        ("age" -> 33)
      )
    )
  )

compact(render(json \\ "spouse"))
// json以下で "spouse" をキーに持つFieldを探す。結果が単一なのでその値を返す。
→ res1: String = {"person":{"name":"Marilyn","age":33}}

compact(render(json \\ "name"))
→ res2: String = {"name":"Joe","name":"Marilyn"}

scala> compact(render(json \ "person" \ "name"))
res4: String = "Joe"
scala> compact(render(json \ "person" \ "spouse" \ "person" \ "name"))
res5: String = "Marilyn"
```

```
val json = parse("""
         { "name": "joe",
           "children": [
             { "name": "Mary", "age": 5 },
             { "name": "Mazy", "age": 3 }
           ]
         }
       """)

scala> (json \ "children")(0)
res0: org.json4s.JsonAST.JValue = JObject(List((name,JString(Mary)), (age,JInt(5))))
// Json直下の"children" の 0番めの値を返す

scala> (json \ "children")(1) \ "name"
// Json直下の"children" の 1番めの値を返す
res1: org.json4s.JsonAST.JValue = JString(Mazy)

scala> json \\ classOf[JInt]
res2: List[org.json4s.JsonAST.JInt#Values] = List(5, 3)
// json 以下で、JInt型の値をまとめて返す

scala> json \ "children" \\ classOf[JString]
// json直下の"children" 以下で、JSring型の値をまとめて返す
res3: List[org.json4s.JsonAST.JString#Values] = List(Mary, Mazy)
```


### 関数を使って条件にある値だけを取り出す系

[json4s/MonadicJValue.scala at 3.4 ・ json4s/json4s](https://github.com/json4s/json4s/blob/3.4/core/src/main/scala/org/json4s/MonadicJValue.scala)

findField --- 再帰的にたどって、評価関数がtrueになる最初のFieldを返す (返り値は Option[JField])
find --- 再帰的にたどって、評価関数がtrueになる最初の値を返す (返り値は Option[JValue])
(find系は、関数は partial function なので、caseに漏れがあってもOK？)

```
json.find { _ == JInt(2) } 
json.findField { case (n,v) => n == "age"}
```

filterField --- 再帰的にたどって、評価関数がtrueになるFieldのListを返す (返り値は List[JField]) 
filter --- 再帰的にたどって、評価関数がtrueになる値のListを返す (返り値は List[JValue]) 

```
json.filterField {
  case ("age", JInt(x)) if x > 18 => true
  case _ => false
}

json.filter {
  case Jint(x) => x > 1
  case _ => false
}
```

withFilter ってのもあるよ。

