from __future__ import absolute_import

import os
import shlex
import sys
import tempfile
import textwrap
import unittest

try:
    from collections import Iterable, Sized  # Py2
except ImportError:
    from collections.abc import Iterable, Sized  # Py3

from io import open

from . import Utils
from .Build import Dependencies
from .CodeWriter import CodeWriter
from .Compiler import Errors, TreePath
from .Compiler.TreeFragment import TreeFragment, strip_common_indent
from .Compiler.Visitor import TreeVisitor, VisitorTransform


class NodeTypeWriter(TreeVisitor):
    def __init__(self):
        super(NodeTypeWriter, self).__init__()
        self._indents = 0
        self.result = []

    def visit_Node(self, node):
        if not self.access_path:
            name = u"(root)"
        else:
            tip = self.access_path[-1]
            if tip[2] is not None:
                name = u"%s[%d]" % tip[1:3]
            else:
                name = tip[1]

        self.result.append(u"  " * self._indents +
                           u"%s: %s" % (name, node.__class__.__name__))
        self._indents += 1
        self.visitchildren(node)
        self._indents -= 1


def treetypes(root):
    """Returns a string representing the tree by class names.
    There's a leading and trailing whitespace so that it can be
    compared by simple string comparison while still making test
    cases look ok."""
    w = NodeTypeWriter()
    w.visit(root)
    return u"\n".join([u""] + w.result + [u""])


class CythonTest(unittest.TestCase):
    longMessage = True  # for consistency between python versions

    def setUp(self):
        self.listing_file = Errors.listing_file
        self.echo_file = Errors.echo_file
        Errors.listing_file = Errors.echo_file = None

    def tearDown(self):
        Errors.listing_file = self.listing_file
        Errors.echo_file = self.echo_file

    def assertLines(self, expected, result):
        "Checks that the given strings or lists of strings are equal line by line"
        if not isinstance(expected, list):
            expected = expected.split(u"\n")
        if not isinstance(result, list):
            result = result.split(u"\n")
        for idx, (expected_line, result_line) in enumerate(zip(expected, result)):
            self.assertEqual(expected_line, result_line,
                             "Line %d:\nExp: %s\nGot: %s" % (idx, expected_line, result_line))
        self.assertEqual(len(expected), len(result),
                         "Unmatched lines. Got:\n%s\nExpected:\n%s" % ("\n".join(expected), u"\n".join(result)))

    def codeToLines(self, tree):
        writer = CodeWriter()
        writer.write(tree)
        return writer.result.lines

    def codeToString(self, tree):
        return "\n".join(self.codeToLines(tree))

    def assertCode(self, expected, result_tree):
        result_lines = self.codeToLines(result_tree)

        expected_lines = strip_common_indent(expected.split("\n"))

        for idx, (line, expected_line) in enumerate(zip(result_lines, expected_lines)):
            self.assertEqual(expected_line, line,
                             "Line %d:\nGot: %s\nExp: %s" % (idx, line, expected_line))
        self.assertEqual(len(result_lines), len(expected_lines),
                         "Unmatched lines. Got:\n%s\nExpected:\n%s" % ("\n".join(result_lines), expected))

    def assertNodeExists(self, path, result_tree):
        self.assertNotEqual(TreePath.find_first(result_tree, path), None,
                            "Path '%s' not found in result tree" % path)

    def fragment(self, code, pxds=None, pipeline=None):
        "Simply create a tree fragment using the name of the test-case in parse errors."
        if pxds is None:
            pxds = {}
        if pipeline is None:
            pipeline = []
        name = self.id()
        if name.startswith("__main__."):
            name = name[len("__main__."):]
        name = name.replace(".", "_")
        return TreeFragment(code, name, pxds, pipeline=pipeline)

    def treetypes(self, root):
        return treetypes(root)

    def should_fail(self, func, exc_type=Exception):
        """Calls "func" and fails if it doesn't raise the right exception
        (any exception by default). Also returns the exception in question.
        """
        try:
            func()
            self.fail("Expected an exception of type %r" % exc_type)
        except exc_type as e:
            self.assertTrue(isinstance(e, exc_type))
            return e

    def should_not_fail(self, func):
        """Calls func and succeeds if and only if no exception is raised
        (i.e. converts exception raising into a failed testcase). Returns
        the return value of func."""
        try:
            return func()
        except Exception as exc:
            self.fail(str(exc))


class TransformTest(CythonTest):
    """
    Utility base class for transform unit tests. It is based around constructing
    test trees (either explicitly or by parsing a Cython code string); running
    the transform, serialize it using a customized Cython serializer (with
    special markup for nodes that cannot be represented in Cython),
    and do a string-comparison line-by-line of the result.

    To create a test case:
     - Call run_pipeline. The pipeline should at least contain the transform you
       are testing; pyx should be either a string (passed to the parser to
       create a post-parse tree) or a node representing input to pipeline.
       The result will be a transformed result.

     - Check that the tree is correct. If wanted, assertCode can be used, which
       takes a code string as expected, and a ModuleNode in result_tree
       (it serializes the ModuleNode to a string and compares line-by-line).

    All code strings are first stripped for whitespace lines and then common
    indentation.

    Plans: One could have a pxd dictionary parameter to run_pipeline.
    """

    def run_pipeline(self, pipeline, pyx, pxds=None):
        if pxds is None:
            pxds = {}
        tree = self.fragment(pyx, pxds).root
        # Run pipeline
        for T in pipeline:
            tree = T(tree)
        return tree


