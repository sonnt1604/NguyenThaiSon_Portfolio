import pandas as pd  
import numpy as np  
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score  
from sklearn.preprocessing import LabelEncoder, StandardScaler  
from sklearn.model_selection import KFold  
from sklearn.linear_model import Perceptron  
import pickle  

# Quá trình huấn luyện với dữ liệu CSV và K-fold cross-validation
def kfold_cross_validation(data, k=7):  # HÀM TRAIN
    # Mã hóa cột 'diagnosis' thành số (B -> 0, M -> 1)
    le = LabelEncoder()
    data["diagnosis"] = le.fit_transform(data["diagnosis"])

    
    X = data.iloc[:, :-1]  # Các cột đặc trưng
    Y = data.iloc[:, -1]   # Cột nhãn 'diagnosis'

    # Chuẩn hóa dữ liệu
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # Khởi tạo K-Fold Cross-Validation với k phân đoạn
    kf = KFold(n_splits=k, random_state=None)

    # Các biến lưu trữ thông tin mô hình tốt nhất
    min_error = float('inf')  
    best_performance = {}  # Để lưu chỉ số của mô hình tốt nhất
    best_model = None  # Để lưu mô hình tốt nhất

    # Các biến cộng dồn chỉ số đánh giá để tính trung bình
    accuracy, precision, recall, f1 = 0, 0, 0, 0

    # Lặp qua từng chia đoạn của K-Fold
    for train_index, validation_index in kf.split(data): # Chia tập dữ liệu thành tập huấn luyện và kiểm tra
        X_train, X_validation = X[train_index], X[validation_index]
        y_train, y_validation = Y[train_index], Y[validation_index]

        # Khởi tạo và huấn luyện mô hình Perceptron
        per_clf = Perceptron(alpha=0.01, max_iter=400)  # Tạo mô hình với tham số alpha (learning rate) và số vòng lặp tối đa
        per_clf.fit(X_train, y_train)  # Huấn luyện mô hình trên tập huấn luyện
        y_train_pred = per_clf.predict(X_train) # Dự đoán trên tập huấn luyện và kiểm tra
        y_validation_pred = per_clf.predict(X_validation)

        # Tính toán các chỉ số đánh giá trên tập kiểm tra
        performance = {
            "accuracy": accuracy_score(y_validation, y_validation_pred),  # Độ chính xác
            "precision": precision_score(y_validation, y_validation_pred),  # Độ chính xác dương tính
            "recall": recall_score(y_validation, y_validation_pred),  # Độ phủ dương tính
            "f1": f1_score(y_validation, y_validation_pred)  # F1-Score
        }

        # Cập nhật mô hình tốt nhất nếu lỗi nhỏ hơn lỗi hiện tại
        per_sum_error = np.sum(y_validation != y_validation_pred)  # Tính tổng lỗi (số lượng nhãn dự đoán sai)
        if per_sum_error < min_error:
            min_error = per_sum_error  # Cập nhật lỗi nhỏ nhất
            best_performance = performance  # Lưu chỉ số tốt nhất
            best_model = per_clf  # Lưu mô hình tốt nhất

        # Cộng dồn các chỉ số để tính trung bình
        accuracy += performance["accuracy"]
        precision += performance["precision"]
        recall += performance["recall"]
        f1 += performance["f1"]

    # Tính trung bình các chỉ số
    accuracy /= k
    precision /= k
    recall /= k
    f1 /= k

    # Trả về các chỉ số đánh giá trung bình, mô hình tốt nhất và scaler
    return accuracy, precision, recall, f1, best_model, scaler

# Hàm dự đoán với dữ liệu đầu vào từ người dùng
def predict_from_user_input(model_file, input_data):  # HÀM TEST
    try:
        # Tải mô hình đã lưu từ file
        with open(model_file, 'rb') as file:
            model = pickle.load(file)
    except FileNotFoundError:
        print(f"Model file '{model_file}' not found.")  # Báo lỗi nếu không tìm thấy file mô hình
        return None

    # Chuyển dữ liệu đầu vào thành mảng và định dạng phù hợp
    input_data = np.array(input_data).reshape(1, -1)
    
    # Dự đoán nhãn từ dữ liệu đầu vào
    prediction = model.predict(input_data)
    return 'M' if prediction[0] == 1 else 'B'  # Trả về nhãn 'M' hoặc 'B'

if __name__ == "__main__":
    # Đọc dữ liệu từ file CSV
    data = pd.read_csv("data_PLA.csv")
    
    # Thực hiện K-Fold Cross Validation và lấy mô hình tốt nhất
    accuracy, precision, recall, f1, best_model, scaler = kfold_cross_validation(data, k=7)
    
    # In ra các chỉ số đánh giá
    print(f"Accuracy: {accuracy}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1: {f1}")
