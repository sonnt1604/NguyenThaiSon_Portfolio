/* ══════════════════════════════════════════════════════════════════════
   app.js  —  Khớp hoàn toàn với index.html
   IDs tham chiếu được kiểm tra 1-1 với HTML
   ══════════════════════════════════════════════════════════════════════ */

Chart.defaults.color = '#8b91a8';
Chart.defaults.borderColor = '#252a3a';

const C = {
    accent: '#f0a832',
    green:  '#34c78a',
    blue:   '#5b9ef9',
    red:    '#e05c6a',
    purple: '#9b7de8',
};

let charts = {};
let activeFilters = { tab1: {}, tab2: {}, tab3: {} };


/* ══════════════════════════════════════════════════════════════════════
   UTILS
   ══════════════════════════════════════════════════════════════════════ */

async function api(endpoint, filters = {}) {
    const params = new URLSearchParams(
        Object.fromEntries(Object.entries(filters).filter(([, v]) => v))
    );
    const res = await fetch(`${endpoint}?${params}`);
    if (!res.ok) throw new Error(`API ${endpoint} lỗi: ${res.status}`);
    return res.json();
}

function setText(id, val) {
    const el = document.getElementById(id);
    if (el) el.textContent = val;
}

function setGrowth(id, pct, unit = '%', prevYear = null) {
    const el = document.getElementById(id);
    if (!el) return;
    // pct = null nghĩa là không có dữ liệu năm trước (VD: đang xem 2014)
    if (pct === null || pct === undefined) {
        el.innerHTML = `<small style="color:#64748b">Không có dữ liệu năm trước</small>`;
        return;
    }
    const color   = pct >= 0 ? C.green : C.red;
    const icon    = pct >= 0 ? '▲' : '▼';
    const yearStr = prevYear ? ` so với ${prevYear}` : ' so với năm trước';
    el.innerHTML = `<span style="color:${color}">${icon} ${Math.abs(pct).toFixed(1)}${unit}</span> <small>${yearStr}</small>`;
}

function mkChart(key, canvasId, config) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    if (charts[key]) charts[key].destroy();
    charts[key] = new Chart(canvas.getContext('2d'), config);
}


/* ══════════════════════════════════════════════════════════════════════
   ĐỒNG HỒ
   ══════════════════════════════════════════════════════════════════════ */

function startClock() {
    const el = document.getElementById('clock');
    if (!el) return;
    setInterval(() => {
        el.textContent = new Date().toLocaleTimeString('vi-VN');
    }, 1000);
}


/* ══════════════════════════════════════════════════════════════════════
   KHỞI TẠO BỘ LỌC
   ══════════════════════════════════════════════════════════════════════ */

async function initFilters() {
    const f = await api('/get_filters');

    ['t1', 't2', 't3'].forEach(prefix => {
        populate(`${prefix}-year`,     f.years);
        populate(`${prefix}-month`,    f.months, m => `Tháng ${m}`);
        populate(`${prefix}-region`,   f.regions);
        populate(`${prefix}-state`,    f.states);
        populate(`${prefix}-category`, f.categories);
        populate(`${prefix}-segment`,  f.segments);

        // Cascading: Region → State
        const regEl   = document.getElementById(`${prefix}-region`);
        const stateEl = document.getElementById(`${prefix}-state`);
        if (regEl && stateEl) {
            regEl.addEventListener('change', () => {
                const reg    = regEl.value;
                const states = reg ? (f.region_state_map?.[reg] || []) : f.states;
                populate(`${prefix}-state`, states);
            });
        }
    });

    // Tổng record sẽ được cập nhật sau khi renderTab1 xong
}

function populate(id, values, labelFn = null) {
    const el = document.getElementById(id);
    if (!el || !values) return;
    el.innerHTML = '<option value="">Tất cả</option>';
    values.forEach(v => {
        const opt       = document.createElement('option');
        opt.value       = v;
        opt.textContent = labelFn ? labelFn(v) : v;
        el.appendChild(opt);
    });
}


