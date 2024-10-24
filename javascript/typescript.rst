===================================
TypeScript
===================================

メモをとりあえず置く::


    ESLint
    Path Intellisense
    Prettier
    TSLinst

    ---------------------------

    script タグの defer 属性

    lite-server Server起動しっぱなしで自動でリロードされる。

    ---------------------------

    TypeScriptでは、 string や number のようなプリミティブ型は小文字です。 StringやNumberではないので注意してください。

        any
        number, string, boolean
        object

        具体的なフィールド名を指定しないobject型 (いわゆるMap・連想配列みたいな使い方)

            Record<string, number>

            インデックス型 (index signature)
            https://typescriptbook.jp/reference/values-types-variables/object/index-signature
                let obj: {
                  [K: string]: number;
                };

                → obj は、キー(フィールド名)が任意のstring型で、値はnumber型
                K のところはなんでもいい。 K や key にすることが多い。

            フィールド名の型はstring、number、symbolのみ指定できる。

        Array型    string[] など
        Tuple型    TypeScript独自の型。長さ固定の配列
                    [number, string];
                    (注) push はできてしまう！

        Enum型     enum { NEW, OLD }

        Union型   string | number    // どちらも入れることができる
        
        Literal型  具体的な値を指定することもできる
                    :30   これは数値の30しか許さない。

        具体的な値のうちどれかを取るという型
            type Reason = 'timeout' | 'notfound' | 'forbidden' 

            下記も同じ。const の配列から変換して作る。
            export const Reasons = [ 'timeout', 'notfound', 'forbidden' ] as const;
            export type Reason = (typeof Reasons)[number];
                Reason は型なので、TSコンパイルすると消える。
                コード中で、Reasonごとに分類するとか、入力値がReasonとして妥当かをチェックするとか、
                そういう場合 Reasons が使えると便利なので、こういうテクニックがある。

        function型
            関数定義における型の指定
                function add(n1: number, n2: number): number {
                    ...
                }

                戻り値なしは void 


            関数型であることの指定

                Function   関数型であればなんでもよい
                
                (a: number, b: number) => number
                    特定の引数型と戻り値型を持つ関数。
                    仮引数名は一致する必要はない。


                戻り値なしが void の型には、何かをreturnする関数でもマッチする
                    (a: number, b: number) => void

        unknown型
            any型と似ているけど....。TODO

        never型
            voidと似ているけど.... TODO


        型エイリアス  カスタム型？  独自の型を定義する
            type Combinable = number | string;



    -------------------------
    https://www.typescriptlang.org/docs/handbook/tsconfig-json.html

    tsc


    watchモード  (-w)   ファイルに変更が入ると自動コンパイル
        tsc -w <ファイル名>


    ---


    tsc --init
        → tsconfig.json     tsc の設定ファイル

    tsc とやるだけでできるようになる。



    include
        デフォルトではプロジェクト全体
    exclude
        デフォルトでは ["node_modules"] になっている。
        自分で設定する場合は、 "node_modules" も入れておくことを忘れるな。
    同時にやると、include の対象から exclude を除く
    files ？


    target


    lib

    sourceMap



    -------------------------
    モダンな JavaScript

    const  定数。変更できない変数。
    var    グローバルスコープか関数スコープしかない
    let    ブロックスコープ

    アロー関数
    デフォルト関数パラメタ
    スプレッドオペレータ
    レストパラメタ
    配列とオブジェクトの分割代入


    -------------------------
    クラスとインターフェース


    コンストラクタ関数の引数に、アクセス修飾子を付けると
        メンバ変数の定義と初期化をすることができる。

        class Department {
            // private id: string;     // 書かなくてよい
            // name: string; 

            constructor(private id: string, public name: string) {
                // this.id = id;      // 書かなくてよい
                // this.name = name;  // 書かなくてよい
            }
        }

    readonly 修飾子  (typescriptのみ)

    getter, setter

    static
    abstract


    interface Greetable {     // extends で他のinterfaceを継承することもできる
        name: string;

        greet(phrase: string): void;
    }

    class Parseon implements Greetable {   // implements はカンマ区切りで複数書ける
        name: string;
        age = 30;

        constructor(n: string) {
            this.name = n;
        }

        greet(phrase: string) {
            console.log(phrase + ' ' + this.name);
        }
    }

    c.f. type での型定義との違い
        interface にないプロパティがあってもマッチする。
        type型だと、余分なプロパティがあったらマッチしない。


    c.f. class の継承との違い
        interfaceは複数実装できる。 クラスは1つの親クラスからしか継承できない

        abstructクラスには、実装を含めることができる。
        interfaceには実装を含めることができない。

    readonly を付けられる。 cf. public や private は付けることはできない。


    interface は interface をexteds することができて、しかも複数書ける。


    関数インターフェース

        interface AddFn {
            (a: number, b: number): number;
        }

        type AddFn = (a: number, b: number) => number;

        これと同じらしい。あんまりやらないらしい。


    オプショナルなプロパティ 
        ? をつける
        interface Named {
            readonly name: string;
            outputName?: string;      // オプショナル
        }

        クラスのメンバ定義でもつけられる。
        コンストラクタの引数にも付けられる。

        指定されない場合は undefined が設定される。



    ---------------------------
    より高度な型について



    交差型
        type Admin = {
            name: string;
            privileges: string[];
        }

        type Employee = {
            name: string;
            startDateL Date;
        }

        type ElevatedEmploee = Admin & Employee;


        これは似ている
        interface ElevatedEmploee extends Employee, Admin {}




        type Combinable = string | number;
        type Numeric = number | boolean;
        type Universal = Combinable & Numeric;   // number 型になる


    型ガード

        type Combinable = string | number;
        function add(a: Combinable, b: Combinable) {
            if (typeof a === 'string || typeof b === 'string') {  // <-- これが型ガード
                return a.toString() + b.toString()
            }

            // ここは、a と b が number であると推定される
            return a + b
        }


        type UnknownEmployee = Employee | Admin;
        function printEmployeeInformation(emp: UnknownEmployee) {
            console.log(emp.name);  // どちらにもある。
            if ('privileges' in emp) {
                // ここでは Admin 型と推定される
                console.log("Privileges: " + emp.privileges);
            }
            if ('startDate' in emp) {
                // ここでは Employee 型と推定される
                console.log("StartDate: " + emp.startDate);
            }
        }

        instanceof も使える。 
        でもこれは class でしかつかえない。interface では使えない。


    判別可能な Union 型

        interface Bird {
            type: 'bird';
            flyingSpeed: number;
        }

        interface Horse {
            type: 'horse';
            runningSpeed: number; 
        }

        type Animal = Bird | Horse;

        function moveAnimal(animal: Animal) {
            let speed;
            switch (animal.type) {
                case 'bird':
                    speed = animal.flyingSpeed;
                    break;
                case 'horse':
                    speed = animal.runningSpeed;
            }
            console.log('移動速度: ' + speed);
        }

        moveAnimal({type: 'bird', flyingSpeed: 100})
        moveAnimal({type: 'horse', flyingSpeed: 50})

    型キャスト

        const e1 = document.getElementById("user-input")
        // → HTMLElement | null と推定される

        const e2 = <HTMLInputElement>document.getElementById("user-input")!
        const e3 = document.getElementById("user-input")! as HTMLInputElement
        // → HTMLInputeElement 型になる
        //  それ以外の型が来ないことは開発者が担保する

        TODO  ! は  null ではないことを伝える。


    インデックス型

        TODO


    関数オーバーロード

        type Combinable = number | string;

        function add(a: nubmer, b: number): number;
        function add(a: string, b: string): string;
        function add(a: string, b: number): string;
        function add(a: nubmer, b: string): string;

        function add(a: Combinable, b: Combinable): Combinable {
            if ( typeof a === 'string || typeof b === 'string') {
                return a.toString() + b.toString();
            }
            return a + b;
        }

        // 関数オーバーロードがないと Combinable 型に推定される
        const ret1 = add(1, 2);          // number型に推定される
        const ret2 = add("aaa", "bbb");  // string型に推定される


    オプショナルチェイニング

        ?. 

    NULL合体演算子

        ??                左が null か undefined なら右。そうでないなら左。

        || と似てるけど。 左がTrusyなら左。そうでないなら右。

                          TODO もっとちゃんと書け。



    ---------------------------
    ジェネリック型

    ジェネリック型 - TypeScript Deep Dive 日本語版
    https://typescript-jp.gitbook.io/deep-dive/type-system/generics



        const names: Array<string> = []    // この場合 string[] と同じ

        const promise = new Promise<string>((resolve, reject) => {
            setTimeout(() => {
                resoleve('終わりました');
            }, 2000);
        })


    独自のジェネリック型

    関数ジェネリック

        function merge<T, U>(objA: T, objB: U) {
            return Object.assign(objA, objB);
        }

        const mergedObj = merge({name: 'Max'}, {age: 30});
        mergedObj.age


    ジェネリッククラス

        class DataStorage<T> {
            private data: T[] = []

            addItem(item: T) {
                this.data.push(item);
            }

            remoteItem(item: T) {
                this.data.splive(this.data.indexOf(item), 1);
            }

            getItems() {
                return [...this.data];
            }
        }

        const textStorage = new DataStorage<string>(); 
        const numberStorage = new DataStorage<number>(); 

    ジェネリックに制約
        <T extends object>
        <T extends string | number | boolean>   // プリミティブ型に限定

    keyof

        <T extends object, U extends keyof T>



    Generic型のユーティリティ

    Partial<T>  --- 型のプロパティをすべて optional 型に変換する

        function createCourseGoal(
            title: string,
            description: string,
            date: Date,
        ): CourseGoal {

            // let courseGoal = {}              // 下の代入の時点で不明なキーなのでエラーになる
            // let courseGoal: CourseGoal = {}  //  GourseGoal に {} は代入できないのでエラーになる
            let courseGoal: Partial<CourseGoal> = {}  

            courseGoal.title = title
            courseGoal.description = description;
            courseGoal.completeUntil = date;
            return courseGoal as CourseGoal;    // もとになった型にキャストできる
        }

    Readonly<T>

        const names: Readonly<string[]> = ['Max', 'Anna'];
        names.push('Manu');  // できない
        names.pop();         // できない






    デコレータ

    TODO むずい。あとでもう一度見直す。

    デコレータをつけられる場所


    - クラス        コンストラクタを受け取る
    - プロパティ    
    - アクセサ
    - メソッド
    - パラメタ


    付ける場所によって、デコレータの引数が異なる

    一部のデコレータは値を返すことができる

        クラスデコレータ → コンストラクタ関数 (実質クラス)
        メソッドデコレータ → ProperyDescripter
        アクセサデコレータ → ProperyDescripter




    デコレーターが実行されるタイミング

    クラスが定義されたタイミング。
    cf. インスタンス化されたタイミングではない




    デコレータとデコレータファクトリ





