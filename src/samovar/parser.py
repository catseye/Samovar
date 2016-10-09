# encoding: UTF-8

from samovar.ast import World, Rule, Cond, Situation, Assert, Retract
from samovar.terms import Term, Var
from samovar.scanner import Scanner


# World         ::= {Rules | Situations}.
# Rules         ::= "rules" {Rule} "end".
# Situations    ::= "situations" {Situation} "end".
# Rule          ::= Cond {Term | Punct} Cond.
# Cond          ::= "[" Expr {"," Expr} "]".
# Scene         ::= Cond.
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
                rules.extend(self.rules())
            if self.scanner.on('situations'):
                situations.extend(self.situations())
        return World(rules=rules, situations=situations)

    def rules(self):
        rules = []
        self.scanner.expect('rules')
        while not self.scanner.on('end'):
            rules.append(self.rule())
        self.scanner.expect('end')
        return rules

    def situations(self):
        situations = []
        self.scanner.expect('situations')
        while not self.scanner.on('end'):
            situations.append(self.situation())
        self.scanner.expect('end')
        return situations

    def rule(self):
        terms = []
        pre = self.cond()
        while not self.scanner.on('['):
            terms.append(self.term())
        post = self.cond()
        return Rule(pre=pre, terms=terms, post=post)

    def cond(self):
        exprs = []
        self.scanner.expect('[')
        if not self.scanner.on(']'):
            exprs.append(self.expr())
            while self.scanner.consume(','):        
                exprs.append(self.expr())
        self.scanner.expect(']')
        return Cond(exprs=exprs)

    def situation(self):
        cond = self.cond()
        return Situation(cond=cond)

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
