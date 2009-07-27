import unittest
import random

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    def testshuffle(self):
        # make sure the shuffled sequence does not lose any elements
        random.shuffle(self.seq)
        self.seq.sort()
        self.assertEqual(self.seq, range(10))

    def testchoice(self):
        element = random.choice(self.seq)
        self.assert_(element in self.seq)

    def testsample(self):
        self.assertRaises(ValueError, random.sample, self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assert_(element in self.seq)

class FroomiTest(unittest.TestCase):
    
    def setUp(self):
        try:
            import froomi
            self.froomi = froomi.Froomi()
        except ImportError, e:
            self.fail(msg)       
    
    def testStartup(self):
        self.failUnless((hasattr(self.froomi, 'debug') is True), 'Froomi missing arrtibute debug')
        self.failUnless((hasattr(self.froomi, 'confd') is True), 'Froomi missing attribute confd')
        
    def test_loadCfg(self):
        self.failUnless(self.froomi._loadCfg() is True, 'froomi._loadCfg() returned false')
        
    def test_loadHTTPD(self):
        self.failUnless(self.froomi._loadHTTPD() is True, 'froomi._loadHTTPD() returned false')
    
       

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(FroomiTest)
    unittest.TextTestRunner(verbosity=2).run(suite)