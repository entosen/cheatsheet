*******************************
Logging, ロギング
*******************************

goのログイングには標準搭載の log と、logrus がある


========
log
========

https://pkg.go.dev/log

特徴

- fmt.Printf に 時刻の表示がついたぐらい。
- いわゆるログレベルの概念はない。

サンプル::

    import "log"
    log.Println("Hello, World")

出力関数
----------

レベル的なものは下記。

::

    Print / Printf / Println
    Fatal / Fatalf / Fatalln
        → 表示したあと os.Exit(1) → defer された処理も動かない
    Panic / Panicf / Panicln
        → 表示したあと panic() を呼ぶ → deferされた処理は動く

    func Output(calldepth int, s string) error
        → 


出力形式、出力先
-----------------

出力形式の制御は SetFlag() で。

::

    SetFlags(Ldate | Ltime)   // セット
    Flags()                   // 確認

    const (
        Ldate         = 1 << iota     // the date in the local time zone: 2009/01/23
        Ltime                         // the time in the local time zone: 01:23:23
        Lmicroseconds                 // microsecond resolution: 01:23:23.123123.  assumes Ltime.
        Llongfile                     // full file name and line number: /a/b/c/d.go:23
        Lshortfile                    // final file name element and line number: d.go:23. overrides Llongfile
        LUTC                          // if Ldate or Ltime is set, use UTC rather than the local time zone
        Lmsgprefix                    // move the "prefix" from the beginning of the line to before the message
        LstdFlags     = Ldate | Ltime // initial values for the standard logger
    )

    例
        デフォルト (Ldate | Ltime)
        2009/01/23 01:23:23 message

        (Ldate | Ltime | Lmicroseconds | Llongfile)
        2009/01/23 01:23:23.123123 /a/b/c/d.go:23: message


    func SetPrefix(prefix string)  / Prefix()


出力先の指定は SetOutput() で。 デフォルトは Stderr ::

    log.SetOutput(os.Stdout)   // 引数は io.Writer
    Writer()                   // 確認


インスタンス
----------------

- ただの関数を呼ぶ(グローバル的に定義された、デフォルトの Logger インスタンスが使われる)
- 自前で Logger を生成して呼ぶことも可能(設定をいろいろ分けたいときなど)::

      func New(out io.Writer, prefix string, flag int) *Logger


=======================
logrus
=======================

- https://github.com/sirupsen/logrus
- https://pkg.go.dev/github.com/sirupsen/logrus

インストール::

    go get github.com/sirupsen/logrus

サンプル。下記のように Logrus を ``log`` としてimportすることが一般的。

::

    package main

    import (
      log "github.com/sirupsen/logrus"
    )

    func main() {
      log.SetLogLevel(log.InfoLevel)
      log.Info("Hello, Logrus")
    }


標準の log パッケージと完全に互換性があるらしいので、
log パッケージの関数も呼べる。


出力関数
--------------

::

    Panic(args...) / Panicln(args...) / Panicf(format, args...)
        → Panic() を呼び出す。 defer された処理は動く
    Fatal(args...) / Fatalln(args...) / Fatalf(format, args...)
        → os.Exit(1) を呼び出す。 defer された処理も動かない
    Error(args...) / Errorln(args...) / Errorf(format, args...)
    Warn(args...)  / Warnln(args...)  / Warnf(format, args...)
    Info(args...)  / Infoln(args...)  / Infof(format, args...)
    Debug(args...) / Debugln(args...) / Debugf(format, args...)
    Trace(args...) / Traceln(args...) / Tracef(format, args...)


    ログレベルのデフォルトは Info 。
    log.SetLevel(log.InfoLevel) 


    // こんな風に Fields を足すこともできる。
    log.WithFields(log.Fields{"animal": "walrus",})
      .Info("A walrus appears")


WarnFn みたいなのもある。

関数名の Warn/Warnln/Wranf は、下記のように違いがある。
また、logrus の関数は、エントリーごとなので、どの関数を使っても改行する。

- Warn 系は fmt.Print() と同じような動作

  - 各引数を文字列に直して、空白なしで連結して、最後改行。
  - (cf. fmt.Print() は、改行しないが、logrus はする。)

- Warnln系は fmt.Println() と同じような動作

  - 下記引数を文字列に直して、空白ありで連結して、最後改行。

- Warnf系は fmt.Printf() と同じような動作

  - 第1引数のフォーマット指定に従って出力する。最後改行。
  - (cf. fmt.Printf() は、改行しないが、logrus はする。)




