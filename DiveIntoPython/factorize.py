class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exception(self):
        cases = ('string', 1.5)
        for case_ in cases:
            with self.subTest(x=case_):
                self.assertRaises(TypeError, factorize, case_)

    def test_negative(self):
        cases = (-1,  -10,  -100)
        for case_ in cases:
            with self.subTest(x=case_):
                self.assertRaises(ValueError, factorize, case_)

    def test_zero_and_one_cases(self):
        cases = (0,  1)
        for case_ in cases:
            with self.subTest(x=case_):
                self.assertTupleEqual(factorize(case_), (case_,))


    def test_simple_numbers(self):
        cases = (3, 13, 29)
        for case_ in cases:
            with self.subTest(x=case_):
                self.assertTupleEqual(factorize(case_), (case_,))

    def test_two_simple_multipliers(self):
        cases = (6, 26, 121)
        passed = (2, 3),   (2, 13),   (11, 11)
        for i, case_ in enumerate(cases):
            with self.subTest(x=case_):
                self.assertTupleEqual(factorize(case_), passed[i])

    def test_many_multipliers(self):
        cases = (1001, 9699690)
        passed = (7, 11, 13),  (2, 3, 5, 7, 11, 13, 17, 19)
        for i, case_ in enumerate(cases):
            with self.subTest(x=case_):
                self.assertTupleEqual(factorize(case_), passed[i])