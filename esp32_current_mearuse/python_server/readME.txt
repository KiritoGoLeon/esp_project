1 安装python3环境, mysql环境
2 mysql新建数据库esp
3 修改config.py里面的mysql数据库地址
4 如果是第一次初始化,需要打开app/init/__init__.py 这个文件DEBUG=True,会自动创建数据库, 如果之后不需要创建数据库, 就设置为DEBUG=False,  不然每次都会全部删除重建