出力形式, 出力先
-------------------------

logrus では Fields という考え方で、テキストではなく構造化されたロギングという考え方。

- 各コードでロギングする際には、できるだけFields に構造化した状態で呼ぶ。
- 実際の出力時に、Formatterによって整形されて出力される。

::

    log.Fatalf("Failed to send event %s to topic %s with key %d", ...)

    よりも

    log.WithFields(log.Fields{
      "event": event,
      "topic": topic,
      "key": key,
    }).Fatal("Failed to send event")

    の方が好ましい

Formatter::

    type Formatter interface {
        Format(*Entry) ([]byte, error)
    }


    log.SetFormatter(

Entry, Fields::

    type Entry struct {
        Time time.Time
        Level Level
        Caller *runtime.Frame   // log.SetReportCaller(true) をやっておく必要がある？

        Data Fields      // ユーザーが WithFields などで指定した Fields
        Message string   // Error,Warn,Infoメソッドなどで渡したメッセージ

        Logger *Logger
        Buffer *bytes.Buffer
        Context context.Context
    }

    type Fields map[string]interface{}


標準では下記のFormatterが用意されている

- JSONFormatter::

      log.SetFormatter(&log.JSONFormatter{})

      {"animal":"walrus","level":"info","msg":"A group of walrus emerges from the ocean","size":10,"time":"2014-03-10 19:57:38.562264131 -0400 EDT"}

- TxtFormatter::

      log.SetFormatter(&log.TextFormatter{})

      time="2015-03-26T01:27:38-04:00" level=debug msg="Started observing beach" animal=walrus number=8


独自Formatter::

    type MyFormatter struct {
    }

    // 人が読みやすい、一般的な形式のログ
    func (f *MyFormatter) Format(entry *logrus.Entry) ([]byte, error) {
        var b *bytes.Buffer

        if entry.Buffer != nil {
            b = entry.Buffer
        } else {
            b = &bytes.Buffer{}
        }

        b.WriteString(entry.Time.Format("Mon Jan 2 15:04:05 2006 "))
        b.WriteString(fmt.Sprint("[", strings.ToUpper(entry.Level.String()), "] "))
        b.WriteString(fmt.Sprintf("%s:%d::%s() ", path.Base(entry.Caller.File), entry.Caller.Line, entry.Caller.Function))
        b.WriteString(entry.Message)

        if len(entry.Data) > 0 {
            keys := make([]string, 0, len(entry.Data))
            for k := range entry.Data {
                keys = append(keys, k)
            }
            sort.Strings(keys)

            for _, k := range keys {
                b.WriteString(fmt.Sprint(" ", k, "=", entry.Data[k]))
            }

        }

        b.WriteString("\n")

        return b.Bytes(), nil
    }


出力先::

    log.SetOutput(os.Stdout)   // 引数は io.Writer


インスタンス
----------------

- ただの関数を呼ぶ(グローバル的に定義された、デフォルトの Logger インスタンスが使われる)
- 自前で Logger を生成して呼ぶことも可能(設定をいろいろ分けたいときなど)::

      MyLogger := log.New()

      MyLogger :=  &logrus.Logger{
          Out: os.Stderr,
          Formatter: new(logrus.TextFormatter),
          Hooks: make(logrus.LevelHooks),
          Level: logrus.DebugLevel,
      }

      ↑では MyLogger と書いたけど、 log という名前で扱うのが推奨らしい。


Hook, フック
---------------------

ロギングの際に、追加の処理を行わせたい場合、Hookを追加することで可能。

- https://github.com/sirupsen/logrus#hooks
- https://github.com/sirupsen/logrus/blob/master/hooks.go

::

    type Hook interface {
        Levels() []Level     // 自分のFireを読んで欲しいログレベルを指定する
        Fire(*Entry) error   // このFireが呼ばれるので、実際の処理を実装する
    }


例) WarnとError以上のログを出力した回数をカウントアップするフック::

    type countUpHook struct{}

    func (hook countUpHook) Fire(e *logrus.Entry) error {
        if e.Level == logrus.WarnLevel {
            metrics.WarnLogCounter.Inc()
        } else {
            metrics.ErrorLogCounter.Inc()
        }
        return nil
    }

    func (hook countUpHook) Levels() []logrus.Level {
        return []logrus.Level{
            logrus.WarnLevel,
            logrus.ErrorLevel,
            logrus.FatalLevel,
            logrus.PanicLevel,
        }
    }

    // --- 登録
    func init() {
      hook := countUpHook{}
      logrus.AddHook(hook)
    }


