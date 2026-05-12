from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import pandas as pd
import os
import json
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATA_PATH = "data/Superstore_dataset.csv"
ANNOTATION_PATH = "data/annotations.json"
df = pd.DataFrame()

def load_initial_data():
    global df
    if os.path.exists(DATA_PATH):
        try:
            df = pd.read_csv(DATA_PATH, encoding="latin1")

            df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
            df['Ship Date'] = pd.to_datetime(df['Ship Date'],  errors='coerce')


            df[['Sales', 'Profit', 'Discount', 'Quantity']] = (
                df[['Sales', 'Profit', 'Discount', 'Quantity']].fillna(0)
            )
            df = df.fillna("")

            print(f"Đã load thành công {len(df)} bản ghi.")
        except Exception as e:
            print(f"Lỗi khi đọc CSV: {e}")
    else:
        print("Không tìm thấy file CSV tại đường dẫn data/!")

load_initial_data()


# Bộ lọc
def apply_filters(source_df: pd.DataFrame) -> pd.DataFrame:
    """Đọc query params từ request và lọc DataFrame."""
    p   = request.args
    out = source_df.copy()

    if p.get("year"):
        out = out[out['Order Date'].dt.year == int(p["year"])]
    if p.get("month"):
        out = out[out['Order Date'].dt.month == int(p["month"])]
    if p.get("region"):
        out = out[out['Region'] == p["region"]]
    if p.get("state"):
        out = out[out['State'] == p["state"]]
    if p.get("category"):
        out = out[out['Category'] == p["category"]]
    if p.get("sub_category"):
        out = out[out['Sub-Category'] == p["sub_category"]]
    if p.get("segment"):
        out = out[out['Segment'] == p["segment"]]
    if p.get("customer_name"):
        out = out[out['Customer Name'].str.contains(p["customer_name"], case=False, na=False)]
    if p.get("discount_max"):
        out = out[out['Discount'] <= float(p["discount_max"]) / 100]

    return out


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route('/get_filters', methods=['GET'])
def get_filters():
    global df
    try:
        region_state_map = {
            region: sorted(df[df['Region'] == region]['State'].unique().tolist())
            for region in df['Region'].unique()
        }

        years  = sorted(df['Order Date'].dt.year.dropna().unique().astype(int).tolist(), reverse=True)
        months = sorted(df['Order Date'].dt.month.dropna().unique().astype(int).tolist())

        filters = {
            "years": years,
            "months": months,
            "regions": sorted(df['Region'].unique().tolist()),
            "segments": sorted(df['Segment'].unique().tolist()),
            "categories": sorted(df['Category'].unique().tolist()),
            "states": sorted(df['State'].unique().tolist()),
            "region_state_map": region_state_map,
        }
        return jsonify(filters)
    except Exception as e:
        print(f"Lỗi get_filters: {e}")
        return jsonify({"error": str(e)})


# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — DOANH THU
# ════════════════════════════════════════════════════════════════════════════════

# Lấy các KPIs chính 
@app.route("/api/tab1/kpis", methods=["GET"])
def tab1_kpis():
    filtered = apply_filters(df)

    total_sales = filtered['Sales'].sum()
    total_profit = filtered['Profit'].sum()
    total_orders = filtered['Order ID'].nunique()
    margin = (total_profit / total_sales * 100) if total_sales else 0

    def growth(cur, base):
        return round((cur - base) / base * 100, 1) if base else 0
    
    # Xác định năm đang xem: lấy từ filter nếu có, không thì lấy năm max của filtered
    p = request.args
    if p.get("year"):
        cur_year = int(p["year"])
    else:
        cur_year = int(filtered['Order Date'].dt.year.max()) if len(filtered) else 0
    prev_year = cur_year - 1
 
    # Áp dụng các filter khác (trừ year) lên năm trước
    prev_df = df[df['Order Date'].dt.year == prev_year].copy()
    if p.get("region"):
        prev_df = prev_df[prev_df['Region'] == p["region"]]
    if p.get("state"):
        prev_df = prev_df[prev_df['State'] == p["state"]]
    if p.get("category"):
        prev_df = prev_df[prev_df['Category'] == p["category"]]
    if p.get("segment"):
        prev_df = prev_df[prev_df['Segment'] == p["segment"]]
 
    has_prev = len(prev_df) > 0
    base_sales = prev_df['Sales'].sum()  if has_prev else 0
    base_profit = prev_df['Profit'].sum() if has_prev else 0
    base_orders = prev_df['Order ID'].nunique() if has_prev else 0
    base_margin = (base_profit / base_sales * 100) if base_sales else 0
 
    return jsonify({
        "total_sales": round(total_sales,  2),
        "total_profit": round(total_profit, 2),
        "total_orders": int(total_orders),
        "profit_margin": round(margin, 2),
        "prev_year": prev_year,
        "has_prev": has_prev,
        "growth": {
            "sales": growth(total_sales,  base_sales)  if has_prev else None,
            "profit": growth(total_profit, base_profit) if has_prev else None,
            "orders": growth(total_orders, base_orders) if has_prev else None,
            "margin": round(margin - base_margin, 2)    if has_prev else None,
        }
    })

