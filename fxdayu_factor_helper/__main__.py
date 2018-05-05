import os
import inspect
import sys
import traceback
import click

def execfile(filename, globals, locals):
    return exec(compile(open(filename, "rb").read(), filename, 'exec'), globals, locals)

@click.command(short_help="Parse a factor file.", help="Parse factor in file FILEPATH")
@click.argument('filename', type=click.Path(exists=True))
def parse(filename):
    loc = {}
    warns = []
    try:
        execfile(filename, loc, loc)
    except Exception as e:
        print("策略代码执行出错")
        print(traceback.format_exc())
        sys.exit(1)
    def get_value(dct, key, message, default=None, throw=True):
        try:
            return dct[key]
        except KeyError:
            if throw:
                raise RuntimeError(message)
            else:
                warns.append(message)
        return default
    try:
        func = get_value(loc, "run_formula", "未找到因子计算函数run_formula的定义")
        if not func.__doc__:
            raise RuntimeError("因子描述为空")
        params = get_value(loc, "default_params", "未定义因子参数的默认值default_params，如因子没有使用参数，请忽略.",
            default={}, throw=False)
        descriptions = loc.get("params_description", {})
        name = filename.split(os.path.sep)[-1].replace(".py", "")
        author = get_value(loc, "__author__", "未填写因子作者")
        code = inspect.getsource(func)
        doc = inspect.cleandoc(func.__doc__)
        print("因子解析成功")
        print("===========")
        print("因子名称: %s" % name)
        print("因子作者: %s" % author)
        print("因子代码:\n%s" % code)
        print("因子描述:\n%s" % doc)
        print("因子参数:%s" % ("" if params else " 无"))
        for k, v in params:
            try:
                description = descriptions[k]
            except KeyError:
                warns.append("找不到参数%s的描述信息" % k)
                description = "Na"
            print("参数名：%s 默认值：%s 描述：%s" % (k, v, description))
        if warns:
            print("===============")
            print("请注意以下警告：")
        for warn in warns:
            print(warn)
    except Exception as e:
        print("因子解析错误:\n%s" % e)
        sys.exit(1)

@click.command(short_help="Generate a factor template at given path.", help="Generate a factor template at FILEPATH")
@click.argument('filepath', type=click.Path(exists=False))
def generate(filepath):
    f = os.path.join(os.path.dirname(__file__), "alpha126.py")
    if os.path.isfile(filepath):
        yes = input("File %s already exist!\nOverwrite it? (y/N)\n" % os.path.abspath(filepath))
    else:
        yes = 'y'
    if yes.lower() == 'y':
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(f, "rb") as src:
            with open(filepath, "wb") as dst:
                dst.write(src.read())
    else:
        print("Aborted.")


@click.group()
def main():
    pass

main.add_command(parse)
main.add_command(generate)

if __name__ == "__main__":
    main()