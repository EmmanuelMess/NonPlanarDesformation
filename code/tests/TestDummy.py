import unittest


class MyTestCase(unittest.TestCase):
    def testSomething(self):
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
