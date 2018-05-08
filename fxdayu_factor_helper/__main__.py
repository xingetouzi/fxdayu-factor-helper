import os
import inspect
import sys
import traceback
import click
from concurrent import futures

from fxdayu_factor_helper.parse import parse_file
from fxdayu_factor_helper.check import check_file
from fxdayu_factor_helper.utils import get_default_data_root, set_data_root

def execfile(filename, globals, locals):
    return exec(compile(open(filename, "rb").read(), filename, 'exec'), globals, locals)

@click.command(short_help="Parse a factor file.", help="Parse factor in file FILEPATH")
@click.argument('filename', type=click.Path(exists=True))
def parse(filename):
    data, ok = parse_file(filename)
    if ok:
        result = data["result"] 
        params = result["params"]
        print("因子解析成功")
        print("===========")
        print("因子名称: %s" % result["name"])
        print("因子作者: %s" % result["author"])
        print("因子代码:\n%s" % result["code"])
        print("因子描述:\n%s" % result["description"])
        print("因子参数:%s" % ("" if params else " 无"))
        for k, v in params.items():
            print("参数名：%s 默认值：%s 描述：%s" % (k, v["default"], v["description"]))
    error = data["error"] 
    if error:
        print(error)
    warnings = data["warnings"]
    if warnings:
        print("===============")
        print("请注意以下警告：")
        for warn in warnings:
            print(warn)
    if not ok:
        sys.exit(1)


@click.command(short_help="Generate a factor template at given path.", help="Generate a factor template at FILEPATH")
@click.argument('filepath', type=click.Path(exists=False))
def generate(filepath):
    filepath = os.path.abspath(filepath)
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


def do_check_file(filepath, data_dir):
    set_data_root(data_dir)
    return check_file(filepath)

@click.command(help="Run check for a factor", short_help="Run calulation of factor in FILEPATH, and check the output.")
@click.argument('filepath', type=click.Path(exists=True))
@click.option("--data-dir", "-d", help="The data dir, default %s" % get_default_data_root())
@click.option("--output", "-o", type=click.Path(exists=False), help="Write output the to given file.")
@click.option("--concurrent", "-c", type=click.INT, help="Concurrent pool number.")
def check(filepath, data_dir, output, concurrent):
    all_ok = True
    success = []
    failed = []
    results = []
    
    def handle_check_file(ok, msg, file):
        nonlocal all_ok
        all_ok = all_ok and ok
        if not ok:
            failed.append(file)
            print("Check factor in file %s\nCheck failed:\n%s" % (file, msg))
        else:
            success.append(file)
            print("Check factor in file %s\nCheck success: %s" % (file, msg))
        if output:
            dct = {"file": file, "result": "OK" if ok else "FAILED", "message": msg}
            results.append(dct)

    files = []
    if os.path.isdir(filepath):
        for file in os.listdir(filepath):
            if file.endswith(".py"):
                files.append(os.path.join(filepath, file))
    elif os.path.isfile(filepath):
       files.append(filepath)
    max_workers = concurrent or os.cpu_count()
    with futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {executor.submit(do_check_file, file, data_dir): file for file in files}
        for future in futures.as_completed(future_to_file):
            file = future_to_file[future]
            ok, msg = future.result()
            handle_check_file(ok, msg, file)

    print("==============")
    print("SUCCESS:")
    for f in success:
        print(f)
    print("==============")
    print("FAILED:")
    for f in failed:
        print(f)
    if output:
        import pandas as pd
        df = pd.DataFrame(results, columns=["file", "result", "message"])
        df.to_csv(output, index=False)
    if not all_ok:
        sys.exit(1)

@click.group()
def main():
    pass

main.add_command(parse)
main.add_command(generate)
main.add_command(check)

if __name__ == "__main__":
    main()