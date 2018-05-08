# encoding: utf-8 
# 文件需要以utf-8格式编码
# 文件名代表因子名称，需满足命名规范
__author__ = "xxx" # 这里填下你的名字
default_params = {} # 这里填写因子参数默认值，比如: {"t1": 10}
params_description = {} # 这里填写因子参数描述信息，比如: {"t1": "并没有用上的参数"}

def run_formula(dv, params=default_params):
    """
    这里填写因子的描述信息,详细阐述因子的逻辑，必要时附带公式说明
    """
    name = "alpha126" # 和文件名即因子名一致
    value = dv.add_formula(name, "(close+high+low)/3",
        is_quarterly=False, add_data=True)
    return value
