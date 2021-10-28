###################################
context.Context
###################################

Goルーチンに親子関係はない (c.f. プロセスのforkは親子関係がある)。
親がキャンセルされた(タイムアウトとか、コネクションが閉じられたとか)場合、
子孫のgoルーチンも止めたい。そういう場合の仕組み。

Contextは木構造を作る。

Contextの役割

- 処理の締め切りを伝達
- キャンセル信号の伝播
- リクエストスコープ値の伝達


Context自体の操作::

    type Context interface {
        // Done は、自分もしくは先祖のContextがキャンセルされたかどうかが分かるチャネルを返す。
        // こいつが close されていたらキャンセルされたってこと。
        Done() <-chan struct{}

        // Err は、Done() のチャネルがcloseされた後に呼ぶと、理由を示すerrorを返す。
        // キャンセルされていない場合は、nil を返す。
        Err() error

        // Deadline はタイムアウトが設定されていればその時刻を返す
        Deadline() (deadline time.Time, ok bool)

        // Value は、keyに紐付いた保管値を返す。なければ nil 。
        Value(key interface{}) interface{}
    }

Err()が返すerrorには2種類ある::

    var Canceled = errors.New("context canceled")   // キャンセルされた
    var DeadlineExceeded error = deadlineExceededError{}  // タイムアウトした




Contextの生成::

    // ルートノードとなるContextを返す。
    // キャンセルなし、タイムアウトなし、保管値なし。
    ctx := context.Background()

    // 実質 Background() と同じ。
    // 開発中で、どのContextを渡せばよいかまだ明確でない場合や、まだ利用できない場合など、
    // それでも nilは渡してほしくないから TODOで空のcontextを作ろうね。
    ctx := context.TODO()

    // コピーして保管値をセットした子Contextを返す。
    // ここに入れるのはリクエストスコープのデータの受け渡しだけで使用すること。
    // 単なる関数のオプショナルデータを渡す場所ではない。
    ctx := context.WithValue(ctx, key, val)

    // 親となるContextを渡すと、子のContextとキャンセル用の関数を作ってくれる。
    // 第２返り値のcancelFuncで返された子のContextをcancelできる。
    newCtx, cancelFunc := WithCancel(ctx)

    // タイムアウト時間も指定
    duration := time.Second * 10
    newCtx, cancelFunc := WithTimeout(ctx, duration)

    // deadline時刻も指定
    deadline := time.Now().Add(time.Second * 10)
    newCtx, cancelFunc := WithDeadline(ctx, deadline)


Done()の使い方::

    // (例) DoSomethingの結果を出力用のチャネルに書く
    func Stream(ctx context.Context, out chan<- Value) error {
        for {
            v, err := DoSomething(ctx)
            if err != nil {
                return err
            }

            select {
            case <-ctx.Done(): // 先に ctx がキャンセルされたら、こっち
                return ctx.Err()
            case out <- v:     // チャネルへの書き込みが先にできた場合、こっち

                               //  default がないので、どちらかが成立するまでブロック
            }
        }
    }



Contextへの保管値のセット/取り出しは、key,value 共に ``interface{}`` で扱いにくいので、
下記のように型限定の口を作って上げるのが定石。

さらに、循環参照を避けるために、Context Value のセット/取り出しと、
それを使う処理(例えば、http.Handler型)はパッケージ分けるのが定石。
Context のセット/取り出しは、Hadnler以外の処理からも使いたくなることが多いので、
その場合の循環参照を避けるため。

::

    // Context の WithValue の key は衝突しないように、
    // パッケージに非公開の型として作っておく。
    // (型が違えばどんな値だったとしても衝突しない)
    type key int            // キーを決める
    const userKey key = 0

    type User struct {...}   // 値の型

    // NewContext は、値をセットした子Contextを生成し返す
    func NewContext(ctx context.Context, u *User) context.Context {
        return context.WithValue(ctx, userKey, u)
    }
    
    // FromContext は、Contextから保管値を取り出す
    func FromContext(ctx context.Context) (*User, bool) {
        u, ok := ctx.Value(userKey).(*User)
        return u, ok
    }


キャンセル系の WithCancel(), WithTimeout(), WithDeadline() で生成した ctx は、
cancelFunc を呼ばないと、静的解析で怒られるらしい。

なので、こういう感じにやっておく。::

    ctxWithTimeout10, cancelFunc := context.WithTimeout(ctx, time.Second*10)
    defer cancelFunc()
    go someChildProcess(ctxWithTimeout10, "with timeout")





http.Request における Context
======================================


基本操作::

    // r の持つ Context を返す
    ctx := r.Context()

    // rをコピーして指定のContextをセットした新しい Request を返す
    rNew := r.WithContext(ctx)

例::

    // Auth 認可ミドルウェア。
    // 認証した結果のUserIDをContextに追加して、後段(next)のハンドラを呼ぶ
    func Auth(next http.HandlerFunc) http.HandlerFunc {
        return func(w http.ResponseWriter, r *http.Request) {
            authKey := r.Header.Get("Authorization")
            u, err := user.Authorize(authKey)
            if err != nil {
                w.WriteHeader(http.StatusUnauthorized)
                fmt.Fprint(w, "UnAuthorized")
                return
            }

            ctx := r.Context()
            ctx = user.ContextWithUser(ctx, u)
            next.ServeHTTP(w, r.WithContext(ctx))
        }
    }

