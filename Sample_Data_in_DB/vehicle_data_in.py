


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
    print("veri tabanı bağlantsııs başarısız", e)

cursor = conn.cursor()
sample_data = [
    ('ABC123', 5, 50000, 10000, 'Company A', 'Sedan'),
    ('DEF456', 7, 70000, 15000, 'Company B', 'SUV'),
    ('GHI789', 4, 30000, 8000, 'Company C', 'Truck'),
    ('JKL012', 6, 60000, 12000, 'Company D', 'Hatchback'),
    ('MNO345', 8, 80000, 20000, 'Company E', 'Minivan'),
    ('PQR678', 3, 40000, 5000, 'Company F', 'Coupe'),
    ('STU901', 5, 45000, 9000, 'Company G', 'Convertible'),
    ('VWX234', 7, 55000, 11000, 'Company H', 'SUV'),
    ('YZA567', 4, 65000, 13000, 'Company I', 'Truck'),
    ('BCD890', 6, 75000, 18000, 'Company J', 'Hatchback'),
    ('EFG123', 3, 85000, 25000, 'Company K', 'Sedan'),
    ('HIJ456', 5, 95000, 30000, 'Company L', 'Coupe'),
    ('KLM789', 4, 55000, 12000, 'Company M', 'Truck'),
    ('NOP012', 6, 65000, 10000, 'Company N', 'Hatchback'),
    ('QRS345', 8, 45000, 8000, 'Company O', 'Minivan'),
    ('TUV678', 4, 35000, 15000, 'Company P', 'Coupe'),
    ('VWX901', 5, 25000, 5000, 'Company Q', 'Sedan'),
    ('YZA234', 7, 15000, 3000, 'Company R', 'SUV'),
    ('BCD567', 6, 20000, 7000, 'Company S', 'Hatchback'),
    ('EFG890', 4, 10000, 2000, 'Company T', 'Coupe'),
    # Diğer veri girişlerini buraya ekle
]

# Verileri tabloya ekle
for data in sample_data:
    cursor.execute('''
        INSERT INTO vehicle (plate, passenger_capacity, vehicle_km, maintain_km, employer, vehicle_type)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', data)

conn.commit()
conn.close()
