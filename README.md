# fxdayu-factor-helper

本模块是帮助fxdayu因子开发的一个模板工具

## 安装
``` bash
pip install git+https://github.com/xingetouzi/fxdayu-factor-helper
```

## 使用
1. 生成因子脚本模板
``` bash
dyfactor generate [FILEPATH]
```
复制因子脚本模板到参数FILEPATH给出的文件中

2. 检查并解析因子脚本文件
``` bash
dyfactor parse [FILENAME]
```
检查参数FILENAME给出的因子脚本文件是否合法，并尝试解析其内容
