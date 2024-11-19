=======================
MUI Data Grid
=======================

表を作るコンポーネント

ライセンス
======================

::

  npm install @mui/x-data-grid          // 無料
  npm install @mui/x-data-grid-pro      // 有料pro
  npm install @mui/x-data-grid-premium  // 有料premium


- `React Data Grid component - MUI X <https://mui.com/x/react-data-grid/>`_



無料・有料の違いで機能に差がある。



- 無料 MIT license

  - ``import { DataGrid } from '@mui/x-data-grid';``
  - 編集、ページング、カラムのグループ化、単一カラムでのソートとフィルタ

- 有料 Pro plan

  - ``import { DataGridPro } from '@mui/x-data-grid-pro';``
  - アドバンスドフィルタリング、カラムpinning、カラムおよび行のreordering、
    ツリーデータのサポート、巨大なデータセットを扱うためのvirtualization

- 有料 Premium plan

  - ``import { DataGridPremium } from '@mui/x-data-grid-premium';``
  - データアナリシス、巨大なデータセット
  - 集約関数(合計・平均など)での行のグルーピング
  - エクセルファイルへのexport

参照

- https://mui.com/x/react-data-grid/
- 機能の比較表 https://mui.com/x/react-data-grid/getting-started/#licenses



チートシート
===================

::

  import * as React from 'react'
  import { DataGrid, GridRowsProp, GridColDef } from '@mui/x-data-grid';

  // 表示したいデータ (rowの配列)
  const rows: GridRowsProp = [
    { id: 1, col1: 'Hello', col2: 'World' },
    { id: 2, col1: 'DataGridPro', col2: 'is Awesome' },
    { id: 3, col1: 'MUI', col2: 'is Amazing' },
  ];

  // カラムの定義
  const columns: GridColDef[] = [
    { field: 'col1', headerName: 'Column 1', width: 150 },
    { field: 'col2', headerName: 'Column 2', width: 150 },
  ];

  export default function App() {
    return (
      <div style={{ height: 300, width: '100%' }}>
        <DataGrid rows={rows} columns={columns} />
      </div>
    );
  }



カラムの定義
====================

参照

- `Data Grid - Column definition - MUI X <https://mui.com/x/react-data-grid/column-definition/>`_
- `GridColDef API - MUI X <https://mui.com/x/api/data-grid/grid-col-def/>`_

カラム(s)は ``GridColDef[]`` で定義される。


TypeScriptの場合は？::

  GridColDef<Rowの型, カラム値の型>

field (必須)
----------------------

field: string (必須)

- rowからのフィールド取り出し方法のデフォルトとして使われる (ref. valueGetter)
- ヘッダ名のデフォルトとして使われる (ref. headerName)


セル値(value)
---------------

下記の3つは区別して扱う。

- row のフィールド値
- セルの内部で保持される値(セル値, value)
- renderされる値

セル値は、下記で使われる

- Filterling
- Sorting
- Renderling (valueFormatter or renderCell が指定されない限り)


::

      row
       |
       |  row[colDef.field]
       |  colDef.valueGetter()
       V
     value  <-- この値でソート、フィルタリングされる
       |
       |  colDef.renderCell()
       |  or colDef.valueFormatter()
       V
      表示


rowからの値(フィールド)の取り出し

#. デフォルトでは field と同名のフィールドを取り出す。 row[colDef.field]
#. valueGetter の指定があればそれも通す。


valueGetter の使いどころの例

- 値の変換 (小数をパーセント値に変換など)
- 複数のフィールドから1つの値を導出 (first name と last name の連結など)
- ネストされたフィールドからの導出 (user.address.city)

::

  // 引数1つ
  const columns: GridColDef[] = [
    {
      field: 'taxRate',
      valueGetter: (value) => {   // row[field] で取り出した値をさらに加工
        if (!value) {
          return value;
        }
        // Convert the decimal value to a percentage
        return value * 100;
      },
    },
  ];

  // 引数2つ
  const columns: GridColDef[] = [
    {
      field: 'fullName',
      valueGetter: (value, row) => {  // row から任意に取り出し加工
        return `${row.firstName || ''} ${row.lastName || ''}`;
      },
    },
  ];



