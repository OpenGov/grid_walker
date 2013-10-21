# This import fixes sys.path issues
import bootstrap
from pydgrid import grid
import unittest

class TableWrapTest(unittest.TestCase):
    '''
    Tests the creation and iteration of grid objects
    '''
    def basic_grid_asserts(self, test_grid, keys, values, items):
        self.assertListEqual(keys, list(test_grid.full_iter()))
        self.assertListEqual(keys, list(test_grid.full_iter_keys()))
        self.assertListEqual(values, list(test_grid.full_iter_values()))
        self.assertListEqual(items, list(test_grid.full_iter_items()))

    def dict_grid_asserts(self, test_grid, checker):
        '''
        Sorts the keys/values to match -- repeated values in the wrong order
        won't raise an exception!
        '''
        self.assertListEqual(sorted(checker.iterkeys()), sorted(list(test_grid.full_iter())))
        self.assertListEqual(sorted(checker.iterkeys()), sorted(list(test_grid.full_iter_keys())))
        self.assertListEqual(sorted(checker.itervalues()), sorted(list(test_grid.full_iter_values())))
        self.assertListEqual(sorted(checker.iteritems()), sorted(list(test_grid.full_iter_items())))

    def test_basic_int_grid(self):
        test_grid = grid.IntGrid((0, 10))
        self.assertListEqual(range(11), list(test_grid))

        for index in test_grid:
            test_grid[index] = -index
        
        tuple_indexes = map(lambda x: (x,), list(range(11)))
        values = range(0,-11,-1)

        self.basic_grid_asserts(test_grid, tuple_indexes, values, zip(tuple_indexes, values))

    def test_multi_dim_int_grid(self):
        test_grid = grid.IntGrid((0, 10), (-20, 20, 2), (0,1))
        full_items_check = {}
        
        for index_1, check_index_1 in zip(test_grid, range(11)):
            self.assertEqual(index_1, check_index_1)
            for index_2, check_index_2 in zip(test_grid[index_1], range(-20, 22, 2)):
                self.assertEqual(index_2, check_index_2)
                for index_3, check_index_3 in zip(test_grid[index_1][index_2], [0, 1]):
                    self.assertEqual(index_3, check_index_3)
                    test_grid[index_1][index_2][index_3] = index_1*index_2*index_3
                    full_items_check[(index_1, index_2, index_3)] = index_1*index_2*index_3

        self.dict_grid_asserts(test_grid, full_items_check)

    def test_basic_float_grid(self):
        test_grid = grid.FloatGrid((0, 10))
        self.assertListEqual(range(11), list(test_grid))

        for index in test_grid:
            test_grid[index] = -index + 0.5
        
        tuple_indexes = map(lambda x: (x,), list(range(11)))
        values = map(lambda index: -index + 0.5, range(11))

        self.basic_grid_asserts(test_grid, tuple_indexes, values, zip(tuple_indexes, values))

    def test_multi_dim_int_grid(self):
        test_grid = grid.FloatGrid((-1, 10), (-20, 20, 3), (0, 0))
        full_items_check = {}
        
        for index_1, check_index_1 in zip(test_grid, range(-1, 11)):
            self.assertEqual(index_1, check_index_1)
            for index_2, check_index_2 in zip(test_grid[index_1], range(-20, 21, 3)):
                self.assertEqual(index_2, check_index_2)
                for index_3, check_index_3 in zip(test_grid[index_1][index_2], [0]):
                    self.assertEqual(index_3, check_index_3)
                    test_grid[index_1][index_2][index_3] = index_1*index_2*index_3 - 0.3
                    full_items_check[(index_1, index_2, index_3)] = index_1*index_2*index_3 - 0.3

        self.dict_grid_asserts(test_grid, full_items_check)

    def test_basic_obj_grid(self):
        test_grid = grid.ObjectGrid((0, 10))
        self.assertListEqual(range(11), list(test_grid))

        for index in test_grid:
            test_grid[index] = 'neg_i='+str(-index) if index % 2 else index
        
        tuple_indexes = map(lambda x: (x,), list(range(11)))
        values = map(lambda index: 'neg_i='+str(-index) if index % 2 else index, range(11))

        self.basic_grid_asserts(test_grid, tuple_indexes, values, zip(tuple_indexes, values))

    def test_multi_dim_str_grid(self):
        test_grid = grid.ObjectGrid((0, 10), (-20, 20, 2), (0,1))
        full_items_check = {}
        
        for index_1, check_index_1 in zip(test_grid, range(11)):
            self.assertEqual(index_1, check_index_1)
            for index_2, check_index_2 in zip(test_grid[index_1], range(-20, 22, 2)):
                self.assertEqual(index_2, check_index_2)
                for index_3, check_index_3 in zip(test_grid[index_1][index_2], [0, 1]):
                    self.assertEqual(index_3, check_index_3)
                    test_grid[index_1][index_2][index_3] = 'i='+str(index_1*index_2*index_3)
                    full_items_check[(index_1, index_2, index_3)] = 'i='+str(index_1*index_2*index_3)

        self.dict_grid_asserts(test_grid, full_items_check)

    # TODO test slices/all combinations of getters/setters

if __name__ == '__main__': 
    unittest.main()
