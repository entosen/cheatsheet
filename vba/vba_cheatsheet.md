
# 前準備

## 最初の一回

参考:
[[Excel2013 で VBA] Visual Basic for Applications (VBA) を用いる準備](http://brain.cc.kogakuin.ac.jp/~kanamaru/lecture/vba2013/01-intro00.html)

- ファイル ＞ オプション ＞ リボンのユーザー設定 ＞ 開発にチェック
- 開発 ＞ マクロのセキュリティ ＞ マクロの設定 ＞ 警告を表示してすべてのマクロ
  を無効にするを選択
- 開発 ＞ Visual Basic
  - 表示 ＞ ツールバー ＞ 「デバッグ」と「標準」にチェック
    - ツールボックスが浮遊するので、ドラッグしてツールバーに収める (お好みで)
  - ツール ＞ オプション ＞ 編集タブ ＞ 変数の宣言を強制する

# 流れ

## 始め方

- 開発 ＞ Visual Basic ＞ 挿入 ＞ 標準モジュール
- 開発 ＞ 挿入 ＞ ボタンなどをシートに追加して ＞ マクロの登録で「新規作成」


## 実行

- 実行は F5 (もしくはツールバーの再生ボタンっぽいやつ)
    - カーソル位置のプロシージャが実行される


# 言語的なこと

## 階層

- Book
    - Microsoft Excel Objects
	- Sheet1
	- ThisWorkbook
    - 標準モジュール
	- Module1
	    - プロシージャ (Sub で始まるやつ)

変数のスコープ

- モジュールレベル
    - プロシージャーレベル



## スタイル

- 大文字小文字は区別されない？
- インデント幅は？ 空白？ タブ？


## 基本構文

```
' コメントはシングルクオートで始める

Sub prog1() 
    MsgBox "こんにちは"
End Sub

' 複数文を1行に書きたい場合はセミコロンで区切る
Sub prog1(): MsgBox "こんにちは": End Sub

' １つの文を複数行に分けて書きたい場合は _ を置いて改行
MsgBox _
"こんにちは"
```

## 変数、型、およびリテラル、演算子、定数

```
Dim x As Integer ' 宣言
    x = 2        ' 代入

' 複数の宣言を1行で
Dim i As Integer, n As Integer

' 定数を宣言
Const myName As String = "..."
```

変数名は大文字小文字を区別しないと思っていた方がいい。
本当はどうかわからないが、VBAのエディタでは、
大文字小文字はどちらかに揃えられてしまうので、入力できない。


[データ型の概要](https://msdn.microsoft.com/ja-jp/library/office/gg251528.aspx "データ型の概要")

型
Integer: 整数型 2バイト？ -32768～32767
Long: 整数型 4バイト？
LongLong: 整数型 4バイト？
Single: 4バイト実数
Double: 8バイト実数
String: 文字列型
Boolean: 論理型
Date: 日付型
Object: オブジェクト型
Variant: 任意のデータ型を格納できる

型を指定しない(As ... をつけないと)、Variant 型になるっぽい。



代入

型違い代入
```
i = "10"    ' OK Stringが数値に変換できる文字列なら可能
i = "AAA"   ' エラー
i = "10.6"  ' OK 11 四捨五入される
i = True    ' OK -1 が入る
i = False   ' OK 0 が入る

s = 10      ' OK "10" という文字列
s = 10 / 3  ' OK "3.33333333333333" という文字列 たぶん。
s = 3 < 4   ' OK "True" という文字列
```

演算子の優先順位とその変更方法 - Excel VBA
http://www.239-programing.com/excel-vba/basic/basic046.html

### 数値型

```
Dim i As Integer
    i = 10

Dim f As Double
    f = 5.5
    f = 5#   ' 5.0 のこと？？？
```


```
a + b  ' 加算
a - b  ' 減算
a * b  ' 乗算
a / b  ' 実数の除算
a \ b  ' 整数の除算(商)
a Mod b ' 整数の除算における余り
a ^ b  ' べき乗
- a    ' 符号の反転

a = b  ' 等しい  これはなぜ代入にならないのか？ 
       ' 代入なのか比較なのかは文脈で決まるっぽい
       ' どうやって決まっているかはまだよくわからない...。
> < >= <=
a <> b    ' 等しくない
```

### 文字列型

```
Dim s As String
    s = "文字列"
```

```
s1 & s2   ' 文字列の連結

s1 Link pattern ' ワイルドカード的なマッチ ? * # [ ] [! ]

' 文字列の分割
Dim a() As String ' 配列を受けるために動的配列、もしくはVariant型にしておく
a = Split("aaa,bbb,ccc", ",")
```

### Boolean

```
Dim b As Boolean
    b = True
    b = False
```

```
Not b    ' 否定
a And b  ' 論理積 (整数に使うとbit論理積になるので注意)
a Or b   ' 論理和 (整数に使うと(略))
a Xor b  ' 排他的論理和 (これも整数に使うと(略) か？)

```

And, Or は短絡評価してくれない。
つまり、 Andの左辺がFalseでも、右辺の評価がされる。。。
VB.NET には以下のようなのがあるらしいが、VBAでは使えないようだ。

```
a AndAlso b ' 論理積 (短絡評価する)
a OrElse b ' 論理積 (短絡評価する)
```

### Variant 型

Variant型は Object型よりも上位。なんでも入る。

基本的には、Variant型を使わずに Long型やString型など明示的な型を使用した方がよい。

Variantの使いどころ

セルが空かどうかを扱いたいとき。

```
Dim i As Long
Dim s As String
Dim v As Variant

i = Cells(1,1).Value ' Empty のとき 0 になる
s = Cells(1,1).Value ' Empty のとき "" になる
v = Cells(1,1).Value ' Empty はそのままEmptyと扱われる

IsEmpty(i) ' false。 0扱いになっているから？
IsEmpty(s) ' false。 ""扱いになっているから？
IsEmpty(v) ' true。

i <> ""    ' 型違いでエラーになる
v <> ""    ' Empty もしくは "" のときに false
```

配列を受ける必要があるとき。
でもこれは動的配列が使えるはず。


### オブジェクト型

一般的には、オブジェクト型の変数には参照を入れるので、Set を使う。

```
Dim r As Range
Set r = Range("A1:C3")

' Setをつけないと
' 「オブジェクト変数または With ブロック変数が設定されていません。」と言われる
' r = Range("A1:C3") 

' Object以外のものを Set で入れようとすると 「型が一致しません」エラーになる
Dim v As Variant
Set v = True
```

### キャスト

型変換関数
```
CBool(式)
CByte(式)
CCur(式)
CDate(式)
CDbl(式)
CInt(式)
CLng(式)
CSng(式)
CVar(式)
CStr(式)
```

### 配列

配列の添字の下限値は、モジュールオプション Option Base によってきまる。
デフォルトは 0。`Option Base 1` とすると添字は1始まりになる。

```
Dim score(10) As Integer  ' 宣言 この場合要素番号は 0～10 の 11個になる。!!!
                          ' 長さ指定は定数でないといけない。
Dim score(1 to 10) As Integer ' 下限も指定する場合

score(3) = 100            ' 代入。
score(3)                  ' 参照。


' 2次元配列
Dim sintable(9,1) As Double  ' 10行x2列 の2次元配列を宣言
points(0, 0) = 0.1
points(0, 1) = Sin(0.1)


' 動的に配列サイズを決めたい場合は ReDim を使う
Dim n As Integer
n = 10
Dim x() As Integer
ReDim x(n)  ' 配列を動的に確保。
...
Erase x     ' 配列がもう不要になった場合。
```

ReDim を何回も呼ぶことは可能だが、その度中身はクリアされる。
`ReDim preserve x(100)` とやれば中身を保持したまま可能。ただし変えられるのは配列の上限のみ。

### コレクション

```
Dim c As Collection
Set c = New Collection
もしくは
Dim c As New Collection

c.Add Item:="アイテム1"
c.Add Item:="アイテム2"
もしくは
c.Add Item:="アイテム1", Key:="i1"  ' Itemは重複を許すが、Keyは重複を許さない
c.Add Item:="アイテム2", Key:="i2"

c.Count  ' 要素数取得
c(1)     ' Add した順の番号を指定して。先頭は1。
c("i1")  ' Add したときの Key を指定して。

For Each elm In c
    ...
Next elm
```

### Null とか Empty とか Nothing とか

参考: [NullとEmptyとNothingと空の文字列の違い：Access VBA｜即効テクニック｜Excel VBAを学ぶならmoug](https://www.moug.net/tech/acvba/0050010.html)

- 長さ0の文字列
- 値0の文字列
- Empty
- Null
- Nothing

```
Debug.Print VarType(myVar)  '--> 1（定数vbNull）と表示される
Debug.Print TypeName(myVar) '--> Null　と表示される
Debug.Print IsNull(myVar)   '--> True　と表示される
```


## 制御構造

If
```
If x Mod 2 = 0 Then  ' 注 == じゃなくて = なんだな。
    ...
End If

' 1行であればこれでも可
If 条件式 Then 処理


If x Mod 2 = 0 Then
    ...
Else
    ...
End If


If 条件1 Then
    ...
ElseIf 条件2 Then
    ...
ElseIf 条件3 Then
    ...
End If
```

Select Case
```
Select Case myMonth
Case 4, 5, 6
    ...
Case 7 To 9
    ...
Case 10, 11, 12
    ...
Case Else
    ...
End Select


Select Case Points
Case Is < 0, Is > 100    'Pointsが0未満または100を超える場合
    ...
Case Is >= 70
    ...
Case Else
    ...
End Select
```


ループ
```
Dim x As Integer  ' ループ変数は宣言済みでないといけない
For x = 1 To 10   ' 10の時も実行、11は実行されない
    ...
Next x

For x = 0 To 10 Setp 2
    ...
Next x

' Exit For を使うことでループを抜けられる (C言語のbreak相当)


' 配列やコレクションの全要素をループする
Dim elm As Variant   ' 配列に対して使う場合は Variant か、変数の型を省略
For Each elm In Points
    ...
Next elm

Dim elm As Worksheet  ' コレクションの中身と同じオブジェクトで定義(sなし)
For Each elm In Worksheets '(sあり)
    ...
Next elm



While x <= 10     ' Do が省略できる？
    ...
Wend

Do While 条件式   ' 条件文がはじめ、満たしているうちはループ
    ...
Loop

Do Until 条件式   ' 条件文がはじめ、満たさないうちはループ
    ...
Loop

Do                ' 条件文が最後、満たしているうちはループ
    ...
Loop While 条件式

Do                ' 条件文が最後、満たさないうちはループ
    ...
Loop Until 条件式

' Exit Do で ループを途中で抜けることができる (C言語のbreak相当)
```

With ステートメント。
あるオブジェクトに対して複数の操作をやりたいとき。
```
With Range("B3")
    .Value = "test"
    .Interior.Color = vbYellow
    .Borders.LineStyle = xlContinuous
End With

' 入れ子にもできます。
With ActiveSheet.Range("A3")
    .Value = "これはテストです。"
    .Interior.Color = vbYellow      'セル内の色を黄色にします。

    'さらにA3セル内のフォントに対してプロパティの変更を行います。
    With .Font
	.Size = 12          'セル内のフォントサイズを12にします。
	.Bold = True        'セル内のフォントを太字にします。
	.Color = vbBlack    'セル内のフォント色を黒にします。
    End With
End With
```

## プロシージャ、サブルーチン、関数

値を返さない Sub プロシージャ と、
値を返す Function プロシージャ がある

定義
```
Sub mysub0()        ' 引数をとらない。この場合でも定義の空括弧は必要。
    ...
End Sub

Sub mysub1(s As String)  ' 引数を取る
    ...
End Sub

Sub mysub2(name As String, age As Integer)  ' 複数の引数を取る
    ...
End Sub

Function sq(x As Double) As Double  ' 値を返す関数
    ...
    sq = x * x    ' 名前 = 結果  とすることで値が返される
End Function


' 引数は参照渡しのため、
' プロシージャの中で代入すると呼び出し元の変数値を変更することができる
' 値渡しにしたい場合は、ByVal を引数名の前に付ける。
Sub mySub22(ByVal name As String, ByVal age As Integer)
    ...
End Sub

' デフォルト引数
Sub mySubDefault(Optional age As Integer = 18)
    ...
End Sub
```

途中で抜けたい場合は
```
Exit Sub
Exit Function
```



呼び出し
```
' Subプロシージャの呼び出し
mysub0
mysub1 "aaa"
mysub2 "aaa", 18
' Subプロシージャの引数を括弧付きで囲むことも可能なよう
' やっぱりだめかも。引数１つだからうまくいっていただけかも。
' mysub1("aaa")  ○
' mysub2("aaa", 18)  ×

' Function の呼び出し
d = sq(x)     ' 引数のリストを括弧で囲む

' 名前付き引数を用いて呼び出す
Offset(rowOffset:=3, columnOffset:=3)
```


再帰呼び出しも可

プロシージャのスコープ
- Private : 同一モジュール内でのみ呼び出しが可能
- Public : 同一プロジェクト内の全てのプロシージャから呼び出し可能 (デフォルト)

## 出力

```
MsgBox "文字列"  ' ポップアップダイアログを出す
Debug.Print "文字列"  ' イミディエイトウィンドウに表示


Chr(10) ' 改行文字
```


# Excelオブジェクト


```
x = Sheet1.Cells(1, 1).Value   ' (行,列)。 1から始まり。
Sheet1.Cells(1, 1).Value = y

With Sheet1
    x = .Cells(1,1).Value
    .Cells(1,1).Value = x + y
End With

' 配列のデータを指定の範囲のセルに出力
' 1セル1セル入れるより、ずっと速い。
' Rangeが1行だとしても、配列は 2次元配列でやり取りする。

Dim celldata() As Variant
ReDim celldata(nd - 1, 1)   ' nd行x2列分の配列を宣言
Range(Cells(1,1), Cells(nd,2)) = celldata 

' 指定範囲のセルを配列として読み込み
Dim celldata As Variant      ' 配列として宣言しなくてよいの？？？
celldata = Range(Cell(1,1), Cell(2,3)).Value  ' こっちはValueがいるの？？？
```

## コレクション型共通

コレクションとは ＝ 同種のオブジェクトが複数集まったもの。
Worksheet に対して Worksheets など。

Rangeだけちょっと特別。Ranges オブジェクトはない。Range自体もコレクション。

コレクションの中から要素を１つ取得するには
```
コレクション.Item(インデックス数値)  ' 最初は1
コレクション.Item(オブジェクト名)
コレクション(インデックス数値)    ' .Item は省略できる
コレクション(オブジェクト名)
例
Workbooks("Book1.xls")
Worksheets("Sheet1")
Worksheets(2)
```

コレクションの数を知るには
```
コレクション.Count
```

コレクションでループするには
```
' インデックス番号を使って
For i = 1 To c.Count   
    ... c(i) ...
Next i

' For Eash を使って
For Each r In Range("2:5").Rows
    ....
Next r
```


## WorkSheet オブジェクト

```
Worksheets(1)   ' シートの並び順 最初が1。非表示のにも番号はつけられる
Worksheets("Sheet1")   ' 名前で指定
ActiveSheet            ' 現在アクティブなシート
Worksheets("Sheet1").Activate  '指定のシートをアクティブに
```

## Rangeオブジェクト

セルの塊(領域)を表すオブジェクト。
基本は2点(左上と右下)の矩形で表される領域。例えば Range("B2:E4")。


Areasプロパティ

Range には複数の領域を含むこともできる。例えば Range("B2:E4,F6:G8")。 
Range.Areas は含まれている領域のコレクション。 Range.Areas.Count で個数がわかる。
Rangeオブジェクトの幾つかのプロパティは、最初の領域しか対象としないものがあるので注意。(Rowsなど)


コレクション

Rangeはコレクションでもある。しかし、コレクションの単位がいろいろある。
- 普通に作ると、セル単位。 Areas順、かつ、矩形の左から右、折り返して下の行、という順でまわる
- Rows で作ると、行単位に回る。
- Columns で作ると、列単位に回る。
- Rows,Columns で作ったRangeも、引数なしのCellsプロパティで、セル単位のRangeに変換できる

### 生成

```
' Worksheet もしくは Range から。
' 上位オブジェクトを指定しない場合は、現在アクティブなシートから。
' Rangeに対しておこなった場合は、その中での位置となる

' Cells プロパティは1つのセルを返す。
.Cells(6,1)              ' 1つのセル。 行x列番号(1始まり)で指定
.Cells(6,"B")            ' 1つのセル。 
.Cells(20)               ' 範囲の中で 左から右、次の行に折り返しで数えた番号で指定
' ただし、引数なしのCellsは全体を返す
.Cells                   ' シート(もしくはRange)の全てのセル


' Rangeプロパティはいくつかのセルの集まりを返す
' 以下は全てセル単位のコレクションとなる
' もとのRangeの範囲よりも大きく指定してもよい。大きくなる。
' カンマ区切りは(たとえ重なりや隣接で1つの矩形になるとしても)別の領域になる
Range("A1")             ' セル A1
Range("A1:B5")          ' セル A1 から B5 まで
Range("C5:D9,G9:H16")   ' 複数の範囲の選択。Areas.Count==2
Range("A:A")            ' 列 A 。Countは 1048576
Range("1:1")            ' 行 1 。Countは 16384
Range("A:C")            ' 列 A から C まで。countは 3145728
Range("1:5")            ' 行 1 から 5 まで。count は 81920
Range("1:1,3:3,8:8")    ' 行 1、3、8 全体。 Areas.Count==3。Count は49512
Range("A:A,C:C,F:F")    ' 列 A、C、および F。 Areas.Count==3。

Range(Cells(1,1), Cells(5,3)) '矩形をCells を用いて指定もできる。セル(1,1)A1から(5,3)C5

[A1:B5]                 ' Range("A1:B5") のショートカット
[A2]
[A1:B5,D8:E9]


' Raws,Colums は行指定・列指定でRangeを生成する
' この場合のコレクションは行単位、列単位になる。
' もとのRangeの範囲をはみ出さない。部分集合になる
' 複数領域のRangeに対しては、最初の領域しか認識しない！！よって結果のAreas.Countは1になる
Raws(1)       ' 行1。行単位のコレクション。 Count == 1。
Columns(1)    ' 列1。列単位のコレクション。 Count == 1。
Columns("A")  ' 列1。列単位のコレクション。 Count == 1。
Raws          ' 全ての行(実質元のレンジと同じ範囲)。行単位のコレクション
Columns       ' 全ての列(実質元のレンジと同じ範囲)。列単位のコレクション


' EntireRowは、そのRangeが重なっている行(元のRangeを左右に伸ばした形)の範囲を返す。
' 返る新しいRangeは行単位コレクション。
' 元のRangeが複数領域を含む場合、それぞれに対して行われる。
' (領域の数は変わらない。たとえ重なったとしても)
' EntireColumn は列に対して同様。
myrange.EntireRow    ' そのRangeに重なる行 (元のレンジを左右に伸ばした形)。行単位コレクション
myrange.EntireColumn ' そのRangeに重なる列 (元のレンジを上下に伸ばした形)。列単位コレクション

' ずらして生成
ActiveCell.Offset(1,3)  ' 基準のセルからの相対位置(1行下、3桁右)でセルを指定
myRange.Offset(1,3)     ' myRenge を (+1,+3) ずらしたもの

myRange.CurrentRegion   ' 元の範囲を含み、空白行と空白列で囲まれた矩形領域

Selection  ' 現在の選択範囲

' Range の合成
' もし、領域が接するか重なりあって１つの矩形で表せるときは、１つの領域になる
' そうでないときは複数の領域になる
' 領域の順番は不定っぽい。
' 結果はセル単位のコレクションになる
Union(Rows(1), Rows(3), Rows(5)) 
```

プロパティ
```
Range.Count ' コレクションの個数
Range.Row    ' 最初の領域の先頭行の行番号。 Long型
Range.Column ' 最初の領域の先頭列の列番号。 Long型
```


## 保護、ロック、編集させたくない

あるセルの内容を編集できなくするには、
「セルのロックが有効、かつ、ワークシートの保護が有効」にする。

### セルのロック

UIからは、セルの書式設定 ＞ 保護 ＞ ロック 。

VBAからは
```
' ロック状態の参照
Range("A1:B3").Locked
  → True : ロックされている
  → False : ロックされていない
  → Null : 混在

' 設定
Range("A1:B3").Locked = True
```

### シートの保護

UIからは、校閲 ＞ シートの保護

オプションとして、保護中でも許可する操作をチェックボックスで選べる。

UIからシートの保護をON/OFFする場合は、「許可する操作」の状態は保持される。

VBAでやる場合
```
' 参照
ActiveSheet.ProtectContents  ' シート保護の有効無効
ActiveSheet.ProtectionMode   ' TrueならUIからのみ変更不可。FalseならUI・スクリプトともに変更不可
ActionSheet.Protection       ' 「許可する操作」の状態
    .AllowFormattingCells
    .AllowFormattingColumns
    .AllowFormattingRows
    .AllowDeletingColumns
    .AllowDeletingRows
    .AllowInsertingColumns
    .AllowInsertingRows
    .AllowInsertingHyperlinks
    .AllowFiltering
    .AllowSorting

' 操作
ActiveSheet.Protect     ' シートの保護
ActiveSheet.Protect UserInterfaceOnly:=True     ' UIからのみ変更不可にする
' 上記操作では、UIの「許可する操作」の状態は引き継がれず、基本Falseにされてしまう。
' なので、追加の引数でそれらを希望の状態に設定する必要がある。
' UserInterfaceOnly の指定は、ファイルを閉じるまでしか有効じゃない。

ActiveSheet.UnProtect   ' シートの保護の解除
```

```
' 指定したシートの状態を文字列で表現して返す
Function toStringSheetProtection(s As WorkSheet) As String
    Dim p As Protection
    Set p = s.Protection
    toStringSheetProtection = "" _
        & "ProtectContents          = " & s.ProtectContents & Char(10) _
        & "ProtectionMode           = " & s.ProtectionMode & Char(10) _
        & "AllowFormattingCells     = " & p.AllowFormattingCells & Chr(10) _
        & "AllowFormattingColumns   = " & p.AllowFormattingColumns & Chr(10) _
        & "AllowFormattingRows      = " & p.AllowFormattingRows & Chr(10) _
        & "AllowDeletingColumns     = " & p.AllowDeletingColumns & Chr(10) _
        & "AllowDeletingRows        = " & p.AllowDeletingRows & Chr(10) _
        & "AllowInsertingColumns    = " & p.AllowInsertingColumns & Chr(10) _
        & "AllowInsertingRows       = " & p.AllowInsertingRows & Chr(10) _
        & "AllowInsertingHyperlinks = " & p.AllowInsertingHyperlinks & Chr(10) _
        & "AllowFiltering           = " & p.AllowFiltering & Chr(10) _
        & "AllowSorting             = " & p.AllowFiltering & Chr(10)
End Function
```

```
' 許可操作を保持したまま、Protect操作をする
Sub protectWithPresentAllows( _
    sheet As Worksheet, _
    Optional UserInterfaceOnly As Boolean = False)

    Dim p As Object
    Set p = sheet.protection

    sheet.Protect _
        UserInterfaceOnly:=UserInterfaceOnly, _
        AllowFormattingCells:=p.AllowFormattingCells, _
        AllowFormattingColumns:=p.AllowFormattingColumns, _
        AllowFormattingRows:=p.AllowFormattingRows, _
        AllowInsertingColumns:=p.AllowInsertingColumns, _
        AllowInsertingRows:=p.AllowInsertingRows, _
        AllowInsertingHyperlinks:=p.AllowInsertingHyperlinks, _
        AllowDeletingColumns:=p.AllowDeletingColumns, _
        AllowDeletingRows:=p.AllowDeletingRows, _
        AllowSorting:=p.AllowSorting, _
        AllowFiltering:=p.AllowFiltering, _
        AllowUsingPivotTables:=p.AllowUsingPivotTables

End Sub
```

# 未整理

```
' 高速化のため
Application.ScreenUpdating = False  ' 画面更新抑制
...                                 ' 大量の更新を行う
Application.ScreenUpdating = True   ' 画面更新抑制
```

Visual Basic 言語リファレンス
https://msdn.microsoft.com/ja-jp/library/office/jj692818.aspx

オブジェクト モデル (Excel ＶＢＡ リファレンス)
https://msdn.microsoft.com/ja-jp/library/ff194068.aspx


プロシージャ、制御構文、変数、セル、シート、各種関数の使用方法解説 - Excel VBA
http://www.239-programing.com/excel-vba/index.html

vimキーバインドは使えないか？

