import pymysql

# 尝试无密码连接
try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        charset='utf8mb4'
    )
    
    try:
        with connection.cursor() as cursor:
            # 创建数据库
            cursor.execute("CREATE DATABASE IF NOT EXISTS femca_platform")
            print("数据库 'femca_platform' 创建成功或已存在")
            
            # 检查数据库是否创建成功
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]
            print("当前存在的数据库:", databases)
            
    finally:
        connection.close()
        
    print("数据库创建完成！")
    
except Exception as e:
    print(f"无密码连接失败: {e}")
    print("尝试其他方式连接...")
    
    # 尝试使用默认密码
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            charset='utf8mb4'
        )
        
        try:
            with connection.cursor() as cursor:
                # 创建数据库
                cursor.execute("CREATE DATABASE IF NOT EXISTS femca_platform")
                print("数据库 'femca_platform' 创建成功或已存在")
                
                # 检查数据库是否创建成功
                cursor.execute("SHOW DATABASES")
                databases = [db[0] for db in cursor.fetchall()]
                print("当前存在的数据库:", databases)
                
        finally:
            connection.close()
            
        print("数据库创建完成！")
        
    except Exception as e2:
        print(f"使用root密码连接失败: {e2}")
        print("尝试其他方式连接...")
        
        # 尝试使用MySQL Workbench连接
        try:
            import mysql.connector
            
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                auth_plugin='mysql_native_password'
            )
            
            try:
                cursor = connection.cursor()
                cursor.execute("CREATE DATABASE IF NOT EXISTS femca_platform")
                print("数据库 'femca_platform' 创建成功或已存在")
                
                cursor.execute("SHOW DATABASES")
                databases = [db[0] for db in cursor.fetchall()]
                print("当前存在的数据库:", databases)
                
            finally:
                cursor.close()
                connection.close()
                
            print("数据库创建完成！")
            
        except Exception as e3:
            print(f"使用mysql.connector连接失败: {e3}")
            print("无法创建数据库。请检查MySQL安装和配置。")