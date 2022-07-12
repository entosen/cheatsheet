




(注) go の http server が受け取る ``r *http.Request`` での Host 関連のフィールドについて。

Host関連フィールドはいくつかあるが、下記のようになっているので、注意。

- Host名(http通信上の ``Host:`` ヘッダ)は、r.Host に入り、r.Header には入らない(除かれる)
- r.URL は、http通信の1行目 ``GET /hoge/fuga?foo=bar HTTP/1.0`` みたいな部分をパースしたものなので、
  r.URL.Host は空になっている

