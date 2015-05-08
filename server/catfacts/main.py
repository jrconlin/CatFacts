# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import configargparse
import sys

import cyclone.web
from twisted.internet import reactor
from twisted.python import log

from catfacts.endpoint import (EndpointHandler)
from catfacts.annoy import (Annoy)

# This is the list of configuration file locations. They're included
# in order specified, with later overriding earlier values.
config_files = [
    './catfacts.ini',
]


def _parse_args(sysargs):
    if sysargs is None:
        sysargs = sys.argv[1:]

    parser = configargparse.ArgumentParser(
        description='Behold the kitty cannon, the cat fact distributor.',
        default_config_files=config_files,
    )
    # Here are the various arguments that we'll use.
    parser.add_argument(
        '-p', '--port',
        help='Public HTTP Endpoint port',
        type=int,
        default=8082,
        env_var="PORT",
    )
    parser.add_argument(
        '--host',
        help='Public HTTP Host address',
        type=str,
        default="localhost",
        env_var="HOSTNAME",
    )
    parser.add_argument(
        '--database',
        help='Path to database file',
        type=str,
        default='./catfacts.db',
        env_var='DATABASE',
    )
    parser.add_argument(
        '-d', '--debug',
        help='Show debug messages',
        type=bool,
        default=False,
        env_var="DEBUG",
    )

    parser.add_argument(
        '--period',
        help='Seconds between cat fact',
        type=int,
        default=10,
        env_var="PERIOD",
    )

    # Parser returns an object with attributes set to the various
    # config values.
    args = parser.parse_args(sysargs)
    return args, parser


def main():
    args, parser = _parse_args(sys.argv[1:])

    end = EndpointHandler
    # Add the log attribute
    setattr(end, 'log', log)
    setattr(args, 'log', log)
    annoy = Annoy(args)
    log.startLogging(sys.stdout)

    # Add the storage
    end.ap_settings = args

    site = cyclone.web.Application([
        (r"/(.*)", end),
    ],
        default_host=args.host,
        debug=args.debug,
    )

    log.msg("Starting on %s" % args.port)
    reactor.listenTCP(args.port, site)
    reactor.suggestThreadPoolSize(50)
    reactor.callLater(args.period, annoy.bother)
    reactor.run()
