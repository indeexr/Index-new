import telebot
from telebot import types
from supabase import create_client, Client
from flask import Flask, request

# --- البيانات (تأكد أنها داخل الاقتباس) ---
TOKEN = '8735543269:AAEcE4UVx94UT6jeEJfVSCH63NijdMsp8vg' 
URL = 'https://ffjwiipirurplgxlwahr.supabase.co'
KEY = 'sb_publishable_TJNgSHdEBfysVIXyxEHMkA_Qf-3Iz8M'

bot = telebot.TeleBot(TOKEN, threaded=False)
db = create_client(URL, KEY)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(m):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("➕ إضافة محاضرة")
    bot.send_message(m.chat.id, "🎓 البوت جاهز!", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "➕ إضافة محاضرة")
def add(m):
    q = bot.send_message(m.chat.id, "👤 اسم الدكتور:")
    bot.register_next_step_handler(q, get_doc)

def get_doc(m):
    d = m.text
    q = bot.send_message(m.chat.id, f"📝 اسم المحاضرة لـ {d}:")
    bot.register_next_step_handler(q, get_file, d)

def get_file(m, d):
    l = m.text
    q = bot.send_message(m.chat.id, "📎 أرسل الملف:")
    bot.register_next_step_handler(q, save, d, l)

def save(m, d, l):
    if m.content_type == 'document':
        try:
            row = {"doctor_name": d, "lec_name": l, "file_id": m.document.file_id}
            db.table("lectures").insert(row).execute()
            bot.send_message(m.chat.id, "✅ تم الحفظ سحابياً!")
        except Exception as e:
            bot.send_message(m.chat.id, f"❌ خطأ: {e}")

@app.route('/' + TOKEN, methods=['POST'])
def post(request):
    bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode('utf-8'))])
    return "!", 200

@app.route('/')
def main():
    return "Server is Running!", 200
