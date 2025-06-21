import pymysql
import requests
from bs4 import BeautifulSoup

#数据库的类
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

#爬取电影名
if __name__ == "__main__":
    # 爬取电影数据
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0"}
    content = requests.get("https://movie.douban.com/top250", headers=headers).text
    soup = BeautifulSoup(content, "html.parser")

    movies = []  # 存储电影名的列表
    count = 0

    all_title = soup.findAll("span", attrs={"class": "title"})
    for title in all_title:
        title_string = title.string
        if "/" not in title_string:  # 过滤英文标题
            movies.append(title_string)
            count += 1
            if count >= 10:
                break

    # 存入数据库
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Qq506582374',
        'database': 'student',
        'port': 3306
    }

    # 使用上下文管理器自动处理连接
    with MySQLHelper(**db_config) as db:

        # 插入电影数据
        insert_sql = "INSERT INTO movies (title) VALUES (%s)"
        for title in movies:
            db.execute(insert_sql, (title,))  # 使用参数化查询防止SQL注入
            print(f"已插入: {title}")

        # 验证数量
        count_sql = "SELECT COUNT(*) AS total FROM movies"
        result = db.query(count_sql)
        print(f"\n成功插入 {len(movies)} 条记录，当前共 {result[0]['total']} 条记录")
