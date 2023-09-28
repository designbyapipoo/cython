from .Compiler import Version
from .Compiler.Nodes import *
from .Compiler.ExprNodes import * 
from .Compiler.ModuleNode import ModuleNode
from .CodeWriter import LinesResult, DeclarationWriter
from .Compiler.Visitor import PrintTree
from .Compiler.AutoDocTransforms import ExpressionWriter, AnnotationWriter

import cython 

cython.declare(PyrexTypes=object, Naming=object, ExprNodes=object, Nodes=object,
               Options=object, UtilNodes=object, LetNode=object,
               LetRefNode=object, TreeFragment=object, EncodedString=object,
               error=object, warning=object, copy=object, _unicode=object)


# Inspired by and based around https://github.com/cython/cython/pull/3818
# with some less lazy changes to it and a few minor improvements and optimzations
# Still needs a few more edits here and there but this is a start...

# TODO planning to implement typehint recovery systems in the future simillar to 
# how Pylance for the VS code extension can do it for any type that is referred to as 
# 'object' as it is too vauge to understand and is not helpful.


# FIXME I plan to make this a little bit more simillar to 
# the Embedsignature Transform in the future but for now this will do...

# FIXME I'm planning on dropping these different annotaions I have in the file if
# they cannot be handled by earlier versions than 3.9 of python, 
# they are currently just here to help me figure out how to write this all 
# down since Im working inside of Vs Code.

# TODO I am Planning to make tools to resolve missing return-types in the 
# future as a feature for cython, it is currently missing and that's because 
# it requires a few new and tricky to write visitor classes and it requires 
# a lot of predicitions and a table of Pyrextypes with function names being 
# the keys - Vizonex 

# FIXME decorators are not being written and needs fixing - Vizonex

# These Functions are temporarly inplace 
# and I plan to optimize everything if required - Vizonex

def ctype_name(arg, node:Node) -> str:

    # TODO Make a better conversion function...
    if arg.type and hasattr(arg.type, "name"):
        # Used C declared type...
        return arg.type.name
        
    py_name = node.type.return_type.py_type_name() # type: ignore
    if "(int, long)" == py_name:
        return "int"
    
    return py_name


def translate_annotations(node) -> list[str]:
    func_annotations = []
    for arg, py_arg in zip(node.type.args, node.declarator.args):
        annotation = ""
        if arg.name == "self":
            annotation = arg.name
        else:
            annotation = "%s: %s" % (arg.name, ctype_name(arg, node))
        if not py_arg.default or not py_arg.default_value:
            annotation += " = ..."
        func_annotations.append(annotation)
    return func_annotations




