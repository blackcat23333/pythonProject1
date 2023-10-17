import mysql.connector

def create_table(hostname, username, password, database, table_name):
    # 创建与数据库的连接
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456',
        database='hardware'
    )

    # 创建一个光标对象
    cursor = cnx.cursor()

    # 创建表格的SQL语句
    create_table_query = '''
        CREATE TABLE {} (
            id INT PRIMARY KEY AUTO_INCREMENT,
            CPU VARCHAR(255),
            MAC VARCHAR(255),
            GPU VARCHAR(255),
            MEMORY VARCHAR(255),
            SYSTEMversion VARCHAR(255)
        )
    '''.format(table_name)

    try:
        # 执行SQL语句创建表格
        cursor.execute(create_table_query)
        print("表格创建成功")
    except mysql.connector.Error as err:
        print(f"创建表格失败: {err}")
    finally:
        # 关闭光标和数据库连接
        cursor.close()
        cnx.close()

# 调用函数来创建表格
create_table('localhost', 'root', 'password', 'mydatabase', 'mytable')