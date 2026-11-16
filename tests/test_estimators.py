import importlib, contextlib, io, unittest
import numpy as np
from variance_reduction.pricing import BS, CMC_euro, CMC_asia
class ProjectTests(unittest.TestCase):
    def test_computational_imports_are_quiet(self):
        output=io.StringIO()
        with contextlib.redirect_stdout(output):
            for module in ['pricing','stratification','antithetic','control_variate']:
                importlib.reload(importlib.import_module('variance_reduction.'+module))
        self.assertEqual(output.getvalue(),'')
    def test_black_scholes_reference(self):
        self.assertAlmostEqual(BS(),12.335998930368717,places=8)
    def test_seeded_estimators_remain_repeatable(self):
        for fn in [lambda: CMC_euro(20),lambda: CMC_asia(20,3)]:
            np.random.seed(12); first=fn()
            np.random.seed(12); second=fn()
            np.testing.assert_allclose(first,second)
if __name__ == '__main__':unittest.main()