/* ══════════════════════════════════════════════════════════════════════
   ĐỌC FILTER TỪ DOM
   ══════════════════════════════════════════════════════════════════════ */

function readFilters(tabPrefix) {
    const ids = ['year', 'month', 'region', 'state', 'category', 'segment'];
    const result = {};
    ids.forEach(id => {
        const el = document.getElementById(`${tabPrefix}-${id}`);
        if (el && el.value) result[id] = el.value;
    });
    return result;
}


/* ══════════════════════════════════════════════════════════════════════
   APPLY / CLEAR  (gọi từ HTML)
   ══════════════════════════════════════════════════════════════════════ */

window.applyFilters = function(tabId) {
    const prefix = tabId.replace('tab', 't');
    activeFilters[tabId] = readFilters(prefix);
    renderTab(tabId);
};

window.clearFilters = function(tabId) {
    const prefix = tabId.replace('tab', 't');
    ['year', 'month', 'region', 'state', 'category', 'segment'].forEach(id => {
        const el = document.getElementById(`${prefix}-${id}`);
        if (el) el.selectedIndex = 0;
    });
    activeFilters[tabId] = {};
    renderTab(tabId);
};


/* ══════════════════════════════════════════════════════════════════════
   SWITCH TAB  (gọi từ HTML)
   ══════════════════════════════════════════════════════════════════════ */

window.switchTab = function(tabId, element) {
    document.querySelectorAll('.content').forEach(t => t.classList.add('tab-hidden'));
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    document.getElementById(tabId)?.classList.remove('tab-hidden');
    element?.classList.add('active');

    const titles = { tab1: 'Doanh thu', tab2: 'Sản phẩm', tab3: 'Khách hàng' };
    setText('pageTitle', titles[tabId] || '');

    renderTab(tabId);
};


/* ══════════════════════════════════════════════════════════════════════
   RENDER THEO TAB
   ══════════════════════════════════════════════════════════════════════ */

async function renderTab(tabId) {
    const f = activeFilters[tabId] || {};
    try {
        if (tabId === 'tab1') await renderTab1(f);
        if (tabId === 'tab2') await renderTab2(f);
        if (tabId === 'tab3') await renderTab3(f);
    } catch (err) {
        console.error(`renderTab ${tabId}:`, err);
    }
}


/* ══════════════════════════════════════════════════════════════════════
   TAB 1 — DOANH THU
   KPI IDs:   totalSales | totalProfit | profitMargin | totalOrders
              salesGrowth | profitGrowth | marginGrowth | orderGrowth
   Canvas:    lineMonthly | lineYearly | stateBarChart
              citySalesBar | cityProfitBar
   ══════════════════════════════════════════════════════════════════════ */

async function renderTab1(f) {
    const [kpis, monthly, yearly, states, citySales, cityProfit] = await Promise.all([
        api('/api/tab1/kpis',              f),
        api('/api/tab1/trend/monthly',     f),
        api('/api/tab1/trend/yearly',      f),
        api('/api/tab1/top-states',        { ...f, n: 10 }),
        api('/api/tab1/top-cities/sales',  { ...f, n: 10 }),
        api('/api/tab1/top-cities/profit', { ...f, n: 10 }),
    ]);

    // ── KPIs ──────────────────────────────────────────────────────────
    setText('totalSales',   `$${(kpis.total_sales  / 1e6).toFixed(2)}M`);
    setText('totalProfit',  `$${(kpis.total_profit / 1e3).toFixed(1)}K`);
    setText('profitMargin', `${kpis.profit_margin.toFixed(1)}%`);
    setText('totalOrders',  kpis.total_orders.toLocaleString());

    setGrowth('salesGrowth',  kpis.growth.sales,  '%',  kpis.prev_year);
    setGrowth('profitGrowth', kpis.growth.profit, '%',  kpis.prev_year);
    setGrowth('orderGrowth',  kpis.growth.orders, '%',  kpis.prev_year);
    setGrowth('marginGrowth', kpis.growth.margin, 'pp', kpis.prev_year);

    setText('sidebar-record-count', `${kpis.total_orders.toLocaleString()} records`);

    // ── Line chart — tháng (có annotation) ───────────────────────────
    drawLineMonthly(monthly);

    // ── Line chart — năm (có annotation) ─────────────────────────────
    drawLineYearly(yearly);

    // ── Grouped bar — Top States ──────────────────────────────────────
    mkChart('stateBar', 'stateBarChart', {
        type: 'bar',
        data: {
            labels: states.labels,
            datasets: [
                barDs('Sales',  states.sales,  C.accent),
                barDs('Profit', states.profit, C.green),
            ],
        },
        options: barOpts({ tickCb: v => '$' + (v / 1000) + 'K' }),
    });

    // ── Horizontal bar — Top Cities Sales ────────────────────────────
    mkChart('citySales', 'citySalesBar',
        hBarConfig(citySales.labels, citySales.values, 'Doanh thu', C.accent,
            v => '$' + (v / 1000).toFixed(0) + 'K')
    );

    // ── Horizontal bar — Top Cities Profit ───────────────────────────
    mkChart('cityProfit', 'cityProfitBar',
        hBarConfig(cityProfit.labels, cityProfit.values, 'Lợi nhuận', C.green,
            v => '$' + (v / 1000).toFixed(0) + 'K')
    );
}


