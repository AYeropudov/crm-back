import unittest

class Test:
    __slots__ = ["one", "two"]

    def __init__(self):
        self.one = None
        self.two = None

    def fill(self, dict):
        for key, value in dict.items():
            setattr(self, key, value)

    def to_dict(self):
        return {key:getattr(self, key) for key in self.__slots__ if getattr(self, key) is not None}

class MyTestCase(unittest.TestCase):
    def test_to_dict(self):
        br = Test()
        sample = {
            "one": "test"
        }
        br.fill(sample)
        self.assertEqual(br.to_dict(), sample)


if __name__ == '__main__':
    unittest.main()
