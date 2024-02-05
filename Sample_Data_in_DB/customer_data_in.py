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
    (1, 'John', 'Doe', 30, 'Male', '1234567890'),
    (2, 'Emma', 'Smith', 25, 'Female', '9876543210'),
    (3, 'Michael', 'Johnson', 40, 'Male', '5556667777'),
    (4, 'Sophia', 'Williams', 22, 'Female', '1112223333'),
    (5, 'William', 'Brown', 28, 'Male', '9998887777'),
    (6, 'Olivia', 'Jones', 35, 'Female', '4443332222'),
    (7, 'James', 'Garcia', 45, 'Male', '7778889999'),
    (8, 'Ava', 'Martinez', 29, 'Female', '6665554444'),
    (9, 'Alexander', 'Robinson', 33, 'Male', '3334445555'),
    (10, 'Mia', 'Clark', 27, 'Female', '2221110000'),
    # Diğer veri girişlerini buraya ekle
]

# Verileri tabloya ekle
for data in sample_data:
    cursor.execute('''
        INSERT INTO customer (customer_id, customer_name, customer_surname, customer_age, customer_gender, customer_phone)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', data)

conn.commit()
conn.close()
