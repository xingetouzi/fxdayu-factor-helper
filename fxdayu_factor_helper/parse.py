import os
import inspect
import traceback
import pathlib

def execfile(filename, globals, locals):
    return exec(compile(open(filename, "rb").read(), filename, 'exec'), globals, locals)

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
        realpath = pathlib.Path(filename).absolute()
        name = str(realpath).split(os.path.sep)[-1].replace(".py", "")
        author = get_value(loc, "__author__", "未填写因子作者")
        code = inspect.getsource(func)
        doc = inspect.cleandoc(func.__doc__)
        params_info = {}
        for k, v in params.items():
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
    return {
        "result": result,
        "error": error,
        "warnings": warnings, 
    }, bool(result)