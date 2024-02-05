import os
import re
from flask import Flask, flash, jsonify, render_template, request, redirect, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import *
import pymysql
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_info' not in session:
            return redirect(url_for('user_login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('Admin girişi gereklidir!', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def check_admin(username, password):
    conn = DatabaseConnection()

    if conn:
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM admin WHERE admin_username = %s AND admin_password = %s"
                cursor.execute(sql, (username, password))
                result = cursor.fetchone()

                if result:  # Eşleşme varsa giriş başarılı
                    return True
                else:
                    return False

        except pymysql.MySQLError as e:
            print("Sorgu hatası:", e)
        finally:
            conn.close()

    return False

#return lastrowid eklendi kullanımı herhangi bir şekilde değişmedi sadece ekleen son satırın idsi return edilip kullanılabilir -mert 
#avaible tickets sorgusu değişmedi hala çalışıyor sorunsuz test edildi -mert
def add_row_to_table(table_name, values):
    """
    Bir tabloya yeni bir satır ekler.

    Args:
    table_name (str): Satırın ekleneceği tablo adı.
    values (dict): Eklenecek satırın değerleri (sütun adı: değer).

    Returns:
    int: Eklenen satırın ID'si
    """
    conn = DatabaseConnection()

    try:
        with conn.cursor() as cursor:
            placeholders = ', '.join(['%s'] * len(values))
            columns = ', '.join(values.keys())
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, list(values.values()))
            conn.commit()
            print("Row added successfully.")

            # Eklenen satırın ID'sini döndür
            return cursor.lastrowid

    except Exception as e:
        print(f"Error adding row to {table_name}: {e}")
    finally:
        conn.close()

def delete_row_from_table(tablo_adi, kosul_sutunu, kosul_degeri):
    """
    Belirli bir koşula göre tablodan satırları siler.

    Argümanlar:
    tablo_adi (str): Satırların silineceği tablo adı.
    kosul_sutunu (str): Silme işlemi için kullanılacak olan sütun adı.
    kosul_degeri (str): Silme işlemi için kullanılacak olan sütundaki değer.
    """

    conn = DatabaseConnection()

    try:
        with conn.cursor() as cursor:
            # Silme işlemi için SQL sorgusunu oluştur
            sql = f"DELETE FROM {tablo_adi} WHERE {kosul_sutunu} = %s"
            # Belirtilen koşul değeri ile sorguyu çalıştır
            cursor.execute(sql, (kosul_degeri,))
            conn.commit()
            # Başarı mesajı göster
            print(
                f"{kosul_sutunu}={kosul_degeri} koşuluyla satır(lar) başarıyla silindi.")

    except Exception as e:
        # Silme işlemi sırasında oluşan herhangi bir hatayı yakala
        print(f"{tablo_adi} tablosundan satır silinirken hata oluştu: {e}")
    finally:
        # İşlem sonrası bağlantıyı kapat
        conn.close()

def update_row_from_table(table_name, row_id, values):
    """
    Bir tablodaki mevcut bir satırı günceller.

    Args:
    table_name (str): Satırın güncelleneceği tablo adı.
    row_id (int): Güncellenecek satırın kimliği.
    values (dict): Güncellenecek satırın yeni değerleri (sütun adı: değer).

    Returns:
    None
    """
    conn = DatabaseConnection()

    try:
        with conn.cursor() as cursor:
            update_values = ', '.join([f"{key} = %s" for key in values.keys()])
            sql = f"UPDATE {table_name} SET {update_values} WHERE {table_name}_id = %s"
            cursor.execute(sql, list(values.values()) + [row_id])
            conn.commit()
            print("Row updated successfully.")

    except Exception as e:
        print(f"Error updating row in {table_name}: {e}")
    finally:
        conn.close()

def DatabaseConnection():
    try:
        db_host = ''
        db_user = ''
        db_password = ''
        db_name = ''
        conn = pymysql.connect(cursorclass=pymysql.cursors.DictCursor, charset='utf8mb4', host=db_host, user=db_user,
                               password=db_password, db=db_name)
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")
        return conn  # Bağlantıyı döndür
    except pymysql.MySQLError as e:
        print("veri tabanı bağlantsııs başarısız", e)
        return None

#kendim kullanmak için attım maine -mert
def get_tables():
    """
    Tabloları getirir.

    Returns:
    list: Tablo adlarını içeren liste
    """
    conn = DatabaseConnection()

    tables = []

    try:
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables_result = cursor.fetchall()

            for table in tables_result:
                tables.append(table[list(table.keys())[0]])  # İlk sütunu alır

    except Exception as e:
        print("Tabloları alma hatası:", e)
    finally:
        conn.close()
    print(tables)
    return tables

def get_table_rows(tablename):
    """
    Tablo satırlarını getirir.

    Args:
    tablename (str): Tablo adı

    Returns:
    list: Tablo satırlarını içeren liste
    """
    
    rows = []
    conn = DatabaseConnection()
    
    try:
        with conn.cursor() as cursor:
            sql = f"SELECT * FROM {tablename}"
            cursor.execute(sql)
            rows = cursor.fetchall()
            
    except Exception as e:
        print("Sorgu hatası:", e)
    finally:
        conn.close()
    #print(rows)
    return rows

#kendim kullanmak için attım maine -mert
def merge_tables(table1, table2, common_columns, id_column):
    """
    İki tabloyu belirli ortak sütunlara göre birleştirir.

    Args:
    table1 (list): Birleştirilecek ilk tablo
    table2 (list): Birleştirilecek ikinci tablo
    common_columns (list): Ortak sütunlar listesi
    id_column (str): Birleştirme sonucu oluşacak listedeki benzersiz kimlik sütunu adı.

    Returns:
    list: Birleştirilmiş tabloyu içeren liste.
    """
    merged_table = []

    for row1 in table1:
        for row2 in table2:
            if all(row1[col] == row2[col] for col in common_columns):
                merged_row = {**row1, **row2}
                merged_row[id_column] = row1[id_column]
                merged_table.append(merged_row)

    return merged_table

def update_traveller_count(route_id, operation='increase'):
    """
    Rotadaki yolcu sayısını günceller.

    Args:
    route_id (int): Güncellenecek rota kimliği.
    operation (str): 'increase' veya 'decrease' olabilen işlem adı.

    Returns:
    None
    """
    conn = DatabaseConnection()

    try:
        with conn.cursor() as cursor:
            # Get the current traveller_count for the route
            cursor.execute("SELECT traveller_count FROM route WHERE route_id = %s", (route_id,))
            current_count = cursor.fetchone()

            if current_count:
                if operation == 'increase':
                    new_count = current_count['traveller_count'] + 1
                elif operation == 'decrease':
                    new_count = current_count['traveller_count'] - 1
                else:
                    print("Invalid operation specified.")
                    return

                # Update the traveller_count for the route
                cursor.execute("UPDATE route SET traveller_count = %s WHERE route_id = %s", (new_count, route_id))
                conn.commit()
                print(f"Traveller count for route_id={route_id} {operation}d successfully.")

    except Exception as e:
        print(f"Error {operation}ing traveller count: {e}")
    finally:
        conn.close()

def get_available_seats(vehicle_id):
    """
    Belirli bir araç için kullanılabilir koltukları getirir.

    Args:
    vehicle_id (int): Araç kimliği.

    Returns:
    list: Kullanılabilir koltuk numaralarını içeren liste.
    """

    conn = DatabaseConnection()
    available_seats = []

    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT passenger_capacity FROM vehicle WHERE vehicle_id = %s
            """
            cursor.execute(sql, (vehicle_id,))
            result = cursor.fetchone()

            if result:
                total_seats = result['passenger_capacity']

                sql = """
                    SELECT seat_no FROM ticket WHERE route_id = %s
                """
                cursor.execute(sql, (vehicle_id,))
                sold_seats = [row['seat_no'] for row in cursor.fetchall()]

                available_seats = [seat for seat in range(1, total_seats + 1) if seat not in sold_seats]

    except Exception as e:
        print(f"Hata: {e}")
    finally:
        conn.close()

    return available_seats

def get_sold_tickets_for_route(route_id):
    """
    Belirli bir rota için satılan biletleri getirir.

    Args:
    route_id (int): Rota kimliği.

    Returns:
    list: Satılan biletleri içeren liste.
    """
    conn = DatabaseConnection()
    sold_tickets = []

    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM ticket WHERE route_id = %s"
            cursor.execute(sql, (route_id,))
            sold_tickets = cursor.fetchall()

    except Exception as e:
        print(f"Hata: {e}")
    finally:
        conn.close()

    return sold_tickets

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        route_rows = get_table_rows('route')
        arrival_stations = set()
        start_stations = set()

        for row in route_rows:
            arrival_stations.add(row['arrival_station'])
            start_stations.add(row['start_station'])

        return render_template("index.html", arrival_stations=arrival_stations, start_stations=start_stations)
    else:
        starting_station = request.form.get("starting_station")
        if not starting_station:
            return apology("You have to choose a starting station!")

        arrival_station = request.form.get("destination")
        if not arrival_station:
            return apology("You have to choose a destination!")

        # contains only routes that have the starting_station and arrival_station and valid dates
        filtered_routes = []
        # flag = false if there is no matching ticket, flag = true if there is
        flag = False

        route_rows = get_table_rows("route")
        vehicle_rows = get_table_rows("vehicle")
        merged_tables = merge_tables(route_rows, vehicle_rows, ['vehicle_id'], 'vehicle_id')

        for row in merged_tables:
            #if starting_station in row.values() and arrival_station in row.values():
            if row['start_station'] == starting_station and row['arrival_station'] == arrival_station and row['traveller_count'] < row['passenger_capacity']:
                # Validate the date_of_journey for the route
                date_of_journey = row.get("date_of_journey")  # Assuming the date is a datetime.date object
                if date_of_journey:
                    date_of_journey_str = date_of_journey.strftime('%Y-%m-%d')  # Convert date to string
                    date_of_journey = datetime.strptime(date_of_journey_str, '%Y-%m-%d')
                    if date_of_journey >= datetime.now():  # Check if date is valid and not in the past
                        filtered_routes.append(row)
                        flag = True

        if flag:
            # Now, let's check available seats within the context of filtered routes
            for ticket in filtered_routes:
                sold_tickets = get_sold_tickets_for_route(ticket['route_id'])
                sold_seats = [ticket['seat_no'] for ticket in sold_tickets]

                available_seats = get_available_seats(ticket['vehicle_id'])
                available_seats = [seat for seat in available_seats if seat not in sold_seats]

            return render_template("available_tickets.html", places=filtered_routes)
        else:
            flash("Unfortunately, such a ticket does not exist or has an invalid date :(")
            return redirect("/")

@app.route("/available_tickets", methods=["GET", "POST"])
@login_required
def available_tickets():
    """Show Available Tickets"""

    if request.method == "GET":
        return render_template("available_tickets.html")
    else:
        route_id = request.form.get("buy_button")
        return redirect(url_for("select_seat", route_id=route_id))

@app.route("/select_seat", methods=["GET", "POST"])
@login_required
def select_seat():
    if request.method == 'GET':
        route_id = int(request.args.get("route_id"))

        route_rows = get_table_rows("route")
        vehicle_rows = get_table_rows("vehicle")
        merged_tables = merge_tables(route_rows, vehicle_rows, ['vehicle_id'], 'vehicle_id')

        for row in merged_tables:
            if route_id == row["route_id"]:
                ticket = row 
        sold_tickets = get_sold_tickets_for_route(route_id)  # Seçilen rotadaki daha önce satılan biletleri al
        sold_seats = [ticket['seat_no'] for ticket in sold_tickets]

        # Araç tipi için tüm mevcut koltukları al
        available_seats = get_available_seats(ticket['vehicle_id'])
        available_seats = [seat for seat in available_seats if seat not in sold_seats]
        
        passenger_capacity = 0
        for row in vehicle_rows:
            if row['vehicle_id'] == ticket['vehicle_id']:
                passenger_capacity = row['passenger_capacity']

        #print(sold_seats)
        #print(available_seats)
        #print(passenger_capacity)
        return render_template("select_seat.html", row=ticket, passenger_capacity=passenger_capacity, booked_seats=sold_seats)
   

    elif request.method == 'POST':
        user_info = session.get('user_info')
        if user_info:
            route_id = request.form.get("route_id")
            seat_number = int(request.form.get("seat_no"))
            sold_tickets = get_sold_tickets_for_route(route_id)
            sold_seats = [ticket['seat_no'] for ticket in sold_tickets]
            if seat_number in sold_seats:
                return apology("Unfortunately, this seat is already taken :(")
            
            if route_id is not None:
                route_id = int(route_id)

                new_ticket = {
                    "route_id": route_id,
                    "customer_id": user_info["customer_id"],
                    "seat_no": seat_number
                }

                new_ticket_id = add_row_to_table("ticket", new_ticket)

                if new_ticket_id:
                    print(f"Yeni bilet eklendi, ID: {new_ticket_id}")
                    update_traveller_count(route_id,operation='increase')
                    flash("Purchase successful!")
                    return redirect(url_for("my_tickets"))
                else:
                    print("Bilet eklenemedi.")
                    # Hata durumunu ele al
            else:
                # route_id None ise burada ele alabilirsin
                pass
        else:
            # Kullanıcı bilgisi None ise burada ele alabilirsin
            pass

    return redirect(url_for("index"))

@app.route("/my_tickets", methods=["GET", "POST"])
def my_tickets():
    conn = DatabaseConnection()
    user_info = session.get("user_info")
    with conn.cursor() as cursor:
        if request.method == "GET":
            cursor.execute("SELECT ticket.ticket_id, customer.customer_name, customer.customer_surname,"
                           " customer.customer_age, customer.customer_gender, customer.customer_phone,"
                           " route.start_station, route.arrival_station, route.date_of_journey, route.time_of_journey,"
                           " ticket.seat_no FROM ticket"
                           " JOIN customer ON ticket.customer_id = customer.customer_id"
                           " JOIN route ON route.route_id = ticket.route_id"
                           " WHERE customer.customer_id = %s", user_info["customer_id"])
            ticket_info = cursor.fetchall()

            return render_template("my_tickets.html", ticket_info=ticket_info)
        else:
            delete_button = request.form.get("delete_button")

            cursor.execute("SELECT ticket.route_id FROM ticket "
                           " WHERE ticket.ticket_id = %s", delete_button)
            route_id = cursor.fetchone()
            update_traveller_count(route_id, "decrease")

            cursor.execute("DELETE FROM ticket WHERE ticket_id = %s", delete_button)
            conn.commit()

            flash("Ticket cancelled successfully!")
            return redirect("/my_tickets")

@app.route('/about')
def about():
    return render_template('about.html')


@app.route("/admin_panel", methods=["GET"])
@admin_required
def admin_panel():
    # Her tablodan verilerin alınması
    route_rows = get_table_rows('route')
    vehicle_rows = get_table_rows('vehicle')
    ticket_rows = get_table_rows('ticket')
    customer_rows = get_table_rows('customer')
    user_rows = get_table_rows('user')
    admin_rows=get_table_rows('admin')
    current_date = datetime.now()

    # Tabloların birleştirilmesi için ortak sütunlar ve birleştirme işlemi
    ortak_sutunlar_route_vehicle = ['vehicle_id']
    ortak_sutunlar_route_ticket = ['route_id']
    ortak_sutunlar_ticket_customer = ['customer_id']

    birlesik_veri_route_vehicle = merge_tables(route_rows, vehicle_rows, ortak_sutunlar_route_vehicle, 'route_id')
    birlesik_veri_route_ticket = merge_tables(birlesik_veri_route_vehicle, ticket_rows, ortak_sutunlar_route_ticket, 'route_id')
    birlesik_veri = merge_tables(birlesik_veri_route_ticket, customer_rows, ortak_sutunlar_ticket_customer, 'customer_id')
    combined_user_customer = merge_tables(user_rows, customer_rows, ['customer_id'], 'customer_id')
    # Şimdi birleştirilmiş veri tüm sütun değerlerini içeriyor


    return render_template("admin_panel.html",current_date=current_date,admin_rows=admin_rows,vehicle_rows=vehicle_rows,birlesik_veri_route_vehicle=birlesik_veri_route_vehicle,combined_user_customer=combined_user_customer,birlesik_veri=birlesik_veri)


@app.route('/route')
@admin_required
def route():


    # Route ve vehicle tablolarından verileri çekme
    route_rows = get_table_rows('route')
    vehicle_rows = get_table_rows('vehicle')
    current_date = datetime.now()
    # Tabloları birleştirme
    combined_data = merge_tables(route_rows, vehicle_rows, ['vehicle_id'], 'route_id')

    # Verileri HTML sayfasına aktarma
    return render_template('route.html',current_date=current_date, combined_data=combined_data)


@app.route('/add_route', methods=['GET', 'POST'])
@admin_required
def add_route():
    if request.method == 'GET':
        # Öncelikle, veritabanından araç bilgilerini alalım
        vehicles = get_table_rows('vehicle')  # vehicle tablosundaki araçları al

        return render_template('add_route.html', vehicles=vehicles)  # Şablonu ve araçları göndererek sayfayı render et

    # POST isteği geldiğinde form verilerini işle
    vehicle_id = request.form['vehicle_id']
    time_of_journey = request.form['time_of_journey']
    start_station = request.form['start_station']
    arrival_station = request.form['arrival_station']
    price = request.form['price']
    date_of_journey = request.form['date_of_journey']
    traveller_count = 0

    values = {
        'vehicle_id': vehicle_id,
        'time_of_journey': time_of_journey,
        'start_station': start_station,
        'arrival_station': arrival_station,
        'price': price,
        'date_of_journey': date_of_journey,
        'traveller_count': traveller_count
    }

    # Yeni rota ekleme işlemi
    new_route_id = add_row_to_table('route', values)

    if new_route_id:
        flash('New route added successfully!', 'success')
        return redirect(url_for('route'))  # Yeni eklenen rotanın detaylarına gitmek
    else:
        flash('Failed to add route. Please try again.', 'error')
        return redirect(url_for('error_page'))  # Hata sayfasına yönlendirme yapılabilir

@app.route('/vehicle')
@admin_required
def vehicle():
    # Vehicle tablosundan verileri çekme
    vehicle_rows = get_table_rows('vehicle')

    # Verileri HTML sayfasına aktarma
    return render_template('vehicle.html', vehicle_rows=vehicle_rows)

@app.route('/add_vehicle', methods=['GET', 'POST'])
@admin_required
def add_vehicle():
    if request.method == 'GET':
        return render_template('add_vehicle.html')  # Varsayılan olarak formun gösterildiği sayfa

    # POST isteği geldiğinde form verilerini işleme kodları
    plate = request.form['plate']
    passenger_capacity = request.form['passenger_capacity']
    vehicle_km = request.form['vehicle_km']
    maintain_km = request.form['maintain_km']
    employer = request.form['employer']
    vehicle_type = request.form['vehicle_type']
    next_maintain_date = request.form['next_maintain_date']
    last_maintain_date = request.form['last_maintain_date']
    values = {
        'plate': plate,
        'passenger_capacity': passenger_capacity,
        'vehicle_km': vehicle_km,
        'maintain_km': maintain_km,
        'employer': employer,
        'vehicle_type': vehicle_type,
        'next_maintain_date': next_maintain_date,
        'last_maintain_date': last_maintain_date
    }

    # Eklenen satırın ID'sini almak için add_row_to_table fonksiyonunu kullan
    new_vehicle_id = add_row_to_table('vehicle', values)

    if new_vehicle_id:
        flash('New vehicle added successfully!', 'success')
        return redirect(url_for('vehicle') ) # Örneğin, yeni aracın detaylarına gitmek
    else:
        flash('Failed to add vehicle. Please try again.', 'error')
        return redirect(url_for('error_page'))  # Eğer bir hata oluştuysa, bir hata sayfasına yönlendirme yapılabilir

@app.route('/customer')
@admin_required
def customer():
    customer_rows = get_table_rows('customer')
    user_rows = get_table_rows('user')
    combined_user_customer = merge_tables(user_rows, customer_rows, ['customer_id'], 'customer_id')
    return render_template('customer.html', combined_user_customer=combined_user_customer)

@app.route('/add_customer_user', methods=['GET', 'POST'])
@admin_required
def add_customer_user():
    if request.method == 'POST':
        # Formdan gelen verileri al
        customer_name = request.form['customer_name']
        customer_surname = request.form['customer_surname']
        customer_age = request.form['customer_age']
        customer_gender = request.form['customer_gender']
        customer_phone = request.form['customer_phone']
        user_name = request.form['user_name']
        user_password = request.form['user_password']

        # Müşteri tablosuna ekle
        customer_values = {
            'customer_name': customer_name,
            'customer_surname': customer_surname,
            'customer_age': customer_age,
            'customer_gender': customer_gender,
            'customer_phone': customer_phone
        }
        customer_id = add_row_to_table('customer', customer_values)

        # Kullanıcı tablosuna ekle
        user_values = {
            'customer_id': customer_id,
            'user_name': user_name,
            'user_password': user_password
        }
        user_id = add_row_to_table('user', user_values)

        if customer_id and user_id:
            # Ekleme başarılıysa başka bir sayfaya yönlendir
            return redirect(url_for('customer'))  # Örnek olarak 'customer' sayfasına yönlendiriyoruz
        else:
            # Hata durumunda bir şeyler yapabiliriz, şu an için sadece bir mesaj döndürelim
            return "Ekleme başarısız oldu."
    else:
        # Eğer POST metodu kullanılmıyorsa (örneğin, GET isteği) ekleme formunu göster
        return render_template('add_customer_user.html')  # İlgili HTML dosyasının adını kullanmalısınız

@app.route('/ticket')
@admin_required
def ticket():
    # Tablo satırlarını getirme
    ticket_rows = get_table_rows('ticket')
    route_rows = get_table_rows('route')
    vehicle_rows = get_table_rows('vehicle')
    customer_rows = get_table_rows('customer')
    # Tabloları birleştirme
    combined_ticket_details = merge_tables(ticket_rows, route_rows, ['route_id'], 'route_id')
    combined_ticket_details = merge_tables(combined_ticket_details, vehicle_rows, ['vehicle_id'], 'vehicle_id')
    combined_ticket_details = merge_tables(combined_ticket_details, customer_rows, ['customer_id'], 'customer_id')
    current_date = datetime.now()
    return render_template('ticket.html',current_date=current_date, combined_ticket_details=combined_ticket_details)

#add_tşcket fonksiyonu çalışıyor
@app.route('/add_ticket', methods=['GET', 'POST'])
@admin_required
def add_ticket():
    if request.method == 'POST':
        route_id = request.form['route_id']
        customer_id = request.form['customer_id']
        seat_no = request.form['seat_no']  # Capture seat_no from form data

        new_ticket = {
            'route_id': route_id,
            'customer_id': customer_id,
            'seat_no': seat_no  # Include seat_no in the new ticket data
        }

        # Rest of your code to add the ticket to the database

   
        # Veritabanına yeni bilet ekleme
        ticket_id = add_row_to_table('ticket', new_ticket)
        if ticket_id:
            return f'Ticket added successfully. Ticket ID: {ticket_id}'
        else:
            return 'Failed to add ticket'
    else:
        routes = get_table_rows('route')
        
        customers = get_table_rows('customer')
        
        return render_template('add_ticket.html', routes=routes,  customers=customers)

#tablodaki satırlar üzerinde işlem yapmak için gerekli routerlar
@app.route('/delete_row/<table_name>/<column_name>/<row_id>', methods=['POST'])
@admin_required
def delete_row(table_name, column_name, row_id):
    conn = DatabaseConnection()
    if table_name == 'ticket':
        # Extract the route_id associated with the ticket
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT route_id FROM {table_name} WHERE {column_name} = %s", (row_id,))
                result = cursor.fetchone()
                if result:
                    route_id = result['route_id']
                    update_traveller_count(route_id,operation='decrease') 
        except Exception as e:
            print(f"Error while fetching route_id: {e}")
        finally:
            conn.close()
    if table_name == 'customer':
        try:
            delete_row_from_table("user","customer_id", row_id)
            delete_row_from_table("customer","customer_id", row_id)
            
        except Exception as e:
            print(f"Error deleting rows: {e}")
        finally:
            conn.close()
            
    delete_row_from_table(table_name, column_name, row_id)
    flash('Row deleted successfully!', 'success')
    return redirect(url_for('previous_page', table_name=table_name))

#tablodaki satırlar üzerinde işlem yapmak için gerekli routerlar
@app.route('/add_row/<table_name>', methods=['GET', 'POST'])
@admin_required
def add_row(table_name):
    conn = DatabaseConnection()

    if request.method == 'POST':
        form_data = request.form.to_dict()
        add_row_to_table(table_name, form_data)
        flash('Satır başarıyla eklendi!', 'success')
        return redirect(url_for('previous_page', table_name=table_name))
    columns = []  # Sütunları tutacak bir liste
    if conn:
        try:
            with conn.cursor() as cursor:
                # Seçilen tablonun sütunlarını al
                cursor.execute(f"SHOW COLUMNS FROM {table_name}")
                columns_data = cursor.fetchall()
                columns = [column['Field'] for column in columns_data]

        except Exception as e:
            print("Sütun bilgisi alınamadı:", e)
        finally:
            conn.close()

    return render_template('add_row.html', table_name=table_name, columns=columns, form_data={})

@app.route('/previous_page/<table_name>')
def previous_page(table_name):
    if table_name=="admin":
        return redirect(url_for("admin_panel"))
    if table_name=="user":
        return redirect(url_for("customer"))  
    # Eğer belirtilen table_name ile ilişkili bir önceki sayfa yoksa, varsayılan bir sayfaya yönlendir
    return redirect(url_for(table_name))

#tablodaki satırlar üzerinde işlem yapmak için gerekli routerlar
@app.route('/edit_row/<table_name>/<row_id>', methods=['GET', 'POST'])
@admin_required
def edit_row(table_name, row_id):
    conn = DatabaseConnection()

    if request.method == 'POST':
        form_data = request.form.to_dict()
        update_row_from_table(table_name, row_id, form_data)
        flash('Satır başarıyla güncellendi!', 'success')
        return redirect(url_for('previous_page', table_name=table_name))

    columns = []  # Sütunları tutacak bir liste
    row_data = {}  # Satır verilerini tutacak bir sözlük
    if conn:
        try:
            with conn.cursor() as cursor:
                # Seçilen tablonun sütunlarını al
                cursor.execute(f"SHOW COLUMNS FROM {table_name}")
                columns_data = cursor.fetchall()
                columns = [column['Field'] for column in columns_data]

                # Seçilen satırın mevcut verilerini al
                cursor.execute(f"SELECT * FROM {table_name} WHERE {table_name}_id = %s", (row_id,))
                row_data = cursor.fetchone()

        except Exception as e:
            print("Veri alınamadı:", e)
        finally:
            conn.close()

    return render_template('edit_row.html', table_name=table_name, columns=columns, row_data=row_data)

@app.route('/save_to_csv/<table_name>', methods=['POST'])
@admin_required
def save_to_csv(table_name):
    # Fetch table_name from route parameter
    
    # Retrieve rows using get_table_rows function (implementation not provided)
    rows = get_table_rows(table_name)  
    
    # Rest of your CSV-saving logic here
    if rows:
        current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


        folder_name = 'table_data'
        
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        
        filename = f"{folder_name}/{table_name}_{current_datetime}.csv"

        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        
        return jsonify({'success': True, 'filename': filename})  # Return success message and filename
    else:
        return jsonify({'success': False, 'message': 'Table not found'})

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if check_admin(username, password):  # Veritabanında admin var mı kontrol et
            session['admin_logged_in'] = True
            flash('Başarıyla giriş yaptınız!', 'success')
            return redirect(url_for('admin_panel'))
        else:
            flash('Geçersiz kullanıcı adı veya şifre!', 'error')

    return render_template('admin_login.html')

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)  # Oturumu sonlandır
    flash('Başarıyla çıkış yaptınız.', 'success')
    return redirect(url_for('admin_login'))

#üye girişi yapıldığında bilgiler db den ilgili userin customer bilgileri çekilip sessiona atanıyor -mert
@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    
    if request.method == 'POST':
        conn = DatabaseConnection()
        username = request.form['username']
        password = request.form['password']

        with conn.cursor() as cursor:
            # Kullanıcı adı ve şifreyi veritabanında kontrol et
            sql = "SELECT * FROM user WHERE user_name = %s"
            cursor.execute(sql, username)
            user = cursor.fetchone()

            if user and check_password_hash(user["user_password"], password):
                # Kullanıcı var, oturumu başlat
                user_id = user['user_id']
                # Kullanıcıya ait müşteri bilgilerini al
                sql_customer = "SELECT * FROM customer WHERE customer_id = (SELECT customer_id FROM user WHERE user_id = %s)"
                cursor.execute(sql_customer, (user_id,))
                customer = cursor.fetchone()

                
                # Müşteri bilgilerini oturumda sakla
                session["user_info"] = {
                    "user_id": user['user_id'],
                    "customer_id": customer['customer_id'],
                    "user_name": user['user_name'],
                    "user_password": user['user_password'],
                    
                    "customer_name": customer['customer_name'],
                    "customer_surname": customer['customer_surname'],
                    "customer_age": customer['customer_age'],
                    "customer_gender": customer['customer_gender'],
                    "customer_phone": customer['customer_phone']
                    
                }
                cursor.close()
                conn.close()
                # Kullanıcı profili varsa profil sayfasına yönlendir
                return redirect(url_for('index'))
            else:
                # Kullanıcı ve şifre yanlışsa giriş sayfasına geri dön
                flash("kullanıcı bilgileri yanlış")
                return render_template('user_login.html')
    else:
        # GET isteği ise giriş sayfasını göster
        return render_template('user_login.html')
    
#üye kaydı yapıldığında bilgiler önce db kaydediliyor sonrasında sessiona kaydediliyor  -mert
#üye hali hazırda var ise flash mesaj ile uyarılmalı
@app.route("/user_register", methods=["GET", "POST"])
def user_register():
    if request.method == "GET":
        return render_template("user_register.html")
    else:
        conn = DatabaseConnection()
        with conn.cursor() as cursor:
            user_name = request.form.get("user_name")
            if len(user_name) < 3:
                flash("Your username must be longer than 2 digits")
                return redirect("user_register")
            user_password = request.form.get("user_password")
            if not re.search(r"(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{5,}", user_password):
                flash("Your password must be at least 5 digits and must have include at least 1 character and 1 number!\n"
                      "Example format: '1abcd' or '12345a'")
                return redirect("/user_register")
            user_password = generate_password_hash(user_password)
            confirmation = request.form.get("confirmation")

            customer_name = request.form.get("customer_name")
            customer_surname = request.form.get("customer_surname")
            customer_age = request.form.get("customer_age")
            customer_gender = request.form.get("customer_gender")
            customer_phone = request.form.get("customer_phone")

            if not check_password_hash(user_password, confirmation):
                return apology("Password and confirmation must be the same!")

            if int(customer_age) < 0:
                flash("Your age can not be lower than 0!")
                return redirect("/user_register")

            cursor.execute("SELECT user_name FROM user WHERE user_name = %s", user_name)
            username = cursor.fetchone()

            if username:
                flash("This username is taken!")
                return redirect("/user_register")

            # dict for add_row_to_table function
            customer_info = dict({
                "customer_name": customer_name,
                "customer_surname": customer_surname,
                "customer_age": customer_age,
                "customer_gender": customer_gender,
                "customer_phone": customer_phone,
            })

            customer_id = add_row_to_table("customer", customer_info)

            user_info = dict({
                "user_name": user_name,
                "user_password": user_password,
                "customer_id": customer_id
            })
            # Add registered user to the database
            user_id = add_row_to_table("user", user_info)

            user_customer_info = {
                "user_id": user_id,
                "customer_id": customer_id,
                "user_name": user_name,
                "user_password": user_password,

                "customer_name": customer_name,
                "customer_surname": customer_surname,
                "customer_age": customer_age,
                "customer_gender": customer_gender,
                "customer_phone": customer_phone,

            }

            session["user_info"] = user_customer_info
            flash("Registered.")

            return redirect("/")
   
 #debug için yazılan sayfa işlevi yok   
#sessionun çalışma mantığını anlamak ve test etmek için örnek bir bilet alma sayfası ekledim -mert
@app.route('/bilet_alma', methods=['GET'])
@admin_required
def bilet_alma():
    user_info = session.get('user_info')  # Oturum bilgilerini al
    return render_template('bilet_alma.html', user_info=user_info)

@app.route('/user_logout')
def user_logout():
    session.pop('user_info', None)
    return redirect(url_for('user_login'))

if __name__ == '__main__':
    app.debug = True
    app.run()
