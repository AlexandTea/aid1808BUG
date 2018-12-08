"""
    这是服务器启动模块,用于服务器的启动
"""

# RegexConverter用于正则表达式匹配动态路由的设置
from config import *

# 导入路由映射路径,新增路由必须在此导入
from views import *








if __name__ == '__main__':
    app.run(debug=True,port=PORT,host=HOST)