
from __future__ import absolute_import, division, print_function

from . import registerParser
from .platform import platformParser

@registerParser('watchdog', parent=platformParser,
                help='configure the hardware watchdog')
def watchdogParser(parser):
   parser = parser.add_mutually_exclusive_group(required=True)
   parser.add_argument('--status', action='store_true', dest='watchdog_status',
      help='print the hardware watchdog status')
   parser.add_argument('--stop', action='store_true', dest='watchdog_stop',
      help='stop the hardware watchdog')
   parser.add_argument('--arm', type=int, nargs='?', const=300, dest='watchdog_timeout',
      help='arm the hardware watchdog for X seconds before it triggers')
