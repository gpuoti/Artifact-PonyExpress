
import unittest
from alternative_set import combine

class TestCombinationGenerator(unittest.TestCase):

    def setUp(self):
        self.integers_alternative_set = [5, 3, 2, 8]  
        self.float_alternative_set =  [0.1, 0.9] 
        self.letters = ['A', 'B', 'C']

    def tearDown(self):
        pass

    def test_iterate_over_alternatives(self):
        """
        AlternativeSet can be iterated just as the elements it contains. It is basically a list.
        """
        expectation = [5, 3, 2, 8]
        expi = 0
        for alternative in self.integers_alternative_set:
            self.assertEqual(expectation[expi], alternative, msg='iteration over alternative must correspond to iteration on the list of objects') 
            expi +=1

    def test_iteration_over_combinations_produce_tuples(self):
        """
        Alternative sets can combine to produce alternative configurations. Each alternative configuration 
        is a tuple with elements ordered as the combined alternative set sequence
        """

        expectations = [
            (self.integers_alternative_set[0], self.float_alternative_set[0]),
            (self.integers_alternative_set[0], self.float_alternative_set[1]),
            (self.integers_alternative_set[1], self.float_alternative_set[0]),
            (self.integers_alternative_set[1], self.float_alternative_set[1]),
            (self.integers_alternative_set[2], self.float_alternative_set[0]),
            (self.integers_alternative_set[2], self.float_alternative_set[1]),
            (self.integers_alternative_set[3], self.float_alternative_set[0]),
            (self.integers_alternative_set[3], self.float_alternative_set[1]),
        ]

        for configuration in combine ([self.integers_alternative_set, self.float_alternative_set]):
            self.assertTrue(len(expectations) > 0, msg='combine produced more cofigurations than expected')
            self.assertEqual(2, len(configuration), msg='each configuration produced combining two alternative set of objects, must be a tuple of two elements')
            self.assertEqual(expectations[0], configuration)
            expectations = expectations[1:]

        self.assertTrue(len(expectations) == 0, msg='check combine produces the right number of configurations\n' +str(expectations))

    def test_iteration_over_combinations_produce_tuples_3(self):
        """
        Alternative sets can combine to produce alternative configurations. Each alternative configuration 
        is a tuple with elements ordered as the combined alternative set sequence
        """

        expectations = [
            (self.integers_alternative_set[0], self.float_alternative_set[0], self.letters[0]),
            (self.integers_alternative_set[0], self.float_alternative_set[0], self.letters[1]),
            (self.integers_alternative_set[0], self.float_alternative_set[0], self.letters[2]),
            (self.integers_alternative_set[0], self.float_alternative_set[1], self.letters[0]),
            (self.integers_alternative_set[0], self.float_alternative_set[1], self.letters[1]),
            (self.integers_alternative_set[0], self.float_alternative_set[1], self.letters[2]),
            (self.integers_alternative_set[1], self.float_alternative_set[0], self.letters[0]),
            (self.integers_alternative_set[1], self.float_alternative_set[0], self.letters[1]),
            (self.integers_alternative_set[1], self.float_alternative_set[0], self.letters[2]),
            (self.integers_alternative_set[1], self.float_alternative_set[1], self.letters[0]),
            (self.integers_alternative_set[1], self.float_alternative_set[1], self.letters[1]),
            (self.integers_alternative_set[1], self.float_alternative_set[1], self.letters[2]),
            (self.integers_alternative_set[2], self.float_alternative_set[0], self.letters[0]),
            (self.integers_alternative_set[2], self.float_alternative_set[0], self.letters[1]),
            (self.integers_alternative_set[2], self.float_alternative_set[0], self.letters[2]),
            (self.integers_alternative_set[2], self.float_alternative_set[1], self.letters[0]),
            (self.integers_alternative_set[2], self.float_alternative_set[1], self.letters[1]),
            (self.integers_alternative_set[2], self.float_alternative_set[1], self.letters[2]),
            (self.integers_alternative_set[3], self.float_alternative_set[0], self.letters[0]),
            (self.integers_alternative_set[3], self.float_alternative_set[0], self.letters[1]),
            (self.integers_alternative_set[3], self.float_alternative_set[0], self.letters[2]),
            (self.integers_alternative_set[3], self.float_alternative_set[1], self.letters[0]),
            (self.integers_alternative_set[3], self.float_alternative_set[1], self.letters[1]),
            (self.integers_alternative_set[3], self.float_alternative_set[1], self.letters[2]),
        ]

        for configuration in combine ([self.integers_alternative_set, self.float_alternative_set, self.letters]):
            self.assertTrue(len(expectations) > 0, msg='combine produced more cofigurations than expected')
            self.assertEqual(3, len(configuration), msg='each configuration produced combining two alternative set of objects, must be a tuple of two elements')
            self.assertEqual(expectations[0], configuration)
            expectations = expectations[1:]

        self.assertTrue(len(expectations) == 0, msg='check combine produces the right number of configurations\n' +str(expectations))