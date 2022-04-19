from __future__ import print_function
import os
from dotenv import load_dotenv #pip install python-dotenv
import sib_api_v3_sdk #pip install sib-api-v3-sdk
import mysql.connector #pip install mysql-connector-python
from sib_api_v3_sdk.rest import ApiException

# setting environment variabel
# buat file .env pada direktori yang sama dan buat environment variabel dengan nama yg sama
# contoh MYSQL_HOST=root
load_dotenv()
db_host = str(os.environ.get("MYSQL_HOST"))
db_user = str(os.environ.get("MYSQL_USER"))
db_name = str(os.environ.get("MYSQL_DATABASE"))
api_key = str(os.environ.get("API_KEY"))
sender_email = str(os.environ.get("EMAIL"))


# set up koneksi database
db = mysql.connector.connect(
    host=db_host,
    user=db_user,
    passwd="",
    database=db_name
)

# mengambil seluruh data email yang belum terkirim dari database
def emailList():
    cursor = db.cursor()
    sql = "SELECT email FROM tb_email WHERE sent = 0"
    cursor.execute(sql)
    hasil = cursor.fetchall()
    return tuple(hasil)

# pengiriman email dan update status email di database
def emailSend(subject,sender_name,receiver_email):
    # konfigurasi api key
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = api_key
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    # isi email
    email_subject = subject
    email_sender = {"name":sender_name,"email":sender_email}
    email_content = "<html><body><h1>Ini adalah Pesan email blast</h1></body></html>"
    email_target = {"email":receiver_email}

    # create an instance of the API class
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    # mempersiapkan pengiriman email
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=[email_target], html_content=email_content, sender=email_sender, subject=email_subject)

    try:
        #pengiriman email
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
        print("Pesan Sukses Terkirim ke",receiver_email)
        cursor = db.cursor()
        # update user telah terkirim ke database
        cursor.execute("UPDATE tb_email SET sent=%s WHERE email=%s",(1,receiver_email))
        db.commit()
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)

list = emailList()
for email in list:
    emailSend(
        subject="Email Blast",
        sender_name="Kelompok 4 IMS",
        receiver_email=email[0]
    )

