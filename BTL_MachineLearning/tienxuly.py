import pandas as pd
from sklearn.model_selection import train_test_split

# Đọc dữ liệu từ file CSV
file_path = 'dataN18.csv' 
data = pd.read_csv(file_path)

# Xóa cột không cần thiết
data = data.drop(columns=['Unnamed: 32', 'id'])

# Chuyển đổi giá trị 'diagnosis' thành số (M: 1, B: 0)
data['diagnosis'] = data['diagnosis'].map({'M': 1, 'B': 0})

# Tách đặc trưng (X) và nhãn (y)
X = data.drop(columns=['diagnosis'])
y = data['diagnosis']

# Chia dữ liệu thành tập train (80%) và test (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Gộp lại các tập train và test để lưu vào file CSV
train_data = pd.concat([X_train, y_train], axis=1)
test_data = pd.concat([X_test, y_test], axis=1)

# Lưu ra file CSV
train_data.to_csv('train_data.csv', index=False)
test_data.to_csv('test_data.csv', index=False)

# Kết quả
print(f"Tập huấn luyện: {X_train.shape}, {y_train.shape}")
print(f"Tập kiểm tra: {X_test.shape}, {y_test.shape}")
print("Đã lưu tập huấn luyện vào 'train_data.csv' và tập kiểm tra vào 'test_data.csv'.")
