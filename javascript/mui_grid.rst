===================================
MUI Grid
===================================

CheatSheet
=====================

MUI Grid v1::

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

MUI Grid v2 (sizeの単一指定)::

    // import Grid2 from '@mui/material/Grid2';
    // import { Grid2 } from '@mui/material';
    import Grid from '@mui/material/Grid2';
    import { Grid2 as Grid } from '@mui/material';

    <Grid container spacing={2}>
      <Grid size={8}>
        <Item>size=8</Item>
      </Grid>
      <Grid size={4}>
        <Item>size=4</Item>
      </Grid>
      <Grid size={4}>
        <Item>size=4</Item>
      </Grid>
      <Grid size={8}>
        <Item>size=8</Item>
      </Grid>
    </Grid>

MUI Grid v2 (sizeのオブジェクト指定=レスポンシブ)::

    <Grid container spacing={2}>
      <Grid size={{ xs: 6, md: 8 }}>
        <Item>xs=6 md=8</Item>
      </Grid>
      <Grid size={{ xs: 6, md: 4 }}>
        <Item>xs=6 md=4</Item>
      </Grid>
      <Grid size={{ xs: 6, md: 4 }}>
        <Item>xs=6 md=4</Item>
      </Grid>
      <Grid size={{ xs: 6, md: 8 }}>
        <Item>xs=6 md=8</Item>
      </Grid>
    </Grid>

MUI Grid v1  と v2 の違い。

- v2 では Grid タグは暗黙的に常に item なので、item prop は付けなくてもよい。
- v1 では、xs, sm, ... が個別prop、v2では size prop でオブジェクト型
- v2 では、Grid container の直接の子の Grid container には、columns と spacing は引き継がれる。
  ref. `Nested grid <https://mui.com/material-ui/react-grid2/#nested-grid>`__




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
- `React Grid component (version 2) - Material UI <https://mui.com/material-ui/react-grid2/>`__
- `Grid API - Material UI <https://mui.com/material-ui/api/grid/>`__
- `Grid2 API - Material UI <https://mui.com/material-ui/api/grid-2/>`__
- `日本語対応！CSS Flexboxのチートシートを作ったので配布します | Webクリエイターボックス <https://www.webcreatorbox.com/tech/css-flexbox-cheat-sheet>`__


概要
==============

MUI Grid は、CSS Flexible Box に相当。(名前に反し、CSS Grid ではない)。

MUI Grid は、幅を 12 として扱う。 (変えることも可能。TODO)

children (item) をひとつひとつ左から横方向に配置していって、
入り切らなくなったら折り返す。


下記2つがある

- Grid Container
- Grid Item

Grid Item であり、かつ、Grid Container というノードも作れる。(入れ子を持つということ) ::

    {/* MUI Grid v1 */}
    <Grid item xs={2} container>

Grid v2 では、Gridタグは(特に指定しなくても)常にitem。
さらに、かつContainerにしたい場合には ``container`` prop を付ける。




ただし、container かつ item で、spacing と幅指定(xs,smなど) を両方持つとおかしな挙動になるらしい。

ref. https://mui.com/material-ui/react-grid/#nested-grid





幅の決め方
-------------------

以下、多分に推測含む。

1. spacing の指定によって隙間(いわゆるガター)の幅を決める
2. 全幅を、11本の隙間と12マスのitem領域になるように item 1マス分の幅を決める
3. item の xs などの指定で、item幅を決定する
4. どのitemのところで折り返すかを決定する
5. 幅が12に満たない行については、justifyContent によって配置を決める

なので、xs={3} (v2の場合は size={3}) と指定した場合は、(item 3個分＋隙間2本分)の幅になる。


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

- size (v2のみ)
- columns 。 だたし、これをそれぞれ指定した場合は、Grid item の幅指定が指定したBreakPoint分必須になる。
- columnSpacing
- derection
- rowSpacing
- spacing
- offset (v2のみ)


Grid item のプロパティ
===========================

幅指定
----------------

そのコンポが何カラム分を占有するか。

デフォルトでは幅全体を12分割した単位で指定する。小数でもいけるっぽい。

breakpoint の一部しか指定されていない場合、
指定がない箇所は、それよりも狭いときの指定を引き継ぐ。

``size={xs: 6, lg: 4}`` なら ``xs:6, sm:6, md:6, lg:4, xl:4`` と同様の意味。


Auto-layout。
^^^^^^^^^^^^^^^^^

明示的に指定されたitemの残りの領域を均等割りする。


MUI Grid v1。 下記の様に数値を指定しない場合 (trueを指定していることになる)::

    <Grid container spacing={3}>
      <Grid item xs>     <Item>xs</Item> </Grid>     // 幅3
      <Grid item xs={6}> <Item>xs=6</Item> </Grid>   // 幅6
      <Grid item xs>     <Item>xs</Item> </Grid>     // 幅3
    </Grid>

    (2) が幅6を占有し、残りの幅6を(1)(3)で均等割り。

MUI Grid v2 ("grow" を指定する)::

    <Grid container spacing={3}>
      <Grid size="grow"> <Item>size=grow</Item> </Grid>  // 幅3
      <Grid size={6}>    <Item>size=6</Item>    </Grid>  // 幅6
      <Grid size="grow"> <Item>size=grow</Item> </Grid>  // 幅3
    </Grid>

    (2) が幅6を占有し、残りの幅6を(1)(3)で均等割り。

"auto" 指定
^^^^^^^^^^^^^^^^^

