import pymysql

try:
    db_host = ''
    db_user = ''
    db_password = ''
    db_name = ''
    conn = pymysql.connect(cursorclass=pymysql.cursors.DictCursor, charset='utf8mb4', host=db_host, user=db_user,
                        password=db_password, db=db_name)
    print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")
except pymysql.MySQLError as e:
    print("Veritabanı bağlantısı başarısız", e)

cursor = conn.cursor()

# Örnek veri
sample_data = [
    (1, 1, 'user1', 'password1'),
    (2, 2, 'user2', 'password2'),
    (3, 3, 'user3', 'password3'),
    (4, 4, 'user4', 'password4'),
    (5, 5, 'user5', 'password5'),
    (6, 6, 'user6', 'password6'),
    (7, 7, 'user7', 'password7'),
    (8, 8, 'user8', 'password8'),
    (9, 9, 'user9', 'password9'),
    (10, 10, 'user10', 'password10'),
    # Diğer veri girişlerini buraya ekle
]

# Verileri tabloya ekle
for data in sample_data:
    cursor.execute('''
        INSERT INTO user (user_id, customer_id, user_name, user_password)
        VALUES (%s, %s, %s, %s)
    ''', data)

conn.commit()
conn.close()
