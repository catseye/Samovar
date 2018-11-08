# encoding: UTF-8

from samovar.ast import World, Scenario, Rule, Cond, Assert, Retract
from samovar.terms import Term, Var
from samovar.scanner import Scanner


# World         ::= {Scenario}.
# Scenario      ::= "scenario" Atom "{" {Import | Proposition | Rule | Goal} ["." | ","] "}".
# Import        ::= "import" Atom.
# Goal          ::= "goal" Cond.
# Proposition   ::= Term.
# Rule          ::= Cond {Var | Atom | Punct} Cond.
# Cond          ::= "[" Expr {"," Expr} "]".
# Expr          ::= Term | NotSym Term.
# Term          ::= Var | Atom ["(" Term {AndSym Term} ")"].
# Var           ::= Qmark | Greek.
# Qmark         ::= '?' Atom.
# Greek         ::= <<one of: αβγδεζθικλμνξοπρστυφχψω>>.
# Atom          ::= <<A-Za-z_>> <<A-Za-z0-9_-'>>*.
# Punct         ::= <<"',.;:?!>>.
# NotSym        ::= '~' | '¬'.
# AndSym        ::= ',' | '∧'.


class Parser(object):
    def __init__(self, text):
        self.scanner = Scanner(text)
        self.scenario_map = {}

    def world(self):
        scenarios = []
        while self.scanner.on('scenario'):
            scenario = self.scenario()
            self.scenario_map[scenario.name] = scenario
            scenarios.append(scenario)
        return World(scenarios=scenarios)

    def scenario(self):
        propositions = []
        rules = []
        goal = None
        self.scanner.expect('scenario')
        self.scanner.check_type('word')
        name = self.scanner.token
        self.scanner.scan()
        self.scanner.expect('{')
        while not self.scanner.on('}'):
            if self.scanner.consume('import'):
                self.scanner.check_type('word')
                from_name = self.scanner.token
                self.scanner.scan()
                from_scenario = self.scenario_map[from_name]
                rules.extend(from_scenario.rules)
                propositions.extend(from_scenario.propositions)
            elif self.scanner.consume('goal'):
                assert goal is None
                goal = self.cond()
            elif self.scanner.on('['):
                rules.append(self.rule())
            else:
                propositions.append(self.proposition())
            self.scanner.consume('.')
            self.scanner.consume(',')
        self.scanner.expect('}')
        return Scenario(name=name, propositions=propositions, rules=rules, goal=goal)

    def proposition(self):
        return self.term()

    def rule(self):
        words = []
        pre = self.cond()
        while not self.scanner.on('['):
            words.append(self.word())
        post = self.cond()
        return Rule(pre=pre, words=words, post=post)

    def cond(self):
        exprs = []
        self.scanner.expect('[')
        if not self.scanner.on(']'):
            exprs.append(self.expr())
            while self.scanner.consume(',', u'∧'):
                exprs.append(self.expr())
        self.scanner.expect(']')
        return Cond(exprs=exprs)

    def expr(self):
        if self.scanner.consume('~', u'¬', '!'):
            return Retract(term=self.term())
        else:
            return Assert(term=self.term())

    def term(self):
        if self.scanner.on_type('variable'):
            return self.var()
        self.scanner.check_type('word')
        constructor = self.scanner.token
        self.scanner.scan()
        subterms = []
        if self.scanner.consume('('):
            subterms.append(self.term())
            while self.scanner.consume(','):
                subterms.append(self.term())
            self.scanner.expect(')')
        return Term(constructor, *subterms)

    def word(self):
        if self.scanner.on_type('variable'):
            return self.var()
        self.scanner.check_type('word', 'punct', 'operator')
        constructor = self.scanner.token
        self.scanner.scan()
        return Term(constructor)

    def var(self):
        self.scanner.check_type('variable')
        name = self.scanner.token
        self.scanner.scan()
        v = Var(name)
        return v