"auto" を指定した場合、そのitemの幅はコンテンツぴったりの幅になる。

v1::

    <Grid container spacing={3}>
      <Grid item xs="auto"> <Item>variable width content</Item> </Grid>  // コンテンツに応じた幅
      <Grid item xs={6}>    <Item>xs=6</Item> </Grid>                    // 幅6
      <Grid item xs>        <Item>xs</Item> </Grid>                      // 残り
    </Grid>

v2::

    <Grid container spacing={3}>
      <Grid size="auto"> <Item>size=auto ooooooooooooooo</Item> </Grid>  // コンテンツに応じた幅
      <Grid size={6}>    <Item>size=6</Item>    </Grid>                  // 幅6
      <Grid size="grow"> <Item>size=grow</Item> </Grid>                  // 残り
    </Grid>


その他
^^^^^^^^^^^^

- false は指定なし扱い。(より狭いときの指定を引き継ぐ)
- どの breakpoint にも指定がない場合は、"auto" 相当の挙動になるっぽい。
  実際にどういう幅になるかは中身による。


Offset (v2のみ)
----------------

::

    <Grid size={2} offset={3}>
    // 左に幅3の隙間が空き、実質幅5のitemとみなされる

    <Grid size={2} offset={"auto"}>
    // 一旦offset=0で折り返し位置を決定し、その後、その行の中で目一杯の隙間を入れる




Grid container のプロパティ
============================

空白 Spacing
------------------

item間(column間、row間)につく空白。

::

    <Grid container spacing={2}>
    <Grid container rowSpacing={1}, columnSpacing={2}>

rowSpacing はrow間、columnSpacing はcolumn間 の空白。spacing はその両方に効く。

spacing指定の1単位が実際にはどれぐらいの長さになるかは、theme.spacing() で決まる(デフォルト 8px)。
container での指定は、その単位何個分かを指定する(0〜正のnumber)。

spaceの指定はitemとitemの間にだけ効いて、外枠部分には効かない。外枠は常に0。

MUI Grid v1 だと、spacing はHTML上は、左と上のpaddingとして効いているっぽい。
ただし、外枠部分はpaddingが外側にはみ出すようになっているので、実質外枠は0になる。

MUI Grid v2 だと、spacing は gap CSS property を使って実現しているっぽい。


向き、配置
---------------------------

Grid container の中の Grid item(s) の配置。

v1::

    <Grid
      container
      direction="row"
      wrap="wrap"
      sx={{
        justifyContent: "flex-start",
        alignItems: "flex-start",
      }}
    >

v2::

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

column, column-reverse にした場合、幅指定(xs, sm, md, lg, xl)およびoffset指定はできない。無視される。



wrap: 折り返したときに行が流れる向き。 CSS Flexbox の flex-wrap に相当

::

    nowrap
    wrap
    wrap-reverse


justifyContent: CSS Flexbox の justify-content に相当

その行のitem幅の合計が12に満たなかった場合にどうするかの指定。

- flex-start: 左寄せ。item間の隙間はspacing指定。(右に満たなかった分の隙間が空く) (デフォルト)
- center: 中央寄せ。item間の隙間はspacing指定。(左右に満たなかった分の隙間が空く)
- flex-end: 右寄せ。item間の隙間はspacing指定。(左に満たなかった分の隙間が空く)
- space-between: 均等割り。満たなかった分の隙間は item間に均等に充填
- space-around: 均等割り。満たなかった分の隙間は item間(1):左外(0.5):右外(0.5) の割合で均等に充填
- space-evenly: 均等割り。満たなかった分の隙間は、item間(1):左外(1):右外(1) の割合で均等に充填

justifyContentによる配置は、幅12に対してitem幅やgap幅、折り返し位置が決定した後で行われる。



alignItems: CSS Flexbox の align-items に相当

各行のitemを垂直方向(cross axis)のどこに揃えるか。(各itemの高さが異なる場合)

- stretch (規定値)
- flex-start
- flex-end
- center
- baseline

alignContent: CSS Flexbox のalign-contentに相当

(複数行の)itemの塊を、containerの領域の中で垂直方向(cross axis)のどこに揃えるか。
(containerの領域の高さが、複数行のitemの塊よりも高い場合)

- stretch (規定値)
- flex-start
- flex-end
- center
- space-between
- space-around
- space-evenly




c.f. Grid item の中の要素の配置を制御したい場合
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

item自体の配置ではなく、itemの中身の要素を制御したいとき。

Grid item タグに、display="flex" を付けて、justifyContent や alignItems を指定する。

v2::

    <Grid container spacing={2} minHeight={160}>
      <Grid display="flex" justifyContent="center" alignItems="center" size="grow">
        <Avatar src="/static/images/avatar/1.jpg" />
      </Grid>
      <Grid display="flex" justifyContent="center" alignItems="center">
        <Avatar src="/static/images/avatar/2.jpg" />
      </Grid>
      <Grid display="flex" justifyContent="center" alignItems="center" size="grow">
        <Avatar src="/static/images/avatar/3.jpg" />
      </Grid>
    </Grid>



columns
-----------------

デフォルトでは幅を12等分した単位で扱う。それの変更。

全体を16分割とか、24分割とかできる。


Nested grid は一部のpropを引き継ぐ(v2のみ)
---------------------------------------------------

v2 では、Grid container の **直接** の子の Grid container には、columns と spacing は引き継がれる。
ref. `Nested grid <https://mui.com/material-ui/react-grid2/#nested-grid>`__


