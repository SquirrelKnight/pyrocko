import sys

if sys.version_info < (2,6) or (3,0) <= sys.version_info:
    sys.exit('This version of Pyrocko requires Python version >=2.6 and <3.0')

import numpy
from distutils.core import setup, Extension
import os, time
from os.path import join as pjoin


class NotInAGitRepos(Exception):
    pass

def git_infos():
    '''Query git about sha1 of last commit and check if there are local modifications.'''

    from subprocess import Popen, PIPE
    import re
    def q(c):
        return Popen(c, stdout=PIPE).communicate()[0]
    
    if not os.path.exists('.git'):
        raise NotInAGitRepos()

    sha1 = q(['git', 'log', '--pretty=oneline', '-n1']).split()[0]
    sha1 = re.sub('[^0-9a-f]', '', sha1)
    sstatus = q(['git', 'status'])
    local_modifications = bool(re.search(r'^#\s+modified:', sstatus, flags=re.M))
    return sha1, local_modifications

def make_info_module(packname, version):
    '''Put version and revision information into file pyrocko/info.py.'''

    sha1, local_modifications = None, None
    combi = '%s-%s' % (packname, version)
    try:
        sha1 , local_modifications = git_infos()
        combi += '-%s' % sha1
        if local_modifications:
            combi += '-modified'

    except (OSError, NotInAGitRepos):
        pass
   
    datestr = time.strftime('%Y-%m-%d_%H:%M:%S')
    combi += '-%s' % datestr

    s = '''# This module is automatically created from setup.py
git_sha1 = %s
local_modifications = %s
version = %s
long_version = %s
installed_date = %s
''' % tuple( [ repr(x) for x in (sha1, local_modifications, version, combi, datestr) ] )
   
    try:
        f = open(pjoin('pyrocko', 'info.py'), 'w')
        f.write(s)
        f.close()
    except:
        pass

def make_prerequisites():
    from subprocess import check_call
    try:
        check_call(['sh', 'prerequisites.sh'])
    except:
        sys.exit('error: failed to build the included prerequisites with "sh prerequisites.sh"')


def double_install_check():
    found = []
    seen = set()
    orig_sys_path = sys.path
    for p in sys.path:

        ap = os.path.abspath(p)
        if ap == os.path.abspath('.'):
            continue

        if ap in seen:
            continue

        seen.add(ap)

        sys.path = [p]

        try:
            import pyrocko
            x = (pyrocko.installed_date, p, pyrocko.__file__, pyrocko.long_version)
            found.append(x)
            del sys.modules['pyrocko']
            del sys.modules['pyrocko.info']
        except:
            pass

    sys.path = orig_sys_path

    e = sys.stderr

    initpyc = '__init__.pyc'
    i = 1

    dates = sorted([x[0] for x in found])
    
    if len(found) > 1:
        print >>e, 'sys.path configuration is: \n  %s' % '\n  '.join(sys.path)
        print >>e

        for (installed_date, p, fpath, long_version) in found:
            oldnew = ''
            if len(dates) >= 2:
                if installed_date == dates[0]:
                    oldnew = ' (oldest)'

                if installed_date == dates[-1]:
                    oldnew = ' (newest)'
            
            if fpath.endswith(initpyc):
                fpath = fpath[:-len(initpyc)]

            print >>e, 'Pyrocko installation #%i:' % i 
            print >>e, '  date installed: %s%s' % (installed_date, oldnew)
            print >>e, '  path: %s' % fpath
            print >>e, '  version: %s' % long_version
            print >>e
            i += 1

    if len(found) > 1:
        print >>e, 'Installation #1 is used with default sys.path configuration.'
        print >>e
        print >>e, 'WARNING: Multiple installations of Pyrocko are present on this system.'
        if found[0][0] != dates[-1]:
            print >>e, 'WARNING: Not using newest installed version.'


packname = 'pyrocko' 
version = '0.3'

subpacknames = [ 'pyrocko.snufflings', 'pyrocko.gf', 'pyrocko.fomosto', 'pyrocko.fdsn' ]

from distutils.cmd import Command
class HeadlessCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

class make_prerequisites_cls(HeadlessCommand):
    def run(self):
        make_prerequisites()

class make_info_module_cls(HeadlessCommand):
    def run(self):
        make_info_module(packname, version)

class double_install_check_cls(HeadlessCommand):
    def run(self):
        double_install_check()

from distutils.command import install, build
build.build.sub_commands[0:0] = [
    ('make_info_module', None),
    ('make_prerequisites', None),
]

install.install.sub_commands.extend([
    ('double_install_check', None),
])

setup(
    cmdclass = {
        'make_info_module': make_info_module_cls,
        'make_prerequisites': make_prerequisites_cls,
        'double_install_check': double_install_check_cls},

    name = packname,
    version = version,
    description = 'Seismological Processing Unit',
    author = 'Sebastian Heimann',
    author_email = 'sebastian.heimann@zmaw.de',
    url = 'http://emolch.github.com/pyrocko/',
    packages = [ packname ] + subpacknames,
    ext_package = packname,
    ext_modules = [ 
        Extension( 'util_ext',
            sources = [ pjoin(packname, 'util_ext.c') ]),
        
        Extension( 'mseed_ext',
            include_dirs = [ numpy.get_include(), 'libmseed' ],
            library_dirs = ['libmseed'],
            libraries = ['mseed'],
            sources = [ pjoin(packname, 'mseed_ext.c') ]),
                
        Extension( 'evalresp_ext',
            include_dirs = [ numpy.get_include(), 'evalresp-3.3.0/include' ],
            library_dirs = [ 'evalresp-3.3.0/lib' ],
            libraries = ['evresp'],
            sources = [ pjoin(packname, 'evalresp_ext.c') ]),
            
        Extension( 'gse2_ext',
            include_dirs = [ numpy.get_include() ],
            sources = [ pjoin(packname, 'gse2_ext.c') ]),

        Extension( 'autopick_ext',
            include_dirs = [ numpy.get_include() ],
            sources = [ pjoin(packname, 'autopick_ext.c') ]),

        Extension( 'gf.store_ext',
            include_dirs = [ numpy.get_include() ],
            extra_compile_args = [ '-D_FILE_OFFSET_BITS=64', '-Wextra' ],
            sources = [ pjoin(packname, 'gf', 'store_ext.c') ]),
    ],
                
    scripts = [ 'apps/snuffler', 'apps/hamster', 'apps/cake', 'apps/fomosto', 
                'apps/jackseis' ],

    package_data = { packname: ['data/*.png', 'data/*.html', 'data/earthmodels/*.nd'] },
)

