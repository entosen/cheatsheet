


TODO 以下未整理
========================

オペレーター
---------------------

::

  ``?:`` エルビスオペレーター
  false と判定される場合に、デフォルト値を指定する。
  数値型に使う場合は0の場合も変換されてしまうので注意 

  user.name ?: "Anonymous"
  user.name ? user.name : "Anonymous" と同じ。


  ``?.`` オペレーター
  nullの可能性があるオブジェクトのメソッドを呼ぶ場合に利用する。

  person?.name


  ``.@`` オペレーター
  getter / setter がある場合に、インスタンス変数を直接参照/更新する場合に利用する。

  user.name   // getter から取得
  user.@name  // インスタンス変数を直接取得

  ``.&`` オペレーター
  メソッドポインタを取得

  def getNameInstance = user.&getName
  getNameInstance()

  ``*.`` オペレーター
  リスト中の特定項目のみを集めたリスト。collectメソッド(Javaのstreamのmapメソッド)の簡易版
 
  cars.collect { it?.make }   // リストの各要素の make を抜き出したリスト。collectを使う場合。
  cars*.make

  null要素があってもOK。その要素の結果は null。
  リスト自体がnullでもOK。その場合は結果は null。

  ``*`` オペレーター
  引数やリスト中にリストを展開。
  def args = [4, 5, 6]
  function(*args)         // function(4, 5, 6)
  function(1, *args, 10)  // function(1, 4, 5, 6, 10)
  [1, 2, 3, *args, 7]     // [1, 2, 3, 4, 5, 6, 7]

  ``*:`` オペレーター
  Mapの中にMapを展開
  def subMap = [c: 3, d: 4]
  def map = [a: 1, b: 2, *:subMap, e: 5]   //  [a:1, b: 2, c: 3, d: 4, e: 5]

  ``<=>`` オペレーター
  compareTo メソッドと等価
  a <=> b

  ``in`` オペレーター
  "Emmy" in list
  list.contains("Emmy")
  list.isCase("Emmy")


  

