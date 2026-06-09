import pandas as pd
import mlflow
import os
import shutil
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1. Mengaktifkan autologging untuk metrik
mlflow.sklearn.autolog()

# 2. Membaca dataset
df = pd.read_csv('heart_failure_preprocessing.csv')

# 3. Memisahkan fitur dan target
X = df.drop(columns=['DEATH_EVENT'])
y = df['DEATH_EVENT']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Training Model
with mlflow.start_run(run_name="CI_Automated_Run"):
    print("Memulai training otomatis dari GitHub Actions...")
    
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    
    acc_rf = accuracy_score(y_test, model.predict(X_test))
    print(f"Training selesai! Akurasi: {acc_rf:.4f}")
    
    # 5. PAKSA SIMPAN KE FOLDER
    model_dir = "saved_model"
    if os.path.exists(model_dir):
        shutil.rmtree(model_dir)
    mlflow.sklearn.save_model(model, model_dir)
    print("Model berhasil disimpan secara hardcode ke folder 'saved_model'!")