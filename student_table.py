import pymysql

class MySQLHelper:
    def __init__(self,
                 host='localhost',  # 数据库地址
                 user='root',  # 用户名
                 password='',  # 密码
                 database='',  # 数据库名
                 port=3306):  # 端口号
        # 存储连接参数
        self.conn_params = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'port': port,
            'cursorclass': pymysql.cursors.DictCursor  #返回字典格式结果
        }
        self.connection = None

    # 自动连接管理（核心功能）
    def __enter__(self):
        #进入 with 语句时自动连接
        self.connection = pymysql.connect(**self.conn_params)
        return self

    def __exit__(self, *args):
        #退出 with 语句时自动关闭
        if self.connection:
            self.connection.close()

    # 核心方法1：执行查询（SELECT）
    def query(self, sql, params=None):
        #执行查询语句，返回结果列表
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params or ())  # 安全传参
            return cursor.fetchall()  # 获取所有结果

    # 核心方法2：执行写操作
    def execute(self, sql, params=None):
        #执行写操作，返回受影响行数
        with self.connection.cursor() as cursor:
            rows = cursor.execute(sql, params or ())  # 安全传参
            self.connection.commit()
            return rows


# 使用示例(添加一个同学然后查询)
if __name__ == "__main__":
    with MySQLHelper(
            host='localhost',
            user='root',
            password='Qq506582374',
            database='student'
    ) as db:

        # 询问用户输入
        while True:
            try:
                student_id = int(input("请输入新学生ID (整数): "))
                break
            except ValueError:
                print("ID输入无效，请输入一个整数。")

        student_name = input("请输入学生姓名: ")

        while True:
            try:
                student_height = float(input("请输入学生身高 (例如: 175.50): "))
                break
            except ValueError:
                print("身高输入无效，请输入一个数字。")

        # 插入数据
        insert_sql = "INSERT INTO student_table (id, name, height) VALUES (%s, %s, %s)"
        try:
            rows_affected = db.execute(insert_sql, (student_id, student_name, student_height))
            if rows_affected > 0:
                print(f"已成功添加")
            else:
                print("添加学生失败")
        except pymysql.Error as e:
            print(f"数据库操作失败: {e}")


        # 查询数据
        students = db.query("SELECT * FROM student_table")
        for s in students:
            print(f"ID: {s['id']}, 姓名: {s['name']}, 身高: {s['height']}cm")