/* ══════════════════════════════════════════════════════════════════════
   TAB 2 — SẢN PHẨM
   KPI IDs:   t2-totalSales | t2-totalProfit | t2-totalQuantity | t2-avgDiscount
   Canvas:    categoryStackedBar | categorySalesBar | subCategoryHorizontalStackedBar
   ══════════════════════════════════════════════════════════════════════ */

async function renderTab2(f) {
    const [kpis, category, subcat] = await Promise.all([
        api('/api/tab2/kpis',        f),
        api('/api/tab2/category',    f),
        api('/api/tab2/subcategory', f),
    ]);

    // ── KPIs ──────────────────────────────────────────────────────────
    setText('t2-totalSales',    `$${(kpis.total_sales  / 1e6).toFixed(2)}M`);
    setText('t2-totalProfit',   `$${(kpis.total_profit / 1e3).toFixed(0)}K`);
    setText('t2-totalQuantity', kpis.total_quantity.toLocaleString());
    setText('t2-avgDiscount',   `${kpis.avg_discount.toFixed(0)}%`);

    // ── Stacked bar — Category ────────────────────────────────────────
    mkChart('catStacked', 'categoryStackedBar', {
        type: 'bar',
        data: {
            labels: category.labels,
            datasets: [
                barDs('Lợi nhuận', category.profit, C.green),
                barDs('Doanh thu', category.sales,  C.accent),
            ],
        },
        options: barOpts({
            stacked: true,
            tickCb: v => '$' + (v / 1000).toFixed(0) + 'K',
        }),
    });

    // ── Horizontal bar — Category Sales ──────────────────────────────
    mkChart('topCat', 'categorySalesBar',
        hBarConfig(category.labels, category.sales, 'Doanh thu',
            [C.accent, C.blue, C.purple],
            v => '$' + (v / 1000).toFixed(0) + 'K')
    );

    // ── Vertical bar — Sub-Category ───────────────────────────────────
    mkChart('topSubCat', 'subCategoryHorizontalStackedBar', {
        type: 'bar',
        data: {
            labels: subcat.labels,
            datasets: [barDs('Doanh thu', subcat.sales, C.accent)],
        },
        options: barOpts({ tickCb: v => '$' + (v / 1000).toFixed(0) + 'K' }),
    });
}


/* ══════════════════════════════════════════════════════════════════════
   TAB 3 — KHÁCH HÀNG
   KPI IDs:   t3-totalCustomers | t3-salesPerCustomer | t3-profitPerCustomer
   Canvas:    segmentPieChart
   Table:     leaderboardBody
   ══════════════════════════════════════════════════════════════════════ */

