# encoding: UTF-8

from samovar.ast import World, Rule, Situation, Cond, Assert, Retract
from samovar.terms import Term, Var
from samovar.scanner import Scanner


# World         ::= {Rules | Situations}.
# Rules         ::= "rules" {Rule} "end".
# Situations    ::= "situations" {Situation} "end".
# Rule          ::= Cond {Term | Punct} Cond.
# Situation     ::= Cond.
# Cond          ::= "[" Expr {"," Expr} "]".
# Expr          ::= Term | "~" Term.
# Term          ::= Var | Word ["(" Term {"," Term} ")"].
# Var           ::= <<one of: αβγδεζθικλμνξοπρστυφχψω>>
# Atom          ::= <<A-Za-z possibly with punctuation on either end>>


class Parser(object):
    def __init__(self, text):
        self.scanner = Scanner(text)

    def world(self):
        rules = []
        situations = []
        while self.scanner.on('rules', 'situations'):
            if self.scanner.on('rules'):
                rules.extend(self._section('rules', self.rule))
            if self.scanner.on('situations'):
                situations.extend(self._section('situations', self.situation))
        return World(rules=rules, situations=situations)

    def _section(self, heading, method):
        items = []
        self.scanner.expect(heading)
        while not self.scanner.on('end'):
            items.append(method())
        self.scanner.expect('end')
        return items

    def rule(self):
        terms = []
        pre = self.cond()
        while not self.scanner.on('['):
            terms.append(self.term())
        post = self.cond()
        return Rule(pre=pre, terms=terms, post=post)

    def situation(self):
        cond = self.cond()
        return Situation(cond=cond)

    def cond(self):
        exprs = []
        self.scanner.expect('[')
        if not self.scanner.on(']'):
            exprs.append(self.expr())
            while self.scanner.consume(','):        
                exprs.append(self.expr())
        self.scanner.expect(']')
        return Cond(exprs=exprs)

    def expr(self):
        if self.scanner.consume('~'):
            return Retract(term=self.term())
        else:
            return Assert(term=self.term())

    def term(self):
        if self.scanner.on_type('variable'):
            return self.var()
        self.scanner.check_type('word', 'punct')
        constructor = self.scanner.token
        self.scanner.scan()
        subterms = []
        if self.scanner.consume('('):
            subterms.append(self.term())
            while self.scanner.consume(','):
                subterms.append(self.term())
            self.scanner.expect(')')
        return Term(constructor, subterms=subterms)

    def var(self):
        self.scanner.check_type('variable')
        name = self.scanner.token
        self.scanner.scan()
        return Var(name)