レンダリング
-------------------


renderCell
^^^^^^^^^^^^^^^^^^^

戻り値は React node 。 なのでセルの中にリッチなものをなんでも作れる。

評価値(0〜5)を星の数で表したり。

::

  renderCell: (params: GridRenderCellParams<any, Date>) => (
    <strong>
      {params.value.getFullYear()}
      <Button
        variant="contained"
        size="small"
        style={{ marginLeft: 16 }}
        tabIndex={params.hasFocus ? 0 : -1}
      >
        Open
      </Button>
    </strong>
  ),


valueFormatter
^^^^^^^^^^^^^^^^^^^

戻り値は string 型。

renderCell の指定がないときの描画に使われる。

また、exporting のときにも使われる。

::

  valueFormatter: (value?: number) => {
    if (value == null) {
      return '';
    }
    return `${value.toLocaleString()} %`;
  },


type
---------------

カラム設定を楽にするために、基本的なtypeがあらかじめ定義されている。

===================   =========================  ================================================
type                  Value type                 効果
===================   =========================  ================================================
'string' (default)    string                     左寄せ。フィルタリング(contains, startsWithなど)
'number'              number                     右寄せ。フィルタリング(不等号など)
'date'                Date() object              日付形式(YYYY/MM/DD)で出力
'dateTime'            Date() object              日付日時形式(YYYY/MM/DD HH:MM:SS)で出力
'boolean'             boolean                    (/)(x)アイコンで出力。
                                                 フィルタリング(is true/false)
'singleSelect'        A value in .valueOptions   編集可にした場合に候補から選ぶようになる。
                                                 フィルタリング(is, is not, is any of)
'action'              値は取らない               セル内にアクションメニューを出せる
'custom' (※1)                                   デフォルトでは 'string' と同じ効果
===================   =========================  =================================================

(※1) ソースコードを見ると 'custom' というのがあった。'string' の場合と同じ値になっている。
独自のtypeを実装した場合は 'custom' にするのがいいっぽい。

typeの設定が効くところ

- 表示形式 (左/右寄せ、フォーマットなど)
- ソート順 (文字列順か数値順かなど)
- フィルタリングの方法

  - 文字系: contains, startsWith, など
  - 数値系: 不等号
  - などなど、形式にあわせたフィルタリング選択肢が出る

参考

- https://github.com/mui/mui-x/tree/master/packages/x-data-grid/src/colDef の 〜ColDef.tsx

  - GridColDef のデフォルト値の塊みたいになっているっぽい。::

      export const GRID_STRING_COL_DEF: GridColTypeDef<any, any> = {
        width: 100,
        minWidth: 50,
        maxWidth: Infinity,
        hideable: true,
        sortable: true,
        resizable: true,
        filterable: true,
        groupable: true,
        pinnable: true,
        // @ts-ignore
        aggregable: true,
        editable: false,
        sortComparator: gridStringOrNumberComparator,
        type: 'string',
        align: 'left',
        filterOperators: getGridStringOperators(),
        renderEditCell: renderEditInputCell,
        getApplyQuickFilterFn: getGridStringQuickFilterFn,
      };


独自型を作りたい場合。


TODO 例えば string[] とかだった場合どうするのがいいのか？


ソート
--------------------

参考

- `Data Grid - Sorting - MUI X <https://mui.com/x/react-data-grid/sorting/>`__
- https://github.com/mui/mui-x/blob/master/packages/x-data-grid/src/hooks/features/sorting/gridSortingUtils.ts


GridColDef でソート関係のもの::

  {
    sortable: boolean,        // sort の有効無効
    hideSortIcons: boolean,   

    // 独自の比較関数
    sortComparator: GridComparatorFn<V>,
    getSortComparator: (sortDirection: GridSortDirection) => GridComparatorFn<V>,
  }

