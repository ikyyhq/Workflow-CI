import pandas as pd
import mlflow
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1. Mengaktifkan autologging untuk kemudahan CI
mlflow.sklearn.autolog()

# 2. Membaca dataset yang sudah diproses
df = pd.read_csv('heart_failure_preprocessing.csv')

# 3. Memisahkan fitur (X) dan target (y)
X = df.drop(columns=['DEATH_EVENT'])
y = df['DEATH_EVENT']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Memulai run MLflow untuk training otomatis
with mlflow.start_run(run_name="CI_Automated_Run"):
    print("Memulai training otomatis dari GitHub Actions...")
    
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    
    acc_rf = accuracy_score(y_test, model.predict(X_test))
    print(f"Training selesai! Akurasi: {acc_rf:.4f}")
    
print("Proses CI Pipeline Modelling Selesai!")