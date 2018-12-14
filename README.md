# aid1808BUG
八阿哥工程组的测试项目,请大家一些测试功能


*使用utf8编码模式
*有部分代码可能使用f的方法格式字符串(python3.6以上才能识别),如果发现了,请大家修改成%s来格式化即可



一.各模块说明
    config.py
        将一些配置文件和全局变量设置于此,便于管理
    manage.py
        非常方便的命令行数据库操作模块
    models.py
        数据库的模型类放置于此
    runserver.py
        服务器启动模块
    view.py
        视图处理函数以及路由函数放置于此

二.文件夹说明
    migrations
        数据库迁移文件,可便捷的将数据库迁移,在命令行操作,不需要进行修改
    static
        静态文件放置于此
    templates
        将所有视图放置于此