async function renderTab3(f) {
    const [kpis, segment, topCustomers] = await Promise.all([
        api('/api/tab3/kpis',          f),
        api('/api/tab3/segment',       f),
        api('/api/tab3/top-customers', { ...f, n: 10 }),
    ]);

    // ── KPIs ──────────────────────────────────────────────────────────
    setText('t3-totalCustomers',    kpis.unique_customers.toLocaleString());
    setText('t3-salesPerCustomer',  `$${kpis.sales_per_customer.toLocaleString()}`);

    // t3-profitPerCustomer: tính từ dữ liệu KPI Tab3 trả về
    const profitPerCust = topCustomers.length
        ? (topCustomers.reduce((s, c) => s + c.profit, 0) / kpis.unique_customers)
        : 0;
    setText('t3-profitPerCustomer', `$${profitPerCust.toFixed(0)}`);

    // ── Pie — Segment (đếm số đơn hàng) ─────────────────────────────
    mkChart('segPie', 'segmentPieChart', {
        type: 'pie',
        data: {
            labels: segment.labels,
            datasets: [{
                data: segment.orders,           // đơn hàng theo segment
                backgroundColor: [C.accent, C.blue, C.purple],
                borderColor: '#1e2230',
                borderWidth: 2,
                hoverOffset: 15,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: { padding: 15 },
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: { color: '#8b91a8', usePointStyle: true, padding: 20 },
                },
                tooltip: {
                    callbacks: {
                        label: ctx => {
                            const total = ctx.dataset.data.reduce((a, b) => a + b, 0);
                            const pct   = (ctx.parsed / total * 100).toFixed(1);
                            return ` ${ctx.label}: ${ctx.parsed.toLocaleString()} đơn (${pct}%)`;
                        },
                    },
                },
            },
        },
    });

    // ── Leaderboard Table ─────────────────────────────────────────────
    const body = document.getElementById('leaderboardBody');
    if (body && topCustomers.length) {
        const maxSales = topCustomers[0].sales;
        body.innerHTML = topCustomers.map((c, i) => `
            <tr>
                <td><span class="rank-badge">${i + 1}</span></td>
                <td>${c['Customer Name']}</td>
                <td>${c.Segment}</td>
                <td>${c.orders}</td>
                <td>$${c.sales.toLocaleString()}</td>
                <td style="color:${c.profit >= 0 ? C.green : C.red}">
                    $${c.profit.toFixed(0)}
                </td>
            </tr>
        `).join('');
    }
}


/* ══════════════════════════════════════════════════════════════════════
   CHART HELPER FACTORIES
   ══════════════════════════════════════════════════════════════════════ */

function lineDs(label, data, color, fill = true) {
    return {
        label, data,
        borderColor:     color,
        backgroundColor: fill ? color + '18' : 'transparent',
        fill, tension: 0.3, pointRadius: 2,
    };
}

function barDs(label, data, color) {
    return { label, data, backgroundColor: color, borderRadius: 4 };
}

function lineOpts({ tickCb = null, maxTicks = 0 } = {}) {
    return {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false },
        plugins: {
            legend: { labels: { color: '#8b91a8', boxWidth: 12 } },
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: { color: 'rgba(255,255,255,0.05)' },
                ticks: { color: '#8b91a8', callback: tickCb },
            },
            x: {
                grid: { display: false },
                ticks: {
                    color: '#8b91a8',
                    ...(maxTicks ? { maxTicksLimit: maxTicks, autoSkip: true, maxRotation: 45, minRotation: 45 } : {}),
                },
            },
        },
    };
}

function barOpts({ stacked = false, tickCb = null } = {}) {
    return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: true, position: 'top', labels: { color: '#8b91a8', boxWidth: 12 } },
        },
        scales: {
            x: { stacked, grid: { display: false }, ticks: { color: '#8b91a8' } },
            y: {
                stacked,
                beginAtZero: true,
                grid: { color: 'rgba(255,255,255,0.05)' },
                ticks: { color: '#8b91a8', callback: tickCb },
            },
        },
    };
}

function hBarConfig(labels, values, label, color, tickCb = null) {
    return {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                label,
                data: values,
                backgroundColor: color,
                borderRadius: 4,
                barThickness: 18,
            }],
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: {
                    beginAtZero: true,
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    ticks: { color: '#8b91a8', callback: tickCb },
                },
                y: {
                    grid: { display: false },
                    ticks: { color: '#8b91a8', font: { size: 11 } },
                },
            },
        },
    };
}


