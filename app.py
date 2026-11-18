
import streamlit as st
import folium
import pandas as pd
import requests
import json
import math
import base64
import html
import uuid
import os

from pathlib import Path
from streamlit_folium import st_folium


# ============================================================
# A. CAU HINH UNG DUNG
# ============================================================

st.set_page_config(
    page_title="Ha Giang Trip Planner",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = "ha_giang_data.json"

DAY_COLORS = [
    "#E53935",
    "#1565C0",
    "#2E7D32",
    "#8E24AA",
    "#EF6C00",
    "#00838F",
    "#6D4C41",
    "#3949AB"
]

CATEGORY_ICONS = {
    "Check-in": "📸",
    "Ăn uống": "🍜",
    "Lưu trú": "🛏️",
    "Ngủ nghỉ": "🛏️",
    "Khách sạn": "🏨",
    "Homestay": "🏡",
    "Làng bản": "🏘️",
    "Tham quan": "🏛️",
    "Trải nghiệm": "🚣",
    "Thác nước": "💦",
    "Thiên nhiên": "🌲",
    "Văn hóa": "🏯",
    "Leo núi": "🥾",
    "Đô thị": "🏙️",
    "Cung đường": "🛣️",
    "Cà phê": "☕",
    "Khác": "📍"
}

CATEGORIES = list(CATEGORY_ICONS.keys())


# ============================================================
# B. DU LIEU DIA DIEM MAU
# Luu y: toa do tham khao, can kiem tra lai tren Google Maps
# ============================================================

DEFAULT_PLACES = [
    {
        "id": "hg_city",
        "name": "Thành phố Hà Giang",
        "category": "Đô thị",
        "lat": 22.8233,
        "lon": 104.9836,
        "description": "Điểm xuất phát và kết thúc hành trình Hà Giang Loop."
    },
    {
        "id": "quan_ba",
        "name": "Cổng trời Quản Bạ",
        "category": "Check-in",
        "lat": 23.0475,
        "lon": 104.9917,
        "description": "Điểm ngắm cảnh núi đôi và thung lũng Quản Bạ."
    },
    {
        "id": "lung_khuy",
        "name": "Hang Lùng Khúy",
        "category": "Tham quan",
        "lat": 23.0655,
        "lon": 104.9825,
        "description": "Hang động nổi tiếng tại Quản Bạ."
    },
    {
        "id": "yen_minh",
        "name": "Yên Minh",
        "category": "Đô thị",
        "lat": 23.1275,
        "lon": 105.1510,
        "description": "Thị trấn Yên Minh."
    },
    {
        "id": "tham_ma",
        "name": "Dốc Thẩm Mã",
        "category": "Check-in",
        "lat": 23.2470,
        "lon": 105.2240,
        "description": "Cung đường đèo nổi tiếng trên cao nguyên đá."
    },
    {
        "id": "pho_cao",
        "name": "Phố Cáo",
        "category": "Làng bản",
        "lat": 23.2650,
        "lon": 105.2500,
        "description": "Ngôi làng với kiến trúc nhà trình tường."
    },
    {
        "id": "sung_la",
        "name": "Thung lũng Sủng Là",
        "category": "Check-in",
        "lat": 23.2760,
        "lon": 105.2850,
        "description": "Thung lũng nổi tiếng với cảnh quan và văn hóa bản địa."
    },
    {
        "id": "lung_cam",
        "name": "Làng văn hóa Lũng Cẩm",
        "category": "Làng bản",
        "lat": 23.2768,
        "lon": 105.2870,
        "description": "Làng văn hóa với những ngôi nhà trình tường truyền thống."
    },
    {
        "id": "vuong",
        "name": "Dinh thự họ Vương",
        "category": "Tham quan",
        "lat": 23.2780,
        "lon": 105.3030,
        "description": "Di tích kiến trúc lịch sử của cao nguyên đá."
    },
    {
        "id": "lung_cu",
        "name": "Cột cờ Lũng Cú",
        "category": "Check-in",
        "lat": 23.3608,
        "lon": 105.3150,
        "description": "Điểm cực Bắc nổi tiếng của Việt Nam."
    },
    {
        "id": "lo_lo",
        "name": "Làng Lô Lô Chải",
        "category": "Làng bản",
        "lat": 23.3580,
        "lon": 105.3130,
        "description": "Làng văn hóa người Lô Lô dưới chân cột cờ Lũng Cú."
    },
    {
        "id": "dong_van",
        "name": "Phố cổ Đồng Văn",
        "category": "Tham quan",
        "lat": 23.2770,
        "lon": 105.3600,
        "description": "Khu phố cổ với kiến trúc và văn hóa đặc trưng."
    },
    {
        "id": "ma_pi_leng",
        "name": "Đèo Mã Pì Lèng",
        "category": "Check-in",
        "lat": 23.1970,
        "lon": 105.3900,
        "description": "Một trong những cung đèo nổi tiếng nhất Hà Giang."
    },
    {
        "id": "nho_que",
        "name": "Sông Nho Quế",
        "category": "Trải nghiệm",
        "lat": 23.1850,
        "lon": 105.4000,
        "description": "Trải nghiệm ngắm cảnh hoặc đi thuyền trên sông Nho Quế."
    },
    {
        "id": "meo_vac",
        "name": "Thị trấn Mèo Vạc",
        "category": "Đô thị",
        "lat": 23.1580,
        "lon": 105.4050,
        "description": "Trung tâm khu vực Mèo Vạc."
    },
    {
        "id": "pa_vi",
        "name": "Làng H'Mông Pả Vi",
        "category": "Làng bản",
        "lat": 23.1750,
        "lon": 105.3900,
        "description": "Làng văn hóa du lịch cộng đồng người H'Mông."
    },
    {
        "id": "panorama",
        "name": "Mèo Vạc Panorama Cafe",
        "category": "Cà phê",
        "lat": 23.1900,
        "lon": 105.3950,
        "description": "Điểm dừng chân ngắm cảnh khu vực Mã Pì Lèng."
    },
    {
        "id": "mau_due",
        "name": "Mậu Duệ",
        "category": "Đô thị",
        "lat": 23.0850,
        "lon": 105.3000,
        "description": "Khu vực trên cung đường nối Mèo Vạc và Du Già."
    },
    {
        "id": "du_gia",
        "name": "Du Già",
        "category": "Làng bản",
        "lat": 22.9700,
        "lon": 105.2100,
        "description": "Khu vực du lịch cộng đồng nổi tiếng."
    },
    {
        "id": "thac_du_gia",
        "name": "Thác Du Già",
        "category": "Thác nước",
        "lat": 22.9700,
        "lon": 105.2050,
        "description": "Thác nước và điểm tắm suối tại Du Già."
    },
    {
        "id": "thuan_hoa",
        "name": "Thuận Hòa – Thái An",
        "category": "Cung đường",
        "lat": 22.9000,
        "lon": 105.0500,
        "description": "Khu vực cung đường cảnh quan Thuận Hòa – Thái An."
    }
]


# ============================================================
# C. CAC HAM XU LY DU LIEU
# ============================================================

def new_id():
    return uuid.uuid4().hex[:10]


def default_plan():
    return {
        "id": "plan_default",
        "name": "Lịch trình Hà Giang 3N2Đ",
        "days": [
            {
                "name": "Ngày 1",
                "stops": [
                    "hg_city",
                    "quan_ba",
                    "yen_minh",
                    "tham_ma",
                    "sung_la",
                    "dong_van"
                ]
            },
            {
                "name": "Ngày 2",
                "stops": [
                    "dong_van",
                    "lung_cu",
                    "lo_lo",
                    "ma_pi_leng",
                    "nho_que",
                    "meo_vac",
                    "pa_vi"
                ]
            },
            {
                "name": "Ngày 3",
                "stops": [
                    "meo_vac",
                    "mau_due",
                    "du_gia",
                    "thac_du_gia",
                    "hg_city"
                ]
            }
        ]
    }


def initial_data():
    plan = default_plan()
    return {
        "places": DEFAULT_PLACES,
        "plans": [plan],
        "selected_plan_id": plan["id"]
    }


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            if "places" not in data:
                data["places"] = DEFAULT_PLACES

            if "plans" not in data or not data["plans"]:
                data["plans"] = [default_plan()]

            if "selected_plan_id" not in data:
                data["selected_plan_id"] = data["plans"][0]["id"]

            return data
        except Exception:
            pass

    return initial_data()


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_place(place_id):
    for p in st.session_state.data["places"]:
        if p["id"] == place_id:
            return p
    return None


def get_current_plan():
    plans = st.session_state.data["plans"]
    selected_id = st.session_state.data["selected_plan_id"]

    for p in plans:
        if p["id"] == selected_id:
            return p

    st.session_state.data["selected_plan_id"] = plans[0]["id"]
    return plans[0]


def get_icon(category):
    return CATEGORY_ICONS.get(category, "📍")


def haversine_km(lat1, lon1, lat2, lon2):
    radius = 6371

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    return 2 * radius * math.asin(math.sqrt(a))


# ============================================================
# D. TINH TUYEN DUONG OSRM
# ============================================================

@st.cache_data(ttl=3600, show_spinner=False)
def get_osrm_route(lat1, lon1, lat2, lon2):
    url = (
        "https://router.project-osrm.org/route/v1/driving/"
        f"{lon1},{lat1};{lon2},{lat2}"
        "?overview=full&geometries=geojson"
    )

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        result = response.json()

        if result.get("code") != "Ok":
            return None

        route = result["routes"][0]

        coordinates = [
            [point[1], point[0]]
            for point in route["geometry"]["coordinates"]
        ]

        return {
            "distance_km": route["distance"] / 1000,
            "duration_min": route["duration"] / 60,
            "coordinates": coordinates,
            "estimated": False
        }

    except Exception:
        return None


def calculate_day_routes(day, places):
    stops = []

    for place_id in day["stops"]:
        place = next(
            (p for p in places if p["id"] == place_id),
            None
        )
        if place:
            stops.append(place)

    total_distance = 0
    total_duration = 0
    route_segments = []
    all_estimated = False

    for i in range(len(stops) - 1):
        a = stops[i]
        b = stops[i + 1]

        route = get_osrm_route(
            a["lat"], a["lon"],
            b["lat"], b["lon"]
        )

        if route:
            distance = route["distance_km"]
            duration = route["duration_min"]
            coordinates = route["coordinates"]
            estimated = False
        else:
            distance = haversine_km(
                a["lat"], a["lon"],
                b["lat"], b["lon"]
            ) * 1.35

            duration = distance / 30 * 60
            coordinates = [
                [a["lat"], a["lon"]],
                [b["lat"], b["lon"]]
            ]
            estimated = True
            all_estimated = True

        total_distance += distance
        total_duration += duration

        route_segments.append({
            "coordinates": coordinates,
            "distance_km": distance,
            "duration_min": duration,
            "estimated": estimated
        })

    return {
        "stops": stops,
        "distance_km": total_distance,
        "duration_min": total_duration,
        "segments": route_segments,
        "estimated": all_estimated
    }


# ============================================================
# E. TAO BAN DO
# ============================================================

def create_map(plan, places, tile_choice="CartoDB Positron"):
    m = folium.Map(
        location=[23.15, 105.25],
        zoom_start=9,
        tiles=None,
        control_scale=True
    )

    tile_options = {
        "CartoDB Positron": {
            "tiles": "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
            "attr": "© OpenStreetMap © CARTO",
            "max_zoom": 20
        },
        "Esri Street": {
            "tiles": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
            "attr": "Tiles © Esri",
            "max_zoom": 19
        },
        "Esri Satellite": {
            "tiles": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            "attr": "Tiles © Esri",
            "max_zoom": 19
        },
        "OpenStreetMap": {
            "tiles": "OpenStreetMap",
            "attr": "© OpenStreetMap contributors",
            "max_zoom": 19
        }
    }

    selected_tile = tile_options.get(
        tile_choice,
        tile_options["CartoDB Positron"]
    )

    folium.TileLayer(
        tiles=selected_tile["tiles"],
        attr=selected_tile["attr"],
        name=tile_choice,
        max_zoom=selected_tile["max_zoom"],
        show=True
    ).add_to(m)

    all_coords = []
    places_by_id = {p["id"]: p for p in places}

    # Ve tuyen duong theo tung ngay
    for day_index, day in enumerate(plan["days"]):
        color = DAY_COLORS[day_index % len(DAY_COLORS)]

        route_data = calculate_day_routes(day, places)

        for segment in route_data["segments"]:
            folium.PolyLine(
                locations=segment["coordinates"],
                color=color,
                weight=5,
                opacity=0.85,
                dash_array="8, 8" if segment["estimated"] else None,
                tooltip=(
                    f"{day['name']} | "
                    f"{segment['distance_km']:.1f} km"
                    + (" | Ước tính" if segment["estimated"] else "")
                )
            ).add_to(m)

        # Marker theo thu tu trong ngay
        for stop_index, place in enumerate(route_data["stops"]):
            lat = place["lat"]
            lon = place["lon"]
            all_coords.append([lat, lon])

            icon_emoji = get_icon(place.get("category", "Khác"))

            popup_html = f"""
            <div style="width:230px;font-family:Arial">
                <h4 style="margin:0 0 7px 0">
                    {html.escape(place['name'])}
                </h4>
                <div>{html.escape(place.get('category', ''))}</div>
                <p style="margin-top:7px">
                    {html.escape(place.get('description', ''))}
                </p>
                <div style="color:{color};font-weight:bold">
                    {html.escape(day['name'])} - Điểm {stop_index + 1}
                </div>
            """

            if place.get("image"):
                popup_html += (
                    '<img src="data:image/jpeg;base64,'
                    + place["image"]
                    + '" style="width:100%;margin-top:8px;border-radius:6px">'
                )

            if place.get("note"):
                popup_html += (
                    '<p style="margin-top:8px">'
                    + html.escape(place["note"])
                    + '</p>'
                )

            popup_html += "</div>"

            marker_html = f"""
            <div style="
                font-size:25px;
                text-align:center;
                width:34px;
                height:34px;
                line-height:34px;
                background:white;
                border:3px solid {color};
                border-radius:50%;
                box-shadow:0 1px 5px rgba(0,0,0,0.35);
            ">{icon_emoji}</div>
            """

            marker = folium.Marker(
                location=[lat, lon],
                tooltip=folium.Tooltip(
                    html.escape(place["name"]),
                    permanent=True,
                    direction="top",
                    sticky=False
                ),
                popup=folium.Popup(
                    popup_html,
                    max_width=280
                ),
                icon=folium.DivIcon(
                    html=marker_html,
                    icon_size=(36, 36),
                    icon_anchor=(18, 18)
                )
            )

            marker.add_to(m)

    # Neu khong co diem trong lich trinh
    if all_coords:
        m.fit_bounds(all_coords)
    else:
        m.location = [23.15, 105.25]
        m.zoom_start = 9

    folium.LayerControl(collapsed=True).add_to(m)

    # Chu thich mau tuyen
    legend_html = """
    <div style="
        position:fixed;
        bottom:25px;
        left:25px;
        z-index:9999;
        background:white;
        padding:10px 13px;
        border-radius:7px;
        box-shadow:0 1px 6px rgba(0,0,0,0.25);
        font-size:12px;
        max-height:220px;
        overflow:auto;
    ">
        <b>Chú thích tuyến đường</b><br>
    """

    for i, day in enumerate(plan["days"]):
        color = DAY_COLORS[i % len(DAY_COLORS)]
        legend_html += (
            f'<div style="margin-top:5px">'
            f'<span style="display:inline-block;width:22px;'
            f'border-top:4px solid {color};margin-right:6px;'
            f'vertical-align:middle"></span>'
            f'{html.escape(day["name"])}'
            f'</div>'
        )

    legend_html += """
    <div style="margin-top:7px;color:#666">
        Nét đứt: tuyến ước tính khi không lấy được dữ liệu đường đi
    </div>
    </div>
    """

    m.get_root().html.add_child(folium.Element(legend_html))

    return m


# ============================================================
# F. CAC HAM HIEN THI
# ============================================================

def format_duration(minutes):
    hours = int(minutes // 60)
    mins = int(round(minutes % 60))

    if hours > 0:
        return f"{hours} giờ {mins} phút"

    return f"{mins} phút"


def render_summary(plan, places):
    rows = []

    for i, day in enumerate(plan["days"]):
        result = calculate_day_routes(day, places)

        names = [
            p["name"] for p in result["stops"]
        ]

        rows.append({
            "Ngày": day["name"],
            "Thời gian di chuyển": format_duration(
                result["duration_min"]
            ),
            "Các điểm đến": " → ".join(names),
            "Quãng đường (km)": round(
                result["distance_km"], 1
            ),
            "Ghi chú": (
                "Có đoạn ước tính"
                if result["estimated"]
                else "Theo tuyến đường"
            )
        })

    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        total_km = sum(
            row["Quãng đường (km)"] for row in rows
        )

        total_minutes = sum(
            calculate_day_routes(day, places)["duration_min"]
            for day in plan["days"]
        )

        c1, c2 = st.columns(2)
        c1.metric("Tổng quãng đường", f"{total_km:.1f} km")
        c2.metric(
            "Tổng thời gian di chuyển",
            format_duration(total_minutes)
        )


def render_share_view(plan, places):
    st.title("🏔️ Lịch trình khám phá Hà Giang")
    st.caption(
        f"Phương án: {plan['name']} | "
        f"{len(plan['days'])} ngày"
    )

    tile_choice = st.selectbox(
        "Nền bản đồ",
        [
            "CartoDB Positron",
            "Esri Street",
            "Esri Satellite",
            "OpenStreetMap"
        ],
        index=0,
        key="share_tile"
    )

    map_object = create_map(
        plan,
        places,
        tile_choice
    )

    st_folium(
        map_object,
        width=None,
        height=650,
        returned_objects=[]
    )

    st.subheader("Tổng hợp lịch trình")
    render_summary(plan, places)

    st.caption(
        "Khoảng cách và thời gian là ước tính theo tuyến đường "
        "ô tô; thực tế có thể thay đổi theo điều kiện giao thông."
    )


# ============================================================
# G. KHOI TAO SESSION
# ============================================================

if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data
places = data["places"]
plan = get_current_plan()

# Chế độ chia sẻ: chỉ hiển thị bản đồ và bảng tổng hợp
try:
    share_mode = st.query_params.get("view") == "share"
except Exception:
    share_mode = False

if share_mode:
    render_share_view(plan, places)
    st.stop()


# ============================================================
# H. GIAO DIEN CHINH
# ============================================================

st.title("🏔️ Hà Giang Trip Planner")
st.caption(
    "Công cụ lập lịch trình, quản lý địa điểm và theo dõi "
    "tuyến đường khám phá Hà Giang."
)


# ============================================================
# I. QUAN LY CAC PHUONG AN LICH TRINH
# ============================================================

st.sidebar.header("📋 Phương án lịch trình")

plan_names = {
    p["id"]: p["name"]
    for p in data["plans"]
}

plan_ids = list(plan_names.keys())
selected_id = data["selected_plan_id"]

if selected_id not in plan_ids:
    selected_id = plan_ids[0]

selected_plan_id = st.sidebar.selectbox(
    "Chọn phương án",
    plan_ids,
    index=plan_ids.index(selected_id),
    format_func=lambda x: plan_names.get(x, x)
)

data["selected_plan_id"] = selected_plan_id
plan = get_current_plan()

new_plan_name = st.sidebar.text_input(
    "Tên phương án mới",
    placeholder="Ví dụ: Hà Giang 4N3Đ"
)

if st.sidebar.button("➕ Tạo phương án mới", use_container_width=True):
    new_plan = {
        "id": new_id(),
        "name": new_plan_name.strip() or "Phương án mới",
        "days": [
            {"name": "Ngày 1", "stops": []},
            {"name": "Ngày 2", "stops": []},
            {"name": "Ngày 3", "stops": []}
        ]
    }

    data["plans"].append(new_plan)
    data["selected_plan_id"] = new_plan["id"]
    st.rerun()


if st.sidebar.button("📑 Nhân bản phương án hiện tại", use_container_width=True):
    copied = json.loads(json.dumps(plan))
    copied["id"] = new_id()
    copied["name"] = plan["name"] + " - Bản sao"

    data["plans"].append(copied)
    data["selected_plan_id"] = copied["id"]
    st.rerun()


edited_plan_name = st.sidebar.text_input(
    "Đổi tên phương án hiện tại",
    value=plan["name"]
)

if st.sidebar.button("Cập nhật tên phương án", use_container_width=True):
    plan["name"] = edited_plan_name.strip() or plan["name"]
    st.rerun()


if len(data["plans"]) > 1:
    if st.sidebar.button(
        "🗑️ Xóa phương án hiện tại",
        use_container_width=True
    ):
        data["plans"] = [
            p for p in data["plans"]
            if p["id"] != plan["id"]
        ]
        data["selected_plan_id"] = data["plans"][0]["id"]
        st.rerun()


# ============================================================
# J. THANH BEN - LUU / NHAP / XUAT
# ============================================================

st.sidebar.divider()
st.sidebar.header("💾 Dữ liệu")

if st.sidebar.button("💾 Lưu dữ liệu", use_container_width=True):
    save_data(data)
    st.sidebar.success("Đã lưu vào file JSON trên máy chủ.")

json_content = json.dumps(
    data,
    ensure_ascii=False,
    indent=2
)

st.sidebar.download_button(
    "⬇️ Tải dữ liệu JSON",
    data=json_content,
    file_name="ha_giang_data.json",
    mime="application/json",
    use_container_width=True
)

uploaded_json = st.sidebar.file_uploader(
    "Nhập dữ liệu JSON",
    type=["json"],
    key="json_import"
)

if uploaded_json is not None:
    if st.sidebar.button("Nhập dữ liệu JSON", use_container_width=True):
        try:
            imported = json.load(uploaded_json)

            if (
                "places" in imported
                and "plans" in imported
                and imported["plans"]
            ):
                st.session_state.data = imported
                st.success("Đã nhập dữ liệu thành công.")
                st.rerun()
            else:
                st.sidebar.error("File JSON không đúng cấu trúc.")
        except Exception as e:
            st.sidebar.error(f"Lỗi đọc JSON: {e}")


# ============================================================
# K. CAC TAB CHUC NANG
# ============================================================

tab_map, tab_itinerary, tab_places, tab_export = st.tabs([
    "🗺️ Bản đồ",
    "📝 Lịch trình",
    "📍 Thư viện địa điểm",
    "📤 Chia sẻ & Xuất dữ liệu"
])


# ============================================================
# TAB 1: BAN DO
# ============================================================

with tab_map:
    st.subheader("Bản đồ hành trình")

    col1, col2 = st.columns([2, 1])

    with col1:
        tile_choice = st.selectbox(
            "Chọn nền bản đồ",
            [
                "CartoDB Positron",
                "Esri Street",
                "Esri Satellite",
                "OpenStreetMap"
            ],
            key="main_tile"
        )

    with col2:
        st.caption(
            "Các tuyến đường được phân biệt màu theo từng ngày."
        )

    map_object = create_map(
        plan,
        places,
        tile_choice
    )

    st_folium(
        map_object,
        width=None,
        height=650,
        returned_objects=[]
    )

    st.subheader("Tổng hợp quãng đường")
    render_summary(plan, places)


# ============================================================
# TAB 2: QUAN LY LICH TRINH
# ============================================================

with tab_itinerary:
    st.subheader("Chỉnh sửa lịch trình")

    # Them ngay
    col_add_day, col_del_day = st.columns(2)

    with col_add_day:
        if st.button("➕ Thêm ngày"):
            plan["days"].append({
                "name": f"Ngày {len(plan['days']) + 1}",
                "stops": []
            })
            st.rerun()

    with col_del_day:
        if len(plan["days"]) > 1:
            if st.button("➖ Xóa ngày cuối"):
                plan["days"].pop()
                st.rerun()

    for day_index, day in enumerate(plan["days"]):
        color = DAY_COLORS[day_index % len(DAY_COLORS)]

        with st.expander(
            f"{day['name']} - {len(day['stops'])} điểm",
            expanded=True
        ):
            day["name"] = st.text_input(
                "Tên ngày",
                value=day["name"],
                key=f"day_name_{plan['id']}_{day_index}"
            )

            st.markdown(
                f'<span style="color:{color};font-weight:bold">'
                f'● Màu tuyến đường của {html.escape(day["name"])}'
                f'</span>',
                unsafe_allow_html=True
            )

            # Them diem vao ngay
            available_places = [
                p for p in places
                if p["id"] not in day["stops"]
            ]

            if available_places:
                place_options = {
                    p["id"]: f"{get_icon(p['category'])} {p['name']}"
                    for p in available_places
                }

                selected_place = st.selectbox(
                    "Chọn địa điểm để thêm",
                    list(place_options.keys()),
                    format_func=lambda x: place_options[x],
                    key=f"add_place_{plan['id']}_{day_index}"
                )

                if st.button(
                    "➕ Thêm địa điểm vào ngày",
                    key=f"add_stop_{plan['id']}_{day_index}"
                ):
                    day["stops"].append(selected_place)
                    st.rerun()

            else:
                st.info("Không còn địa điểm mới trong thư viện.")

            st.divider()

            # Danh sach diem den
            if not day["stops"]:
                st.info("Ngày này chưa có địa điểm.")
            else:
                for stop_index, place_id in enumerate(day["stops"]):
                    place = get_place(place_id)

                    if not place:
                        continue

                    col_name, col_up, col_down, col_move, col_remove = st.columns(
                        [5, 0.7, 0.7, 1.2, 0.8]
                    )

                    with col_name:
                        st.write(
                            f"{stop_index + 1}. "
                            f"{get_icon(place['category'])} "
                            f"**{place['name']}**"
                        )

                    with col_up:
                        if st.button(
                            "⬆️",
                            key=f"up_{plan['id']}_{day_index}_{stop_index}",
                            disabled=(stop_index == 0)
                        ):
                            day["stops"][stop_index - 1], day["stops"][stop_index] = (
                                day["stops"][stop_index],
                                day["stops"][stop_index - 1]
                            )
                            st.rerun()

                    with col_down:
                        if st.button(
                            "⬇️",
                            key=f"down_{plan['id']}_{day_index}_{stop_index}",
                            disabled=(stop_index == len(day["stops"]) - 1)
                        ):
                            day["stops"][stop_index + 1], day["stops"][stop_index] = (
                                day["stops"][stop_index],
                                day["stops"][stop_index + 1]
                            )
                            st.rerun()

                    with col_move:
                        other_days = [
                            i for i in range(len(plan["days"]))
                            if i != day_index
                        ]

                        if other_days:
                            target_day = st.selectbox(
                                "Chuyển",
                                other_days,
                                format_func=lambda x: plan["days"][x]["name"],
                                key=f"move_target_{plan['id']}_{day_index}_{stop_index}"
                            )

                            if st.button(
                                "Chuyển",
                                key=f"move_{plan['id']}_{day_index}_{stop_index}"
                            ):
                                moved_id = day["stops"].pop(stop_index)
                                plan["days"][target_day]["stops"].append(moved_id)
                                st.rerun()

                    with col_remove:
                        if st.button(
                            "❌",
                            key=f"remove_{plan['id']}_{day_index}_{stop_index}"
                        ):
                            day["stops"].pop(stop_index)
                            st.rerun()

            # Ghi chu va hinh anh cho cac diem trong ngay
            day_places = [
                get_place(pid)
                for pid in day["stops"]
                if get_place(pid)
            ]

            if day_places:
                st.divider()
                note_place = st.selectbox(
                    "Chọn địa điểm để thêm ghi chú / ảnh",
                    [p["id"] for p in day_places],
                    format_func=lambda x: get_place(x)["name"],
                    key=f"note_place_{plan['id']}_{day_index}"
                )

                current_place = get_place(note_place)

                note_value = st.text_area(
                    "Ghi chú",
                    value=current_place.get("note", ""),
                    key=f"note_text_{plan['id']}_{day_index}"
                )

                uploaded_image = st.file_uploader(
                    "Thêm ảnh cho địa điểm",
                    type=["png", "jpg", "jpeg", "webp"],
                    key=f"note_image_{plan['id']}_{day_index}"
                )

                if st.button(
                    "Lưu ghi chú",
                    key=f"save_note_{plan['id']}_{day_index}"
                ):
                    current_place["note"] = note_value

                    if uploaded_image is not None:
                        image_bytes = uploaded_image.getvalue()
                        current_place["image"] = base64.b64encode(
                            image_bytes
                        ).decode("utf-8")

                    st.success("Đã cập nhật ghi chú.")
                    st.rerun()

                if current_place.get("image"):
                    st.image(
                        base64.b64decode(current_place["image"]),
                        caption=current_place["name"],
                        width=300
                    )


# ============================================================
# TAB 3: THU VIEN DIA DIEM
# ============================================================

with tab_places:
    st.subheader("Thư viện địa điểm Hà Giang")

    st.caption(
        "Địa điểm trong thư viện có thể được thêm vào nhiều phương án "
        "và nhiều ngày khác nhau."
    )

    with st.expander("➕ Thêm địa điểm mới", expanded=False):
        with st.form("add_place_form"):
            new_name = st.text_input("Tên địa điểm")
            new_category = st.selectbox(
                "Phân loại",
                CATEGORIES
            )

            c1, c2 = st.columns(2)

            with c1:
                new_lat = st.number_input(
                    "Latitude",
                    value=23.1500,
                    format="%.6f"
                )

            with c2:
                new_lon = st.number_input(
                    "Longitude",
                    value=105.2500,
                    format="%.6f"
                )

            new_description = st.text_area("Mô tả")

            add_submitted = st.form_submit_button(
                "Thêm địa điểm"
            )

            if add_submitted:
                if new_name.strip():
                    places.append({
                        "id": new_id(),
                        "name": new_name.strip(),
                        "category": new_category,
                        "lat": float(new_lat),
                        "lon": float(new_lon),
                        "description": new_description
                    })

                    st.success("Đã thêm địa điểm.")
                    st.rerun()
                else:
                    st.error("Vui lòng nhập tên địa điểm.")

    st.divider()

    # Sua dia diem
    with st.expander("✏️ Chỉnh sửa địa điểm", expanded=False):
        if places:
            edit_id = st.selectbox(
                "Chọn địa điểm",
                [p["id"] for p in places],
                format_func=lambda x: get_place(x)["name"],
                key="edit_place_id"
            )

            edit_place = get_place(edit_id)

            with st.form("edit_place_form"):
                edit_name = st.text_input(
                    "Tên",
                    value=edit_place["name"]
                )

                edit_category = st.selectbox(
                    "Phân loại",
                    CATEGORIES,
                    index=(
                        CATEGORIES.index(edit_place["category"])
                        if edit_place.get("category") in CATEGORIES
                        else CATEGORIES.index("Khác")
                    )
                )

                c1, c2 = st.columns(2)

                with c1:
                    edit_lat = st.number_input(
                        "Latitude",
                        value=float(edit_place["lat"]),
                        format="%.6f"
                    )

                with c2:
                    edit_lon = st.number_input(
                        "Longitude",
                        value=float(edit_place["lon"]),
                        format="%.6f"
                    )

                edit_description = st.text_area(
                    "Mô tả",
                    value=edit_place.get("description", "")
                )

                edit_submitted = st.form_submit_button(
                    "Cập nhật địa điểm"
                )

                if edit_submitted:
                    edit_place["name"] = edit_name.strip()
                    edit_place["category"] = edit_category
                    edit_place["lat"] = float(edit_lat)
                    edit_place["lon"] = float(edit_lon)
                    edit_place["description"] = edit_description

                    st.success("Đã cập nhật.")
                    st.rerun()

    # Xoa dia diem
    with st.expander("🗑️ Xóa địa điểm", expanded=False):
        if places:
            delete_id = st.selectbox(
                "Chọn địa điểm cần xóa",
                [p["id"] for p in places],
                format_func=lambda x: get_place(x)["name"],
                key="delete_place_id"
            )

            if st.button("Xóa địa điểm khỏi thư viện"):
                data["places"] = [
                    p for p in data["places"]
                    if p["id"] != delete_id
                ]

                for p in data["plans"]:
                    for d in p["days"]:
                        d["stops"] = [
                            x for x in d["stops"]
                            if x != delete_id
                        ]

                st.rerun()

    st.divider()

    # Hien thi danh sach
    place_rows = []

    for p in data["places"]:
        place_rows.append({
            "Địa điểm": p["name"],
            "Phân loại": p["category"],
            "Icon": get_icon(p["category"]),
            "Latitude": p["lat"],
            "Longitude": p["lon"]
        })

    st.dataframe(
        pd.DataFrame(place_rows),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TAB 4: CHIA SE VA XUAT DU LIEU
# ============================================================

with tab_export:
    st.subheader("Chia sẻ lịch trình")

    st.markdown(
        "Chế độ chia sẻ chỉ hiển thị bản đồ và bảng tổng hợp. "
        "Các phần chỉnh sửa được ẩn trong giao diện chia sẻ."
    )

    try:
        current_url = st.context.url
        share_url = current_url.split("?")[0] + "?view=share"

        st.code(share_url, language=None)

        st.button(
            "📋 Sao chép link chia sẻ",
            on_click=None,
            disabled=True,
            help="Hãy sao chép đường link phía trên."
        )

    except Exception:
        st.info(
            "Sau khi deploy trên Streamlit Cloud, thêm "
            "?view=share vào cuối URL ứng dụng để mở chế độ chia sẻ."
        )

    st.divider()

    st.subheader("Xuất Excel")

    excel_rows = []

    for day_index, day in enumerate(plan["days"]):
        route_data = calculate_day_routes(day, places)

        for stop_index, place in enumerate(route_data["stops"]):
            excel_rows.append({
                "Ngày": day["name"],
                "Thứ tự": stop_index + 1,
                "Địa điểm": place["name"],
                "Phân loại": place["category"],
                "Latitude": place["lat"],
                "Longitude": place["lon"],
                "Mô tả": place.get("description", ""),
                "Ghi chú": place.get("note", "")
            })

    excel_df = pd.DataFrame(excel_rows)

    import io

    excel_buffer = io.BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:
        excel_df.to_excel(
            writer,
            index=False,
            sheet_name="Lich trinh"
        )

        pd.DataFrame(data["places"]).to_excel(
            writer,
            index=False,
            sheet_name="Thu vien dia diem"
        )

    st.download_button(
        "⬇️ Tải lịch trình Excel",
        data=excel_buffer.getvalue(),
        file_name="lich_trinh_ha_giang.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.divider()

    st.subheader("Xuất dữ liệu JSON")

    st.download_button(
        "⬇️ Tải toàn bộ dữ liệu JSON",
        data=json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ),
        file_name="ha_giang_data.json",
        mime="application/json"
    )


# ============================================================
# L. THONG TIN CUOI TRANG
# ============================================================

st.divider()

st.caption(
    "Ha Giang Trip Planner | "
    "Bản đồ sử dụng dữ liệu nền từ các nhà cung cấp bản đồ bên thứ ba. "
    "Tuyến đường và thời gian chỉ mang tính tham khảo."
)