class TreeAssertVisitor(VisitorTransform):
    # actually, a TreeVisitor would be enough, but this needs to run
    # as part of the compiler pipeline

    def visit_CompilerDirectivesNode(self, node):
        directives = node.directives
        if 'test_assert_path_exists' in directives:
            for path in directives['test_assert_path_exists']:
                if TreePath.find_first(node, path) is None:
                    Errors.error(
                        node.pos,
                        "Expected path '%s' not found in result tree" % path)
        if 'test_fail_if_path_exists' in directives:
            for path in directives['test_fail_if_path_exists']:
                if TreePath.find_first(node, path) is not None:
                    Errors.error(
                        node.pos,
                        "Unexpected path '%s' found in result tree" % path)
        self.visitchildren(node)
        return node

    visit_Node = VisitorTransform.recurse_to_children


def unpack_source_tree(tree_file, workdir, cython_root):
    programs = {
        'PYTHON': [sys.executable],
        'CYTHON': [sys.executable, os.path.join(cython_root, 'cython.py')],
        'CYTHONIZE': [sys.executable, os.path.join(cython_root, 'cythonize.py')]
    }

    if workdir is None:
        workdir = tempfile.mkdtemp()
    header, cur_file = [], None
    with open(tree_file, 'rb') as f:
        try:
            for line in f:
                if line[:5] == b'#####':
                    filename = line.strip().strip(b'#').strip().decode('utf8').replace('/', os.path.sep)
                    path = os.path.join(workdir, filename)
                    if not os.path.exists(os.path.dirname(path)):
                        os.makedirs(os.path.dirname(path))
                    if cur_file is not None:
                        to_close, cur_file = cur_file, None
                        to_close.close()
                    cur_file = open(path, 'wb')
                elif cur_file is not None:
                    cur_file.write(line)
                elif line.strip() and not line.lstrip().startswith(b'#'):
                    if line.strip() not in (b'"""', b"'''"):
                        command = shlex.split(line.decode('utf8'))
                        if not command: continue
                        # In Python 3: prog, *args = command
                        prog, args = command[0], command[1:]
                        try:
                            header.append(programs[prog]+args)
                        except KeyError:
                            header.append(command)
        finally:
            if cur_file is not None:
                cur_file.close()
    return workdir, header


def clear_function_and_Dependencies_caches():
    Utils.clear_function_caches()
    Dependencies._dep_tree = None  # discard method caches


def fresh_cythonize(*args, **kwargs):
    """Clear function caches and run cythonize"""
    clear_function_and_Dependencies_caches()
    Dependencies.cythonize(*args, **kwargs)


def touch_file(path):
    """Set the access and modified times of the file
    specified by path as the current time"""

    os.utime(path, None)


def relative_lines(lines, line, start, end, fallback=None):
    """Returns the lines specified by `start` and `end` relative to `line`.

    If `fallback` (Sized Iterable) is specified, it will be used for `line`, `start`, `end`
    applied to `lines` to generate a message for a ValueError
    if the original `line` is not found in `lines`."""

    if fallback:
        if not isinstance(fallback, Sized):
            raise TypeError("'fallback' must be a Sized instance")

        if not isinstance(fallback, Iterable):
            raise TypeError("'fallback' must be an instance of the Iterable")

        if len(fallback) != 3:
            raise ValueError("'fallback' must contain three values"
                             " for 'line', 'start', 'end'")

    try:
        ind = lines.index(line)
        return lines[ind+start: ind+end]
    except ValueError as e:
        if fallback is None:
            raise e

        fallback_lines = map(repr, relative_lines(lines, *fallback))

        raise ValueError(
            "{0!r} was not found, presumably in \n{1}".format(
                line, "\n".join(fallback_lines)))


def relative_lines_from_file(path, line, start, end, fallback=None):
    """Same as `relative_lines`, but uses `path`
    as source for `lines` and returns joined lines."""

    with open(path) as f:
        lines = f.readlines()

    return "".join(relative_lines(lines, line, start, end, fallback=fallback))


def write_file(file_path, content, dedent=False):
    r"""Write some content (text or bytes) to the file
    at `file_path` in utf-8 without translating `'\n'` into `os.linesep`.
    """

    encoding = None
    newline = None
    mode = "w"
    if isinstance(content, bytes):
        mode += "b"
    else:
        # unlike OS X or Linux,
        # Windows defaults to 8-bit character set like windows-1252
        encoding = "utf-8"

        # any '\n' characters written are not translated
        # to the system default line separator, os.linesep
        newline = "\n"

    if dedent:
        content = textwrap.dedent(content)

    with open(file_path, mode=mode, encoding=encoding, newline=newline) as f:
        f.write(content)


def write_newer_file(file_path, newer_than, content, dedent=False):
    r"""
    Write `content` to the file `file_path` in utf-8 without translating `'\n'`
    into `os.linesep` and make sure it is newer than the file `newer_than`.
    """
    write_file(file_path, content, dedent=dedent)

    try:
        other_time = os.path.getmtime(newer_than)
    except OSError:
        # Support writing a fresh file (which is always newer than a non-existant one)
        other_time = None

    while other_time is None or other_time >= os.path.getmtime(file_path):
        touch_file(file_path)