デフォルトの挙動は GridColDef.type によって変わる。(ref. type)


type: "string", "singleSelect", "custom" の場合
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

gridStringOrNumberComparator(value1, value2)::

  export const gridStringOrNumberComparator: GridComparatorFn = (value1, value2) => {
    const nillResult = gridNillComparator(value1, value2);
    if (nillResult !== null) {
      return nillResult;
    }

    if (typeof value1 === 'string') {
      return collator.compare(value1!.toString(), value2!.toString());
    }
    return (value1 as any) - (value2 as any);
  };

- 両方nullなら引き分け(0)、片方nullならnullの方が小さい
- value1 が string型の場合、文字列比較
- それ以外、 ``(value1 as any) - (value2 as any)``::

    (数値型)   100 - 500               -> -400  // ソート可
    (boolean)  false - true            -> -1    // ソート可

    (配列) [100] - [500]               -> -400  // これに限ってはできるけど
           ["100,200"] - ["300,400"]   -> NaN   // 実質は配列はソート不可
           ["aaa"] - ["bbb"]           -> NaN

    (オブジェクト)
           {a: 100} - {a: 200}         -> NaN   // オブジェクトもソート不可

つまり、
string型, number型, boolean型の場合はこの関数でソートできるが、
それ以外(オブジェクト、配列、など)はソートできない。


type: "number", "boolean" の場合
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

gridNumberComparator(value1, value2)::

  export const gridNumberComparator: GridComparatorFn = (value1, value2) => {
    const nillResult = gridNillComparator(value1, value2);
    if (nillResult !== null) {
      return nillResult;
    }

    return Number(value1) - Number(value2);
  };

(注) Number関数ちょっとクセがあるので注意::

  Number(100)                      -> 100   // ソート可
  Number("100")                    -> 100   // ソート可

  Number([])        -> ("")        -> 0     // 配列は実質ソート不可
  Number([100])     -> ("100")     -> 100
  Number([100,200]) -> ("100,200") -> Nan



type: "date", "dateTime" の場合
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Date用のソート関数。



独自の sort 関数
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

sortComparator と getSortComparator の2種類の指定の仕方がある。


``sortComparator: GridComparatorFn<V>``

例::

  const nameSortComparator: GridComparatorFn = (v1, v2, param1, param2) => {
    return gridStringOrNumberComparator(
      v1.name, v2.name, param1, param2
    );
  }

  v1 < v2    : ret <  0
  v1 = v2    : ret == 0
  v1 > v2    : ret >  0


``getSortComparator: (sortDirection: GridSortDirection) => GridComparatorFn<V>``

通常は前述の sortComparator を使えばよい。

もし "ASC", "DESC" 両方とも null を後ろに持って行きたいなど、非対称なソートをしたい場合には、
getSortComparator を使う。

例::

    getSortComparator: (sortDirection) => {
      const modifier = sortDirection === 'desc' ? -1 : 1;
      return (value1, value2, cellParams1, cellParams2) => {
        if (value1 === null) {
          return 1;
        }
        if (value2 === null) {
          return -1;
        }
        return (
          modifier *
          gridStringOrNumberComparator(value1, value2, cellParams1, cellParams2)
        );
      };
    },


どちらが使われるかは、下記のようなコードで決まる。getSortComparator が優先。

gridSortingUtils.ts::

  if (column.getSortComparator) {
    comparator = column.getSortComparator(sortItem.sort);
  } else {
    comparator = isDesc(sortItem.sort)
      ? (...args) => -1 * column.sortComparator!(...args)
      : column.sortComparator!;
  }



フィルタ、Filter
-----------------------

参考

- `Data Grid - Filtering - MUI X <https://mui.com/x/react-data-grid/filtering/>`__
- https://github.com/mui/mui-x/tree/master/packages/x-data-grid/src/colDef の 〜Operators.ts


