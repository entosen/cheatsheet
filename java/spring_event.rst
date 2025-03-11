

参考
=====

- `SpringBootの非同期イベント発行に必要な手順 #Java - Qiita <https://qiita.com/alpha_pz/items/0d709fa0e86b81ef0bb7>`__

  - 古いかも

- `Spring Bootにおける非同期処理: ApplicationEventPublisherとSpockのPollingConditionsによるテスト #Java - Qiita <https://qiita.com/seijikohara/items/7dc9e511f77893e50aee>`__


- `EventListener (Spring Framework API) - Javadoc <https://spring.pleiades.io/spring-framework/docs/current/javadoc-api/org/springframework/context/event/EventListener.html>`_
- `TransactionalEventListener (Spring Framework API) - Javadoc <https://spring.pleiades.io/spring-framework/docs/current/javadoc-api/org/springframework/transaction/event/TransactionalEventListener.html>`_


基本ケース
================

概要、やること
--------------------

- Eventの定義。ApplicationEvent を継承した独自イベントを定義する
- Publisher側。 ApplicationEventPublisher.publishEvent(event) に投げ込む。


Eventの定義
-------------------

ApplicationEvent を継承した独自イベントを定義する。

PrimaryEvent.java::

    @Getter
    public class PrimaryEvent extends ApplicationEvent {

        private final SampleMessage sampleMessage;

        public PrimaryEvent(Object source,  SampleMessage sampleMessage) {
            super(source);
            this.sampleMessage = sampleMessage;
        }

    }

注

- Spring Framework 4.2より前のバージョンではApplicationEventの継承が必須でしたが、
  以降のバージョンでは継承が任意となりました。


Publisher側
------------------

org.springframework.context.ApplicationEventPublisher の publishEvent(event) メソッドに投げ込む。

PrimaryEventPublisher.java::

    import org.springframework.context.ApplicationEventPublisher;
    import org.springframework.stereotype.Component;

    import lombok.AllArgsConstructor;
    import lombok.extern.log4j.Log4j2;

    @Component
    @AllArgsConstructor
    public class PrimaryEventPublisher {

        private final ApplicationEventPublisher applicationEventPublisher;

        public void ignite(String message) {
            SampleMessage sampleMessage = SampleMessage.of(message);
            
            // イベント作成する
            PrimaryEvent event = new PrimaryEvent(this, sampleMessage);

            // イベント発行！
            applicationEventPublisher.publishEvent(event);
        }
    }


Listener側
------------------

org.springframework.context.ApplicationListenerインタフェースを実装します。
Spring管理下に置く必要がある(@Component を付けるなど)。

この書き方古いかも::

    import org.springframework.context.ApplicationListener;
    import org.springframework.stereotype.Component;

    import lombok.extern.log4j.Log4j2;

    @Component
    public class PrimaryEventListener implements ApplicationListener<PrimaryEvent>{

        @Override
        public void onApplicationEvent(PrimaryEvent event) {
            SampleMessage sampleMessage = event.getSampleMessage();
            
            // メッセージを受けた後の後続処理↓......
        }

    }


``@EventListener`` を付与したメソッドは、指定された型のイベントが発行されたときに呼び出される。

::

    @Component
    public class OrderEventListener {
        private final OrderRepository orderRepository;

        public OrderEventListener(OrderRepository orderRepository) {
            this.orderRepository = orderRepository;
        }

        @Async
        @EventListener
        @Transactional
        public void handleOrderCreatedEvent(OrderCreatedEvent event) {
            var order = new OrderEntity(
                null,
                event.orderNumber(),
                event.occurredAt()
            );
            orderRepository.save(order);
        }
    }


さらに ``@Async`` を付けることで非同期になる。 
その場合、(どこに？Applicationに？) ``@EnableAsync`` を付ける必要もある。

::

    @SpringBootApplication
    @EnableAsync
    public class Application {
        ...
    }

Transactional?

- ``@EventLister`` は、通常のイベントリスナー
- ``@TransactionEventListener`` は、リスナーは、デフォルトでは、トランザクションのコミットフェーズにバインドされる

  - ``@EvenLister`` と ``@Transactional`` を同時に付けるのと同じか？？


自分が受け取るクラスを指定::

    @TransactionalEventListener(classes = MyEvent.class)
    @Async
    public void processEvent(MyEvent event) {...}
    
    @TransactionalEventListener(classes = {MyEvent1.class, MyEvent2.class})
    @Async
    public void processEvent(MyEventInterface event) {...} // MyEvent[12]どちらも受け取れるようにInterfaceを用意しておく

↑サンプル見ると明示的に指定しなくても動きそうだけどな。TODO
