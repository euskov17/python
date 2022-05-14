"""
Simplified VM code which works for some cases.
You need extend/rewrite code to pass all cases.
"""

import builtins
import dis
import types
import typing as tp


class Frame:
    """
    Frame header in cpython with description
        https://github.com/python/cpython/blob/3.6/Include/frameobject.h#L17

    Text description of frame parameters
        https://docs.python.org/3/library/inspect.html?highlight=frame#types-and-members
    """

    def __init__(self,
                 frame_code: types.CodeType,
                 frame_builtins: tp.Dict[str, tp.Any],
                 frame_globals: tp.Dict[str, tp.Any],
                 frame_locals: tp.Dict[str, tp.Any]) -> None:
        self.code = frame_code
        self.builtins = frame_builtins
        self.globals = frame_globals
        self.locals = frame_locals
        self.data_stack: tp.Any = []
        self.instruction_mapping: tp.Any = {instr.offset: instr for instr in dis.get_instructions(self.code)}
        self.max_offset = (len(self.instruction_mapping) - 1) * 2
        self.current_offset: int = 0
        self.loop_endings: tp.Any = []
        self.allow_change_offset_in_run: bool = True
        self.return_value = None

    def top(self) -> tp.Any:
        return self.data_stack[-1]

    def top1(self) -> tp.Any:
        return self.data_stack[-2]

    def top2(self) -> tp.Any:
        return self.data_stack[-3]

    def pop(self) -> tp.Any:
        return self.data_stack.pop()

    def push(self, *values: tp.Any) -> None:
        self.data_stack.extend(values)

    def popn(self, n: int) -> tp.Any:
        """
        Pop a number of values from the value stack.
        A list of n values is returned, the deepest value first.
        """
        if n > 0:
            returned = self.data_stack[-n:]
            self.data_stack[-n:] = []
            return returned
        else:
            return []

    def run(self) -> tp.Any:
        while self.current_offset <= self.max_offset:
            instruction = self.instruction_mapping[self.current_offset]
            getattr(self, instruction.opname.lower() + "_op")(instruction.argval)
            if self.allow_change_offset_in_run:
                self.current_offset = instruction.offset + 2
            else:
                self.allow_change_offset_in_run = True
        return self.return_value

    def call_function_op(self, arg: int) -> None:
        """
        Operation description:
            https://docs.python.org/3/library/dis.html#opcode-CALL_FUNCTION

        Operation realization:
            https://github.com/python/cpython/blob/3.7/Python/ceval.c#L3121
        """
        arguments = self.popn(arg)
        f = self.pop()
        self.push(f(*arguments))

    def call_function_kw_op(self, total_arg_count: int) -> None:
        kw_arg_names = self.pop()
        num_pos_args, num_kw_args = total_arg_count - len(kw_arg_names), len(kw_arg_names)
        kw_arg_values = self.popn(num_kw_args)
        pos_arg_values = self.popn(num_pos_args)
        kw_mapping = dict()
        for i in range(num_kw_args):
            kw_mapping[kw_arg_names[i]] = kw_arg_values[i]
        f = self.pop()
        self.push(f(*pos_arg_values, **kw_mapping))

    def load_name_op(self, arg: str) -> None:
        """
        Partial realization

        Operation description:
            https://docs.python.org/3/library/dis.html#opcode-LOAD_NAME

        Operation realization:
            https://github.com/python/cpython/blob/3.7/Python/ceval.c#L2057
        """
        if arg in self.locals:
            self.push(self.locals[arg])
        elif arg in self.globals:
            self.push(self.globals[arg])
        elif arg in self.builtins:
            self.push(self.builtins[arg])

    def load_method_op(self, method_name: str) -> None:
        obj = self.pop()
        if hasattr(obj, method_name):
            self.push(getattr(obj, method_name))
        else:
            raise AttributeError

    def call_method_op(self, arg: str) -> None:
        method_pos_args = int(arg)
        args = self.popn(method_pos_args)
        method = self.pop()
        self.push(method(*args))

    def load_fast_op(self, arg: str) -> None:
        self.push(self.locals[arg])

    def load_global_op(self, arg: str) -> None:
        """
        Operation description:
            https://docs.python.org/3/library/dis.html#opcode-LOAD_GLOBAL

        Operation realization:
            https://github.com/python/cpython/blob/3.7/Python/ceval.c#L2108
        """
        if arg in self.globals:
            self.push(self.globals[arg])
        elif arg in self.builtins:
            self.push(self.builtins[arg])

    def load_const_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/3/library/dis.html#opcode-LOAD_CONST

        Operation realization:
            https://github.com/python/cpython/blob/3.7/Python/ceval.c#L1088
        """
        self.push(arg)

    def return_value_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/3/library/dis.html#opcode-RETURN_VALUE

        Operation realization:
            https://github.com/python/cpython/blob/3.7/Python/ceval.c#L1641
        """
        self.return_value = self.pop()

    def pop_top_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/3/library/dis.html#opcode-POP_TOP

        Operation realization:
            https://github.com/python/cpython/blob/3.7/Python/ceval.c#L1102
        """
        self.pop()

    def make_function_op(self, arg: int) -> None:
        """
        Operation description:
            https://docs.python.org/3/library/dis.html#opcode-MAKE_FUNCTION

        Operation realization:
            https://github.com/python/cpython/blob/3.7/Python/ceval.c#L3203

        Parse stack:
            https://github.com/python/cpython/blob/3.7/Objects/call.c#L158

        Call function in cpython:
            https://github.com/python/cpython/blob/3.7/Python/ceval.c#L4554
        """
        name = self.pop()  # the qualified name of the function (at TOS)  # noqa
        code = self.pop()  # the code associated with the function (at TOS1)

        # TODO: use arg to parse function defaults

        def f(*args: tp.Any, **kwargs: tp.Any) -> tp.Any:
            # TODO: parse input arguments using code attributes such as co_argcount

            parsed_args: tp.Dict[str, tp.Any] = {}
            for i in range(code.co_argcount):
                parsed_args[code.co_varnames[i]] = args[i]
            f_locals = dict(self.locals)
            f_locals.update(parsed_args)

            frame = Frame(code, self.builtins, self.globals, f_locals)  # Run code in prepared environment
            return frame.run()

        self.push(f)

    def store_name_op(self, arg: str) -> None:
        """
        Operation description:
            https://docs.python.org/3/library/dis.html#opcode-STORE_NAME

        Operation realization:
            https://github.com/python/cpython/blob/3.7/Python/ceval.c#L1923
        """
        const = self.pop()
        self.locals[arg] = const

    def delete_global_op(self, arg: str) -> None:
        if arg in self.globals:
            self.globals.pop(arg)
        elif arg in self.builtins:
            self.builtins.pop(arg)
        else:
            raise NameError

    def store_fast_op(self, arg: str) -> None:
        self.locals[arg] = self.pop()

    def delete_fast_op(self, arg: str) -> None:
        if arg in self.locals:
            self.locals.pop(arg)
        else:
            raise NameError

    def store_global_op(self, arg: str) -> None:
        global_op_name = self.pop()
        self.globals[arg] = global_op_name

    def inplace_add_op(self, arg: str) -> None:
        right_operand = self.pop()
        self.data_stack[-1] += right_operand

    def binary_add_op(self, arg: str) -> None:
        right_operand = self.pop()
        left_operand = self.pop()
        self.push(left_operand + right_operand)

    def inplace_subtract_op(self, arg: str) -> None:
        right_operand = self.pop()
        self.data_stack[-1] -= right_operand

    def binary_subtract_op(self, arg: str) -> None:
        right_operand = self.pop()
        left_operand = self.pop()
        self.push(left_operand - right_operand)

    def inplace_multiply_op(self, arg: str) -> None:
        right_operand = self.pop()
        self.data_stack[-1] *= right_operand

    def binary_multiply_op(self, arg: str) -> None:
        right_operand = self.pop()
        left_operand = self.pop()
        self.push(left_operand * right_operand)

    def inplace_floor_divide_op(self, arg: str) -> None:
        right_operand = self.pop()
        self.data_stack[-1] //= right_operand

    def binary_floor_divide_op(self, arg: str) -> None:
        right_operand = self.pop()
        left_operand = self.pop()
        self.push(left_operand // right_operand)

    def inplace_true_divide_op(self, arg: str) -> None:
        right_operand = self.pop()
        self.data_stack[-1] /= right_operand

    def binary_true_divide_op(self, arg: str) -> None:
        right_operand = self.pop()
        left_operand = self.pop()
        self.push(left_operand / right_operand)

    def inplace_lshift_op(self, arg: str) -> None:
        right_operand = self.pop()
        self.data_stack[-1] <<= right_operand

    def binary_lshift_op(self, arg: str) -> None:
        right_operand = self.pop()
        left_operand = self.pop()
        self.push(left_operand << right_operand)

    def inplace_rshift_op(self, arg: str) -> None:
        right_operand = self.pop()
        self.data_stack[-1] >>= right_operand

    def binary_rshift_op(self, arg: str) -> None:
        right_operand = self.pop()
        left_operand = self.pop()
        self.push(left_operand >> right_operand)

    def inplace_modulo_op(self, arg: str) -> None:
        right_operand = self.pop()
        self.data_stack[-1] %= right_operand

    def binary_modulo_op(self, arg: str) -> None:
        right_operand = self.pop()
        left_operand = self.pop()
        self.push(left_operand % right_operand)

    def inplace_power_op(self, arg: str) -> None:
        right_operand = self.pop()
        self.data_stack[-1] **= right_operand

    def binary_power_op(self, arg: str) -> None:
        right_operand = self.pop()
        left_operand = self.pop()
        self.push(left_operand ** right_operand)

    def inplace_and_op(self, arg: str) -> None:
        right_operand = self.pop()
        self.data_stack[-1] &= right_operand

    def binary_and_op(self, arg: str) -> None:
        right_operand = self.pop()
        left_operand = self.pop()
        self.push(left_operand & right_operand)

    def inplace_or_op(self, arg: str) -> None:
        right_operand = self.pop()
        self.data_stack[-1] |= right_operand

    def binary_or_op(self, arg: str) -> None:
        right_operand = self.pop()
        left_operand = self.pop()
        self.push(left_operand | right_operand)

    def inplace_xor_op(self, arg: str) -> None:
        right_operand = self.pop()
        self.data_stack[-1] ^= right_operand

    def binary_xor_op(self, arg: str) -> None:
        right_operand = self.pop()
        left_operand = self.pop()
        self.push(left_operand ^ right_operand)

    def inplace_matrix_multiply_op(self, arg: str) -> None:
        right_operand = self.pop()
        self.data_stack[-1] @= right_operand

    def binary_matrix_multiply_op(self, arg: str) -> None:
        right_operand = self.pop()
        left_operand = self.pop()
        self.push(left_operand @ right_operand)

    def map_add_op(self, i: int) -> None:
        value, key = self.popn(2)
        dict.__setitem__(self.data_stack[-i], key, value)

    def set_add_op(self, i: int) -> None:
        value_to_add = self.pop()
        set.add(self.data_stack[-i], value_to_add)

    def list_append_op(self, i: int) -> None:
        value_to_append = self.pop()
        list.append(self.data_stack[-i], value_to_append)

    def get_iter_op(self, arg: str) -> None:
        self.data_stack[-1] = iter(self.top())

    def for_iter_op(self, out_loop_offset: int) -> None:
        iterator = self.data_stack[-1]
        try:
            iter_res = next(iterator)
            self.push(iter_res)
        except StopIteration:
            self.pop()
            self.current_offset = out_loop_offset
            if self.loop_endings and self.loop_endings[-1] == self.current_offset:
                self.loop_endings.pop()
            self.allow_change_offset_in_run = False

    def jump_absolute_op(self, offset: int) -> None:
        self.current_offset = offset
        self.allow_change_offset_in_run = False

    def setup_loop_op(self, arg: str) -> None:
        self.loop_endings.append(int(arg))

    def pop_block_op(self, arg: str) -> None:
        pass

    def compare_op_op(self, arg: str) -> None:
        right_operand = self.pop()
        left_operand = self.pop()
        cmp_result = False
        if arg == "==":
            cmp_result = left_operand == right_operand
        elif arg == "!=":
            cmp_result = left_operand != right_operand
        elif arg == "in":
            cmp_result = left_operand in right_operand
        elif arg == "not in":
            cmp_result = left_operand not in right_operand
        elif arg == ">":
            cmp_result = left_operand > right_operand
        elif arg == ">=":
            cmp_result = left_operand >= right_operand
        elif arg == "<":
            cmp_result = left_operand < right_operand
        elif arg == "<=":
            cmp_result = left_operand <= right_operand
        else:
            raise NotImplementedError
        self.push(cmp_result)

    def pop_jump_if_false_op(self, arg: str) -> None:
        condition = self.pop()
        if not condition:
            self.current_offset = int(arg)
            self.allow_change_offset_in_run = False

    def pop_jump_if_true_op(self, arg: str) -> None:
        condition = self.pop()
        if condition:
            self.current_offset = int(arg)
            self.allow_change_offset_in_run = False

    def extended_arg_op(self, arg: str) -> None:
        pass

    def unpack_sequence_op(self, arg: str) -> None:
        sequence = list(self.pop())
        self.data_stack.extend(sequence[::-1])

    def unary_positive_op(self, arg: str) -> None:
        value = self.top()
        self.data_stack[-1] = +value

    def unary_negative_op(self, arg: str) -> None:
        value = self.top()
        self.data_stack[-1] = -value

    def unary_invert_op(self, arg: str) -> None:
        value = self.top()
        self.data_stack[-1] = ~value

    def unary_not_op(self, arg: str) -> None:
        value = self.top()
        self.data_stack[-1] = not value

    def build_list_op(self, arg: int) -> None:
        num_values = arg
        values = list(self.popn(num_values))
        self.push(values)

    def build_tuple_op(self, arg: int) -> None:
        num_values = arg
        values = tuple(self.popn(num_values))
        self.push(values)

    def build_set_op(self, arg: int) -> None:
        num_values = arg
        values = set(self.popn(num_values))
        self.push(values)

    def build_const_key_map_op(self, arg: str) -> None:
        num_values = int(arg)
        keys = self.pop()
        result_dict = dict.fromkeys(keys)
        values = self.popn(num_values)
        for i in range(num_values):
            result_dict[keys[i]] = values[i]
        self.push(result_dict)

    def build_map_op(self, arg_count: int) -> None:
        values = self.popn(arg_count)
        keys = self.popn(arg_count)
        result_map = dict()
        for i in range(arg_count):
            result_map[keys[i]] = values[i]
        self.push(result_map)

    def build_slice_op(self, num_slice_args: int) -> None:
        if num_slice_args == 2:
            start, end = self.popn(num_slice_args)
            self.push(slice(start, end))
        else:
            start, end, step = self.popn(num_slice_args)
            self.push(slice(start, end, step))


    def store_subscr_op(self, arg: str) -> None:
        subscr_value = self.top()
        subscr_obj = self.top1()
        value_to_assign = self.top2()
        subscr_obj[subscr_value] = value_to_assign

    def delete_subscr_op(self, arg: str) -> None:
        subscr_value = self.top()
        subscr_obj = self.top1()
        del subscr_obj[subscr_value]

    def binary_subscr_op(self, arg: str) -> None:
        subscr_value = self.pop()
        obj = self.pop()
        self.push(obj[subscr_value])

class VirtualMachine:
    def run(self, code_obj: types.CodeType) -> None:
        """
        :param code_text_or_obj: code for interpreting
        """
        globals_context: tp.Dict[str, tp.Any] = {'print': print, 'list': list, 'range': range, 'sorted': sorted}
        frame = Frame(code_obj, builtins.globals()['__builtins__'], globals_context, globals_context)
        return frame.run()