関連する GridColumnDef
^^^^^^^^^^^^^^^^^^^^^^^^

::

  {
    filterable: boolean,   // フィルタの有効無効
    filterOperators: GridFilterOperator<R, V, F>[]   // フィルタの設定
  }


デフォルトの動作。
^^^^^^^^^^^^^^^^^^^^^

type によって異なる。


type: "string"  (``getGridStringOperators``)

===============  =========
operator         入力欄
===============  =========
contains         単一入力
doesNotContain   単一入力
equals           単一入力
doesNotEqual     単一入力
startWith        単一入力
endWith          単一入力
isEmpty          なし
isNotEmpty       なし
isAnyOf          複数入力
===============  =========

type: "number" (``getGridNumericOperators``)

===============  ==========================
operator         入力欄
===============  ==========================
=                単一入力(上下ボタン付き)
!=               単一入力(上下ボタン付き)
>                単一入力(上下ボタン付き)
>=               単一入力(上下ボタン付き)
<                単一入力(上下ボタン付き)
<=               単一入力(上下ボタン付き)
isEmpty          なし
isNotEmpty       なし
isAnyOf          複数入力(上下ボタン付き)
===============  ==========================

type: "boolean" (``getGridBooleanOperators``)

===============  ==================
operator         入力欄
===============  ==================
is               any/true/false
===============  ==================


type: "date", "dateTime" (``getGridDateOperators``)

===============  ==================
operator         入力欄
===============  ==================
is               Date (DateTime)
not              Date (DateTime)
after            Date (DateTime)
onOrAfter        Date (DateTime)
before           Date (DateTime)
onOrBefore       Date (DateTime)
isEmpty          なし
isNotEmpty       なし
===============  ==================

type: "singleSelect" (``getGridSingleSelectOperators``)

===============  =========
operator         入力欄
===============  =========
is               単一選択
not              単一選択
isAnyOf          複数選択
===============  =========


フィルタを独自実装するには
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

全部を独自実装するのは大変そう。特に入力欄。
既存のフィルタをうまく使うことを考える。

カラムの値をstring型に直し、string用のフィルタを使う::

  TODO

一部のオペレータを無効にする::

  const filterOperators = getGridNumericOperators().filter(
    (operator) => operator.value === '>' || operator.value === '<',
  );




完全に自前で実装する場合::

  const operator: GridFilterOperator<any, number> = {
    label: 'From',     // フィルタオペレータの表示名
    value: 'from',     // フィルタの識別子

    // フィルタの判定関数(を返す関数)
    getApplyFilterFn: (filterItem, column) => {
      if (!filterItem.field || !filterItem.value || !filterItem.operator) {
        return null;
      }

      return (value, row, column, apiRef) => {
        return Number(value) >= Number(filterItem.value);
      };
    },

    requiresFilterValue: false,               // isEmpty など値入力欄不要の場合は false
    InputComponent: RatingInputValue,         // フィルタの値入力欄のReactコンポーネント
    InputComponentProps: { type: 'number' },  // ↑に渡るProps ？
  };


  getApplyFilterFn の引数の filterItem は下記の形
  {
    field,     // どのフィールド(カラム)に対し
    operator,  // operator の名前 (GridFilterOperator.valueで指定したもの)
    value,     // ユーザーがフィルタとして入れた値。検索文字列や閾値
  }


行の定義
================

行の定義というか、表示させたいデータ。

::

  const rows: GridRowsProp = [
    { id: 1, col1: 'Hello', col2: 'World' },
    { id: 2, col1: 'DataGridPro', col2: 'is Awesome' },
    { id: 3, col1: 'MUI', col2: 'is Amazing' },
  ];


各行はユニークなIDを持たないといけない。

- ``id`` フィールド
- getRawId prop で、フィールドからユニーク値を取り出す関数を指定::

    <DataGrid getRowId={(row) => row.internalId} />;

