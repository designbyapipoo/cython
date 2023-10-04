from Cython.Compiler import Version
from Cython.Compiler.Nodes import *
from Cython.Compiler.ExprNodes import * 
from Cython.Compiler.ModuleNode import ModuleNode
from Cython.CodeWriter import DeclarationWriter
from Cython.Compiler.AutoDocTransforms import AnnotationWriter, ExpressionWriter
import cython 

cython.declare(PyrexTypes=object, Naming=object, ExprNodes=object, Nodes=object,
               Options=object, UtilNodes=object, LetNode=object,
               LetRefNode=object, TreeFragment=object, EncodedString=object,
               error=object, warning=object, copy=object, _unicode=object)


# Inspired by and based around https://github.com/cython/cython/pull/3818
# with some less lazy changes to it and a few minor improvements and optimzations...

# Decided to revert to an older variant I had wrote of this code for the sake of 
# maintainability - Vizonex



# TODO Save this implemenation commented out if required....
# if sys.version_info >= (3, 9):
#     typing_module = "typing"
# else:
#     typing_module = "typing_extensions"

def ctype_name(arg, node:"Node") -> str:

    # TODO Make a better conversion function...
    if arg.type and hasattr(arg.type, "name"):
        # Used C declared type...
        # TODO see about using a check to see if users wants to include cython's shadow varaibales...
        return arg.type.name
        
    py_name = node.type.return_type.py_type_name() # type: ignore
    if "(int, long)" == py_name:
        return "int"
    
    return py_name


def translate_annotations(node) -> list[str]:
    func_annotations = []
    for arg, py_arg in zip(node.type.args, node.declarator.args):
        annotation = ""
        # TODO Maybe have a flag to check if were currently using 
        # a class inside of here as an extra check?
        if arg.name == "self":
            annotation = arg.name
        else:
            annotation = "%s: %s" % (arg.name, ctype_name(arg, node))
        if not py_arg.default or not py_arg.default_value:
            # TODO: See if there is a better way of going about finding an ellipsis...
            annotation += " = ..."
        func_annotations.append(annotation)
    return func_annotations


# TODO Find something smarter than a variable stack, I'm not sure what it's original purpose was for - Vizonex

# FIXME I plan to make this a little bit more simillar to 
# the Embedsignature Transform in the future but for now this will do...


# FIXME I'm planning on dropping these different annotaions I have in the file if
# they cannot be handled by earlier versions than 3.9 of python... 
# they are currently just here to help me figure out how to write this all 
# down since Im working inside of Vs Code.



