import unittest
from unittest import TestCase

from samovar.terms import Term, Var


class TermTestCase(TestCase):
    def test_term_basic_properties(self):
        t1 = Term('alice')
        t2 = Term('actor', subterms=[t1])
        v1 = Var('?A')
        t3 = Term('actor', subterms=[v1])

        self.assertTrue(t1.is_atom())
        self.assertFalse(t2.is_atom())
        self.assertFalse(v1.is_atom())
        self.assertFalse(t3.is_atom())

        self.assertTrue(t1.is_ground())
        self.assertTrue(t2.is_ground())
        self.assertFalse(v1.is_ground())
        self.assertFalse(t3.is_ground())

        self.assertEqual(t2, Term('actor', subterms=[Term('alice')]))

    def test_term_replace(self):
        t = Term('actor', subterms=[Var('?A')])
        r = t.replace(Var('?A'), Term('alice'))
        self.assertEqual(r, Term('actor', subterms=[Term('alice')]))


if __name__ == '__main__':
    unittest.main()
