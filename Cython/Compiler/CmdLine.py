#
#   Copyright 2011 Stefano Sanfilippo <satufk on GitHub>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

'''Cython - Command Line Parsing'''

from Cython import __version__ as version
import Options

menu = {
    'default' : {
        ('-V', '--version') : {
            'dest' : 'show_version', 'action' : 'version',
            'version' : 'Cython version %s' % version,
            'help' : 'Display version number of cython compiler'},
        ('sources') : {
            'nargs' : '+', 'metavar' : 'sourcefile.{py,pyx}',
            'help' : 'Source file(s) to be compiled.' }},
    'environment setup': {
        ('-l', '--create-listing') : {
            'dest' : 'use_listing_file', 'const' : 1, 'action' : 'store_const',
            'help' : 'Write error messages to a listing file'},
        ('-I', '--include-dir') : {
            'dest' : 'include_path', 'action' : 'append', 'metavar' : '<directory>',
            'help' : '''Search for include files in named <directory>
                        (multiple include directories are allowed).'''},
        ('-o', '--output-file') : {
            'dest' : 'output_file', 'metavar' : '<output file>',
            'help' : 'Specify name of generated C file'},
        ('-w', '--working') : {
            'dest' : 'working_path', 'metavar' : '<directory>',
            'help' : '''Sets the working directory for Cython 
                        (the directory modules are searched from)'''}},
    'compilation' : {
        ('-t', '--timestamps') : {
            'dest' : 'timestamps', 'const' : 1, 'action' : 'store_const',
            'help' : 'Only compile newer source files (implied)'},
        ('-f', '--force') : {
            'dest' : 'timestamps', 'const' : 0, 'action' : 'store_const',
            'help' : 'Compile all source files (overrides -t)'},
        ('-z', '--pre-import') : {
            'dest' : 'pre_import', 'metavar' : '<module>',
            'help' : 'Import <module> before compilation.' },
        ('--fast-fail') : {
            'dest' : 'fast_fail', 'action' : 'store_true',
            'help' : 'Abort the compilation on the first error.' },
        ('-Werror', '--warning-errors'): {
            'dest' : 'warning_errors', 'action' : 'store_true',
            'help' : 'Make all warnings into errors.' },
        ('-Wextra', '--warning-extra'): {
            'dest' : 'compiler_directives', 'const' : Options.extra_warnings,
            'action' : 'append_const',
            'help' : 'Enable extra warnings' }},
    'debugging' : {
        ('--cleanup') : {
            'dest' : 'generate_cleanup_code', 'type' : int, 'metavar' : '<level>',
            'help' : '''Release interned objects on python exit, for memory debugging.
                        <level> indicates aggressiveness, default 0 releases nothing.'''},
        ('--gdb') : {
            'dest' : 'gdb_debug', 'action' : 'store_true',
            'help' : 'Output debug information for cygdb'}},
    'Python compatibility options' : {
        ('-2') : {
            'dest' : 'language_level', 'const' : 2, 'action' : 'store_const',
            'help' : 'Compile based on Python-2 syntax and code semantics.'},
        ('-3') : {
            'dest' : 'language_level', 'const' : 3, 'action' : 'store_const',
            'help' : 'Compile based on Python-3 syntax and code semantics.'}},
    'recursive compilation': {
        ('-r', '--recursive') : {
            'dest' : 'recursive', 'const' : 1, 'action' : 'store_const',
            'help' : 'Recursively find and compile dependencies (implies -t)'},
        ('-q', '--quiet') : {
            'dest' : 'quiet', 'const' : 1, 'action' : 'store_const',
            'help' : "Don't print module names in recursive mode" },
        ('-v', '--verbose') : {
            'dest' : 'verbose', 'action' : 'count',
            'help' : 'Be verbose, print file names on multiple compilation' }},
    'code annotation' : {
        ('-a', '--annotate') : {
            'dest' : 'annotate', 'action' : 'store_true',
            'help' : 'Produce a colorized HTML version of the source.' },
        ('--line-directives') : {
            'dest' : 'emit_linenums', 'action' : 'store_true',
            'help' : 'Produce #line directives pointing to the .pyx source' }},
    'code generation' : {
        ('--embed') : {
            'dest' : 'embed', 'const' : 'main', 'nargs' : '?', 'metavar' : '<module>',
            'help' : 'Generate a main() function that embeds the Python interpreter.'},
        ('-+', '--cplus') : {
            'dest' : 'cplus', 'const' : 1, 'action' : 'store_const',
            'help' : 'Output a C++ rather than C file.' },
        ('-p', '--embed-positions') : {
            'dest' : 'embed_pos_in_docstring', 'const' : 1, 'action' : 'store_const',
            'help' : '''If specified, the positions in Cython files of each
                        function definition is embedded in its docstring.''' },
        ('--no-c-in-traceback') : {
            'dest' : 'c_line_in_traceback', 'action' : 'store_false',
            'help' : 'Omit C source code line when printing tracebacks.' },
        ('--convert-range') : {
            'dest' : 'convert_range', 'action' : 'store_true',
            'help' : '''Convert `for x in range():` statements in pure C for(),
                      whenever possibile.''' },
        ('-D', '--no-docstrings') : {
            'dest' : 'docstrings', 'action' : 'store_false',
            'help' : 'Strip docstrings from the compiled module.' },
        ('--disable-function-redefinition') : {
            'dest' : 'disable_function_redefinition', 'action' : 'store_true',
            'help' : 'For legacy code only, needed for some circular imports.' },
        ('--old-style-globals') : {
            'dest' : 'old_style_globals', 'action' : 'store_true',
            'help' : '''Makes globals() give the first non-Cython module
                        globals in the call stack. For SAGE compatibility''' }},
   'internal options' : {
       ('--directive', '-X') : {
           'dest' : 'compiler_directives', 'action' : 'append',
           'metavar' : '<name>=<value>,', 'nargs' : '+',
           'help' : 'Overrides a #pragma compiler directive'},
       ('--debug') : {
            'dest' : 'debug_flags', 'action' : 'append',
            'metavar' : '<flag>', 'nargs' : '+',
            'help' : "Sets Cython's internal debug options"}},
#    'experimental options' : { # MacOS X only
#        ('-C', '--compile') : {
#            'dest' : 'compile', 'action' : 'store_true',
#            'help' : 'Compile generated .c file to .o file' },
#        ('--link') : {
#            'dest' : 'link', 'action' : 'store_true',
#            'help' : '''Link .o file to produce extension module (implies -C)
#                        Additional .o files to link may be supplied when using -X.''' }},
}