class PyiWriter(DeclarationWriter):
    """Used By Cython to help Write stubfiles
    this comes in handy for ides like Pylance 
    which suffer from having no code acess to 
    annotations from compiled python modules...


    Currently borrows parts from the `EmbedSignature` to 
    transform python functions off and it's other features 
    are to help with formatting and translating the objects 
    and annotations off as if the module directives said we would 
    embed the signatures to python...
    """

    indent_string = u"    "

    def __init__(self, result=None):
        super(PyiWriter, self).__init__()
        if result is None:
            result = LinesResult()
        self.result = result
        self.numindents = 0
        self.current_directives = None
        self.class_indentures = 0
        self.need_typehints = False
        self._next_is_static_method = False 
        self.num_of_functions = 0

    def write(self, tree):
        self.visit(tree)
        if isinstance(tree, ModuleNode):
            self.current_directives = tree.directives
        return self.result

    def place_in_front(self, s):
        self.result.lines = [s] + self.result.lines

    def skiplines(self, n):
        for _ in range(n):
            self.endline()

    def _fmt_annotation(self, node):
        writer = AnnotationWriter()
        result = writer.write(node)
        return result
    
    def _fmt_expr(self, node):
        writer = ExpressionWriter()
        result = writer.write(node)
        # print(type(node).__name__, '-->', result)
        return result

    def _visitchildren_indented(self, node):
        self.indent()
        self.visitchildren(node)
        self.dedent()
    
    # Reasons for using parts of Embedsignature should be simple to understand
    # A: It's better than wiriting this all myself 
    # B: Annotations and function signatures are translated and formatted 

    # In the Future I plan to Merge Embedsignature and hack the internal structure 
    # to force python directives to be used this pyiwriter to make it easier to maintain...

    # It does not go all the way to _fmt_signature due to the nature or chance of a node 
    # carrying an 'async' definition

    def _fmt_arg(self, arg):
        arg_doc = arg.name 
        annotation = None
        defaultval = None
        
        if not arg.annotation:
            annotation = self._fmt_type(arg.type)

        if arg.default:
            defaultval = self._fmt_expr(arg.default)

        if annotation:
            arg_doc = arg_doc + (': %s' % annotation)
            if defaultval:
                arg_doc = arg_doc + (' = %s' % defaultval)

        elif defaultval:
            arg_doc = arg_doc + ('=%s' % defaultval)

        return arg_doc

    def _fmt_type(self, type:PyrexTypes.PyrexType):
        if type is PyrexTypes.py_object_type:
            return None
        annotation = None
        if type.is_string:
            annotation = self.current_directives['c_string_type']
        elif type.is_numeric:
            annotation = type.py_type_name()
        if annotation is None:
            code = type.declaration_code('', for_display=1)
            annotation = code.replace(' ', '_').replace('*', 'p')
        return annotation

    def _fmt_arglist(self, args,
                     npoargs=0, npargs=0, pargs=None,
                     nkargs=0, kargs=None,
                     hide_self=False):
        arglist = []
        for arg in args:
            if not hide_self or not arg.entry.is_self_arg:
                arg_doc = self._fmt_arg(arg)
                arglist.append(arg_doc)
        if pargs:
            arg_doc = self._fmt_star_arg(pargs)
            arglist.insert(npargs + npoargs, '*%s' % arg_doc)
        elif nkargs:
            arglist.insert(npargs + npoargs, '*')
        if npoargs:
            arglist.insert(npoargs, '/')
        if kargs:
            arg_doc = self._fmt_star_arg(kargs)
            arglist.append('**%s' % arg_doc)
        
        return arglist

    def _fmt_star_arg(self, arg):
        arg_doc = arg.name
        if arg.annotation:
            annotation = self._fmt_annotation(arg.annotation)
            arg_doc = arg_doc + (': %s' % annotation)
        return arg_doc


    def visit_ImportNode(self, node: ImportNode):
        module_name:str = node.module_name.value

        if not node.name_list:
            self.putline("import %s" % module_name) 
        else:
            all_imported_children = ", ".join((arg.value for arg in node.name_list.args))

            if node.level > 0:
                module_name = "%s%s" % ("." * node.level , module_name)
            self.putline("from %s import %s" % (module_name, all_imported_children))
        return node


    def visit_Node(self, node):
        self.visitchildren(node)
        return node 
    
    
    def write_decorator(self, decorator):
        if isinstance(decorator, CallNode):
            # cython directive so it can be ignored... 
            return
        
        self.startline("@")
        if isinstance(decorator, NameNode):

            self.endline("%s" % decorator.name)
        else:
            # TODO allow for multiple modules to stack on top of each other to form a path to the decorator required...
            assert isinstance(decorator, AttributeNode) , "Decorator was not an attribute node..."
            self.endline("%s.%s" % (decorator.obj.name,decorator.attribute))
    
    def visit_CDefExternNode(self,node:CDefExternNode):
        return node
    
    def skip_visitation(self, node):
        return node

    visit_CImportStatNode = skip_visitation
    visit_FromCImportStatNode = skip_visitation
    
    def visit_CVarDefNode(self, node: CVarDefNode):

        # if they aren't public or readonly then the variable inside of a class 
        # or outisde should be ignored by default...

        if node.visibility in ["readonly", "public"]:

            # TODO handle ctypedef nodes and give them a 
            # new type-registry system to help translate 
            # all incomming variables... 

            py_name = self._fmt_type(node.base_type)
            
            # Final check...
            if py_name is not None:
                # Write in all the objects listed on the defined line...
                for d in node.declarators:
                    self.putline("%s: %s" % (d.name, py_name))
                    
        return node
    
    def visit_SingleAssignmentNode(self, node: SingleAssignmentNode): # type: ignore
        if not isinstance(node.rhs, ImportNode):
            return node

        module_name = node.rhs.module_name.value

        parent_module = module_name

        pos = module_name.find('.')

        if pos != -1:
            parent_module = module_name[:pos]
        
        imported_name = node.lhs.name

        if parent_module == imported_name:
            self.visitchildren(node)
            return node

        self.putline("import %s as %s" % (module_name, imported_name))
        return node 

    def visit_DefNode(self, node:DefNode):
        # TODO Track for staticmethod decorators...
        if node.decorators is not None:
            for decorator in node.decorators:
                print(decorator.__dict__)
                self.write_decorator(decorator.decorator)

        self.startline()
        if node.is_async_def or hasattr(node, "is_coroutine") and node.is_coroutine is True:
            self.put("async ")
        
        func_name = node.name

        if func_name == '__cinit__':
            func_name = '__init__'

        self.put("def %s(" % func_name)

        # Now we go into a simillar phase as embedsignature 
        # to write down our arguments and annotation arguments 
        # as well as any declared variables
        npoargs = getattr(node, 'num_posonly_args', 0)
        nkargs = getattr(node, 'num_kwonly_args', 0)
        npargs = len(node.args) - nkargs - npoargs

        result_args = self._fmt_arglist(
            node.args, 
            npoargs, 
            npargs, 
            node.star_arg, 
            nkargs, 
            node.starstar_arg,
            hide_self=self.class_indentures < 1)
        
        self.put(", ".join(result_args))

        # TODO Add A Return Type Recovery tool to resolve all 
        # missing return type annotations from functions being called and returned...
        return_type = getattr(node, "return_type_annotation", None)

        if return_type is not None:
            annotation = self._fmt_annotation(return_type)
            if (node.is_generator and not annotation.startswith("Generator")):
                # TODO figure out how the extract the other two required variables...
                # Also the function could be an Iterator but 
                # hadn't added the "__iter__" function name-check just yet...

                # Typehints are now required to be imported at beginning of the pyi stub 
                # for the sake of readabiluty
                self.need_typehints = True
                self.put(") -> Genertor[ %s, None, None]:..." % annotation)
            else:
                self.put(") -> %s:..." % annotation)
        else:
            # Unknown Annotations can sitll be recoverable via returnStatNode...
            # TODO Recover entries and returntypes if python objects are found...
            self.put("):...")
        # Move by 2 lines down...
        self.skiplines(2)
        return node
    
    
    def visit_ClassDefNode(self, node:ClassDefNode):
    
        try:
            # PyClassDefNode
            class_name = node.name
        except AttributeError:
            # CClassDefNode
            class_name = node.class_name

        self.startline("class %s" % class_name)
        if getattr(node,"bases",None) and isinstance(node.bases, TupleNode):
            self.put("(" + ",".join([name.name for name in node.bases.args]) + ")")
    
        self.endline(":")
        # Track class recursions so we know if the function may have a self argument inplace...
        self.class_indentures += 1
        
        if node.body.stats:
            self._visitchildren_indented(node)
        else:
            self.indent()
            self.putline("pass")
            self.dedent()
            self.skiplines(1)
        self.class_indentures -= 1
        return node 
    
    def visit_CFuncDefNode(self, node:CFuncDefNode):
        # cdef functions are not allowed and should be skipped...
        if not node.overridable:
            return node
        
        func_name = node.declared_name()

        self.startline()
        self.put("def %s(" % func_name)

        self.put(", ".join(translate_annotations(node)))

        _type = self._fmt_type(node.type.return_type)

        self.endline((") -> %s: ..." % _type) if _type else "):...")

        return node 
    
    def visit_NameNode(self, node:NameNode):
        return node

    def visit_ExprStatNode(self,node:ExprStatNode):
        if isinstance(node.expr, NameNode):
            # self.set_Stack_As_Occupied()

            expr = node.expr
            name = expr.name # type: ignore
            if expr.annotation:
                self.putline("%s: %s " % (name, self.annotation_Str(expr.annotation)))
            else:
                self.putline("%s " % name)
        return node 
    # needed here otherwise this will completely break the current compiler...
    visit_CClassDefNode = visit_ClassDefNode

    def write(self, root:Node, _debug:bool = False):
        # Top Notice will likely chage once I've made a full on pull request...
        self.putline("# Python stub file generated by Cython %s" % Version.watermark)
        self.endline()

        if isinstance(root, ModuleNode):
            self.current_directives = root.directives

        self.visitchildren(root)

        # Added a new debugger incase needed for now...
        if _debug:
            print("# -- Pyi Result --")
            print("\n".join(self.result.lines))
            print("# -- End Of Pyi Result --")

        return self.result
