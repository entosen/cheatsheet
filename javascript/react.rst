

JSX記法中のコメント
=========================

::

    <div>
        {/* 1行コメント */}
        Hello world!
        {
            // 1行コメント。 `//` を使うときは `}` の前に改行が必要
        }

        {/* 複数行の
        コメントは
        こんな感じ */}

        {
            // もしくは
            // こんな感じで
            // 複数行
        }
    </div>


タグの前後の空白は除かれるから、
隙間を空けたいときは、こう::

    {''}


JSX記法のreturn
=========================

複数行になるときは丸括弧::

    return (
        <div>
            hogehoge
        </div>
    )


return値は単一のタグでないといけない。

複数のタグを返したいときは、下記のようにする

React.Fragmentで囲む::

    return (
        <React.Fragment>
            <div>foo</div>
            <div>bar</div>
        </React.Fragment>
    )



``<> 〜 </>`` で囲む::

    return (
        <>
            <div>foo</div>
            <div>bar</div>
        </>
    );