epilog = '''\
Cython (http://cython.org) is a compiler for code written
in the Cython language. Cython is based on Pyrex by Greg Ewing.

WARNING: RECURSIVE COMPILATION IS STILL BROKEN
(see http://trac.cython.org/cython_trac/ticket/379).'''

import os

def XXX_assign_variables(options):
    for option in ['embed', 'embed_pos_in_docstring', 'pre_import',
                    'generate_cleanup_code', 'docstrings', 'annotate',
                    'convert_range', 'fast_fail', 'warning_errors',
                    'disable_function_redefinition', 'old_style_globals',
                    'warning_errors', 'disable_function_redefinition',
                    'old_style_globals']:
        setattr(Options, option, getattr(options, option, None))
        try:
            del options.__dict__[option]
        except KeyError:
            pass

def XXX_parse_debug_flags(parser, flags, options):
    for option in flags:
        if option.startswith('--debug'):
            option = option[2:].replace('-', '_')
            import DebugFlags
            if option in dir(DebugFlags):
                setattr(DebugFlags, option, True)
            else:
                parser.error('unknown debug flag: %s' % option)
        elif option.startswith('-X'):
            if option[2:].strip():
                x_args = option[2:]
            else:
                x_args = pop_arg()
            try:
                options.compiler_directives = Options.parse_directive_list(
                    x_args, relaxed_bool=True,
                    current_settings=options.compiler_directives)
            except ValueError, e:
                parser.error('error in compiler directive: %s' % e.args[0])

class BasicParser:
    def refine(self, results):
        options, extra = results
        sources = options.sources
        del options.sources

        if options.gdb_debug:
            options.output_dir = os.curdir
        if not sources:
            self.error('no source file specified.')
        if options.output_file and len(sources) > 1:
            self.error('only one source file allowed when using -o')
        if options.embed and len(sources) > 1:
            self.error('only one source file allowed when using --embed')

        XXX_parse_debug_flags(self, extra, options)
        XXX_assign_variables(options)

        return options, sources


from Main import CompilationOptions, default_options #Cython.Compiler.
import sys

if sys.version_info >= (2, 7):
    import argparse

    class Parser(BasicParser, argparse.ArgumentParser):
        def __init__(self):
            argparse.ArgumentParser.__init__(self, epilog=epilog,
                formatter_class=argparse.RawDescriptionHelpFormatter,
                fromfile_prefix_chars='@')
            newgroup = lambda t: self.add_argument_group(title=t)
            for grouptitle, flaglist in menu.iteritems():
                group = self if grouptitle == 'default' else newgroup(grouptitle)
                for flag, parameters in flaglist.iteritems():
                    if isinstance(flag, str):
                        group.add_argument(flag, **parameters)
                    else:
                        group.add_argument(*flag, **parameters)

        def parse(self, args):
            options = CompilationOptions(default_options)
            results = parser.parse_known_args(args, namespace=options)
            return self.refine(results)

else:
    import optparse

    class Parser(BasicParser, optparse.OptionParser):
        def __init__(self):
            optparse.OptionParser.__init__(self, epilog=epilog,
                version=menu['default'][('-V', '--version')]['version'],
                usage="%prog [options] sourcefile.{pyx,py} ...")
            newgroup = lambda t: optparse.OptionGroup(self, t)
            for grouptitle, flaglist in menu.iteritems():
                group = self if grouptitle == 'default' else newgroup(grouptitle)
                for flag, parameters in flaglist.iteritems():
                    try:
                        if isinstance(flag, str):
                            group.add_option(flag, **parameters)
                        else:
                            group.add_option(*flag, **parameters)
                    except optparse.OptionError:
                        pass

                if group is not self: self.add_option_group(group)

        def parse(self, args):
            options, sources = parser.parse_args(args, values=CompilationOptions)
            options.sources = sources
            options, sources = self.refine((options, sources))
            return CompilationOptions(options), sources


parser = Parser()


def parse_command_line(args):
    return parser.parse(args)


if __name__ == '__main__':
    import sys
    options, sources = parse_command_line(sys.argv[1:])
    print vars(options)
    print Options.embed
    print sources