/* ══════════════════════════════════════════════════════════════════════
   ANNOTATIONS — POST / GET / DELETE
   ══════════════════════════════════════════════════════════════════════ */

// ── Màu theo type ─────────────────────────────────────────────────────
const ANN_STYLE = {
    warning: { icon: '⚠️', color: C.accent,  pointColor: '#f0a832' },
    info:    { icon: 'ℹ️', color: C.blue,    pointColor: '#5b9ef9' },
    success: { icon: '✅', color: C.green,   pointColor: '#34c78a' },
};

// ── State ─────────────────────────────────────────────────────────────
let allAnnotations = [];   // cache local

// ── Load tất cả annotation từ server ─────────────────────────────────
async function fetchAnnotations() {
    try {
        allAnnotations = await api('/api/annotations');
    } catch {
        allAnnotations = [];
    }
}

// ── Lưu annotation mới (POST) ─────────────────────────────────────────
async function postAnnotation(label, note, type) {
    const res = await fetch('/api/annotations', {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ label, note, type }),
    });
    if (!res.ok) throw new Error('POST annotation thất bại');
    const saved = await res.json();
    allAnnotations.push(saved);
    return saved;
}

// ── Xoá annotation (DELETE) ───────────────────────────────────────────
async function deleteAnnotation(id) {
    await fetch(`/api/annotations/${id}`, { method: 'DELETE' });
    allAnnotations = allAnnotations.filter(a => a.id !== id);
}

// ── Lấy annotation theo label ─────────────────────────────────────────
function getAnnotationsByLabel(label) {
    return allAnnotations.filter(a => a.label === label);
}

// ── Tạo panel ghi chú nổi (modal) ────────────────────────────────────
function buildAnnotationPanel() {
    if (document.getElementById('ann-panel')) return;

    const panel = document.createElement('div');
    panel.id = 'ann-panel';
    panel.style.cssText = `
        display:none; position:fixed; z-index:9999;
        background:#1a1f2e; border:1px solid #2d3650;
        border-radius:12px; padding:20px; width:320px;
        box-shadow:0 8px 32px rgba(0,0,0,.5);
        font-family:'DM Sans',sans-serif;
    `;
    panel.innerHTML = `
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
            <span id="ann-panel-title" style="font-size:13px;font-weight:600;color:#e2e8f0;">
                Ghi chú — <span id="ann-label-display"></span>
            </span>
            <button onclick="closeAnnotationPanel()"
                style="background:none;border:none;color:#64748b;font-size:18px;cursor:pointer;line-height:1;">×</button>
        </div>

        <!-- Danh sách annotation hiện có -->
        <div id="ann-list" style="margin-bottom:14px;max-height:160px;overflow-y:auto;"></div>

        <!-- Form thêm mới -->
        <div style="border-top:1px solid #2d3650;padding-top:14px;">
            <div style="font-size:11px;color:#64748b;margin-bottom:8px;text-transform:uppercase;letter-spacing:1px;">
                Thêm ghi chú mới
            </div>
            <textarea id="ann-note-input" rows="2" placeholder="Nhập ghi chú..."
                style="width:100%;background:#0f1420;border:1px solid #2d3650;border-radius:6px;
                       color:#e2e8f0;padding:8px 10px;font-size:12px;resize:none;
                       font-family:inherit;outline:none;"></textarea>
            <div style="display:flex;gap:6px;margin-top:8px;">
                <select id="ann-type-select"
                    style="background:#0f1420;border:1px solid #2d3650;border-radius:6px;
                           color:#e2e8f0;padding:6px 8px;font-size:11px;flex:1;cursor:pointer;">
                    <option value="warning">⚠️ Cảnh báo</option>
                    <option value="info">ℹ️ Ghi chú</option>
                    <option value="success">✅ Tích cực</option>
                </select>
                <button onclick="submitAnnotation()"
                    style="background:#f0a832;border:none;border-radius:6px;color:#0a0e1a;
                           font-weight:700;font-size:12px;padding:6px 16px;cursor:pointer;">
                    Lưu
                </button>
            </div>
        </div>
    `;
    document.body.appendChild(panel);
}

