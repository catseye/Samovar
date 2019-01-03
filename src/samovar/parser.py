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
# Cond          ::= "[" Expr {"," Expr} ["where" {Var "=" Term [","]}"]".
# Expr          ::= Term | NotSym Term.
# Term          ::= Var | Atom ["(" Term {AndSym Term} ")"].
# Var           ::= Qmark | Greek.
# Qmark         ::= '?' Atom.
# Greek         ::= <<one of: αβγδεζθικλμνξοπρστυφχψω>>.
# Atom          ::= <<A-Za-z_>> <<A-Za-z0-9_-'>>*.
# Punct         ::= <<"',.;:?!>>.
# NotSym        ::= '~' | '¬'.
# AndSym        ::= ',' | '∧'.


class SamovarSyntaxError(ValueError):
    pass


def variables_in_cond(cond):
    vars_ = set()
    for expr in cond.exprs:
        expr.term.collect_variables(vars_)
    return vars_


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

        if post.bindings:
            raise SamovarSyntaxError("Consequences of a rule cannot include a `where` clause")

        pre_variables = variables_in_cond(pre)

        words_variables = set(w for w in words if isinstance(w, Var))
        if '?_' in [w.name for w in words_variables]:
            raise SamovarSyntaxError("Text contains wildcard")
        extra_vars_in_words = words_variables - pre_variables
        if extra_vars_in_words:
            extra_vars = ', '.join([str(v) for v in sorted(extra_vars_in_words)])
            raise SamovarSyntaxError("Text contains unbound variables: {}".format(extra_vars))

        post_variables = variables_in_cond(post)
        if '?_' in [w.name for w in post_variables]:
            raise SamovarSyntaxError("Consequences contains wildcard")
        extra_vars_in_post = post_variables - pre_variables
        if extra_vars_in_post:
            extra_vars = ', '.join([str(v) for v in sorted(extra_vars_in_words)])
            raise SamovarSyntaxError("Consequences contains unbound variables: {}".format(extra_vars))

        return Rule(pre=pre, words=words, post=post)

    def cond(self):
        exprs = []
        bindings = {}
        self.scanner.expect('[')
        if not self.scanner.on(']') and not self.scanner.on('where'):
            exprs.append(self.expr())
            while self.scanner.consume(',', u'∧'):
                exprs.append(self.expr())
        if self.scanner.consume('where'):
            while not self.scanner.on(']'):
                v = self.var()
                self.scanner.expect('=')
                t = self.term()
                bindings[v.name] = t
                self.scanner.consume(',', u'∧')
        self.scanner.expect(']')
        return Cond(exprs=exprs, bindings=bindings)

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
