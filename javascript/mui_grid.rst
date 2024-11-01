===================================
MUI Grid
===================================


CheatSheet
=====================

::

    import Grid from '@mui/material/Grid';
    // import { Grid } from '@mui/material';  // これでも可

    <Grid container spacing={2}>
      <Grid item xs={6} md={8}>
        <Item>xs=6 md=8</Item>
      </Grid>
      <Grid item xs={6} md={4}>
        <Item>xs=6 md=4</Item>
      </Grid>
      <Grid item xs={6} md={4}>
        <Item>xs=6 md=4</Item>
      </Grid>
      <Grid item xs={6} md={8}>
        <Item>xs=6 md=8</Item>
      </Grid>
    </Grid>

デフォルトでは、幅全体を 12 として扱う。

BreakPoints::

    xs (extra-small) :    0px〜
    sm (small      ) :  600px〜
    md (medium     ) :  900px〜
    lg (large      ) : 1200px〜
    xl (extra-large) : 1536px〜


参照
==============

- `React Grid component - Material UI <https://mui.com/material-ui/react-grid/>`__
- `Grid API - Material UI <https://mui.com/material-ui/api/grid/>`__
- `日本語対応！CSS Flexboxのチートシートを作ったので配布します | Webクリエイターボックス <https://www.webcreatorbox.com/tech/css-flexbox-cheat-sheet>`__

概要
==============

MUI Grid は、CSS Flexible Box に相当。(名前に反し、CSS Grid ではない)。

MUI Grid は、幅を 12 として扱う。 (変えることも可能。TODO)

下記2つがある

- Grid Container
- Grid Item

Grid Item であり、かつ、Grid Container というノードも作れる。(入れ子を持つということ) ::

    <Grid item xs={2} container>

ただし、container かつ item で、spacing と幅指定(xs,smなど) を両方持つとおかしな挙動になるらしい。

ref. https://mui.com/material-ui/react-grid/#nested-grid


Breakpoints
===================

参照

- `Breakpoints - Material UI <https://mui.com/material-ui/customization/breakpoints/>`__


::

    xs (extra-small) :    0px〜
    sm (small      ) :  600px〜
    md (medium     ) :  900px〜
    lg (large      ) : 1200px〜
    xl (extra-large) : 1536px〜

小さい breakpoint で指定した設定は、別途指定がなければ「それ以上」の範囲にも効く。

TODO これは何の幅を元に決定される？ 親要素の幅？ ページの幅？

Gridに指定するいくつかのプロパティは、単一の値だけでなく、Breakpoint それぞれの値を指定できる::

    <Grid container spacing={{ xs: 2, md: 3 }} columns={{ xs: 4, sm: 8, md: 12 }}>

それぞれ指定が可能なもの

- columns 。 だたし、これをそれぞれ指定した場合は、Grid item の幅指定が指定したBreakPoint分必須になる。
- columnSpacing
- derection
- rowSpacing
- spacing
- all the other props of MUI Sytem


Grid item のプロパティ
===========================

幅指定
----------------

そのコンポが何カラム分を占有するか。

デフォルトでは幅全体を12分割した単位で指定する。小数でもいけるっぽい。


Auto-layout。

下記の様に数値を指定しない場合 (trueを指定していることになる)、
利用可能な領域の均等割りになる。

::

    <Grid container spacing={3}>
      <Grid item xs>     <Item>xs</Item> </Grid>     // 幅3
      <Grid item xs={6}> <Item>xs=6</Item> </Grid>   // 幅6
      <Grid item xs>     <Item>xs</Item> </Grid>     // 幅3
    </Grid>

    (2) が幅6を占有し、残りの幅6を(1)(3)で均等割り。

"auto" 指定

"auto" を指定した場合、そのitemの幅はコンテンツぴったりの幅になる。

::

    <Grid container spacing={3}>
      <Grid item xs="auto"> <Item>variable width content</Item> </Grid>  // コンテンツに応じた幅
      <Grid item xs={6}>    <Item>xs=6</Item> </Grid>                    // 幅6
      <Grid item xs>        <Item>xs</Item> </Grid>                      // 残り
    </Grid>


Grid container のプロパティ
============================

空白 Spacing
------------------

子item間および外周につく空白。

::

    <Grid container spacing={2}>
    <Grid container rowSpacing={1}, columnSpacing={2}>

rowSpacing はrow間、columnSpacing はcolumn間 の空白。spacing はその両方に効く。

spacing指定の1単位が実際にはどれぐらいの長さになるかは、theme.spaceing() で決まる。(デフォルト 8px)

container での指定は、その単位何個分かを指定する。(0〜正のnumber)



向き、配置
---------------------------

::

    <Grid
      container
      direction="row"
      wrap="wrap"
      sx={{
        justifyContent: "flex-start",
        alignItems: "flex-start",
      }}
    >

direction: item の流れる向き。CSS Flexbox の flex-direction に相当。

::

    row
    row-reverse
    column
    column-reverse

column, column-reverse にした場合、幅指定(xs, sm, md, lg, xl)はできない。無視される。



wrap: 折り返したときに行が流れる向き。 CSS Flexbox の flex-wrap に相当

::

    nowrap
    wrap
    wrap-reverse


justifyContent: CSS Flexbox の justify-content に相当

alignItems: CSS Flexbox の align-items に相当

alignContent: これも使えるのか？ CSS Flexbox のalign-contentに相当？


columns
-----------------

デフォルトでは幅を12等分した単位で扱う。それの変更。

全体を16分割とか、24分割とかできる。


