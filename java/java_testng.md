java testNG

- [TestNG - Welcome](http://testng.org/doc/index.html)
- [次世代テストフレームワークでテストを変える（2）：JUnitにはないTestNGの“5”つの強力なテスト用機能 (1/2) - ＠IT](http://www.atmarkit.co.jp/ait/articles/0809/22/news117.html)

```java
import org.testng.Assert;
import org.testng.annotations.*;

public class SimpleTest {
 
 @BeforeClass
 public void setUp() {
   // code that will be invoked when this test is instantiated
 }
 
 @Test
 public void testAAA() {
   Assert.assertEquals(x,y)
 }
 
 
}
```

@Test
@Test(groups = { "fast" })

メソッド名は任意。


```
@BeforeMethod  // 各テストメソッドの実行前に呼ばれる
@BeforeClass   // そのクラスのどのテストメソッドよりも先に呼ばれる
@BeforeGroups
@BeforeTest
@BeforeSuite
@AfterMethod
@AfterClass
@AfterGroups
@AfterTest
@AfterSuite
```

メソッド名は任意


Assertion

```
Assert.assertEquals(x, y);
Assert.assertSame(x, y);
Assert.assertTrue(x);
Assert.assertFalse(x);

```

例外が飛ぶことをチェック
@Test(expectedExceptions = { java.lang.RuntimeException.class })





@DataProvider --- テストメソッドに引数を渡す。

```
import static org.testng.Assert.assertEquals;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;
public class DataProviderSample {

    // name を指定しなかった場合は、メソッド名が name になる？
    @DataProvider(name = "add")
    public Object[][] data() {
        return new Object[][] {
            { 1, 2, 3 }, { 3, 3, 6 }, { 6, 4, 10 } };
    }

    @Test(dataProvider = "add")
    public void verifyAdd(int a, int b, int expected) {
        Target target = new Target();
        int actual = target.add(a, b);
        assertEquals(actual, expected);
    }
}
```

