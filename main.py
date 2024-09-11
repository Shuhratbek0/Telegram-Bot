import telebot
from telebot import types
import qrcode
from io import BytesIO

# Bot tokenini o'rnatamiz
API_TOKEN = '6973785998:AAGQ960vEicJaVp6nd6jmawaFwj84LaW2Gs'
bot = telebot.TeleBot(API_TOKEN)


# /start komanda bosilganida
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Assalomu alaykum! Men siz yuborgan matnni QR kodga aylantirib beraman. Iltimos, matnni yuboring."
    )


# Matnni qabul qiluvchi funksiya
@bot.message_handler(func=lambda message: True)
def generate_qr(message):
    try:
        # QR kod yaratamiz
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(message.text)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')

        # QR kodni baytlarga aylantiramiz
        bio = BytesIO()
        bio.name = 'image.png'
        img.save(bio, 'PNG')
        bio.seek(0)

        # QR kodni foydalanuvchiga yuboramiz
        bot.send_photo(message.chat.id, bio)

    except Exception as e:
        bot.reply_to(message, f"Xatolik yuz berdi: {str(e)}")


bot.polling()
