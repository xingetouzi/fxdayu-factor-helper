import codecs
from fxdayu_factor_helper.parse import parse_code
import pathlib

example = pathlib.Path(__file__).parent.parent /"fxdayu_factor_helper" / "examples" / "alpha126.py"

if __name__ == "__main__":
    import pprint
    with codecs.open(str(example), encoding="utf-8") as f:
        data, ok = parse_code("alpha126", f.read())
    pprint.pprint(data)
    print(ok)