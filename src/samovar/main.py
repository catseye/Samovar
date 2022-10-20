from argparse import ArgumentParser
import codecs
import json
import sys

from samovar.parser import Parser
from samovar.generators.stochastic import StochasticGenerator
from samovar.generators.complete import CompleteGenerator
from samovar.randomness import CannedRandomness


def main(args):
    argparser = ArgumentParser()

    argparser.add_argument(
        'input_files', nargs='+', metavar='FILENAME', type=str,
        help='Source files containing the scenario descriptions'
    )
    argparser.add_argument(
        "--verbosity", type=int, default=0,
        help="Show some information about the world as generation takes place"
    )
    argparser.add_argument(
        "--verbose", action="store_true",
        help="Show some progress information (alias for --verbosity=1)"
    )
    argparser.add_argument(
        "--debug", action="store_true",
        help="Show state before and after each move (alias for --verbosity=2)"
    )
    argparser.add_argument(
        "--dump-ast", action="store_true",
        help="Just show the AST and stop"
    )
    argparser.add_argument(
        "--generator", choices=('stochastic', 'complete',), default='stochastic',
        help="Specify which generator engine to use"
    )
    argparser.add_argument(
        "--generate-scenarios", type=str, default=None,
        help="If given, generate only these scenarios"
    )
    argparser.add_argument(
        "--lengthen-factor", type=float, default=2.0,
        help="When scenario goal was not met, multiply number of events to generate by this"
    )
    argparser.add_argument(
        "--min-events", type=int, default=1,
        help="Generate at least this many events for each scenario"
    )
    argparser.add_argument(
        "--max-events", type=int, default=1000000,
        help="Conclude that something has gone wrong and abort if more than this many events are generated"
    )
    argparser.add_argument(
        "--output-type", choices=('naive-text', 'events-json', 'scenarios-json',), default='naive-text',
        help="Specify what to output and in what format"
    )
    argparser.add_argument(
        "--randomness-type", choices=('python', 'canned',), default='python',
        help="Specify what provides random values to the generator"
    )
    argparser.add_argument(
        "--unsorted-search", action="store_true",
        help="Turn off sorting the database before searching it, to improve performance at "
             "the cost of having less deterministic behaviour"
    )
    argparser.add_argument(
        "--seed", type=int, default=None,
        help="Set random seed (to select moves deterministically, when randomness-type=python)"
    )
    argparser.add_argument('--version', action='version', version="%(prog)s 0.5")

    options = argparser.parse_args(args)

    verbosity = options.verbosity
    if options.verbose:
        verbosity = max(verbosity, 1)
    if options.debug:
        verbosity = max(verbosity, 2)

    generator_cls = {
        'stochastic': StochasticGenerator,
        'complete': CompleteGenerator,
    }[options.generator]

    text = ''
    for arg in options.input_files:
        with codecs.open(arg, 'r', encoding='UTF-8') as f:
            text += f.read()

    p = Parser(text)
    ast = p.world()
    if options.dump_ast:
        print(ast)
        sys.exit(0)

    if options.randomness_type == 'python':
        import random
        if options.seed is not None:
            random.seed(options.seed)
        randomness = random
    elif options.randomness_type == 'canned':
        randomness = CannedRandomness()
    else:
        raise NotImplementedError('Not a valid randomness-type: {}'.format(options.randomness_type))

    event_buckets = []
    for n, scenario in enumerate(ast.scenarios):
        if verbosity >= 1:
            sys.stderr.write("{}. {}\n".format(n, scenario.name))
        if scenario.goal is None:
            continue
        if options.generate_scenarios is not None and scenario.name not in options.generate_scenarios:
            continue
        g = generator_cls(
            ast, scenario,
            verbosity=verbosity, sorted_search=(not options.unsorted_search), randomness=randomness
        )
        events = g.generate_events(
            min_count=options.min_events, max_count=options.max_events, lengthen_factor=options.lengthen_factor
        )
        event_buckets.append(events)

    if options.output_type == 'naive-text':
        for b in event_buckets:
            for e in b:
                sys.stdout.write("%s\n" % e)
            sys.stdout.write("\n")
    elif options.output_type == 'events-json':
        def jsonify_bucket(b):
            return [e.to_json() for e in b]
        jsonified_buckets = [jsonify_bucket(b) for b in event_buckets]
        sys.stdout.write(json.dumps(jsonified_buckets, indent=4, sort_keys=True))
    elif options.output_type == 'scenarios-json':
        raise NotImplementedError("'scenarios-json' output-type not currently implemented")
    else:
        raise NotImplementedError('Not a valid output-type: {}'.format(options.output_type))
