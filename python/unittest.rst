========================
unittest
========================




起動のさせ方
================


単一のモジュール(ファイル)のみの場合、下記を書いて実行すればいい。
(unittest.main() はそのモジュール内のテストクラスを実行する)

::

    if __name__ == '__main__':
        unittest.main()


複数のファイルがある場合。

(例) こんな構造だとする::

    ./testcace/
        test_a.py    
        test_b.py
        __init__.py

test_a.py::

    import unittest
    class TestA(unittest.TestCase):

        def test_a_1(self):
            self.assertEqual(1+1, 2)
            
        def test_a_2(self):
            self.assertEqual(10-3, 7)


test_b.py::

    import unittest
    class TestB(unittest.TestCase):

        def test_b_1(self):
            self.assertEqual(3*7, 21)

        def test_b_2(self):
            self.assertEqual(108/4, 27)


コマンドラインから::

    # カレントディレクトリ以下を走査 (デフォルトのパターンは test_*.py)
    python -m unittest
    python -m unittest discover
    python -m unittest discover -p '*_b.py'   # テストファイル名パターン指定

    # モジュール指定、TestCaseクラス指定、メソッド指定
    python -m unittest testcase.test_a testcase.test_b
    python -m unittest testcase.test_a.TestA
    python -m unittest testcase.test_a.TestA.test_a_1

    # ファイルパスでもいける
    python -m unittest testcase/test_a.py

    # verbose にする場合
    python -m unittest -v
    python -m unittest discover -v


pythonコードから実行する::

    import unittest

    suite = unittest.TestSuite()

    suite.addTest(unittest.defaultTestLoader.discover('.'))

    runner = unittest.TextTestRunner()  # verbosity=2 をつけると verbose
    result = runner.run(suite)
    sys.exit(not result.wasSuccessful())


テストを指定する方法::

    # 名前(文字列)で指定。 import も自動でしてくれる
    suite.addTest(unittest.defaultTestLoader.loadTestsFromName('testcase.test_a.TestA.test_a_2'))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromName('testcase.test_b'))

    # モジュール以下の全てのテスト
    suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(testcase.test_a))

    # テストケース以下の全てのテスト
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testcase.test_a.TestA))

    # TestCaseクラスのインスタンスの生成から自前でやる場合
    # TestCaseクラスは、テストメソッド毎にインスタンス化される (コンストラクタの引数に指定)
    suite.addTest(testcase.test_a.TestA('test_a_1'))
    suite.addTest(testcase.test_a.TestA('test_a_2'))
    suite.addTest(testcase.test_b.TestB('test_b_1'))
    suite.addTest(testcase.test_b.TestB('test_b_2'))

    # テストメソッド名はクラスから取り出すこともできる
    for name in unittest.defaultTestLoader.getTestCaseNames(testcase.test_a.TestA):
        suite.addTest(testcase.test_a.TestA(name))
    for name in unittest.defaultTestLoader.getTestCaseNames(testcase.test_b.TestB):
        suite.addTest(testcase.test_b.TestB(name))

