# 🚀 Linkak Production Deployment Guide

دليل شامل لنشر Linkak في بيئة الإنتاج مع جميع التحسينات الأمنية والأداء والمراقبة.

## 📋 المتطلبات الأساسية

### متطلبات الخادم
- **نظام التشغيل**: Ubuntu 20.04 LTS أو أحدث
- **المعالج**: 2 cores كحد أدنى (4 cores مُستحسن)
- **الذاكرة**: 4GB RAM كحد أدنى (8GB مُستحسن)
- **التخزين**: 50GB SSD كحد أدنى
- **الشبكة**: اتصال إنترنت مستقر مع IP ثابت

### البرامج المطلوبة
- Docker 20.10+
- Docker Compose 2.0+
- Git
- Nginx (يُثبت تلقائياً)
- Certbot (للـ SSL)

## 🔧 التثبيت السريع

### 1. تحميل الكود
```bash
# تحميل المشروع
git clone https://github.com/muhammedatef98/Linkak.git
cd Linkak

# جعل الـ scripts قابلة للتنفيذ
chmod +x scripts/*.sh scripts/*.py deploy/entrypoint.sh
```

### 2. النشر التلقائي
```bash
# نشر كامل مع إعداد المسؤول
sudo ./scripts/deploy.sh \
    --admin-username admin \
    --admin-email admin@yourdomain.com \
    --admin-password YourSecurePassword123 \
    --environment production
```

### 3. النشر المخصص
```bash
# للتحكم الكامل في العملية
sudo ./scripts/deploy.sh --help
```

## 📁 هيكل المشروع المحسّن

```
Linkak/
├── src/                          # كود التطبيق الرئيسي
│   ├── main_production.py        # التطبيق المحسّن للإنتاج
│   ├── config.py                 # إعدادات متعددة البيئات
│   └── middleware/
│       └── security.py           # حماية متقدمة
├── deploy/                       # ملفات النشر
│   ├── Dockerfile               # Docker للإنتاج
│   ├── docker-compose.yml       # خدمات متكاملة
│   ├── nginx.conf               # إعداد Nginx
│   ├── gunicorn.conf.py         # إعداد Gunicorn
│   ├── supervisor.conf          # إدارة العمليات
│   └── entrypoint.sh            # نقطة البداية
├── scripts/                     # أدوات الإدارة
│   ├── deploy.sh                # نشر تلقائي
│   ├── backup.sh                # نسخ احتياطية
│   ├── health_monitor.py        # مراقبة صحية
│   ├── backup_scheduler.py      # جدولة النسخ
│   └── database_manager.py      # إدارة قاعدة البيانات
└── requirements-production.txt  # مكتبات الإنتاج
```

## 🐳 نشر Docker

### 1. بناء الصورة
```bash
# بناء صورة الإنتاج
docker build -t linkak:latest .
```

### 2. تشغيل الخدمات
```bash
# تشغيل جميع الخدمات
docker-compose up -d

# مراقبة السجلات
docker-compose logs -f web
```

### 3. إدارة الخدمات
```bash
# إعادة تشغيل التطبيق
docker-compose restart web

# تحديث التطبيق
docker-compose pull && docker-compose up -d

# إيقاف الخدمات
docker-compose down
```

## 🔐 الحماية والأمان

### 1. إعداد متغيرات البيئة
```bash
# نسخ ملف البيئة
cp .env.example .env

# تحرير الإعدادات
nano .env
```

#### المتغيرات الأساسية
```env
# أمان (مطلوب تغييرها!)
SECRET_KEY=your-generated-secret-key
SECURITY_SALT=your-generated-salt

# قاعدة البيانات
DATABASE_URL=postgresql://linkak_user:password@db:5432/linkak_db
DB_PASSWORD=secure_database_password

# البريد الإلكتروني
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# النطاق
DOMAIN_NAME=yourdomain.com
```

### 2. إعداد Firewall
```bash
# تفعيل جدار الحماية
sudo ufw enable

# السماح بالمنافذ المطلوبة
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

### 3. إعداد SSL/HTTPS
```bash
# تثبيت Certbot
sudo apt install certbot python3-certbot-nginx

# الحصول على شهادة SSL
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# تجديد تلقائي
sudo crontab -e
# إضافة: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 4. حماية إضافية
```bash
# تفعيل Fail2Ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# مراقبة المحاولات المشبوهة
sudo fail2ban-client status
```

## 📊 المراقبة والتحليلات

### 1. Prometheus Metrics
- **الرابط**: `http://your-server:9090`
- **المقاييس**: أداء التطبيق، قاعدة البيانات، النظام

### 2. Grafana Dashboard
- **الرابط**: `http://your-server:3000`
- **المستخدم**: admin
- **كلمة المرور**: (محددة في .env)

### 3. مراقبة الصحة
```bash
# فحص حالة التطبيق
curl http://localhost/api/health

# مراقبة مستمرة
python3 scripts/health_monitor.py
```

### 4. السجلات
```bash
# سجلات التطبيق
tail -f logs/linkak.log

# سجلات Nginx
tail -f logs/nginx_access.log

# سجلات قاعدة البيانات
docker-compose logs -f db
```

## 💾 النسخ الاحتياطية

### 1. نسخ تلقائية
```bash
# تفعيل النسخ الاحتياطية اليومية
# (يتم تفعيلها تلقائياً عند النشر)

# تشغيل نسخة فورية
./scripts/backup.sh
```

