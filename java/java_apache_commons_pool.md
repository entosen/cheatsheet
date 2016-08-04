
# 参考ドキュメント

- https://commons.apache.org/proper/commons-pool/
- https://commons.apache.org/proper/commons-pool/api-2.4.2/index.html


# sbt

```
libraryDependencies += "org.apache.commons" % "commons-pool2" % "2.4.2"
```

# 重要なインターフェースと役割

- PooledObjectFactoryインターフェース
  - ObjectPool の裏にいて、目的のオブジェクトの生成や解放を担う。
  - 目的のオブジェクトをそのまま返すのではなく、PooledObjectにくるんで返す
- PooledObjectインターフェース
  - 管理のために目的のオブジェクトをくるむ。
  - borrowされた回数や時間などの記憶に使っているようだ
- ObjectPoolインターフェース
  - 内部にオブジェクトをプールしておいて、外からの borrow,return に対応する。
  - 必要に応じて、Factoryを用いて、オブジェクトの生成、解放を行う



基本的には PooledObjectFactoryインターフェース を
扱いたいオブジェクトに合わせて実装しなければならない。
通常は BasePooledObjectFactory抽象クラスをベースに作る。


## PooledObjectFactory

ObjectPool の裏側にいて、主に目的のオブジェクトの生成、解放を担う。

https://commons.apache.org/proper/commons-pool/api-2.4.2/org/apache/commons/pool2/PooledObjectFactory.html

```java
public interface PooledObjectFactory<T> {
    PooledObject<T> makeObject(); 
      // オブジェクトを生成する
      // Poolが新しいインスタンスが必要だとなったときに呼ばれる
      // インスタンスを PooledObjectFactory にくるんで返す必要がある。

    void activateObject(PooledObject<T> obj);
      // 過去にpassivateされたインスタンスが、再度borrowObjectで貸し出されるときに呼ばれる

    void passivateObject(PooledObject<T> obj);
      // インスタンスが returnObject でプールに戻されるときに呼ばれる

    boolean validateObject(PooledObject<T> obj); 
      // オブジェクトがきちんと動作する状態かを判定する
      // インスタンスが貸し出される際(activate後)や、
      // インスタンスが戻された際(passivate前)に呼ばれる可能性がある。
      // この関数に渡される際の obj は active な状態でのみ呼ばれる。

    void destroyObject(PooledObject<T> obj); 
      // オブジェクトを解放する
      // プールが、このObjectはもう不要と判断したときに呼ばれる
      // (validateObjectの判定結果がどうか、もしくはプール側での実装によって)
      // これが呼ばれるときのObjectは、activeかpassiveか、そもそも一貫性のある状態かは保証されない
}
```

目的のオブジェクトの生成・解放をするために、
PooledObjectFactoryインターフェースを実装したクラスを用意する必要がある。
通常は BasePooledObjectFactoryクラスから作る。

factoryはスレッドセーフにする必要がある。
immutableに作れば、スレッドセーフといえる。
中に状態を持つ場合は、synchronized などの排他処理が必要。

https://commons.apache.org/proper/commons-pool/api-2.4.2/org/apache/commons/pool2/BasePooledObjectFactory.html

```java
import org.apache.commons.pool2.BasePooledObjectFactory

public class MyPooledObjectFactory extends BasePooledObjectFactory<T> {

  PooledObject<T> makeObject() {
    // ベースで、以下のように create と wrap に連鎖するようになっているので、
    // 通常は override しなくてよい。
    wrap(create())
  }

  abstract T create() {
    // オブジェクトTの新規作成処理を記述する。
    ...
  }

  PooledObject<T> wrap(T pooledObject) {
    // オブジェクトT を PooledObject に包んで返す。
    // 通常は以下のようにDefaultPooledObjectをnewするだけでよい。
    return new DefaultPooledObject<T>(pooledObject);
  }

  void activateObject(PooledObject<T> pooledObject) {
    // ベースクラスでは No-op なので、必要ならOverrideする。
    // pooledObject.getObject で中身が取れるのでそれを操作。(バッファのcleanとか)
  }
  void passivateObject(PooledObject<T> pooledObject) {
    // ベースクラスでは No-op なので、必要ならOverrideする。
  }
  boolean validateObject(PooledObject<T> pooledObject) {
    // ベースクラスでは常にtrueが返るので、必要ならOverrideする。
  }
  void destroyObject(PooledObject<T> pooledObject) {
    // ベースクラスでは No-op なので、必要ならOverrideする。
  }
}
```


## ObjectPool

インターフェース
```
public interface ObjectPool<T> {
  T borrowObject()
    // Poolからインスタンスを取得する
    // 取得したインスタンスは、returnObjectかinvalidateObject で
    // プールに戻さないといけない。
    // プールに余りがなく、返せない場合の挙動は実装依存

  void returnObject(T obj)
    // インスタンスをプールに戻す

  void invalidateObject(T obj)
    // インスタンスを不正なものとしてプールに戻す。
    // インスタンスを使っているうちに例外が発生した場合など。

  void addObject()
    // あらかじめインスタンスを作っておくようにPoolに指示を出す。
    // Factoryのcreate作業が重い場合などに、あらかじめ作っておく場合などに使う。

  int getNumIdle()   // 現在の空きインスタンスの数を返す
  int getNumActive() // 現在貸出中のインスタンスの数を返す

  void clear() 
    // プール中の空きインスタンスを開放するよう指示を出す
  void close() 
    // プール中の全てのリソースを解放する。
    // ただし GenericObjectPool の実装だと、以降、borrowObjectできなくなるってだけのよう。
    // その時点既に空いているインスタンスは destroyObject される。
    // ひきつづき returnObject,invalidateObject はでき、それで戻されたインスタンスは destroy される。
}
```


通常は、GenericObjectPool を使えばよい。

https://commons.apache.org/proper/commons-pool/api-2.4.2/org/apache/commons/pool2/impl/GenericObjectPool.html

```
val factory = new MyFactory  // PooledObjectFactory[MyClass]
val pool = new GenericObjectPool[MyClass](factory)

// デフォルトではプールの上限が 8 (環境によるかも)
// 変えたい場合は、以下のように GenericObjectPoolConfig に設定して渡す
val factory = new MyFactory
val config = new GenericObjectPoolConfig()
config.setMaxTotal(3)
config.setMaxIdle(3)
val pool = new GenericObjectPool[MyClass](factory, config)

// もしくは pool の setXX メソッドで設定する
pool.setMaxTotal(3)
pool.setMaxIdle(3)

// 設定値を表示するには
logger.trace("pool.getMaxTotal=" + pool.getMaxTotal)
logger.trace("pool.getMaxIdle=" + pool.getMaxIdle)
logger.trace("pool.getMinIdle=" + pool.getMinIdle)
logger.trace("pool.getBlockWhenExhausted=" + pool.getBlockWhenExhausted)
```

その他
```
// Poolに空きがない場合にブロックするかどうか。falseだとBlockしない。
// その場合 java.util.NoSuchElementException: Pool exhausted が投げられる。
setBlockWhenExhausted(false) 
```

