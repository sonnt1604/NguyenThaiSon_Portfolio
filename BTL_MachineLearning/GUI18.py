import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from sklearn.tree import DecisionTreeClassifier
import pickle
import subprocess
import numpy as np
import pla_model
import trainID3
# Hàm tạo GUI
def create_gui():
    root = tk.Tk()
    root.title("Dự Đoán Ung Thư Vú")
    root.geometry("1000x800")
    root.configure(bg="#f2f2f2")

    font_title = ("Helvetica", 18, "bold")
    font_label = ("Helvetica", 12)
    font_button = ("Helvetica", 12, "bold")

    frame = tk.Frame(root, bg="#f2f2f2")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Tiêu đề
    title_label = tk.Label(frame, text="DỰ ĐOÁN UNG THƯ VÚ", font=font_title, fg="#333", bg="#f2f2f2")
    title_label.pack(pady=10)

    # Chọn loại mô hình
    model_type_var = tk.StringVar(value="ID3")
    model_type_frame = tk.Frame(frame, bg="#f2f2f2")
    model_type_frame.pack(pady=10)
    tk.Label(model_type_frame, text="Chọn mô hình:", font=font_label, bg="#f2f2f2").pack(side="left", padx=10)
    ttk.Combobox(model_type_frame, values=["ID3", "PLA"], textvariable=model_type_var, font=font_label, state="readonly").pack(side="left", padx=10)

    # Ô nhập liệu
    labels = [
        'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean',
        'compactness_mean', 'concavity_mean', 'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean',
        'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se', 'compactness_se', 'concavity_se',
        'concave points_se', 'symmetry_se', 'fractal_dimension_se', 'radius_worst', 'texture_worst',
        'perimeter_worst', 'area_worst', 'smoothness_worst', 'compactness_worst', 'concavity_worst',
        'concave points_worst', 'symmetry_worst', 'fractal_dimension_worst'
    ]

    input_frame = tk.Frame(frame, bg="#f2f2f2")
    input_frame.pack(pady=10)

    entries = []
    for i, label in enumerate(labels):
        tk.Label(input_frame, text=label, font=font_label, bg="#f2f2f2", anchor="w").grid(row=i // 4, column=(i % 4) * 2, padx=10, pady=5, sticky="w")
        entry = ttk.Entry(input_frame, font=font_label, width=15)
        entry.grid(row=i // 4, column=(i % 4) * 2 + 1, padx=10, pady=5)
        entries.append(entry)

    # Nút huấn luyện mô hình
    def train_model():
        try:
            selected_model = model_type_var.get()
            if selected_model == "ID3":
                result = subprocess.run(['python', 'trainID3.py'], capture_output=True, text=True)
            elif selected_model == "PLA":
                result = subprocess.run(['python', 'pla_model.py'], capture_output=True, text=True)

            output = result.stdout
            lines = output.split("\n")

            accuracy = float(lines[0].split(":")[1].strip())
            precision = float(lines[1].split(":")[1].strip())
            recall = float(lines[2].split(":")[1].strip())
            f1 = float(lines[3].split(":")[1].strip())

            accuracy_label.config(text=f"Accuracy: {accuracy:.2f}")
            precision_label.config(text=f"Precision: {precision:.2f}")
            recall_label.config(text=f"Recall: {recall:.2f}")
            f1_label.config(text=f"F1-Score: {f1:.2f}")

            messagebox.showinfo("Thông báo", f"Mô hình {selected_model} đã được huấn luyện thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể huấn luyện mô hình: {e}")

    # Nút dự đoán
    def predict():
        try:
            # Lấy dữ liệu từ các ô nhập liệu và chuyển đổi sang kiểu float
            input_data = [float(entry.get()) for entry in entries]
            
            # Chọn mô hình dựa trên loại mô hình đã chọn
            selected_model = model_type_var.get()
            if selected_model == "ID3":
                model_file = 'id3_model.pkl'  # Chọn mô hình ID3
                result = trainID3.predict_from_user_input(model_file, input_data)  # Gọi hàm dự đoán từ trainID3
            elif selected_model == "PLA":
                model_file = 'pla_model.pkl'  # Chọn mô hình PLA
                result = pla_model.predict_from_user_input(model_file, input_data)  # Gọi hàm dự đoán từ pla_model
            
            # Hiển thị kết quả dự đoán
            result_label.config(text=f"Dự đoán: {result}")
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập đúng các giá trị số.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

    

    button_frame = tk.Frame(frame, bg="#f2f2f2")
    button_frame.pack(pady=20)

    train_button = tk.Button(button_frame, text="Huấn luyện mô hình", font=font_button, bg="#4CAF50", fg="white", command=train_model, relief="flat")
    train_button.pack(side="left", padx=20, pady=10)

    predict_button = tk.Button(button_frame, text="Dự đoán", font=font_button, bg="#2196F3", fg="white", command=predict, relief="flat")
    predict_button.pack(side="right", padx=20, pady=10)

    # Kết quả dự đoán
    result_label = tk.Label(frame, text="Dự đoán", font=font_title, bg="#f2f2f2", fg="#333")
    result_label.pack(pady=10)

    # Hiển thị các chỉ số đánh giá
    metrics_frame = tk.Frame(frame, bg="#f2f2f2")
    metrics_frame.pack(pady=20)

    accuracy_label = tk.Label(metrics_frame, text="Accuracy: ", font=font_label, bg="#f2f2f2", anchor="w")
    accuracy_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

    precision_label = tk.Label(metrics_frame, text="Precision: ", font=font_label, bg="#f2f2f2", anchor="w")
    precision_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

    recall_label = tk.Label(metrics_frame, text="Recall: ", font=font_label, bg="#f2f2f2", anchor="w")
    recall_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

    f1_label = tk.Label(metrics_frame, text="F1-Score: ", font=font_label, bg="#f2f2f2", anchor="w")
    f1_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
