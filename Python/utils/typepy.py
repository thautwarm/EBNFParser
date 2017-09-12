#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 14:55:27 2017
@author: misakawa
"""


class Typedef:
    def __init__(self, type_, error_msg="Type of {return_or_input} {idx_or_key} should be {type}."):
        self.type_ = type_
        self.error_msg = error_msg

    def set_lambda(self, dual_callable_obj):
        self.check = lambda input_var: dual_callable_obj(input_var, self.type_)
        return self


NEq = lambda type_: Typedef(type_, error_msg="Type of {return_or_input} {idx_or_key} shouldn't be {type}.").set_lambda(
    lambda input_var, input_type: not isinstance(input_var, input_type))
Or = lambda *type_: Typedef(type_, error_msg="Type of {return_or_input} {idx_or_key} should  be in {type}").set_lambda(
    lambda input_var, input_type: input_var.__class__ in input_type)


def error_helper(template_msg, **kwargs):
    template = template_msg + '\n' + "The type of current input {return_or_input} is {input_var_type}."
    return template.format(**kwargs)


def _check(input_var, check_type, idx=None, key=None, ret=None):
    return_or_input = lambda: "return" if ret else "argument"
    error_render    = lambda: dict(idx_or_key=key if key else idx,
                                return_or_input=return_or_input(),
                                type=_type,
                                input_var_type=input_var.__class__)
    if isinstance(check_type, Typedef):
        _type = check_type.type_
        if not check_type.check(input_var):
            raise TypeError(error_helper(check_type.error_msg, **error_render()))
    else:
        _type = check_type
        if not isinstance(input_var, check_type):
            raise TypeError(error_helper("Type of {return_or_input} {idx_or_key} should be {type}.", **error_render()))


class strict:
    def __new__(self):
        return strict

    def args(*typeargs: "*[, typearg]", **typekwargs: "**dict(, kw = arg)"):
        def _1(func):
            def _2(*args, **kwargs):

                for arg_idx, (arg, typearg) in enumerate(zip(args, typeargs)):
                    try:
                        _check(arg, typearg, idx=arg_idx)
                    except TypeError as e:
                        raise TypeError(e)

                for key in kwargs:
                    try:
                        _check(kwargs[key], typekwargs[key], key=key)
                    except TypeError as e:
                        raise TypeError(e)

                return func(*args, **kwargs)

            return _2

        return _1

    def ret(*typerets: "*[, typearg]"):
        def _1(func):
            def _2(*args, **kwargs):
                ret = func(*args, **kwargs)

                if len(typerets) > 1:
                    for ret_idx, (ret_i, typeret) in enumerate(zip(ret, typerets)):
                        try:
                            _check(ret_i, typeret, idx=ret_idx)
                        except TypeError as e:
                            raise TypeError(e)
                else:
                    try:
                        _check(ret, typerets[0], idx=0)
                    except TypeError as e:
                        raise TypeError(e)
                return ret
            return _2
        return _1