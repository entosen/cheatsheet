


参考

- `Springの@Autowiredの方式 #Java - Qiita <https://qiita.com/bluespoon/items/6060389eab983c2e045e>`__


@Autowiredとは
==========================

SpringのDIコンテナから、インスタンスを注入するための指定のこと。
まずDIコンテナとSpringフレームワークの仕組みを知る必要がある。



- @Component
- @Controller
- @Service
- @Repository
- @RestController
- @ControllAdvice
- ManagedBean
- @Named


注入する方法

::

  種類
  コンストラクタインジェクション   コンストラクタの前で指定        省略可能
  セッターインジェクション         セッターメソッドの前で指定      
  フィールドインジェクション       変数の前で指定                  非推奨とされている


コンストラクタ インジェクション::

  public class MemoController {
      //この方法のみ、finalと指定している。
      private final MemoService memoService;

      @Autowired  // 省略可能
      public MemoController(MemoService memoService){
          this.memoService = memoService;
      }
  }

セッター インジェクション::

  public class MemoController {
    private MemoService memoService;

    @Autowired
    public setMemoService(MemoService memoService){
        this.memoService = memoService;
    }
  }

フィールド インジェクション::

  public class MemoController {
      @Autowired
      private MemoService memoService;
  }




@Configuration, @Bean
==========================

@Beanと書いたメソッドでインスタンス化されたクラスがシングルトンクラスとしてDIコンテナに登録される。任意のクラスで@Autowiredで注入してアクセスできる。

::

  TODO


TODO
==================

@Qualifier

