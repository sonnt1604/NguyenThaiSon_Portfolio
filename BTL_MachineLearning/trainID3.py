import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pickle

def train_and_evaluate_model(train_file, test_file, output_model_file):
    # Đọc dữ liệu huấn luyện và kiểm tra từ các file CSV
    train_data = pd.read_csv(train_file)
    test_data = pd.read_csv(test_file)

    # Tách đặc trưng (X) và nhãn (y) từ tập huấn luyện
    X_train = train_data.drop(columns=['diagnosis'])
    y_train = train_data['diagnosis']

    # Tách đặc trưng (X) và nhãn (y) từ tập kiểm tra
    X_test = test_data.drop(columns=['diagnosis'])
    y_test = test_data['diagnosis']

    # Khởi tạo mô hình DecisionTreeClassifier (thuật toán ID3)
    model = DecisionTreeClassifier(criterion='entropy', random_state=42)

    # Huấn luyện mô hình
    model.fit(X_train, y_train)

    # Dự đoán trên tập kiểm tra
    y_pred = model.predict(X_test)

    # Tính toán các chỉ số đánh giá
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    # Lưu mô hình đã huấn luyện vào file .pkl
    with open(output_model_file, 'wb') as file:
        pickle.dump(model, file)

    # Trả về các chỉ số đánh giá
    return accuracy, precision, recall, f1

def predict_from_user_input(model_file, input_data):
    # Tải mô hình đã lưu từ file .pkl
    with open(model_file, 'rb') as file:
        model = pickle.load(file)

    # Chuyển đổi dữ liệu nhập từ người dùng thành một DataFrame
    input_data = [float(i) for i in input_data]
    columns = ['radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean',
               'compactness_mean', 'concavity_mean', 'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean',
               'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se', 'compactness_se', 'concavity_se',
               'concave points_se', 'symmetry_se', 'fractal_dimension_se', 'radius_worst', 'texture_worst',
               'perimeter_worst', 'area_worst', 'smoothness_worst', 'compactness_worst', 'concavity_worst',
               'concave points_worst', 'symmetry_worst', 'fractal_dimension_worst']
    
    new_data = pd.DataFrame([input_data], columns=columns)

    # Dự đoán nhãn (diagnosis) cho dữ liệu mới
    prediction = model.predict(new_data)

    # In kết quả dự đoán
    return 'M' if prediction[0] == 1 else 'B'  # 'M' là u ác tính, 'B' là u lành tính

if __name__ == "__main__":
    train_file = 'train_data.csv'  # Đường dẫn file CSV chứa dữ liệu huấn luyện
    test_file = 'test_data.csv'    # Đường dẫn file CSV chứa dữ liệu kiểm tra
    output_model_file = 'id3_model.pkl'  # Đường dẫn file lưu mô hình

    accuracy, precision, recall, f1 = train_and_evaluate_model(train_file, test_file, output_model_file)

    # In kết quả đánh giá
    print(f"Accuracy: {accuracy:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1-Score: {f1:.2f}")