# Lấy dữ liệu trend doanh thu và lợi nhuận theo tháng 
@app.route("/api/tab1/trend/monthly", methods=["GET"])
def tab1_trend_monthly():
    filtered = apply_filters(df)
    grp = (
        filtered.groupby([filtered['Order Date'].dt.year.rename('year'),
                          filtered['Order Date'].dt.month.rename('month')])
        .agg(sales=('Sales', 'sum'), profit=('Profit', 'sum'))
        .reset_index()
        .sort_values(['year', 'month'])
    )
    grp['label'] = grp['month'].astype(str) + '/' + grp['year'].astype(str)
    return jsonify({
        "labels": grp['label'].tolist(),
        "sales":  grp['sales'].round(2).tolist(),
        "profit": grp['profit'].round(2).tolist(),
    })

# Lấy dữ liệu trend doanh thu và lợi nhuận theo năm
@app.route("/api/tab1/trend/yearly", methods=["GET"])
def tab1_trend_yearly():
    filtered = apply_filters(df)
    grp = (
        filtered.groupby(filtered['Order Date'].dt.year.rename('year'))
        .agg(sales=('Sales', 'sum'), profit=('Profit', 'sum'))
        .reset_index()
        .sort_values('year')
    )
    return jsonify({
        "labels": grp['year'].astype(str).tolist(),
        "sales": grp['sales'].round(2).tolist(),
        "profit": grp['profit'].round(2).tolist(),
    })

# Lấy top bang theo doanh thu và lợi nhuận
@app.route("/api/tab1/top-states", methods=["GET"])
def tab1_top_states():
    filtered = apply_filters(df)
    n = int(request.args.get("n", 10))
    grp = (
        filtered.groupby('State')
        .agg(sales=('Sales', 'sum'), profit=('Profit', 'sum'))
        .reset_index()
        .sort_values('sales', ascending=False)
        .head(n)
    )
    return jsonify({
        "labels": grp['State'].tolist(),
        "sales": grp['sales'].round(2).tolist(),
        "profit": grp['profit'].round(2).tolist(),
    })

# Lấy top thành phố theo doanh thu
@app.route("/api/tab1/top-cities/sales", methods=["GET"])
def tab1_top_cities_sales():
    filtered = apply_filters(df)
    n = int(request.args.get("n", 10))
    grp = (
        filtered.groupby('City')['Sales'].sum()
        .reset_index()
        .sort_values('Sales', ascending=False)
        .head(n)
    )
    return jsonify({
        "labels": grp['City'].tolist(),
        "values": grp['Sales'].round(2).tolist(),
    })

# Lấy top thành phố theo lợi nhuận
@app.route("/api/tab1/top-cities/profit", methods=["GET"])
def tab1_top_cities_profit():
    filtered = apply_filters(df)
    n = int(request.args.get("n", 10))
    grp = (
        filtered.groupby('City')['Profit'].sum()
        .reset_index()
        .sort_values('Profit', ascending=False)
        .head(n)
    )
    return jsonify({
        "labels": grp['City'].tolist(),
        "values": grp['Profit'].round(2).tolist(),
    })


# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — Sản phẩm
# ════════════════════════════════════════════════════════════════════════════════

# Lấy các KPIs chính
@app.route("/api/tab2/kpis", methods=["GET"])
def tab2_kpis():
    filtered = apply_filters(df)

    total_qty = int(filtered['Quantity'].sum())
    avg_discount = round(filtered['Discount'].mean() * 100, 2) if len(filtered) else 0
    total_sales = filtered['Sales'].sum()
    total_profit = filtered['Profit'].sum()

    return jsonify({
        "total_quantity": total_qty,
        "avg_discount": avg_discount,
        "total_sales": round(total_sales,  2),
        "total_profit": round(total_profit, 2),
    })

# Lấy doanh thu, lợi nhuận theo category
@app.route("/api/tab2/category", methods=["GET"])
def tab2_category():
    filtered = apply_filters(df)
    grp = (
        filtered.groupby('Category')
        .agg(sales=('Sales', 'sum'), profit=('Profit', 'sum'), qty=('Quantity', 'sum'))
        .reset_index()
        .sort_values('sales', ascending=False)
    )
    return jsonify({
        "labels": grp['Category'].tolist(),
        "sales": grp['sales'].round(2).tolist(),
        "profit": grp['profit'].round(2).tolist(),
        "qty": grp['qty'].tolist(),
    })

