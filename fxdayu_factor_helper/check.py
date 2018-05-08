import sys
import traceback

from fxdayu_factor_helper.parse import parse_file
from fxdayu_factor_helper.utils import get_data_root

def _handle_import_exception(e):
    print("要运行因子测试，请先确保安装jaqs_fxdayu!")
    raise e

def get_dv(start = 20170101,end = 20180101):
    import warnings
    warnings.filterwarnings("ignore")
    try:
        import jaqs_fxdayu
        jaqs_fxdayu.patch_all()
        from jaqs.data import DataView
        from jaqs_fxdayu.data.dataservice import LocalDataService
    except ImportError as e:
        _handle_import_exception(e)

    ds = LocalDataService(fp = get_data_root())
    
    ZZ800_id = ds.query_index_member("000906.SH", start, end)
    stock_symbol = list(set(ZZ800_id))
    
    dv_props = {'start_date': start, 'end_date': end, 'symbol':','.join(stock_symbol),
             'fields': "",
             'freq': 1,
             "prepare_fields": True}
    
    dv = DataView()
    dv.init_from_config(dv_props, data_api=ds)
    dv.prepare_data()
    return dv

def check(factor, data):
    """
    check the factor output
    """
    import pandas as pd
    if not isinstance(data, pd.core.frame.DataFrame):
        raise TypeError('On factor {} ,output must be a pandas.DataFrame!'.format(factor))
    else:
        try:
            index_name = data.index.names[0]
            columns_name = data.index.names[0]
        except:
            if not (index_name in ['trade_date','report_date'] and columns_name == 'symbol'):
                raise NameError('''Error index name,index name must in ["trade_date","report_date"],columns name must be "symbol" ''')
                
        index_dtype = data.index.dtype_str
        columns_dtype = data.columns.dtype_str
        
        if columns_dtype not in ['object','str']:
            raise TypeError('error columns type')
            
        if index_dtype not in ['int32','int64','int']:
            raise TypeError('error index type')

def check_file(filepath):
    """
    Check a factor in given file
    """
    data, ok = parse_file(filepath) 
    try:
        if not ok:
            error = data["error"]
            raise RuntimeError("因子解析错误: %s,请先运行dyfactor parse尝试解析因子" % error)
        name = data["result"]["name"]
        func = data["result"]["func"]
        check(name, func(get_dv()))
    except Exception:
        return False, traceback.format_exc()
    return True, "%s OK!" % name