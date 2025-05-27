import unittest


class MyTestCase(unittest.TestCase):
    def testSomething(self) -> None:
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