// ── Mở panel tại vị trí click ─────────────────────────────────────────
function openAnnotationPanel(label, x, y) {
    buildAnnotationPanel();
    const panel = document.getElementById('ann-panel');

    // Hiển thị label
    document.getElementById('ann-label-display').textContent = label;
    panel.dataset.currentLabel = label;
    document.getElementById('ann-note-input').value = '';

    // Render danh sách annotation đã có cho label này
    renderAnnotationList(label);

    // Định vị panel gần điểm click, tránh ra ngoài màn hình
    const pw = 320, ph = 320;
    let px = x + 12, py = y - ph / 2;
    if (px + pw > window.innerWidth  - 20) px = x - pw - 12;
    if (py < 10)                           py = 10;
    if (py + ph > window.innerHeight - 10) py = window.innerHeight - ph - 10;

    panel.style.left    = px + 'px';
    panel.style.top     = py + 'px';
    panel.style.display = 'block';
}

window.closeAnnotationPanel = function() {
    const panel = document.getElementById('ann-panel');
    if (panel) panel.style.display = 'none';
};

// ── Render danh sách ghi chú trong panel ─────────────────────────────
function renderAnnotationList(label) {
    const list = document.getElementById('ann-list');
    if (!list) return;
    const items = getAnnotationsByLabel(label);

    if (!items.length) {
        list.innerHTML = `<div style="font-size:12px;color:#64748b;text-align:center;padding:8px 0;">
            Chưa có ghi chú nào</div>`;
        return;
    }

    list.innerHTML = items.map(a => {
        const st = ANN_STYLE[a.type] || ANN_STYLE.warning;
        return `
        <div style="display:flex;align-items:flex-start;gap:8px;margin-bottom:10px;
                    background:#0f1420;border-radius:6px;padding:8px 10px;
                    border-left:3px solid ${st.color};">
            <span style="font-size:14px;line-height:1.4;">${st.icon}</span>
            <div style="flex:1;min-width:0;">
                <div style="font-size:12px;color:#e2e8f0;word-break:break-word;">${a.note}</div>
                <div style="font-size:10px;color:#64748b;margin-top:4px;">${a.created_at}</div>
            </div>
            <button onclick="removeAnnotation('${a.id}')"
                style="background:none;border:none;color:#64748b;cursor:pointer;
                       font-size:14px;padding:0;line-height:1;flex-shrink:0;">🗑</button>
        </div>`;
    }).join('');
}

// ── Submit ghi chú mới ────────────────────────────────────────────────
window.submitAnnotation = async function() {
    const panel = document.getElementById('ann-panel');
    const label = panel?.dataset.currentLabel;
    const note  = document.getElementById('ann-note-input')?.value.trim();
    const type  = document.getElementById('ann-type-select')?.value;

    if (!note) {
        document.getElementById('ann-note-input').style.borderColor = C.red;
        return;
    }
    document.getElementById('ann-note-input').style.borderColor = '#2d3650';

    try {
        await postAnnotation(label, note, type);
        document.getElementById('ann-note-input').value = '';
        renderAnnotationList(label);

        // Redraw line charts để cập nhật điểm có annotation
        const f = activeFilters['tab1'] || {};
        const [monthly, yearly] = await Promise.all([
            api('/api/tab1/trend/monthly', f),
            api('/api/tab1/trend/yearly',  f),
        ]);
        drawLineMonthly(monthly);
        drawLineYearly(yearly);
    } catch (err) {
        console.error('Lưu annotation thất bại:', err);
    }
};

// ── Xoá ghi chú ──────────────────────────────────────────────────────
window.removeAnnotation = async function(id) {
    await deleteAnnotation(id);
    const panel  = document.getElementById('ann-panel');
    const label  = panel?.dataset.currentLabel;
    if (label) renderAnnotationList(label);

    // Redraw charts
    const f = activeFilters['tab1'] || {};
    const [monthly, yearly] = await Promise.all([
        api('/api/tab1/trend/monthly', f),
        api('/api/tab1/trend/yearly',  f),
    ]);
    drawLineMonthly(monthly);
    drawLineYearly(yearly);
};

