# ======== 1. Import thư viện cần thiết ========
import pandas as pd  # Xử lý dữ liệu bảng
import numpy as np   # Tính toán số học
from sklearn.cluster import DBSCAN  # Thuật toán phân cụm DBSCAN
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
# Các chỉ số đánh giá chất lượng phân cụm
from sklearn.decomposition import PCA  # Giảm chiều dữ liệu
import matplotlib.pyplot as plt  # Vẽ biểu đồ
import seaborn as sns  # Vẽ biểu đồ đẹp hơn với matplotlib

# ======== 2. Đọc và tiền xử lý dữ liệu ========
data = pd.read_csv('video_features_scaled.csv')  # Đọc dữ liệu video đã được chuẩn hóa
features = data.drop(['video_name', 'category'], axis=1).fillna(0)
# Loại bỏ cột tên video và nhãn, đồng thời thay thế các giá trị NaN bằng 0

# ======== 3. Giảm chiều dữ liệu bằng PCA ========
pca = PCA(n_components=0.95)  # Chỉ giữ các thành phần chính sao cho tổng phương sai giữ lại ≥ 95%
features_reduced = pca.fit_transform(features)  # Biến đổi dữ liệu
print(f"Số chiều sau PCA: {features_reduced.shape[1]}")  # In ra số chiều mới
print(f"Tỷ lệ phương sai được giữ lại: {sum(pca.explained_variance_ratio_):.4f}")  # Kiểm tra tỉ lệ giữ lại

# ======== 4. Áp dụng DBSCAN ban đầu ========
eps = 2.0  # Khoảng cách lân cận để xét điểm hàng xóm
min_samples = 5  # Số điểm tối thiểu để hình thành 1 cụm
dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric='euclidean')  # Tạo mô hình
labels = dbscan.fit_predict(features_reduced)  # Gán nhãn cụm (-1 là nhiễu)

# ======== 5. Điều chỉnh eps để đạt đúng 8 cụm (không tính nhiễu) ========
cluster_count = len(np.unique(labels)) - (1 if -1 in labels else 0)  # Số cụm thực sự
attempts = 0
max_attempts = 20  # Giới hạn số lần điều chỉnh để tránh lặp vô hạn

while cluster_count != 8 and attempts < max_attempts:
    if cluster_count > 8:
        eps -= 0.05  # Giảm eps nếu cụm nhiều quá
    elif cluster_count < 8:
        eps += 0.05  # Tăng eps nếu cụm ít
    dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric='euclidean')
    labels = dbscan.fit_predict(features_reduced)
    cluster_count = len(np.unique(labels)) - (1 if -1 in labels else 0)
    attempts += 1

# ======== 6. Gán lại số cụm để dễ đọc (bắt đầu từ 1, trừ nhiễu là -1) ========
unique_labels = sorted([l for l in np.unique(labels) if l != -1])
label_map = {old: new+1 for new, old in enumerate(unique_labels)}  # Đánh lại chỉ số cụm từ 1
labels_mapped = np.array([label_map[l] if l in label_map else -1 for l in labels])  # Gán lại nhãn

# ======== 7. Gán nhãn cụm vào DataFrame gốc ========
data['cluster'] = labels_mapped

# ======== 8. Phân tích cụm: tính size, trung bình đặc trưng, ví dụ video ========
cluster_stats = {}
feature_names = data.drop(['video_name', 'category', 'cluster'], axis=1).columns
for label in np.unique(labels_mapped):
    cluster_data = data[data['cluster'] == label]
    cluster_stats[label] = {
        'size': len(cluster_data),  # Số video trong cụm
        'features': cluster_data.drop(['video_name', 'category', 'cluster'], axis=1).mean().to_dict(),
        # Trung bình giá trị các đặc trưng
        'example': cluster_data['video_name'].iloc[0] if len(cluster_data) > 0 else None  # Một video đại diện
    }

# ======== 9. Đánh giá chất lượng phân cụm ========
if cluster_count >= 2:  # Chỉ tính khi có ít nhất 2 cụm (không tính nhiễu)
    non_noise_mask = labels_mapped != -1  # Bỏ các điểm nhiễu
    features_non_noise = features_reduced[non_noise_mask]
    labels_non_noise = labels_mapped[non_noise_mask]

    silhouette = silhouette_score(features_non_noise, labels_non_noise)  # Gần 1 là tốt
    davies_bouldin = davies_bouldin_score(features_non_noise, labels_non_noise)  # Càng thấp càng tốt
    calinski_harabasz = calinski_harabasz_score(features_non_noise, labels_non_noise)  # Càng cao càng tốt