### 2. إدارة النسخ
```bash
# عرض حالة النسخ
python3 scripts/backup_scheduler.py status

# استرداد نسخة احتياطية
./scripts/restore.sh backup_file.dump
```

### 3. نسخ سحابية
```env
# في ملف .env
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
BACKUP_S3_BUCKET=your-backup-bucket
```

## 🗄️ إدارة قاعدة البيانات

### 1. إعداد أولي
```bash
# إنشاء الجداول
python3 scripts/database_manager.py create

# بيانات تجريبية (للتطوير فقط)
python3 scripts/database_manager.py seed
```

### 2. إدارة المستخدمين
```bash
# إنشاء مسؤول
python3 scripts/database_manager.py admin \
    --username admin \
    --email admin@domain.com \
    --password SecurePassword
```

### 3. صيانة
```bash
# إحصائيات قاعدة البيانات
python3 scripts/database_manager.py stats

# تنظيف البيانات القديمة
python3 scripts/database_manager.py cleanup --days 30

# فحص سلامة البيانات
python3 scripts/database_manager.py verify
```

## ⚡ تحسين الأداء

### 1. إعدادات Nginx
```nginx
# في ملف nginx.conf
worker_processes auto;
worker_connections 1024;

# تفعيل الضغط
gzip on;
gzip_types text/css application/javascript;

# التخزين المؤقت
expires 1y;
add_header Cache-Control "public, immutable";
```

### 2. إعدادات Gunicorn
```python
# في gunicorn.conf.py
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
worker_connections = 1000
max_requests = 1000
```

### 3. تحسين قاعدة البيانات
```sql
-- إضافة فهارس
CREATE INDEX idx_links_user_id ON links(user_id);
CREATE INDEX idx_shorturl_alias ON short_urls(custom_alias);

-- تحليل الأداء
EXPLAIN ANALYZE SELECT * FROM links WHERE user_id = 1;
```

## 🔄 التحديث والصيانة

### 1. تحديث التطبيق
```bash
# سحب آخر تحديث
git pull origin main

# إعادة بناء الصورة
docker-compose build web

# إعادة تشغيل الخدمات
docker-compose up -d web
```

### 2. صيانة دورية
```bash
# تنظيف Docker
docker system prune -f

# تدوير السجلات
logrotate /etc/logrotate.d/linkak

# فحص مساحة القرص
df -h
```

### 3. مراقبة الأداء
```bash
# استخدام الموارد
htop

# مراقبة الشبكة
netstat -tulpn

# حالة الخدمات
systemctl status nginx
systemctl status docker
```

## 🚨 استكشاف الأخطاء

### مشاكل شائعة

#### 1. التطبيق لا يستجيب
```bash
# فحص السجلات
docker-compose logs web

# إعادة تشغيل الخدمة
docker-compose restart web

# فحص الذاكرة
free -h
```

#### 2. مشاكل قاعدة البيانات
```bash
# فحص اتصال قاعدة البيانات
docker-compose exec db psql -U linkak_user -d linkak_db -c "SELECT 1;"

# إعادة تشغيل قاعدة البيانات
docker-compose restart db
```

#### 3. مشاكل SSL
```bash
# فحص الشهادة
openssl x509 -in /app/ssl/cert.pem -text -noout

# تجديد الشهادة
sudo certbot renew
```

#### 4. مشاكل الذاكرة
```bash
# فحص استخدام الذاكرة
docker stats

# تقليل عدد Workers
# تعديل WORKERS في ملف .env
```

### أوامر مفيدة للتشخيص
```bash
# فحص شامل للنظام
./scripts/health_monitor.py

# فحص الشبكة
curl -I http://localhost/api/health

# فحص قاعدة البيانات
python3 scripts/database_manager.py verify

# فحص المساحة
du -sh /app/*
```

## 📞 الدعم والمساعدة

### السجلات المهمة
- `/app/logs/linkak.log` - سجل التطبيق الرئيسي
- `/app/logs/nginx_access.log` - سجل وصول Nginx
- `/app/logs/nginx_error.log` - سجل أخطاء Nginx
- `/app/logs/backup.log` - سجل النسخ الاحتياطية

### أوامر مراقبة مفيدة
```bash
# مراقبة السجلات المباشرة
tail -f /app/logs/linkak.log

# فحص استخدام الموارد
htop

# حالة Docker
docker-compose ps

# حالة قاعدة البيانات
python3 scripts/database_manager.py stats
```

### نصائح الأمان
1. **غيّر كلمات المرور الافتراضية فوراً**
2. **فعّل النسخ الاحتياطية التلقائية**
3. **راقب السجلات بانتظام**
4. **حدّث النظام والتطبيق باستمرار**
5. **استخدم شهادات SSL صالحة**

---

## 🎉 تهانينا!

إذا وصلت إلى هنا، فقد نجحت في نشر Linkak في بيئة إنتاج محترفة! 

موقعك الآن:
- ✅ محمي بأقوى معايير الأمان
- ✅ محسّن للأداء العالي
- ✅ مراقب 24/7 
- ✅ يُنسخ احتياطياً تلقائياً
- ✅ جاهز لاستقبال آلاف المستخدمين

**استمتع بموقعك الجديد! 🚀**