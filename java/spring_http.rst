=======================================
SpringのHttp関連
=======================================
















HttpMessageConverter(s)
=================================

参考ドキュメント
------------------

- `HTTP メッセージ変換 :: Spring Framework - リファレンス <https://spring.pleiades.io/spring-framework/reference/web/webmvc/message-converters.html>`__


概要
-----------

Spring の webサーバや、RestTemplate などの http client は、
オブジェクトと http request/response とをマッピングする機能を持っている。

- http server

  - http request → オブジェクト
  - http response ← オブジェクト

- RestTemplate など http client

  - オブジェクト → http request
  - オブジェクト ← http response


このために、web サーバや、RestTemplate は HttpMessageConverter のリストを内包している。


確認の方法(RestTemplateの場合)(groovy)::

    restTemplate.messageConverters.eachWithIndex { c, i ->
        println("converter[" + i + "]=" + c.class.name + " mediaTypes=" + c.supportedMediaTypes)
    }

例::

    springBoot 4系
    [0] org.springframework.http.converter.ByteArrayHttpMessageConverter
    [1] org.springframework.http.converter.StringHttpMessageConverter
    [2] org.springframework.http.converter.ResourceHttpMessageConverter
    [3] org.springframework.http.converter.support.AllEncompassingFormHttpMessageConverter
    [4] org.springframework.http.converter.json.JacksonJsonHttpMessageConverter
    [5] org.springframework.http.converter.cbor.MappingJackson2CborHttpMessageConverter
    [6] org.springframework.http.converter.yaml.MappingJackson2YamlHttpMessageConverter
    [7] org.springframework.http.converter.xml.JacksonXmlHttpMessageConverter


    SpringBoot 3系
    [0] org.springframework.http.converter.ByteArrayHttpMessageConverter
    [1] org.springframework.http.converter.StringHttpMessageConverter
    [2] org.springframework.http.converter.StringHttpMessageConverter
    [3] org.springframework.http.converter.ResourceHttpMessageConverter
    [4] org.springframework.http.converter.ResourceRegionHttpMessageConverter
    [5] org.springframework.http.converter.support.AllEncompassingFormHttpMessageConverter
    [6] org.springframework.http.converter.json.MappingJackson2HttpMessageConverter
    [7] org.springframework.http.converter.cbor.MappingJackson2CborHttpMessageConverter
    [8] org.springframework.http.converter.xml.MappingJackson2XmlHttpMessageConverter


どのコンバーターが使われるかは、http の Content-Type の値と、オブジェクトの型で決まる。
先頭から各converterに canRead(),canWrite() で聞いていく。



converter(s) のカスタマイズの方法
-----------------------------------------

例えば、Jsonで空リストをnullにするとか、カスタマイズしたい場合は、
この converter(s) をカスタマイズすることで対応する。


SpringBoot 4系の場合
^^^^^^^^^^^^^^^^^^^^^^^^^^

SpringBoot 4系では、

Beanに直接 HttpMessageConveter (を継承したインスタンス) を追加した場合、リストの先頭に追加される。

これはあまり推奨されず、下記の Customizer を使う。

例(カスタマイズしたJsonMapperを内包した JacksonHttpMessageConverter を使う)::

  @Configuration
  public class JacksonJsonHttpMessageConverterConfig {

      @Bean
      public ClientHttpMessageConvertersCustomizer clientHttpMessageConvertersCustomizer(JsonMapper origJsonMapper) {
          return builder -> {
              JsonMapper jsonMapper = origJsonMapper.rebuild()
                      .disable(SerializationFeature.WRITE_EMPTY_JSON_ARRAYS)
                      .disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES)
                      .build();

              builder.withJsonConverter(new JacksonJsonHttpMessageConverter(jsonMapper));
          };
      }

      @Bean
      public ServerHttpMessageConvertersCustomizer serverHttpMessageConvertersCustomizer(JsonMapper origJsonMapper) {
          return builder -> {
              JsonMapper jsonMapper = origJsonMapper.rebuild()
                      .disable(SerializationFeature.WRITE_EMPTY_JSON_ARRAYS)
                      .disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES)
                      .build();

              builder.withJsonConverter(new JacksonJsonHttpMessageConverter(jsonMapper));
          };
      }
  }

ClientHttpMessageConvertersCustomizer/ServerHttpMessageConvertersCustomizer 
がフック的な役割になっていて、これをBean定義しておくと、converters を組み立てるときに呼ばれる。

- https://spring.pleiades.io/spring-boot/reference/web/servlet.html#web.servlet.spring-mvc.message-converters
- https://spring.pleiades.io/spring-boot/api/java/org/springframework/boot/http/converter/autoconfigure/ServerHttpMessageConvertersCustomizer.html
- https://spring.pleiades.io/spring-boot/api/java/org/springframework/boot/http/converter/autoconfigure/ClientHttpMessageConvertersCustomizer.html

builder は、HttpMessageConverters.Builder 型で、下記のメソッドを持っている。
https://docs.spring.io/spring-boot/api/java/org/springframework/boot/http/converter/autoconfigure/HttpMessageConverters.html

- addCustomConverter(...)  --- 先頭に追加
- withStringConverter(...) --- StringConveterを上書き
- withJsonConverter(...)  --- JSONのConverterを上書き


なお、上のサンプルコードでは、
JsonMapper.builder() ではなく、 origJsonMapper.build() を用いている。
これは、JsonMapper を Bean で差し替え可能な柔軟性を残すようにするため。



SpringBoot 3系の場合
^^^^^^^^^^^^^^^^^^^^^^^^^^

SpringBoot 3系では、 org.springframework.boot.autoconfigure.http.HttpMessageConverters が、
ApplicationContext 上の HttpMessageConverter Bean を集めて、デフォルト converter とマージしていました。

このときのルールは Javadoc に明記されていて、
追加 converter は、同じ型のデフォルト converter の直前に追加される。
もし同じ型のデフォルト converter がなければリスト先頭に追加される。

→ https://docs.spring.io/spring-boot/3.4/api/java/org/springframework/boot/autoconfigure/http/HttpMessageConverters.html

    additionalConverters - additional converters to be added. 
    Items are added just before any default converter of the same type
    (or at the front of the list if no default converter is found)

なので、 カスタマイズしたい HttpMessageConverter の Bean を定義すればよい。

例(カスタマイズしたObjectMapperを内包した MappingJackson2HttpMessageConverterConfig を使う)::

    @Configuration
    public class MappingJackson2HttpMessageConverter {

        @Bean
        public MappingJackson2HttpMessageConverter mappingJackson2HttpMessageConverter() {
            ObjectMapper objectMapper = new ObjectMapper();
            objectMapper.configure(SerializationFeature.WRITE_EMPTY_JSON_ARRAYS, false);
            objectMapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
            objectMapper.registerModule(new JavaTimeModule());
            return new MappingJackson2HttpMessageConverter(objectMapper);
        }
    }


