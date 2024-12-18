from telegram import Bot
from binance.client import Client
import datetime

# إعداد التوكنات
TELEGRAM_TOKEN = "8049959483:AAE2zdlnZOpoWkW47AkTgU66aTtYUTeGeh8"  # توكن البوت الخاص بك
CHAT_ID = "5905497328"  # شات آي دي الخاص بك
BINANCE_API_KEY = "IMM0Jet5QVI28cc7n4kuSTCH7aTPvbfLCqMEC67IOQka6afPeYKFPRRDfdtofQsY"  # مفتاح Binance API
BINANCE_SECRET_KEY = "bfS5YVmRkA7dNQKt21cD1HKJ3CwBLdNMTutOwper9ZqI8GQFKPgspdlDHh1i151X"  # المفتاح السري لـ Binance API

# إعداد البوت
bot = Bot(token=TELEGRAM_TOKEN)
client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)

# وظيفة إرسال الإشارة
def send_signal(pair, entry_price, targets):
    message = f"""
    🎉 New Trading Signal 🎉
    📌 Signal ID: {datetime.datetime.now().timestamp()}
    🔗 Pair: {pair}
    💵 Entry Price: {entry_price}

    🎯 Profit Targets:
    {targets}
    ⏳ Trade started at: {datetime.datetime.now()}
    """
    bot.send_message(chat_id=CHAT_ID, text=message)

# مثال لإرسال توصية
pair = "NEAR/USDT"
entry_price = 6.9300
targets = """
    Target 1: 7.0166 (+1.25%)
    Target 2: 7.0686 (+2%)
    Target 3: 7.2765 (+5%)
    Target 4: 7.4151 (+7%)
    Target 5: 7.6230 (+10%)
    Target 6: 7.9695 (+15%)
    Target 7: 8.3160 (+20%)
"""
send_signal(pair, entry_price, targets)
