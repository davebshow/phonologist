# -*- coding: utf-8 -*-
import unittest

from phonologist import Words


class PhonologistTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_words(self):
        w = u"yo escribo un test"
        words = Words(w)
        self.assertEquals(words.tokens, [u'yo', u'escrib', u'un', u'test'])


if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    suite = test_loader.loadTestsFromTestCase(PhonologistTestCase)
    run = unittest.TextTestRunner(verbosity=2).run(suite)
    if run.errors or run.failures:
        exit(1)
