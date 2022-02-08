# http://pyrocko.org - GPLv3
#
# The Pyrocko Developers, 21st Century
# ---|P------/S----------~Lg----------

from __future__ import absolute_import, print_function

from .. import common


def setup_subcommand(subparsers):
    return common.add_parser(
        subparsers, 'scan',
        help='Scan and index files and directories.',
        description='''Scan and index given files and directories.

Read and cache meta-data of all files in formats understood by Squirrel under
selected paths. Subdirectories are recursively traversed and file formats are
auto-detected unless a specific format is forced with the --format option.
Modification times of files already known to Squirrel are checked by default
and re-indexed as needed. To speed up scanning, these checks can be disabled
with the --optimistic option. With this option, only new files are indexed
during scanning and modifications are handled "last minute" (i.e. just before
the actual data (e.g. waveform samples) are requested by the application).

Usually, the contents of files given to Squirrel are made available within the
application through a runtime selection which is discarded again when the
application quits. Getting the cached meta-data into the runtime selection can
be a bottleneck for application startup with large datasets. To speed up
startup of Squirrel-based applications, persistent selections created with the
--persistent option can be used.

After scanning, information about the current data selection is printed.
''')


def setup(parser):
    common.add_selection_arguments(parser)


def call(parser, args):
    squirrel = common.squirrel_from_selection_arguments(args)
    print(squirrel)