class PyiWriter(DeclarationWriter):
    """Used By Cython to help Write stubfiles
    this comes in handy for ides like Pylance 
    which suffer from having no code acess to 
    annotations from compiled python modules...
    """

    def __init__(self):
        DeclarationWriter.__init__(self)
        # TODO Maybe have arguments 
        # for how shadow.pyi is implemented be passed into here 
        # if we want them to be even imported at 
        # all and if so C Variables should be translated as such...
    
        # TODO in the future allow context variables to be passed so that a directive can be used to 
        # pass along docstring infromation so tools such as sphinx can generate clean documentation...

        self.translation_table:dict[str,str] = {}
        """Used as an eternal resource for translating ctype declarations into python-types"""

        self.use_typing : bool = False
        """if true we must import typing's generator typehint..."""


    def _visitchildren_indented(self, node):
        self.indent()
        self.visitchildren(node)
        self.dedent()
    
    def translate_pyrex_type(self, ctype:PyrexTypes.PyrexType):
        # TODO implement Pyrex to cython shadow typehints converter...
        
        if isinstance(ctype, PyrexTypes.CIntType):
            return "int"

        elif isinstance(ctype, PyrexTypes.CFloatType):
            return "float"
    
        elif isinstance(ctype,PyrexTypes.PyObjectType):
            py_name = ctype.py_type_name()
            if py_name:
                # Try returning the python type name and put it into quotes 
                # incase the object has not been registered yet....
                return py_name if py_name in self.stack else f"{py_name!r}"

        return 'object'


    # Instead of doing it into C, we're doing it backwards...
    def translate_base_type_to_py(
        self,
        base:CSimpleBaseTypeNode
        ):

        # Try checking our table first...
        if self.translation_table.get(base.name):
            return self.translation_table[base.name]

        elif base.name == "object":
            return "object"

        elif base.name in ("unicode","basestring"):
            return "str"

        elif not base.is_basic_c_type:
            # Likely that it's already a python object that's being handled...
            # execpt for basestring and unicode...
            return base.name 

        elif base.name == "bint":
            return "bool"

        ctype = PyrexTypes.simple_c_type(base.signed, base.longness, base.name) # type: ignore
        return self.translate_pyrex_type(ctype)

    def emptyline(self):
        self.result.putline("")

    def visit_ModuleNode(self, node: ModuleNode):
        # visit the children and start looking for anything usefull...
        self.visitchildren(node)
        return node 

    def visit_CImportStatNode(self,node):
        return node
    
    def visit_FromCImportStatNode(self,node):
        return node
    
    def visit_CDefExternNode(self,node:CDefExternNode):
        self.visitchildren(node)

    def visit_CEnumDefNode(self, node:CEnumDefNode):
        # TODO Figure out how to define an enum-class via typehints...

        # NOTE It seems that only public will make the enum acessable to python so 
        # I'll just have it check if the enums will be public for now... - Vizonex
        if node.visibility == "public":
            # Enum's name is not in or visable in the final product beacuse 
            # it's not an enum class so do not indent here...
            # Also Leave visit_CEnumDefItemNode up to the previous 
            # class's function...
            self.putline("# -- enum %s --" % node.name)
            self.visitchildren(node)
        return node 

    # Used in our translation table to register return types variables from...
    def visit_CTypeDefNode(self,node:CTypeDefNode):
        if isinstance(node.declarator, CNameDeclaratorNode):
            # Register a new type to use in our translation table...
            self.translation_table[node.declarator.name] = self.translate_base_type_to_py(node.base_type)
    
    def visit_CStructOrUnionDefNode(self, node:CStructOrUnionDefNode):
        # XXX : Currenlty, I don't know what to do here yet but ignoring 
        # is triggering some problems currently...
        return node
        

    def visit_CVarDefNode(self, node: CVarDefNode):

        # if they aren't public or readonly then the variable inside of a class 
        # or outisde should be ignored by default...

        if node.visibility in ["readonly", "public"]:

            # TODO handle ctypedef nodes and give them a 
            # new type-registry system to help translate 
            # all incomming variables... 

            py_name = self.translate_base_type_to_py(node.base_type)
            
            # Final check...
            if py_name is not None:
                # Write in all the objects listed on the defined line...
                for d in node.declarators:
                    self.putline("%s: %s" % (d.name, py_name))
    
        return node


    


    def visit_ImportNode(self, node: ImportNode):
        module_name = node.module_name.value

        if not node.name_list:
            self.putline("import %s" % module_name) 
        else:
            all_imported_children = ", ".join((arg.value for arg in node.name_list.args))

            if node.level > 0:
                module_name = "%s%s" % ("." * node.level , module_name)

            self.putline("from %s import %s" % (module_name, all_imported_children))

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
    
    # Optimized orginal code by having there be one function to take 
    # the place of two of them I could see what Scoder meant when 
    # said the orginal pull request needed to be cleaned up...

    def write_class(self, node, class_name):
        self.put("class %s" % class_name)
        if getattr(node,"bases",None) and isinstance(node.bases, TupleNode):
            self.put("(")
            self.put(",".join([name.name for name in node.bases.args]))
            self.endline("):")
        else:
            self.put(":")
        self._visitchildren_indented(node)
        self.emptyline()
        return node 
    
    # I have tried to merege these before via visit_ClassDefNode but it causes the system to break so this 
    # was the best I could do to minigate the problem - Vizonex 
    def visit_CClassDefNode(self, node: CClassDefNode):
        return self.write_class(node, node.class_name)

    def visit_PyClassDefNode(self, node:PyClassDefNode):
        return self.write_class(node, node.name)

    def visit_CFuncDefNode(self, node: CFuncDefNode):
        # cdefs are for C only...
        if not node.overridable:
            return node 

        func_name = node.declared_name()

        self.startline()
        self.put("def %s(" % func_name)
        # Cleaned up alot of what the orginal author did by making a new function
        self.put(", ".join(translate_annotations(node)))
        # TODO Maybe Try passing docstrings in the future for vscode users' sake
        # or have it also be a compiler argument?...
        self.endline(") -> %s: ..." % ctype_name(node.type.return_type))
        return node

    def print_Decorator(self, decorator):
        if isinstance(decorator, CallNode):
            return
        
        self.startline("@")
        if isinstance(decorator, NameNode):
            self.endline("%s" % decorator.name)
        else:
            assert isinstance(decorator, AttributeNode) , "Decorator was not an attribute node..."
            self.endline("%s.%s" % (decorator.obj.name,decorator.attribute))
        

    def annotation_Str(self, annotation:ExprNode) -> str:
        return annotation.name if hasattr(annotation,"name") and annotation.is_name else  annotation.string.unicode_value 
        
     

    def visit_DefNode(self,node:DefNode):
        func_name = node.name

        # TODO Change how init is being handled...
        if func_name == '__cinit__':
            func_name = '__init__'
        
        def argument_str(arg:CArgDeclNode):
            value = arg.declarator.name

            if arg.annotation is not None:
                value += (": %s" % self.annotation_Str(arg.annotation))

            elif hasattr(arg.base_type,"name") and arg.base_type.name is not None:
                value += ": %s" % self.translate_base_type_to_py(arg.base_type)
                
            if (arg.default is not None or
                arg.default_value is not None):
                value += " = ..."

            return value
        
        # TODO See if "*," or "/," or an "Ellipsis" 
        # can be passed through and accepted into all the stub 
        # files with a regex to check it off as a unittest.
        
        async_name = "async " if node.is_async_def or getattr(node,"is_coroutine", None) else ""

        if node.decorators is not None:
            for decorator in node.decorators:
                self.print_Decorator(decorator.decorator)

        self.startline("%sdef %s(" % (async_name, func_name))

        # TODO Maybe look into trying AutoDocTransforms?

        args_list = []
        
        # Ordinary arguments:
        args_list += (argument_str(arg) for arg in node.args)

        # extra postional and keyword arguments:
        star_arg = node.star_arg
        starstar_arg = node.starstar_arg
        
        # Calculations of Postion or Keyword only arguments 
        # Implementation from EmbedSignature

        npoargs = getattr(node, 'num_posonly_args', 0)
        nkargs = getattr(node, 'num_kwonly_args', 0)
        npargs = len(node.args) - nkargs - npoargs
        
        if star_arg is not None:
            
            args_list.insert(npargs + npoargs, "*%s" % star_arg.name)
        
        elif nkargs:
            args_list.insert(npargs + npoargs, '*')
        
        if npoargs:
            args_list.insert(npoargs,'/')

        if starstar_arg is not None:
            args_list.append("**%s" % starstar_arg.name)

        self.put(", ".join(args_list))

        retype = node.return_type_annotation

        if retype is not None:
            
            # This is a little bit different than the original pull request 
            # since I wanted there to be propper typehints given to all the 
            # objects which is why I added the "Generator" as a typehint & keyword...

            annotation = self.annotation_Str(retype)
            if (node.is_generator and not annotation.startswith("Generator")):
                # TODO figure out how the extract the other two required variables...
                # Also the function could be an Iterator but 
                # hadn't added the "__iter__" function name-check just yet...
                self.use_typing = True
                self.put(") -> Genertor[ %s, None, None]:..." % annotation)
            else:
                self.put(") -> %s: ..." % annotation)

        # TODO Add Return Type Recovery tool to resolve all missing annotations...
        else:
            self.put("): ...")
        self.endline()



    def visit_ExprNode(self,node:ExprNode):
        return node 
        
    def visit_SingleAssignmentNode(self,node:SingleAssignmentNode):
        if isinstance(node.rhs, ImportNode):
            self.visitchildren(node)
            return node
        
        name = node.lhs.name
        if node.lhs.annotation:
            # TODO Check if the annotation's values are existant...
            self.putline("%s : %s = ..." % (name, node.lhs.annotation.string.value))
        else:
            self.putline("%s : %s" % (name, self.translate_pyrex_type(node.rhs.type)))

    def visit_NameNode(self, node:NameNode):
        return node

    def visit_ExprStatNode(self,node:ExprStatNode):
        if isinstance(node.expr, NameNode):
            expr = node.expr
            name = expr.name # type: ignore
            if expr.annotation:
                self.putline("%s: %s " % (name, self.annotation_Str(expr.annotation)))
            else:
                self.putline("%s " % name)
        return node 



    def visit_Node(self, node:Node):
        self.visitchildren(node)
        return node

    def putline_at(self,index, line):
        self.result.lines.insert(index, line)

    def write(self, root:Node, _debug:bool = False):
        # Top Notice will likely chage once I've made a full on pull request...
        self.putline("# Python stub file generated by Cython %s" % Version.watermark)
        self.emptyline()

        self.visit(root)
        if self.use_typing:
            # Inject Keyword Generator
            self.putline_at(1, "from typing import Generator")

        # added a new debugger incase needed for now...
        if _debug:
            print("# -- Pyi Result --")
            print("\n".join(self.result.lines))
            print("# -- End Of Pyi Result --")

        return self.result

  
    

   
