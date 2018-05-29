


## 乱数

### rand 関数

Linux C の場合は、rand 関数は random 関数と同じ。

以前FreeBSDのときは rand は下位ビットのランダム性が低すぎて
(偶数と奇数が交互に返る)問題になったが、そういうことはないみたい。

ただ、それでもどちらかというと下位ビットのランダム性は低い部類の
アルゴリズムなので、以下のように上位ビットを使うようにするのがよい。

参考:
- https://ja.wikipedia.org/wiki/Rand
- http://www.kouno.jp/home/c_faq/c13.html#16
- [良い乱数・悪い乱数](http://www001.upp.so-net.ne.jp/isaku/rand.html)

```c
#include <stdlib.h>
#include <time.h>

void func() {

    srand((unsigned int) time(NULL));

    while(1) {
	/* 0.0 以上 1.0 未満 の double 値 */
	double d = (rand() / ((double)RAND_MAX + 1.0));

	/* 0 から N-1 までの整数を返そうとする場合 */
	int r = (int)((double)rand() / ((double)RAND_MAX + 1) * N)
    }
}
```
