import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split

# تحميل البيانات (تأكد من أن لديك بيانات التدريب)
def load_data():
    # إنشاء بعض البيانات الوهمية كعينة (يجب عليك استبدال هذه البيانات بالبيانات الفعلية)
    data = pd.DataFrame({
        'RSI': np.random.rand(1000),
        'EMA': np.random.rand(1000),
        'MACD': np.random.rand(1000),
        'close': np.random.rand(1000),
        'target': np.random.randint(2, size=1000)  # 0 أو 1 كأهداف (مثال: شراء أو بيع)
    })
    return data

# تقسيم البيانات إلى تدريب واختبار
def split_data(data):
    X = data[['RSI', 'EMA', 'MACD', 'close']]
    y = data['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

# بناء النموذج
def build_model():
    model = Sequential([
        Dense(64, input_dim=4, activation='relu'),
        Dropout(0.2),
        Dense(128, activation='relu'),
        Dropout(0.2),
        Dense(64, activation='relu'),
        Dense(1, activation='sigmoid')  # طبقة الإخراج (0 أو 1)
    ])
    model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])
    return model

# تدريب النموذج
def train_model(X_train, y_train, X_test, y_test):
    model = build_model()
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test), verbose=2)
    return model

# حفظ النموذج المحسن
def save_model(model):
    model.save('your_model.keras')  # حفظ النموذج بصيغة Keras الحديثة
    print("تم حفظ النموذج في 'your_model.keras'")

# تحسين النموذج واختباره
def improve_and_test_model():
    # تحميل البيانات
    data = load_data()

    # تقسيم البيانات
    X_train, X_test, y_train, y_test = split_data(data)

    # تدريب النموذج
    model = train_model(X_train, y_train, X_test, y_test)

    # اختبار النموذج
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"دقة النموذج على بيانات الاختبار: {accuracy * 100:.2f}%")

    # حفظ النموذج المحسن
    save_model(model)

# تشغيل عملية تحسين النموذج
if __name__ == "__main__":
    improve_and_test_model()
