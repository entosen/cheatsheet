# gmake

https://www.ecoop.net/coop/translated/GNUMake3.77/make_toc.jp.html

## Makefile

### 変数

```
変数名
    大文字小文字を区別
    
    - makefileの内部利用が目的の変数には小文字
    - 大文字の変数名は暗黙のルールを制御する媒介変数(parameters)や
	コマンドオプションで上書きすべき媒介変数(parameters)

代入
    =      
	再帰展開変数。
	右辺は変数展開されない。一字一句同じに格納される。
	あとで再帰的に評価。
    :=     
	単純展開変数。
	右辺は(再帰的に)評価されて結果の値が格納される



define？


展開
    $(変数名)
    ${変数名}



分岐
    ifndef
    ifeq
    else
    endif


自動変数
    $@    ルールのターゲットのファイル名
    $*    語幹
```

### ルール

TODO
