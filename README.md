Hızlı ve Etkili Seyahat Yönetimi Web Uygulaması:Python_Travel_v2

Merhaba seyahat severler! Bugün sizlere, seyahat acenteleri için özel olarak geliştirilmiş “Ticket Control & Management System” projesinden bahsedeceğim. Adından da anlaşılacağı gibi, bu proje seyahat süreçlerini daha hızlı ve etkili bir şekilde yönetmeyi hedefliyor. Gel, bu teknik serüvene birlikte göz atalım!

Proje Amaçları ve Kapsamı:

Yola çıkarken belirlediğimiz ana hedefler şunlar:
- Hızlı ve basit bir kullanım sunmak
- Seyahat acentesi koşullarına uygunluk
- Kullanıcı dostu ve orijinal bir tasarım

Yol arkadaşlarımızın mutluluğu ise bizim için en öncelikli başarı kriteri. Hadi, projenin teknik detaylarına geçelim!

Kullanılan Teknolojiler:

1. Python & Flask: Projemizin kalbinde Python ve hafif yapısıyla öne çıkan Flask bulunuyor. Seyahat acentelerinin ihtiyaçlarına özel olarak tasarlanan bu web uygulama çerçevesi, projemize hız ve esneklik katıyor.

2. PyMySQL & MySQL:Python ile MySQL veritabanı arasındaki iletişimi sağlamak adına kullandığımız PyMySQL, projenin veri yönetimini sağlıyor. Veritabanında araç ve rota bilgilerini depoluyoruz.

3. Werkzeug.Security: Flask içinde güvenlik özellikleri sunan Werkzeug, özellikle şifreleme işlemlerinde bize destek oluyor. Kullanıcı bilgilerini güvenle saklamamıza yardımcı oluyor.

4. HTML & CSS & Jinja: Kullanıcı arayüzü oluştururken HTML ve CSS kullanıyoruz. Jinja ise Python tabanlı bir şablon motoru olarak, Flask projelerinde HTML içeriği oluşturmak için bize kolaylık sağlıyor.

5. Git & Terminus:Projenin sürüm kontrolü için Git kullanıyoruz. Terminus ise Git tabanlı bir terminal servisi olarak, terminal üzerinden komut çalıştırmamıza olanak tanıyor.

6. Amazon AWS: Proje için bulut tabanlı hizmetleri içeren bir platform olan AWS, altyapı hizmetlerini sağlamak adına projemize güç katıyor.

Projenin Gelişim Süreci: RAD Model

Projemizi hızlı bir şekilde teslim etmek ve güncellemeleri kolayca yapabilmek adına RAD Modeli’ni tercih ettik. Her bir modülü ayrı ayrı geliştirip entegre etmek, müşteriyi süreç boyunca dahil etmek ve geliştirmeyi hızlandırmak için bu modeli seçtik. Esnek ve müşteri odaklı olması, hızlı ve dinamik projeler için oldukça etkili bir tercih olmasını sağlıyor.

Risk Analizi ve Gereksinimlere Uygunluk: Seyahat Yönetiminde Teknolojik Güvence

Merhaba seyahat severler! Bu yazıda, “Ticket Control & Management System” projemizin biraz daha derinliklerine inerek, risk analizi ve gereksinimlere uygunluğunu ele alacağız. Haydi, bu teknolojik yolculuğumuza birlikte devam edelim!

Risk Analizi:

Her projede olduğu gibi, bu seyahat yönetim projesinde de bazı risklere karşı önlemler almamız gerekiyor. İşte karşılaşabileceğimiz riskler ve bu risklere karşı alınan önlemler:

1. Veri Entegrasyonu Zorlukları:
—Risk: Farklı veri kaynaklarından bilgi uyumlu bir şekilde çekilmeli.
— Önlem: Modüler entegrasyon yöntemleri kullanılarak bu süreç daha yönetilebilir hale getirildi. Backup veri kaynakları kullanılmaya hazır.