else:
    silhouette = None
    davies_bouldin = None
    calinski_harabasz = None

# ======== 10. In kết quả phân cụm ========
print("Phân tích phân cụm DBSCAN")
print(f"Số lượng cụm: {cluster_count}")
print(f"Số lượng điểm nhiễu: {len(data[data['cluster'] == -1])}")
print(f"Giá trị eps cuối cùng: {eps:.2f}")

print("\nĐánh giá chất lượng phân cụm:")
if cluster_count >= 2:
    print(f"Silhouette Score: {silhouette:.4f} (gần 1 là tốt)")
    print(f"Davies-Bouldin Index: {davies_bouldin:.4f} (càng thấp càng tốt)")
    print(f"Calinski-Harabasz Index: {calinski_harabasz:.4f} (càng cao càng tốt)")
else:
    print("Không thể tính các chỉ số đánh giá vì số lượng cụm < 2.")

# ======== 11. Hàm nhận định cụm dựa vào đặc trưng nổi bật nhất ========
def nhan_dinh_cum(features_dict):
    dac_trung = max(features_dict, key=features_dict.get)  # Đặc trưng lớn nhất
    if dac_trung in ['motion_intensity_scaled', 'optical_flow_mean_scaled']:
        return "Video chuyển động mạnh"
    elif dac_trung in ['mfcc_0_scaled', 'spectral_centroid_scaled']:
        return "Video âm thanh nổi bật"
    elif dac_trung in ['blue_intensity_scaled', 'green_intensity_scaled']:
        return "Video màu sắc sáng"
    elif dac_trung == 'hu_moment_1_scaled':
        return "Video tĩnh, hình dạng đặc trưng"
    elif dac_trung == 'motion_consistency_scaled':
        return "Video ngắn, chuyển động lặp"
    elif dac_trung in ['texture_lbp_variance_scaled', 'edge_density_scaled']:
        return "Video kết cấu phức tạp"
    else:
        return f"Video nổi bật về {dac_trung}"

# ======== 12. In chi tiết từng cụm ========
print("\nChi tiết các cụm:")
for label in sorted(cluster_stats.keys()):
    cluster_name = f"Cụm {label}" if label != -1 else "Nhiễu"
    print(f"\n{cluster_name}:")
    print(f"Kích thước: {cluster_stats[label]['size']} video")
    if label == -1:  # Nếu là nhiễu, hiển thị đặc trưng max
        print("Đặc trưng chính:")
        print(f"  Scene Complexity (max): {data[data['cluster'] == -1]['scene_complexity_scaled'].max():.2f}")
        print(f"  Motion Intensity (max): {data[data['cluster'] == -1]['motion_intensity_scaled'].max():.2f}")
        print("Nhận định: Video có giá trị đặc trưng cực đoan hoặc độc đáo, ví dụ: độ phức tạp cảnh cao (v_Archery_g06_c05.avi).")
    else:
        print("Đặc trưng chính:")
        for feature, value in cluster_stats[label]['features'].items():
            print(f"  {feature}: {value:.2f}")
        nhan_dinh = nhan_dinh_cum(cluster_stats[label]['features'])
        print(f"Nhận định: {nhan_dinh}")
        print(f"Ví dụ video: {cluster_stats[label]['example'] or 'N/A'}")

# ======== 13. Biểu đồ Scatter thể hiện phân cụm trên 2 thành phần chính đầu tiên ========
plt.figure(figsize=(8, 6))
sns.scatterplot(
    x=features_reduced[:, 0],
    y=features_reduced[:, 1],
    hue=[f"Cụm {l}" if l != -1 else "Nhiễu" for l in data['cluster']],
    palette='deep',
    style=[f"Cụm {l}" if l != -1 else "Nhiễu" for l in data['cluster']]
)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('Phân bố các cụm DBSCAN trên không gian 2 thành phần chính')
plt.legend(title='Cụm', loc='best')
plt.show()

# ======== 14. Biểu đồ cột: số lượng video trong từng cụm ========
plt.figure(figsize=(8, 6))
cluster_sizes = pd.Series(data['cluster']).value_counts().sort_index()
cluster_sizes.index = [f"Cụm {i}" if i != -1 else "Nhiễu" for i in cluster_sizes.index]
cluster_sizes.plot(kind='bar')
plt.xlabel('Cụm')
plt.ylabel('Số lượng video')
plt.title('Số lượng video trong từng cụm')
plt.show()
