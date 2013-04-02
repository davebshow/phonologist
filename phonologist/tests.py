# -*- coding: utf-8 -*-
import unittest

from phonologist import Words


class Phonologist(object):
    """docstring for phonologist"""

    def __init__(self):
        super(Phonologist, self).__init__()
        self._words = []

    def _get_words(self):
        return self._words

    def _set_words(self, words_list):
        self._words = words_list

    words = property(_get_words, _set_words)


class PhonologistTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_words(self):
        w = u"yo escribo un test"
        words = Words(w)
        self.assertEquals(words.tokens, [u'yo', u'escribo', u'un', u'test'])

    def test_one(self):
        ph = Phonologist()
        ph.words = ["one", "word"]
        self.assertEquals(ph.words, ["one", "word"])


if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    suite = test_loader.loadTestsFromTestCase(PhonologistTestCase)
    run = unittest.TextTestRunner(verbosity=2).run(suite)
    if run.errors or run.failures:
        exit(1)