// ── Plugin vẽ điểm annotation lên Chart.js ───────────────────────────
function makeAnnotationPlugin(chartKey) {
    return {
        id: `ann-${chartKey}`,
        afterDraw(chart) {
            const { ctx, scales: { x, y } } = chart;
            chart.data.labels.forEach((label, i) => {
                const items = getAnnotationsByLabel(label);
                if (!items.length) return;

                // Lấy màu theo type đầu tiên
                const st  = ANN_STYLE[items[0].type] || ANN_STYLE.warning;
                const xPx = x.getPixelForValue(i);
                const yPx = y.getPixelForValue(
                    chart.data.datasets[0].data[i] ?? 0
                ) - 18;

                ctx.save();
                ctx.font      = '14px serif';
                ctx.textAlign = 'center';
                ctx.fillText(st.icon, xPx, yPx);

                // Badge số lượng nếu > 1
                if (items.length > 1) {
                    ctx.fillStyle    = st.color;
                    ctx.font         = 'bold 9px DM Sans, sans-serif';
                    ctx.fillText(`×${items.length}`, xPx + 9, yPx - 6);
                }
                ctx.restore();
            });
        },
    };
}

// ── Hàm click handler gắn vào chart ──────────────────────────────────
function attachClickHandler(chartKey, canvasId) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    canvas.addEventListener('click', function(e) {
        const chart = charts[chartKey];
        if (!chart) return;
        const pts = chart.getElementsAtEventForMode(e, 'index', { intersect: false }, true);
        if (!pts.length) return;

        const idx   = pts[0].index;
        const label = chart.data.labels[idx];
        const rect  = canvas.getBoundingClientRect();
        openAnnotationPanel(label, rect.left + pts[0].element.x, rect.top + pts[0].element.y + window.scrollY);
    });
    canvas.style.cursor = 'pointer';
}


/* ══════════════════════════════════════════════════════════════════════
   TÁCH HÀM VẼ LINE CHART ĐỂ DÙNG LẠI KHI REDRAW
   ══════════════════════════════════════════════════════════════════════ */

function drawLineMonthly(monthly) {
    if (charts['lineMonthly']) charts['lineMonthly'].destroy();
    const canvas = document.getElementById('lineMonthly');
    if (!canvas) return;
    charts['lineMonthly'] = new Chart(canvas.getContext('2d'), {
        type: 'line',
        data: {
            labels: monthly.labels,
            datasets: [
                lineDs('Sales',  monthly.sales,  C.accent),
                lineDs('Profit', monthly.profit, C.green, false),
            ],
        },
        options: lineOpts({ tickCb: v => '$' + (v / 1000).toFixed(0) + 'K', maxTicks: 20 }),
        plugins: [makeAnnotationPlugin('lineMonthly')],
    });
    attachClickHandler('lineMonthly', 'lineMonthly');
}

function drawLineYearly(yearly) {
    if (charts['lineYearly']) charts['lineYearly'].destroy();
    const canvas = document.getElementById('lineYearly');
    if (!canvas) return;
    charts['lineYearly'] = new Chart(canvas.getContext('2d'), {
        type: 'line',
        data: {
            labels: yearly.labels,
            datasets: [
                lineDs('Doanh thu', yearly.sales,  C.accent),
                lineDs('Lợi nhuận', yearly.profit, C.green, false),
            ],
        },
        options: lineOpts({ tickCb: v => '$' + (v / 1000).toFixed(0) + 'K' }),
        plugins: [makeAnnotationPlugin('lineYearly')],
    });
    attachClickHandler('lineYearly', 'lineYearly');
}




document.addEventListener('DOMContentLoaded', async () => {
    startClock();
    await initFilters();
    await fetchAnnotations();   // load annotation trước khi vẽ chart
    await renderTab('tab1');
});