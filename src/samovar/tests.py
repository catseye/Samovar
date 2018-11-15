import unittest
from unittest import TestCase

from samovar.ast import Assert, Retract, join_sentence_parts
from samovar.terms import Term, Var
from samovar.query import match_all


def t(s, *args):
    if s.startswith('?'):
        return Var(s)
    else:
        return Term(s, *args)


def a(t):
    return Assert(term=t)


def r(t):
    return Retract(term=t)


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


class RenderTestCase(TestCase):
    def test_join_sentence_parts_1(self):
        self.assertEqual(
            join_sentence_parts(['"', "Hello", ",", '"', "said", "the", "mouse", "."]),
            '"Hello," said the mouse.'
        )

    def test_join_sentence_parts_2(self):
        self.assertEqual(
            join_sentence_parts(["The", "mouse", "asked", ",", '"', "What", "is", "it", "?", '"']),
            'The mouse asked, "What is it?"'
        )

    def test_join_sentence_parts_3(self):
        self.assertEqual(
            join_sentence_parts(["It", "was", "very", ",", "very", "dark", '.']),
            'It was very, very dark.'
        )


class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        self.database = [
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


class TestMatchAll(DatabaseTestCase):

    def assertMatchAll(self, query, result):
        self.assertEqual(match_all(self.database, query, {}), result)

    def test_match_all(self):
        # Find all actors who are Cody.  Since there is no such actor, this will return no matches.
        self.assertMatchAll(
            [a(t('actor', t('cody')))],
            []
        )
        # Find all actors who are Alice.  This will return one match, but no bindings.
        self.assertMatchAll(
            [a(t('actor', t('alice')))],
            [{}]
        )
        # Find all drinks.  This will return one match, with ?D bound to the result.
        self.assertMatchAll(
            [a(t("drink", t("?D")))],
            [{'?D': Term('gin')}]               # there was a match, in which ?D was bound
        )
        # Find all actors.
        self.assertMatchAll(
            [a(t('actor', t('?C')))],
            [{'?C': Term('alice')}, {'?C': Term('bob')}]
        )
        # Find all actors who are holding the revolver.
        self.assertMatchAll(
            [a(t('actor', t('?C'))), a(t('holding', t('?C'), t('revolver')))],
            [{'?C': t('bob')}]
        )
        # Find all actors who are holding a weapon.
        self.assertMatchAll(
            [a(t('actor', t('?C'))), a(t('weapon', t('?W'))), a(t('holding', t('?C'), t('?W')))],
            [{'?W': t('knife'), '?C': t('alice')}, {'?W': t('revolver'), '?C': t('bob')}]
        )

    def test_match_all_with_unique_binding(self):
        # Find all pairs of actors.  Because the actors must be different, there are only 2 matches.
        self.assertMatchAll(
            [a(t('actor', t('?A'))), a(t('actor', t('?B')))],
            [{'?A': Term('alice'), '?B': Term('bob')}, {'?A': Term('bob'), '?B': Term('alice')}]
        )
        # Find all pairs of drinks.  Since there is only one, and we can't return (gin,gin),
        # there will be no matches.
        self.assertMatchAll(
            [a(t('drink', t('?A'))), a(t('drink', t('?B')))],
            []
        )

    def test_match_all_with_negation(self):
        # Find all actors who are not holding the revolver.
        self.assertMatchAll(
            [a(t('actor', t('?C'))), r(t('holding', t('?C'), t('revolver')))],
            [{'?C': t('alice')}]
        )
        # Find all actors who are not holding a weapon.  Or rather, all pairs
        # of (actor, weapon) where the actor is not holding that weapon.
        self.assertMatchAll(
            [a(t('actor', t('?C'))), a(t('weapon', t('?W'))), r(t('holding', t('?C'), t('?W')))],
            [
                {'?W': t('revolver'), '?C': t('alice')},
                {'?W': t('club'), '?C': t('alice')},
                {'?W': t('knife'), '?C': t('bob')},
                {'?W': t('club'), '?C': t('bob')},
            ]
        )
        # Note that we can't say "Find all actors who aren't Alice".
        # We can say this:
        self.assertMatchAll(
            [a(t('actor', t('?C'))), r(t('actor', t('alice')))],
            []
        )
        # ... but what this is saying is "Find all actors if Alice doesn't exist."

        # For a one-off case, we can do something like this:
        self.database.append(t('is_alice', t('alice')))
        self.assertMatchAll(
            [a(t('actor', t('?C'))), r(t('is_alice', t('?C')))],
            [{'?C': t('bob')}]
        )

        # For the general case, we'll need to think about equality tests.

        # Note also that we can't search on negative clauses with free variables:
        with self.assertRaises(KeyError):
            match_all(self.database, [a(t('actor', t('?C'))), r(t('weapon', t('?W')))], {})


if __name__ == '__main__':
    unittest.main()
