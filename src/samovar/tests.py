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

    def test_term_match_ground(self):
        t1 = Term('actor', subterms=[Term('alice')])
        p1 = Term('actor', subterms=[Term('alice')])
        u = {}
        p1.match(t1, u)
        self.assertEqual(u, {})

    def test_term_no_match_ground(self):
        t1 = Term('actor', subterms=[Term('alice')])
        p1 = Term('actor', subterms=[Term('bob')])
        u = {}
        with self.assertRaises(ValueError):
            p1.match(t1, u)
        self.assertEqual(u, {})

    def test_term_match_bind_var(self):
        t1 = Term('actor', subterms=[Term('alice')])
        p1 = Term('actor', subterms=[Var('?A')])
        u = {}
        p1.match(t1, u)
        self.assertEqual(u, {u'?A': Term('alice')})

    def test_term_match_already_bound_var(self):
        t1 = Term('actor', subterms=[Term('alice')])
        p1 = Term('actor', subterms=[Var('?A')])
        u = {u'?A': Term('alice')}
        p1.match(t1, u)
        self.assertEqual(u, {u'?A': Term('alice')})

    def test_term_no_match_already_bound_var(self):
        t1 = Term('actor', subterms=[Term('alice')])
        p1 = Term('actor', subterms=[Var('?A')])
        u = {u'?A': Term('bob')}
        with self.assertRaises(ValueError):
            p1.match(t1, u)
        self.assertEqual(u, {u'?A': Term('bob')})

    def test_term_subst(self):
        t = Term('actor', subterms=[Var('?A')])
        r = t.subst({u'?A': Term('alice')})
        self.assertEqual(r, Term('actor', subterms=[Term('alice')]))


if __name__ == '__main__':
    unittest.main()
