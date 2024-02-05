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

    (3, '13:00:00', 'Station E', 'Station F', 150.00, '2023-12-18', 4),
    (4, '14:30:00', 'Station G', 'Station H', 80.00, '2023-12-19', 6),
    (5, '16:00:00', 'Station I', 'Station J', 200.00, '2023-12-20', 7),
    (6, '17:30:00', 'Station K', 'Station L', 90.00, '2023-12-21', 5),
    (7, '19:00:00', 'Station M', 'Station N', 110.00, '2023-12-22', 8),
    (8, '20:30:00', 'Station O', 'Station P', 130.00, '2023-12-23', 6),
  
    # Diğer veri girişlerini buraya ekle
]

# Verileri tabloya ekle
for data in sample_data:
    cursor.execute('''
        INSERT INTO route (vehicle_id, time_of_journey, start_station, arrival_station, price, date_of_journey, traveller_count)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', data)

conn.commit()
conn.close()
