# We declare all of these here to type the first argument.

from Cython.Compiler.Scanning cimport PyrexScanner


cpdef p_ident(PyrexScanner s, message =*)
cpdef p_ident_list(PyrexScanner s)

cpdef p_binop_expr(PyrexScanner s, ops, p_sub_expr)
cpdef p_simple_expr(PyrexScanner s)
cpdef p_test(PyrexScanner s)
cpdef p_or_test(PyrexScanner s)
cpdef p_rassoc_binop_expr(PyrexScanner s, ops, p_subexpr)
cpdef p_and_test(PyrexScanner s)
cpdef p_not_test(PyrexScanner s)
cpdef p_comparison(PyrexScanner s)
cpdef p_cascaded_cmp(PyrexScanner s)
cpdef p_cmp_op(PyrexScanner s)
cpdef p_starred_expr(PyrexScanner s)
cpdef p_bit_expr(PyrexScanner s)
cpdef p_xor_expr(PyrexScanner s)
cpdef p_and_expr(PyrexScanner s)
cpdef p_shift_expr(PyrexScanner s)
cpdef p_arith_expr(PyrexScanner s)
cpdef p_term(PyrexScanner s)
cpdef p_factor(PyrexScanner s)
cpdef p_typecast(PyrexScanner s)
cpdef p_sizeof(PyrexScanner s)
cpdef p_yield_expression(PyrexScanner s)
cpdef p_power(PyrexScanner s)
cpdef p_trailer(PyrexScanner s, node1)
cpdef p_call(PyrexScanner s, function)
cpdef p_index(PyrexScanner s, base)
cpdef p_subscript_list(PyrexScanner s)
cpdef p_subscript(PyrexScanner s)
cpdef p_slice_element(PyrexScanner s, follow_set)
cpdef expect_ellipsis(PyrexScanner s)
cpdef make_slice_nodes(pos, subscripts)
cpdef make_slice_node(pos, start, stop = *, step = *)
cpdef p_atom(PyrexScanner s)
cpdef p_name(PyrexScanner s, name)
cpdef p_cat_string_literal(PyrexScanner s)
cpdef p_opt_string_literal(PyrexScanner s)
cpdef p_string_literal(PyrexScanner s)
cpdef p_list_maker(PyrexScanner s)
cpdef p_list_iter(PyrexScanner s, body)
cpdef p_list_for(PyrexScanner s, body)
cpdef p_list_if(PyrexScanner s, body)
cpdef p_dict_or_set_maker(PyrexScanner s)
cpdef p_backquote_expr(PyrexScanner s)
cpdef p_simple_expr_list(PyrexScanner s)
cpdef p_expr(PyrexScanner s)
cpdef p_testlist(PyrexScanner s)

#-------------------------------------------------------
#
#   Statements
#
#-------------------------------------------------------

cpdef flatten_parallel_assignments(input, output)

cpdef p_global_statement(PyrexScanner s)
cpdef p_expression_or_assignment(PyrexScanner s)
cpdef p_print_statement(PyrexScanner s)
cpdef p_exec_statement(PyrexScanner s)
cpdef p_del_statement(PyrexScanner s)
cpdef p_pass_statement(PyrexScanner s, bint with_newline = *)
cpdef p_break_statement(PyrexScanner s)
cpdef p_continue_statement(PyrexScanner s)
cpdef p_return_statement(PyrexScanner s)
cpdef p_raise_statement(PyrexScanner s)
cpdef p_import_statement(PyrexScanner s)
cpdef p_from_import_statement(PyrexScanner s, bint first_statement = *)
cpdef p_imported_name(PyrexScanner s, bint is_cimport)
cpdef p_dotted_name(PyrexScanner s, bint as_allowed)
cpdef p_as_name(PyrexScanner s)
cpdef p_assert_statement(PyrexScanner s)
cpdef p_if_statement(PyrexScanner s)
cpdef p_if_clause(PyrexScanner s)
cpdef p_else_clause(PyrexScanner s)
cpdef p_while_statement(PyrexScanner s)
cpdef p_for_statement(PyrexScanner s)
cpdef p_for_bounds(PyrexScanner s)
cpdef p_for_from_relation(PyrexScanner s)
cpdef p_for_from_step(PyrexScanner s)
cpdef p_target(PyrexScanner s, terminator)
cpdef p_for_target(PyrexScanner s)
cpdef p_for_iterator(PyrexScanner s)
cpdef p_try_statement(PyrexScanner s)
cpdef p_except_clause(PyrexScanner s)
cpdef p_include_statement(PyrexScanner s, ctx)
cpdef p_with_statement(PyrexScanner s)
cpdef p_simple_statement(PyrexScanner s, bint first_statement = *)
cpdef p_simple_statement_list(PyrexScanner s, ctx, bint first_statement = *)
cpdef p_compile_time_expr(PyrexScanner s)
cpdef p_DEF_statement(PyrexScanner s)
cpdef p_IF_statement(PyrexScanner s, ctx)
cpdef p_statement(PyrexScanner s, ctx, bint first_statement = *)
cpdef p_statement_list(PyrexScanner s, ctx, bint first_statement = *)
cpdef p_suite(PyrexScanner s, ctx = *, bint with_doc = *, bint with_pseudo_doc = *)
cpdef p_positional_and_keyword_args(PyrexScanner s, end_sy_set, type_positions= *, type_keywords= * )

