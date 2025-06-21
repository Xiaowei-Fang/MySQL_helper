# MySQL_helper
一个Python 类，用于封装常见的 MySQL 数据库操作，使得与 MySQL 交互更加便捷。

# 优势
*   使用上下文管理器 (`with` 语句) 自动管理数据库连接的打开和关闭。
*   查询结果默认以字典列表形式返回，方便按列名访问数据。
*   支持参数化查询，有效防止 SQL 注入。
*   封装了 `SELECT` 查询和 `INSERT/UPDATE/DELETE` 执行操作。

# 用法
首先要有一个名为student的数据库，里面有一个table名为student_table。此表格是一个学生表，包含学生的id，name，height三个字段。我提供了一个文件名为“学生表.txt”，示范了创建数据库，并且对其中的数据进行增删改查的操作，在mysql中运行。

创建完数据库即可执行名为“student_table.py”的python代码。在执行代码后，代码会依次询问需要新添加学生的id，name，height，然后会自动展示添加完成后的table。

# 局限性
在目前的代码中，仅能实现添加学生的操作，如需修改或者删除已添加的学生，需要在mysql中操作，在后续工作中会改善这点。另外，pymysql 支持 executemany() 方法用于批量插入或更新，这比循环调用 execute() 更高效。可以考虑增加一个 execute_many() 方法。

# 爬虫
在文件pachong.py中，定义了一个主程序，利用MysqlHelper这个类，首先从豆瓣电影Top250网站爬取前10个中文电影名，然后将这些电影名批量存入指定的MySQL数据库的movies表中，并在完成后打印出插入的记录数和数据库中的总记录数。