2. Güvenlik Zafiyetleri:
— Risk: Kullanıcı bilgilerini korumak için yeterli güvenlik önlemleri alınmalı.
— Önlem: Güçlü şifreleme ve güvenlik algoritmalarının kullanımıyla, acil durum güncellemeleri ve kullanıcı bildirimleri yapılarak güvenlik güçlendirildi.

3. Performans Sorunları:
— Risk: Yoğun kullanımda web uygulamasının performansında düşüş yaşanabilir.
— Önlem: Yük dengeleme ve önbellekleme stratejileri uygulanarak, performans monitörleme ve hızlı tepki planları geliştirildi.

4. Veritabanı İlişkileri:
— Risk: Veritabanı tabloları arasındaki ilişkiler eksik veya alt-optimal olabilir.
— Önlem: Veritabanı yapıları optimize edilerek, veri bütünlüğünü korumak için planlar oluşturuldu.

5. Kullanıcı Deneyimi Kısmi Eksiklikleri:
— Risk: Arayüz ve fonksiyonlarda eksiklikler olabilir.
— Önlem:Kullanıcı test senaryoları oluşturularak, geri bildirim döngüleri sayesinde arayüz iyileştirmeleri hızla yapıldı.

Gereksinimlere Uygunluk:

Projemiz, belirlenen fonksiyonel ve non-fonksiyonel gereksinimleri karşılamak için tasarlandı. İşte bazı temel gereksinimler ve onlara uygunluk durumu:

1. Kullanıcı İşlemleri:
— Kullanıcılar giriş yapabilir, hesap oluşturabilir, bilet arama ve seçme işlemleri gerçekleştirebilir.
— Kişisel bilgilerini düzenleyebilir.

2. Bilet Yönetimi ve İşlemleri:
— Biletler satın alınabilir, iptal edilebilir ve rota/araç/tarih bazında aranabilir.

3. Rota ve Araç Yönetimi:
— Rota bilgileri (kalkış noktaları, varış noktaları, yolcu sayısı, seyahat süresi, ücret, seyahat tarihi) düzenlenebilir.
— Araç bilgileri (kapasite, tip, plaka, bakım kilometre, çalışan bilgisi) yönetilebilir.

4. Admin İşlemleri:
— Yöneticiler, kullanıcı hesaplarını düzenleyebilir, bilet, kullanıcı, rota, araç ve seyahat bilgilerini görüntüleyip düzenleyebilir.
— Çalışan bilgileri güncellenebilir, veritabanı tabloları yönetilebilir.

Sonuç ve Gelecek Adımlar:

Bu projede bir araya gelen Python, Flask, MySQL ve diğer teknolojiler, seyahat acentelerine özel bir çözüm sunuyor. Kullanıcı dostu arayüzü, hızlı işlemleri ve güvenliğiyle bu projenin sektöre yeni bir soluk getireceğine inanıyoruz.

Gelecek adımlarımız arasında projenin kullanıcı deneyimini daha da iyileştirmek, performansını artırmak ve güvenlik önlemlerini güncellemek bulunuyor. Siz de bu seyahat teknolojisiyle tanışmak istiyorsanız, takipte kalın! İyi yolculuklar! 🚗💨

Sonuç olarak, “Ticket Control & Management System” projesi, seyahat acentelerine özel olarak tasarlanmış, güvenli, hızlı ve kullanıcı dostu bir çözüm sunmayı hedefliyor. Gelişen teknolojiyle birlikte projenin gelecekteki adımları da, daha da iyileştirmeye odaklı. Seyahat etmeye hazır mısınız? 🌍✈️
Proje Geliştiricileri ve Github Bağlantıları:Mert Metin Erdemli
Emirhan Balcı:@CheesyFrappe
Ahmet Burak Biçer:@BurakAhmet
Medium Blog:https://medium.com/@mertmetin-1/h%C4%B1zl%C4%B1-ve-etkili-seyahat-y%C3%B6netimi-web-uygulamas%C4%B1-python-travel-v2-78382aaa8407

