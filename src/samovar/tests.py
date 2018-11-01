import unittest
from unittest import TestCase

from samovar.terms import Term, Var
from samovar.query import match_all


def t(s, *args):
    if s.startswith('?'):
        return Var(s)
    else:
        return Term(s, *args)


class TermTestCase(TestCase):
    def test_term_basic_properties(self):
        t1 = Term('alice')
        t2 = Term('actor', t1)
        v1 = Var('?A')
        t3 = Term('actor', v1)

        self.assertTrue(t1.is_atom())
        self.assertFalse(t2.is_atom())
        self.assertFalse(v1.is_atom())
        self.assertFalse(t3.is_atom())

        self.assertTrue(t1.is_ground())
        self.assertTrue(t2.is_ground())
        self.assertFalse(v1.is_ground())
        self.assertFalse(t3.is_ground())

        self.assertEqual(t2, Term('actor', Term('alice')))

    def test_term_match_ground(self):
        t1 = Term('actor', Term('alice'))
        p1 = Term('actor', Term('alice'))
        u = p1.match(t1, {})
        self.assertEqual(u, {})

    def test_term_no_match_ground(self):
        t1 = Term('actor', Term('alice'))
        p1 = Term('actor', Term('bob'))
        with self.assertRaises(ValueError):
            p1.match(t1, {})

    def test_term_match_bind_var(self):
        t1 = Term('actor', Term('alice'))
        p1 = Term('actor', Var('?A'))
        e = {}
        u = p1.match(t1, e)
        self.assertEqual(u, {u'?A': Term('alice')})
        self.assertEqual(e, {})

    def test_term_match_already_bound_var(self):
        t1 = Term('actor', Term('alice'))
        p1 = Term('actor', Var('?A'))
        u = p1.match(t1, {u'?A': Term('alice')})
        self.assertEqual(u, {u'?A': Term('alice')})

    def test_term_no_match_already_bound_var(self):
        t1 = Term('actor', Term('alice'))
        p1 = Term('actor', Var('?A'))
        u = {u'?A': Term('bob')}
        with self.assertRaises(ValueError):
            p1.match(t1, u)
        self.assertEqual(u, {u'?A': Term('bob')})

    def test_term_subst(self):
        t = Term('actor', Var('?A'))
        r = t.subst({u'?A': Term('alice')})
        self.assertEqual(r, Term('actor', Term('alice')))


DATABASE = [
    t('actor', t('alice')),
    t('actor', t('bob')),

    t('drink', t('gin')),

    t('weapon', t('revolver')),
    t('weapon', t('knife')),
    t('weapon', t('club')),

    t('holding', t('bob'), t('revolver')),
    t('holding', t('alice'), t('gin')),
    t('holding', t('alice'), t('knife')),
]


class TestMatchAll(unittest.TestCase):

    def assertMatchAll(self, query, result):
        self.assertEqual(match_all(DATABASE, query, {}), result)

    def test_match_all(self):
        # Find all actors who are Cody.  Since there is no such actor, this will return no matches.
        self.assertMatchAll(
            [t('actor', t('cody'))],
            []
        )
        # Find all actor who are Alice.  This will return one match, but no bindings.
        self.assertMatchAll(
            [t('actor', t('alice'))],
            [{}]
        )
        # Find all drinks.  This will return one match, with ?D bound to the result.
        self.assertMatchAll(
            [t("drink", t("?D"))],
            [{'?D': Term('gin')}]               # there was a match, in which ?D was bound
        )
        # Find all actors.
        self.assertMatchAll(
            [t('actor', t('?C'))],
            [{'?C': Term('alice')}, {'?C': Term('bob')}]
        )
        # Find all actors who are holding the revolver.
        self.assertMatchAll(
            [t('actor', t('?C')), t('holding', t('?C'), t('revolver'))],
            [{'?C': t('bob')}]
        )
        # Find all actors who are holding a weapon.
        self.assertMatchAll(
            [t('actor', t('?C')), t('weapon', t('?W')), t('holding', t('?C'), t('?W'))],
            [{'?W': t('knife'), '?C': t('alice')}, {'?W': t('revolver'), '?C': t('bob')}]
        )


if __name__ == '__main__':
    unittest.main()
