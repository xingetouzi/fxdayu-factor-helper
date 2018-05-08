import os
import inspect
import traceback
import pathlib
import json

def execfile(filename, globals, locals):
    return exec(compile(open(filename, "rb").read(), filename, 'exec'), globals, locals)

def _parse(loc, name, code=None):
    result = {}
    error = None
    warnings = []

    def get_value(dct, key, message, default=None, throw=True):
        try:
            return dct[key]
        except KeyError:
            if throw:
                raise RuntimeError(message)
            else:
                warnings.append(message)
        return default
    try:
        func = get_value(loc, "run_formula", "未找到因子计算函数run_formula的定义")
        if not func.__doc__:
            raise RuntimeError("因子描述为空")
        params = get_value(loc, "default_params", "未定义因子参数的默认值default_params，如因子没有使用参数，请忽略.",
            default={}, throw=False)
        descriptions = loc.get("params_description", {})
        author = get_value(loc, "__author__", "未填写因子作者")
        code = code if code is not None else inspect.getsource(func)
        doc = inspect.cleandoc(func.__doc__)
        params_info = {}
        for k, v in params.items():
            try:
                json.dumps(v)
            except Exception:
                raise TypeError("参数%s默认值类型错误,只支持可被json序列化的类型" % k)
            try:
                description = descriptions[k]
            except KeyError:
                warnings.append("找不到参数%s的描述信息" % k)
                description = "Na"
            params_info[k] = {"default": v, "description": description}
        result = {
            "name": name,
            "author": author,
            "func": func,
            "code": code,
            "description": doc,
            "params": params_info
        }
    except Exception:
        error = "因子解析错误:\n%s" % traceback.format_exc()
        result = {}
    return result, error, warnings

def parse_code(name, code):
    loc = {}
    result = {}
    error = None
    warnings = []
    try:
        exec(compile(code, name + ".py", 'exec'), loc, loc)
    except Exception:
        error = "策略代码执行出错:\n%s" % traceback.format_exc()
        return {
            "result": result,
            "error": error,
            "warnings": warnings, 
        }, False
    result, error, warnings = _parse(loc, name, code)
    return {
        "result": result,
        "error": error,
        "warnings": warnings, 
    }, error is None

def parse_file(filename):
    loc = {}
    result = {}
    error = None
    warnings = []
    try:
        execfile(filename, loc, loc)
    except Exception:
        error = "策略代码执行出错:\n%s" % traceback.format_exc()
        return {
            "result": result,
            "error": error,
            "warnings": warnings, 
        }, False
    realpath = pathlib.Path(filename).absolute()
    name = str(realpath).split(os.path.sep)[-1].replace(".py", "")
    result, error, warnings = _parse(loc, name, None)
    return {
        "result": result,
        "error": error,
        "warnings": warnings, 
    }, error is None
