from argparse import ArgumentParser
import codecs
import json
import sys

from samovar.parser import Parser
from samovar.generator import Generator
from samovar.randomness import CannedRandomness


def main(args):
    argparser = ArgumentParser()

    argparser.add_argument('input_files', nargs='+', metavar='FILENAME', type=str,
        help='Source files containing the scenario descriptions'
    )
    argparser.add_argument("--debug", action="store_true",
        help="Show state before and after each move"
    )
    argparser.add_argument("--verbose", action="store_true",
        help="Show some progress information"
    )
    argparser.add_argument("--dump-ast",
                         action="store_true",
                         help="Just show the AST and stop")
    argparser.add_argument("--generate-scenarios",
                         type=str, default=None,
                         help="If given, generate only these scenarios")
    argparser.add_argument("--lengthen-factor",
                         type=float, default=2.0,
                         help="When scenario goal was not met, multiply number of events to generate by this")
    argparser.add_argument("--min-events",
                         type=int, default=1,
                         help="Generate at least this many events for each scenario")
    argparser.add_argument("--max-events",
                         type=int, default=1000000,
                         help="Assume something's gone wrong if more than this many events are generated")
    argparser.add_argument("--output-type",
                         choices=('naive-text', 'events-json', 'scenarios-json',),
                         default='naive-text',
                         help="Specify what to output and in what format")
    argparser.add_argument("--randomness-type",
                         choices=('python', 'canned',),
                         default='python',
                         help="Specify what provides random values to the generator")
    argparser.add_argument("--seed",
                         type=int, default=None,
                         help="Set random seed (to select moves deterministically, when randomness-type=python)")

    options = argparser.parse_args(args)

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
        if options.verbose:
            sys.stderr.write("{}. {}\n".format(n, scenario.name))
        if scenario.goal is None:
            continue
        if options.generate_scenarios is not None and scenario.name not in options.generate_scenarios:
            continue
        g = Generator(randomness, ast, scenario, debug=options.debug, verbose=options.verbose)
        events = g.generate_events(options.min_events, options.max_events, options.lengthen_factor)
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