cpdef p_c_base_type(PyrexScanner s, bint self_flag = *, bint nonempty = *)
cpdef p_calling_convention(PyrexScanner s)
cpdef p_c_complex_base_type(PyrexScanner s)
cpdef p_c_simple_base_type(PyrexScanner s, self_flag, nonempty)
cpdef p_buffer_access(PyrexScanner s, base_type_node)
cpdef bint looking_at_name(PyrexScanner s) except -2
cpdef bint looking_at_expr(PyrexScanner s) except -2
cpdef bint looking_at_base_type(PyrexScanner s) except -2
cpdef bint looking_at_dotted_name(PyrexScanner s) except -2
cpdef p_sign_and_longness(PyrexScanner s)
cpdef p_opt_cname(PyrexScanner s)
cpdef p_c_declarator(PyrexScanner s, ctx = *, bint empty = *, bint is_type = *, bint cmethod_flag = *,
                   bint assignable = *, bint nonempty = *,
                   bint calling_convention_allowed = *)
cpdef p_c_array_declarator(PyrexScanner s, base)
cpdef p_c_func_declarator(PyrexScanner s, pos, ctx, base, bint cmethod_flag)
cpdef p_c_simple_declarator(PyrexScanner s, ctx, bint empty, bint is_type, bint cmethod_flag,
                          bint assignable, bint nonempty)
cpdef p_nogil(PyrexScanner s)
cpdef p_with_gil(PyrexScanner s)
cpdef p_exception_value_clause(PyrexScanner s)
cpdef p_c_arg_list(PyrexScanner s, ctx = *, bint in_pyfunc = *, bint cmethod_flag = *,
                 bint nonempty_declarators = *, bint kw_only = *)
cpdef p_optional_ellipsis(PyrexScanner s)
cpdef p_c_arg_decl(PyrexScanner s, ctx, in_pyfunc, bint cmethod_flag = *, bint nonempty = *, bint kw_only = *)
cpdef p_api(PyrexScanner s)
cpdef p_cdef_statement(PyrexScanner s, ctx)
cpdef p_cdef_block(PyrexScanner s, ctx)
cpdef p_cdef_extern_block(PyrexScanner s, pos, ctx)
cpdef p_c_enum_definition(PyrexScanner s, pos, ctx)
cpdef p_c_enum_line(PyrexScanner s, items)
cpdef p_c_enum_item(PyrexScanner s, items)
cpdef p_c_struct_or_union_definition(PyrexScanner s, pos, ctx)
cpdef p_visibility(PyrexScanner s, prev_visibility)
cpdef p_c_modifiers(PyrexScanner s)
cpdef p_c_func_or_var_declaration(PyrexScanner s, pos, ctx)
cpdef p_ctypedef_statement(PyrexScanner s, ctx)
cpdef p_decorators(PyrexScanner s)
cpdef p_def_statement(PyrexScanner s, decorators = *)
cpdef p_py_arg_decl(PyrexScanner s)
cpdef p_class_statement(PyrexScanner s, decorators)
cpdef p_c_class_definition(PyrexScanner s, pos,  ctx)
cpdef p_c_class_options(PyrexScanner s)
cpdef p_property_decl(PyrexScanner s)
cpdef p_doc_string(PyrexScanner s)
cpdef p_code(PyrexScanner s, level= *)
cpdef p_compiler_directive_comments(PyrexScanner s)
cpdef p_module(PyrexScanner s, pxd, full_module_name)
