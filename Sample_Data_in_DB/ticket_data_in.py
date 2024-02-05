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
    (1, 1, 1, 1),
    (2, 2, 2, 2),
    (3, 3, 3, 3),
    (4, 4, 4, 4),
    (5, 5, 5, 5),
    (6, 6, 6, 6),
    (7, 7, 7, 7),
    (8, 8, 8, 8),
    (9, 9, 9, 9),
    (10, 10, 10, 10),
    # Diğer veri girişlerini buraya ekle
]

# Verileri tabloya ekle
for data in sample_data:
    cursor.execute('''
        INSERT INTO ticket (ticket_id, route_id, customer_id, seat_no)
        VALUES (%s, %s, %s, %s)
    ''', data)

conn.commit()
conn.close()
