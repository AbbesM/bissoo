import pandas as pd
import numpy as np
import pandas_ta as ta
import requests
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import telegram
from datetime import datetime
import time

# توكن Telegram والمعرف
TELEGRAM_TOKEN = "8049959483:AAE2zdlnZOpoWkW47AkTgU66aTtYUTeGeh8"  # استبدل التوكن
CHAT_ID = "5905497328"  # استبدل بالـ Chat ID الخاص بك

# تهيئة بوت Telegram
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# وظيفة إرسال الرسائل إلى Telegram
def send_telegram_message(message):
    try:
        bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"خطأ في إرسال الرسالة: {e}")

# جلب بيانات السوق من Binance API
def get_data(symbol, interval='1h', limit=1000):
    url = f'https://api.binance.com/api/v1/klines?symbol={symbol}&interval={interval}&limit={limit}'
    data = requests.get(url).json()
    df = pd.DataFrame(data, columns=["time", "open", "high", "low", "close", "volume", "close_time",
                                     "quote_asset_volume", "number_of_trades",
                                     "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"])
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df['close'] = pd.to_numeric(df['close'])
    df['high'] = pd.to_numeric(df['high'])
    df['low'] = pd.to_numeric(df['low'])
    return df

# حساب المؤشرات الفنية باستخدام Pandas TA
def calculate_indicators(df):
    df['RSI'] = ta.rsi(df['close'], length=14)
    df['EMA'] = ta.ema(df['close'], length=14)
    macd = ta.macd(df['close'], fast=12, slow=26, signal=9)
    df['MACD'] = macd['MACD_12_26_9']
    df['MACD_signal'] = macd['MACDs_12_26_9']
    df['MACD_hist'] = macd['MACDh_12_26_9']
    return df.dropna()  # حذف القيم المفقودة

# تجهيز البيانات للتدريب
def prepare_data(df):
    df = calculate_indicators(df)
    
    # اختيار الأعمدة المناسبة للتدريب
    features = df[['RSI', 'EMA', 'MACD', 'close']]
    
    # إنشاء الهدف (target): إذا كان السعر سيرتفع في الخطوة التالية
    df['target'] = np.where(df['close'].shift(-1) > df['close'], 1, 0)
    
    # تقسيم البيانات إلى مدخلات وأهداف
    X = features
    y = df['target']
    
    # تقسيم البيانات إلى تدريب واختبار
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # تطبيع البيانات
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    return X_train, X_test, y_train, y_test, scaler

# بناء نموذج الشبكة العصبية
def build_model(input_dim):
    model = Sequential()
    model.add(Dense(64, input_dim=input_dim, activation='relu'))
