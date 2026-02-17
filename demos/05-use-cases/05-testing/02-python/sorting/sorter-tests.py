import unittest
from sorting import ObjectSorter

class TestObjectSorter(unittest.TestCase):
    def setUp(self):
        self.objects = [{"name": "B", "age": 30}, {"name": "A", "age": 20}, {"name": "C", "age": 40}]
        self.sorter = ObjectSorter(self.objects)

    def test_sort_ascending(self):
        sorted_objects = self.sorter.sort("name", ascending=True)
        self.assertEqual(sorted_objects, [{"name": "A", "age": 20}, {"name": "B", "age": 30}, {"name": "C", "age": 40}])

    def test_sort_descending(self):
        sorted_objects = self.sorter.sort("name", ascending=False)
        self.assertEqual(sorted_objects, [{"name": "C", "age": 40}, {"name": "B", "age": 30}, {"name": "A", "age": 20}])
                
if __name__ == '__main__':
    unittest.main()