# Lấy doanh thu, lợi nhuận theo sub-category
@app.route("/api/tab2/subcategory", methods=["GET"])
def tab2_subcategory():
    filtered = apply_filters(df)
    grp = (
        filtered.groupby('Sub-Category')
        .agg(sales=('Sales', 'sum'), profit=('Profit', 'sum'))
        .reset_index()
        .sort_values('sales', ascending=False)
    )
    return jsonify({
        "labels": grp['Sub-Category'].tolist(),
        "sales": grp['sales'].round(2).tolist(),
        "profit": grp['profit'].round(2).tolist(),
    })


# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — CUSTOMER
# ════════════════════════════════════════════════════════════════════════════════

# Lấy các KPIs chính
@app.route("/api/tab3/kpis", methods=["GET"])
def tab3_kpis():
    filtered = apply_filters(df)

    unique_customers = filtered['Customer ID'].nunique()
    total_sales = filtered['Sales'].sum()
    total_orders = filtered['Order ID'].nunique()
    sales_per_cust = round(total_sales / unique_customers, 2) if unique_customers else 0

    return jsonify({
        "unique_customers": int(unique_customers),
        "sales_per_customer": sales_per_cust,
        "total_orders": int(total_orders),
    })

# Lấy doanh thu, số đơn theo phân khúc khách hàng
@app.route("/api/tab3/segment", methods=["GET"])
def tab3_segment():
    filtered = apply_filters(df)
    grp = (
        filtered.groupby('Segment')
        .agg(sales=('Sales', 'sum'), orders=('Order ID', 'nunique'))
        .reset_index()
    )
    return jsonify({
        "labels": grp['Segment'].tolist(),
        "sales": grp['sales'].round(2).tolist(),
        "orders": grp['orders'].tolist(),
    })

# Lấy top khách hàng theo doanh thu
@app.route("/api/tab3/top-customers", methods=["GET"])
def tab3_top_customers():
    filtered = apply_filters(df)
    n = int(request.args.get("n", 10))
    grp = (
        filtered.groupby(['Customer ID', 'Customer Name', 'Segment'])
        .agg(
            sales=('Sales', 'sum'),
            profit=('Profit', 'sum'),
            orders=('Order ID', 'nunique'),
        )
        .reset_index()
        .sort_values('sales', ascending=False)
        .head(n)
    )
    max_sales = grp['sales'].max()
    grp['share_pct'] = (grp['sales'] / max_sales * 100).round(1)

    return jsonify(grp.round(2).to_dict(orient="records"))


# ════════════════════════════════════════════════════════════════════════════════
# ANNOTATIONS  (GET / POST / DELETE)
# ════════════════════════════════════════════════════════════════════════════════

# Các annotation sẽ được lưu trong file JSON với cấu trúc
def load_annotations() -> list:
    """Đọc file JSON, trả về list. Tạo file mới nếu chưa tồn tại."""
    if not os.path.exists(ANNOTATION_PATH):
        return []
    try:
        with open(ANNOTATION_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

# Ghi list annotation xuống file JSON
def save_annotations(data: list) -> None:
    """Ghi list annotation xuống file JSON."""
    os.makedirs(os.path.dirname(ANNOTATION_PATH), exist_ok=True)
    with open(ANNOTATION_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# GET lấy danh sách annotations
@app.route("/api/annotations", methods=["GET"])
def get_annotations():
    """Lấy tất cả annotation, có thể lọc theo label (tháng/năm)."""
    annotations = load_annotations()
    label = request.args.get("label")
    if label:
        annotations = [a for a in annotations if a.get("label") == label]
    return jsonify(annotations)

# POST thêm annotation mới
@app.route("/api/annotations", methods=["POST"])
def add_annotation():
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Body JSON không hợp lệ"}), 400

    label = (body.get("label") or "").strip()
    note  = (body.get("note") or "").strip()
    if not label or not note:
        return jsonify({"error": "Thiếu label hoặc note"}), 422

    allowed_types = {"warning", "info", "success"}
    ann_type = body.get("type", "warning")
    if ann_type not in allowed_types:
        ann_type = "warning"

    new_annotation = {
        "id": str(uuid.uuid4()),
        "label": label,
        "note": note,
        "type": ann_type,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    annotations = load_annotations()
    annotations.append(new_annotation)
    save_annotations(annotations)

    return jsonify(new_annotation), 201

# DELETE xoá annotation theo ID
@app.route("/api/annotations/<ann_id>", methods=["DELETE"])
def delete_annotation(ann_id: str):
    """Xoá annotation theo ID."""
    annotations = load_annotations()
    original_len = len(annotations)
    annotations = [a for a in annotations if a.get("id") != ann_id]

    if len(annotations) == original_len:
        return jsonify({"error": "Không tìm thấy annotation"}), 404

    save_annotations(annotations)
    return jsonify({"deleted": ann_id}), 200


# ── RUN ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000)