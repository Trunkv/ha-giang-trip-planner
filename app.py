
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
import io
import hashlib

from pathlib import Path
from streamlit_folium import st_folium


# ============================================================
# A. CAU HINH
# ============================================================

st.set_page_config(
    page_title="Ha Giang Trip Planner",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = "ha_giang_data.json"
SUPABASE_TABLE = "trip_planner_data"
SUPABASE_RECORD_ID = "ha_giang_trip_planner"

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

# Font Awesome icon + mau rieng theo danh muc
CATEGORY_ICONS = {
    "Check-in": ("camera", "#E53935"),
    "Ăn uống": ("utensils", "#FB8C00"),
    "Lưu trú": ("bed", "#3949AB"),
    "Ngủ nghỉ": ("bed", "#3949AB"),
    "Khách sạn": ("hotel", "#3949AB"),
    "Homestay": ("house", "#8E24AA"),
    "Làng bản": ("house-chimney", "#795548"),
    "Tham quan": ("landmark", "#1565C0"),
    "Trải nghiệm": ("person-hiking", "#00897B"),
    "Thác nước": ("water", "#039BE5"),
    "Thiên nhiên": ("mountain-sun", "#2E7D32"),
    "Văn hóa": ("monument", "#8E24AA"),
    "Leo núi": ("mountain", "#2E7D32"),
    "Đô thị": ("city", "#546E7A"),
    "Cung đường": ("road", "#607D8B"),
    "Cà phê": ("mug-hot", "#6D4C41"),
    "Khác": ("location-dot", "#757575")
}

CATEGORIES = list(CATEGORY_ICONS.keys())


def get_icon(category):
    return CATEGORY_ICONS.get(
        category,
        ("location-dot", "#757575")
    )


def icon_html(category, size=16):
    icon_name, color = get_icon(category)

    return (
        f'<span style="color:{color};font-size:{size}px">'
        f'<i class="fa-solid fa-{icon_name}"></i></span>'
    )


# ============================================================
# B. DU LIEU DIA DIEM MAC DINH
# Toa do tham khao - nen kiem tra lai tren Google Maps
# ============================================================

DEFAULT_PLACES = [
    {
        "id": "hg_city",
        "name": "Thành phố Hà Giang",
        "category": "Đô thị",
        "lat": 22.8233,
        "lon": 104.9836,
        "description": "Điểm xuất phát và kết thúc hành trình Hà Giang."
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
        "lat": 23.363761,
        "lon": 105.316222,
        "description": "Điểm tham quan cột cờ Lũng Cú."
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
        "name": "Bến thuyền Hẻm Tu Sản",
        "category": "Trải nghiệm",
        "lat": 23.261362,
        "lon": 105.381910,
        "description": "Điểm xuống thuyền tham quan sông Nho Quế và hẻm Tu Sản."
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
        "lat": 23.066542,
        "lon": 105.234503,
        "description": "Khu vực phố chợ Mậu Duệ."
    },
    {
        "id": "du_gia",
        "name": "Du Già",
        "category": "Làng bản",
        "lat": 22.930910,
        "lon": 105.224570,
        "description": "Khu vực du lịch cộng đồng Du Già."
    },
    {
        "id": "thac_du_gia",
        "name": "Thác Du Già",
        "category": "Thác nước",
        "lat": 22.925948,
        "lon": 105.198540,
        "description": "Thác nước Du Già."
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
# C. KHOI TAO LICH TRINH
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


# ============================================================
# D. DOC VA CAP NHAT DU LIEU JSON CU
# ============================================================

def normalize_image(image):
    """Chuyen anh cu/moi ve object {name, mime_type, data}."""
    if not image:
        return None
    if isinstance(image, str):
        return {"name": "image.jpg", "mime_type": "image/jpeg", "data": image}
    if isinstance(image, dict) and image.get("data"):
        return {
            "name": image.get("name", "image"),
            "mime_type": image.get("mime_type", "image/jpeg"),
            "data": image["data"]
        }
    return None


def normalize_stop(stop, places_by_id):
    """Tuong thich ca stop cu dang place_id va stop moi dang dict."""
    if isinstance(stop, str):
        place_id = stop
        stop_data = {}
    elif isinstance(stop, dict):
        place_id = stop.get("place_id") or stop.get("id")
        stop_data = stop
    else:
        return None

    if not place_id:
        return None

    place = places_by_id.get(place_id, {})
    raw_images = stop_data.get("images", [])
    if not isinstance(raw_images, list):
        raw_images = [raw_images]
    images = [img for img in (normalize_image(x) for x in raw_images) if img]

    # Di chuyen du lieu ghi chu/anh cu cap dia diem vao stop neu stop chua co.
    if not images and place.get("image"):
        old_image = normalize_image(place.get("image"))
        if old_image:
            images.append(old_image)
    note = stop_data.get("note")
    if note is None or note == "":
        note = place.get("note", "")

    return {
        "place_id": place_id,
        "arrival_time": stop_data.get("arrival_time", stop_data.get("time", "")) or "",
        "note": note or "",
        "images": images
    }


def normalize_data(data):
    if not isinstance(data, dict):
        raise ValueError("Dữ liệu JSON không phải một object hợp lệ.")
    if "places" not in data or not isinstance(data["places"], list):
        data["places"] = DEFAULT_PLACES
    if "plans" not in data or not isinstance(data["plans"], list) or not data["plans"]:
        data["plans"] = [default_plan()]

    places_by_id = {p.get("id"): p for p in data["places"] if p.get("id")}
    for plan in data["plans"]:
        plan.setdefault("id", new_id())
        plan.setdefault("name", "Phương án")
        plan.setdefault("days", [])
        for day in plan["days"]:
            day.setdefault("name", f"Ngày {plan['days'].index(day) + 1}")
            raw_stops = day.get("stops", [])
            day["stops"] = [
                normalized for normalized in
                (normalize_stop(x, places_by_id) for x in raw_stops)
                if normalized is not None
            ]

    selected = data.get("selected_plan_id")
    if selected not in [p["id"] for p in data["plans"]]:
        data["selected_plan_id"] = data["plans"][0]["id"]

    # Cap nhat thong tin diem ben thuyen cu, khong thay doi ID trong plan.
    for place in data["places"]:
        if place.get("id") == "nho_que":
            place.update({
                "name": "Bến thuyền Hẻm Tu Sản",
                "category": "Trải nghiệm",
                "lat": 23.261362,
                "lon": 105.381910,
                "description": "Điểm xuống thuyền tham quan sông Nho Quế và hẻm Tu Sản."
            })

    has_nho_que = any(p.get("id") == "nho_que" for p in data["places"])
    if has_nho_que:
        data["places"] = [p for p in data["places"] if p.get("id") != "ben_ta_lang"]
        for plan in data["plans"]:
            for day in plan.get("days", []):
                for stop in day.get("stops", []):
                    if stop["place_id"] == "ben_ta_lang":
                        stop["place_id"] = "nho_que"

    return data


def get_supabase_config():
    """Đọc thông tin kết nối từ Streamlit Community Cloud Secrets."""
    try:
        secrets = st.secrets
        supabase_url = str(secrets.get("SUPABASE_URL", "")).strip().rstrip("/")
        # Nên dùng service_role key trong Secrets vì ứng dụng cần quyền đọc/ghi.
        supabase_key = str(
            secrets.get("SUPABASE_SERVICE_ROLE_KEY", "")
            or secrets.get("SUPABASE_KEY", "")
        ).strip()
    except Exception:
        supabase_url, supabase_key = "", ""

    if not supabase_url or not supabase_key:
        st.error(
            "Chưa cấu hình Supabase. Trong Streamlit Community Cloud, mở "
            "App → Settings → Secrets và khai báo SUPABASE_URL cùng "
            "SUPABASE_SERVICE_ROLE_KEY. Xem hướng dẫn thiết lập đi kèm ứng dụng."
        )
        st.stop()

    return supabase_url, supabase_key


def supabase_request(method, params=None, payload=None):
    """Gọi Supabase REST API; lỗi kết nối không được âm thầm thay bằng dữ liệu rỗng."""
    supabase_url, supabase_key = get_supabase_config()
    url = f"{supabase_url}/rest/v1/{SUPABASE_TABLE}"
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json",
        # Bắt buộc để POST + on_conflict thực hiện UPSERT thay vì INSERT trùng khóa.
        "Prefer": "resolution=merge-duplicates,return=minimal",
    }
    try:
        response = requests.request(
            method,
            url,
            params=params,
            json=payload,
            headers=headers,
            timeout=45,
        )
        response.raise_for_status()
        return response
    except requests.RequestException as exc:
        detail = ""
        if getattr(exc, "response", None) is not None:
            detail = f" | Phản hồi: {exc.response.text[:1000]}"
        raise RuntimeError(
            "Không thể kết nối/lưu dữ liệu lên Supabase. "
            "Dữ liệu trên màn hình chưa được xác nhận đã lưu. "
            f"Chi tiết: {exc}{detail}"
        ) from exc


def data_fingerprint(data):
    raw = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def find_legacy_data_file():
    """Tìm bản JSON cũ để nạp lên Supabase trong lần chạy đầu tiên."""
    candidates = [DATA_FILE, "ha_giang_data_3n2d.json"]
    for filename in candidates:
        if os.path.isfile(filename):
            return filename
    return None


def load_data():
    """Đọc dữ liệu từ Supabase; nếu DB chưa có bản ghi thì migrate JSON cũ."""
    response = supabase_request(
        "GET",
        params={
            "id": f"eq.{SUPABASE_RECORD_ID}",
            "select": "data",
            "limit": "1",
        },
    )
    records = response.json() if response.content else []

    if records:
        if not isinstance(records[0].get("data"), dict):
            raise RuntimeError("Bản ghi dữ liệu trong Supabase không đúng cấu trúc JSON.")
        loaded = normalize_data(records[0]["data"])
        st.session_state.last_saved_fingerprint = data_fingerprint(loaded)
        return loaded

    # Chưa có dữ liệu trên DB: ưu tiên migrate file đang dùng, sau đó file dữ liệu
    # 3N2Đ/4N3Đ đi kèm. Không ghi đè dữ liệu DB nếu bản ghi đã tồn tại.
    legacy_file = find_legacy_data_file()
    if legacy_file:
        try:
            with open(legacy_file, "r", encoding="utf-8") as f:
                loaded = normalize_data(json.load(f))
        except Exception as exc:
            raise RuntimeError(
                f"Không thể đọc file dữ liệu cũ {legacy_file}: {exc}. "
                "Không khởi tạo dữ liệu trắng để tránh mất dữ liệu."
            ) from exc
    else:
        loaded = initial_data()

    save_data(loaded)
    return loaded


def save_data(data):
    """Lưu toàn bộ cấu trúc dữ liệu hiện tại vào một bản ghi JSONB trên Supabase."""
    payload = [{"id": SUPABASE_RECORD_ID, "data": data}]
    supabase_request(
        "POST",
        params={"on_conflict": "id"},
        payload=payload,
    )
    st.session_state.last_saved_fingerprint = data_fingerprint(data)


def save_if_changed(data):
    """Tự động lưu khi dữ liệu thay đổi, tránh ghi DB ở mọi lần rerun không cần thiết."""
    current_fingerprint = data_fingerprint(data)
    if current_fingerprint != st.session_state.get("last_saved_fingerprint"):
        save_data(data)


def persist_and_rerun():
    """Lưu trước khi rerun để không mất thay đổi từ các nút thao tác."""
    try:
        save_data(st.session_state.data)
    except Exception as exc:
        st.error(str(exc))
        st.stop()
    st.rerun()


# ============================================================
# E. CAC HAM DU LIEU
# ============================================================

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


def format_duration(minutes):
    hours = int(minutes // 60)
    mins = int(round(minutes % 60))

    if hours > 0:
        return f"{hours} giờ {mins} phút"

    return f"{mins} phút"


# ============================================================
# F. LAY TUYEN DUONG OSRM
# ============================================================

@st.cache_data(ttl=3600, show_spinner=False)
def get_osrm_route(lat1, lon1, lat2, lon2):
    url = (
        "https://router.project-osrm.org/route/v1/driving/"
        f"{lon1},{lat1};{lon2},{lat2}"
        "?overview=full&geometries=geojson"
    )

    try:
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "HaGiangTripPlanner/1.0"}
        )

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
    place_dict = {p["id"]: p for p in places}
    stops = []
    for raw_stop in day.get("stops", []):
        stop_data = raw_stop if isinstance(raw_stop, dict) else {"place_id": raw_stop}
        place_id = stop_data.get("place_id")
        if place_id in place_dict:
            # Ban sao rieng cho lan ghe tham, khong sua thu vien dia diem.
            merged = dict(place_dict[place_id])
            merged["_stop"] = stop_data
            stops.append(merged)

    total_distance = 0
    total_duration = 0
    route_segments = []
    all_estimated = False

    for i in range(len(stops) - 1):
        a, b = stops[i], stops[i + 1]
        route = get_osrm_route(a["lat"], a["lon"], b["lat"], b["lon"])
        if route:
            distance = route["distance_km"]
            duration = route["duration_min"]
            coordinates = route["coordinates"]
            estimated = False
        else:
            distance = haversine_km(a["lat"], a["lon"], b["lat"], b["lon"]) * 1.35
            duration = distance / 30 * 60
            coordinates = [[a["lat"], a["lon"]], [b["lat"], b["lon"]]]
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


def render_detailed_itinerary(plan, places):
    rows = []
    place_dict = {p["id"]: p for p in places}
    for day in plan.get("days", []):
        for index, stop in enumerate(day.get("stops", []), start=1):
            stop_data = stop if isinstance(stop, dict) else {"place_id": stop}
            place = place_dict.get(stop_data.get("place_id"))
            if not place:
                continue
            rows.append({
                "Ngày": day.get("name", ""),
                "Thứ tự": index,
                "Thời gian đến": stop_data.get("arrival_time", ""),
                "Địa điểm": place.get("name", ""),
                "Ghi chú": stop_data.get("note", "")
            })
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("Chưa có điểm đến trong lịch trình.")



# ============================================================
# G. TAO BAN DO
# Chi su dung mot nen Esri World Street Map
# ============================================================

def create_map(plan, places):

    m = folium.Map(
        location=[23.15, 105.25],
        zoom_start=9,
        tiles=None,
        control_scale=True
    )

    folium.TileLayer(
        tiles=(
            "https://server.arcgisonline.com/ArcGIS/rest/services/"
            "World_Street_Map/MapServer/tile/{z}/{y}/{x}"
        ),
        attr="Tiles © Esri",
        name="Esri World Street Map",
        max_zoom=19,
        show=True
    ).add_to(m)

    # Font Awesome
    fontawesome = """
    <link rel="stylesheet"
    href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    """

    m.get_root().header.add_child(
        folium.Element(fontawesome)
    )

    all_coords = []

    place_dict = {
        p["id"]: p for p in places
    }

    # Tinh tuyen tung ngay mot lan. Marker se duoc uu tien theo thu tu ngay:
    # neu mot dia diem xuat hien o cuoi ngay truoc va dau ngay sau, thong tin
    # marker cua lan xuat hien dau tien (ngay truoc) se duoc giu lai.
    day_route_data = []
    for day_index, day in enumerate(plan["days"]):
        route_data = calculate_day_routes(day, places)
        day_route_data.append((day_index, day, route_data))

    # Ve tuyen theo thu tu nguoc de tuyen cua ngay som hon nam tren cung
    # khi hai ngay co doan duong trung nhau. Mau tuyen moi ngay van doc lap.
    for day_index, day, route_data in reversed(day_route_data):
        color = DAY_COLORS[day_index % len(DAY_COLORS)]

        for segment in route_data["segments"]:
            folium.PolyLine(
                locations=segment["coordinates"],
                color=color,
                weight=5,
                opacity=0.88,
                dash_array=("8, 8" if segment["estimated"] else None),
                tooltip=(
                    f"{day['name']} | {segment['distance_km']:.1f} km"
                    + (" | Ước tính" if segment["estimated"] else "")
                )
            ).add_to(m)

    # Marker duoc ve theo thu tu ngay tang dan. Moi dia diem chi co mot
    # marker; lan xuat hien dau tien duoc uu tien cho popup, thoi gian, ghi chu,
    # anh va nhan Ngay/Điểm. Cac lan lap lai van giu nguyen tren tuyen duong.
    marker_place_ids = set()
    for day_index, day, route_data in day_route_data:
        color = DAY_COLORS[day_index % len(DAY_COLORS)]

        for stop_index, place in enumerate(route_data["stops"]):
            lat = place["lat"]
            lon = place["lon"]
            all_coords.append([lat, lon])

            place_id = place.get("id")
            if place_id in marker_place_ids:
                continue
            marker_place_ids.add(place_id)

            icon_name, icon_color = get_icon(place.get("category", "Khác"))

            marker_html = f"""
            <div style="
                width:38px;
                height:38px;
                background:{icon_color};
                border:3px solid white;
                border-radius:50%;
                box-shadow:0 2px 6px rgba(0,0,0,0.4);
                display:flex;
                align-items:center;
                justify-content:center;
                color:white;
                font-size:17px;
            ">
                <i class="fa-solid fa-{icon_name}"></i>
            </div>
            """

            popup_html = f"""
            <div style="
                width:240px;
                font-family:Arial,sans-serif;
                font-size:13px;
            ">
                <h4 style="margin:0 0 7px 0">
                    {html.escape(place['name'])}
                </h4>

                <div style="color:{icon_color};font-weight:bold">
                    <i class="fa-solid fa-{icon_name}"></i>
                    {html.escape(place.get('category', ''))}
                </div>

                <p style="margin-top:8px">
                    {html.escape(place.get('description', ''))}
                </p>

                <div style="
                    color:{color};
                    font-weight:bold;
                    margin-top:8px;
                ">
                    {html.escape(day['name'])}
                    - Điểm {stop_index + 1}
                </div>
            """

            stop_data = place.get("_stop", {})
            arrival_time = stop_data.get("arrival_time", "")
            if arrival_time:
                popup_html += (
                    '<div style="margin-top:8px;font-weight:bold">'
                    '🕒 Đến: ' + html.escape(arrival_time) + '</div>'
                )
            if stop_data.get("note"):
                popup_html += (
                    '<p style="margin-top:8px">'
                    + html.escape(stop_data["note"])
                    + '</p>'
                )
            for image_data in stop_data.get("images", [])[:8]:
                normalized_image = normalize_image(image_data)
                if normalized_image:
                    popup_html += (
                        '<img src="data:' + html.escape(normalized_image["mime_type"]) + ';base64,'
                        + normalized_image["data"]
                        + '" style="width:100%;margin-top:8px;border-radius:6px">'
                    )

            popup_html += "</div>"

            marker = folium.Marker(
                location=[lat, lon],
                tooltip=folium.Tooltip(
                    html.escape(place["name"]),
                    permanent=True,
                    direction="top",
                    sticky=False
                ),
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.DivIcon(
                    html=marker_html,
                    icon_size=(38, 38),
                    icon_anchor=(19, 19)
                )
            )
            marker.add_to(m)

    # Tu dong zoom de hien thi cac diem trong lich trinh
    if all_coords:
        m.fit_bounds(all_coords)
    else:
        m.location = [23.15, 105.25]
        m.zoom_start = 9

    # Chu thich mau tuyen tung ngay
    legend_html = """
    <div style="
        position:fixed;
        bottom:25px;
        left:25px;
        z-index:9999;
        background:white;
        padding:11px 14px;
        border-radius:8px;
        box-shadow:0 1px 7px rgba(0,0,0,0.25);
        font-size:12px;
        max-height:220px;
        overflow:auto;
    ">
        <b>CHÚ THÍCH TUYẾN ĐƯỜNG</b><br>
    """

    for i, day in enumerate(plan["days"]):
        color = DAY_COLORS[i % len(DAY_COLORS)]

        legend_html += (
            f'<div style="margin-top:6px">'
            f'<span style="display:inline-block;width:23px;'
            f'border-top:4px solid {color};margin-right:7px;'
            f'vertical-align:middle"></span>'
            f'{html.escape(day["name"])}'
            f'</div>'
        )

    legend_html += """
        <div style="margin-top:8px;color:#666">
            Nét đứt: tuyến ước tính
        </div>
    </div>
    """

    m.get_root().html.add_child(
        folium.Element(legend_html)
    )

    return m


# ============================================================
# H. BANG TONG HOP LICH TRINH
# ============================================================

def render_summary(plan, places):

    rows = []

    for day in plan["days"]:

        result = calculate_day_routes(
            day,
            places
        )

        names = [
            p["name"]
            for p in result["stops"]
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

    if not rows:
        st.info("Chưa có dữ liệu lịch trình.")
        return

    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    total_km = sum(
        row["Quãng đường (km)"]
        for row in rows
    )

    total_minutes = sum(
        calculate_day_routes(day, places)["duration_min"]
        for day in plan["days"]
    )

    c1, c2 = st.columns(2)

    c1.metric(
        "Tổng quãng đường",
        f"{total_km:.1f} km"
    )

    c2.metric(
        "Tổng thời gian di chuyển",
        format_duration(total_minutes)
    )


# ============================================================
# I. CHIA SE VIEW
# ============================================================

def render_share_view(data):

    st.title("🏔️ Lịch trình khám phá Hà Giang")

    # Cho phep nguoi xem tu chon phuong an, doc lap voi selected_plan_id
    # cua nguoi quan ly/chinh sua lich trinh.
    plans = data.get("plans", [])

    if not plans:
        st.warning("Chưa có phương án lịch trình để chia sẻ.")
        return

    plan_options = {p["id"]: p for p in plans}
    default_plan_id = data.get("selected_plan_id")
    if default_plan_id not in plan_options:
        default_plan_id = plans[0]["id"]

    selected_share_plan_id = st.selectbox(
        "Chọn phương án lịch trình",
        options=list(plan_options.keys()),
        index=list(plan_options.keys()).index(default_plan_id),
        format_func=lambda plan_id: plan_options[plan_id].get("name", "Phương án"),
        key="share_selected_plan_id"
    )

    plan = plan_options[selected_share_plan_id]
    places = data.get("places", [])

    st.caption(
        f"Phương án: {plan['name']} | "
        f"{len(plan['days'])} ngày"
    )

    map_object = create_map(
        plan,
        places
    )

    st_folium(
        map_object,
        width=None,
        height=680,
        returned_objects=[]
    )

    st.subheader("Tổng hợp lịch trình")

    render_summary(
        plan,
        places
    )

    st.subheader("Lịch trình chi tiết từng điểm")
    render_detailed_itinerary(plan, places)

    st.caption(
        "Khoảng cách và thời gian là ước tính theo tuyến đường "
        "ô tô. Thực tế có thể thay đổi theo điều kiện giao thông."
    )


# ============================================================
# J. KHOI TAO SESSION
# ============================================================

if "data" not in st.session_state:
    st.session_state.data_load_failed = False
    try:
        st.session_state.data = normalize_data(load_data())
    except Exception as exc:
        st.error(str(exc))
        st.info(
            "Ứng dụng đã dừng để bảo vệ dữ liệu. Hãy kiểm tra cấu hình Secrets, "
            "bảng Supabase và file JSON dữ liệu cũ trước khi tải lại trang."
        )
        st.stop()

data = st.session_state.data
places = data["places"]
plan = get_current_plan()

try:
    share_mode = st.query_params.get("view") == "share"
except Exception:
    share_mode = False

if share_mode:
    render_share_view(data)
    st.stop()


# ============================================================
# K. GIAO DIEN CHINH
# ============================================================

st.title("🏔️ Hà Giang Trip Planner")

st.caption(
    "Công cụ lập lịch trình, quản lý địa điểm "
    "và theo dõi tuyến đường khám phá Hà Giang."
)


# ============================================================
# L. QUAN LY PHUONG AN
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

if st.sidebar.button(
    "➕ Tạo phương án mới",
    use_container_width=True
):

    new_plan = {
        "id": new_id(),
        "name": (
            new_plan_name.strip()
            or "Phương án mới"
        ),
        "days": [
            {"name": "Ngày 1", "stops": []},
            {"name": "Ngày 2", "stops": []},
            {"name": "Ngày 3", "stops": []}
        ]
    }

    data["plans"].append(new_plan)
    data["selected_plan_id"] = new_plan["id"]

    persist_and_rerun()


if st.sidebar.button(
    "📑 Nhân bản phương án hiện tại",
    use_container_width=True
):

    copied = json.loads(
        json.dumps(plan)
    )

    copied["id"] = new_id()
    copied["name"] = plan["name"] + " - Bản sao"

    data["plans"].append(copied)
    data["selected_plan_id"] = copied["id"]

    persist_and_rerun()


edited_plan_name = st.sidebar.text_input(
    "Đổi tên phương án hiện tại",
    value=plan["name"]
)

if st.sidebar.button(
    "Cập nhật tên phương án",
    use_container_width=True
):

    plan["name"] = (
        edited_plan_name.strip()
        or plan["name"]
    )

    persist_and_rerun()


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

        persist_and_rerun()


# ============================================================
# M. LUU / NHAP / XUAT JSON
# ============================================================

st.sidebar.divider()
st.sidebar.header("💾 Dữ liệu")

if st.sidebar.button(
    "💾 Lưu dữ liệu",
    use_container_width=True,
    disabled=st.session_state.get("data_load_failed", False)
):

    try:
        save_data(data)
        st.sidebar.success("Đã lưu dữ liệu lên Supabase.")
    except Exception as exc:
        st.sidebar.error(str(exc))


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

    if st.sidebar.button(
        "Nhập dữ liệu JSON",
        use_container_width=True
    ):

        try:
            imported = json.load(uploaded_json)

            if (
                "places" in imported
                and "plans" in imported
                and imported["plans"]
            ):

                st.session_state.data = normalize_data(imported)
                st.session_state.data_load_failed = False

                try:
                    save_data(st.session_state.data)
                    st.success(
                        "Đã nhập dữ liệu thành công, chuẩn hóa và lưu lên Supabase."
                    )
                    st.rerun()
                except Exception as exc:
                    st.error(str(exc))

            else:
                st.sidebar.error(
                    "File JSON không đúng cấu trúc."
                )

        except Exception as e:
            st.sidebar.error(
                f"Lỗi đọc JSON: {e}"
            )


# ============================================================
# N. CAC TAB
# ============================================================

tab_map, tab_itinerary, tab_places, tab_export = st.tabs([
    "🗺️ Bản đồ",
    "📝 Lịch trình",
    "📍 Thư viện địa điểm",
    "📤 Chia sẻ & Xuất dữ liệu"
])


# ============================================================
# TAB 1 - BAN DO
# ============================================================

with tab_map:

    st.subheader("Bản đồ hành trình")

    st.caption(
        "Nền bản đồ Esri World Street Map. "
        "Mỗi ngày có một màu tuyến đường riêng."
    )

    map_object = create_map(
        plan,
        places
    )

    st_folium(
        map_object,
        width=None,
        height=680,
        returned_objects=[]
    )

    st.subheader("Tổng hợp quãng đường")

    render_summary(
        plan,
        places
    )

    st.divider()
    st.subheader("📋 Lịch trình chi tiết từng điểm")
    render_detailed_itinerary(plan, places)


# ============================================================
# TAB 2 - CHINH SUA LICH TRINH
# ============================================================

with tab_itinerary:

    st.subheader("Chỉnh sửa lịch trình")

    col_add_day, col_del_day = st.columns(2)

    with col_add_day:

        if st.button("➕ Thêm ngày"):
            plan["days"].append({
                "name": f"Ngày {len(plan['days']) + 1}",
                "stops": []
            })

            persist_and_rerun()

    with col_del_day:

        if len(plan["days"]) > 1:

            if st.button("➖ Xóa ngày cuối"):
                plan["days"].pop()
                persist_and_rerun()


    for day_index, day in enumerate(plan["days"]):
        color = DAY_COLORS[day_index % len(DAY_COLORS)]
        with st.expander(f"{day['name']} - {len(day['stops'])} điểm", expanded=True):
            day["name"] = st.text_input(
                "Tên ngày", value=day["name"],
                key=f"day_name_{plan['id']}_{day_index}"
            )
            st.markdown(
                f'<span style="color:{color};font-weight:bold">● Màu tuyến đường của '
                f'{html.escape(day["name"])}</span>',
                unsafe_allow_html=True
            )

            existing_ids = [
                x.get("place_id") if isinstance(x, dict) else x
                for x in day["stops"]
            ]
            available_places = [p for p in places if p["id"] not in existing_ids]
            if available_places:
                place_options = {p["id"]: f"{p['name']} ({p['category']})" for p in available_places}
                selected_place = st.selectbox(
                    "Chọn địa điểm để thêm", list(place_options.keys()),
                    format_func=lambda x: place_options[x],
                    key=f"add_place_{plan['id']}_{day_index}"
                )
                if st.button("➕ Thêm địa điểm vào ngày", key=f"add_stop_{plan['id']}_{day_index}"):
                    day["stops"].append({
                        "place_id": selected_place,
                        "arrival_time": "",
                        "note": "",
                        "images": []
                    })
                    persist_and_rerun()
            else:
                st.info("Không còn địa điểm mới trong thư viện cho ngày này.")

            st.divider()
            if not day["stops"]:
                st.info("Ngày này chưa có địa điểm.")

            for stop_index, stop in enumerate(day["stops"]):
                if isinstance(stop, str):
                    stop = normalize_stop(stop, {p["id"]: p for p in places})
                    day["stops"][stop_index] = stop
                place = get_place(stop.get("place_id")) if stop else None
                if not place:
                    continue

                with st.container(border=True):
                    col_name, col_up, col_down, col_move, col_remove = st.columns([5, 0.55, 0.55, 1.3, 0.65])
                    with col_name:
                        st.markdown(
                            f'{stop_index + 1}. {icon_html(place.get("category", "Khác"), 17)} '
                            f'**{html.escape(place["name"])}**',
                            unsafe_allow_html=True
                        )
                    with col_up:
                        if st.button("⬆️", key=f"up_{plan['id']}_{day_index}_{stop_index}", disabled=stop_index == 0):
                            day["stops"][stop_index - 1], day["stops"][stop_index] = day["stops"][stop_index], day["stops"][stop_index - 1]
                            persist_and_rerun()
                    with col_down:
                        if st.button("⬇️", key=f"down_{plan['id']}_{day_index}_{stop_index}", disabled=stop_index == len(day["stops"]) - 1):
                            day["stops"][stop_index + 1], day["stops"][stop_index] = day["stops"][stop_index], day["stops"][stop_index + 1]
                            persist_and_rerun()
                    with col_move:
                        other_days = [i for i in range(len(plan["days"])) if i != day_index]
                        if other_days:
                            target_day = st.selectbox(
                                "Chuyển đến", other_days,
                                format_func=lambda x: plan["days"][x]["name"],
                                key=f"move_target_{plan['id']}_{day_index}_{stop_index}"
                            )
                            if st.button("Chuyển", key=f"move_{plan['id']}_{day_index}_{stop_index}"):
                                moved_stop = day["stops"].pop(stop_index)
                                plan["days"][target_day]["stops"].append(moved_stop)
                                persist_and_rerun()
                    with col_remove:
                        if st.button("❌", key=f"remove_{plan['id']}_{day_index}_{stop_index}"):
                            day["stops"].pop(stop_index)
                            persist_and_rerun()

                    st_data = stop
                    time_col, note_col = st.columns([1, 3])
                    with time_col:
                        st_data["arrival_time"] = st.text_input(
                            "Thời gian đến (HH:MM)",
                            value=st_data.get("arrival_time", ""),
                            placeholder="Ví dụ: 09:30",
                            key=f"arrival_{plan['id']}_{day_index}_{stop_index}"
                        )
                    with note_col:
                        st_data["note"] = st.text_area(
                            "Ghi chú cho điểm này",
                            value=st_data.get("note", ""),
                            height=85,
                            key=f"stop_note_{plan['id']}_{day_index}_{stop_index}"
                        )

                    st.markdown("**Ảnh đính kèm**")
                    current_images = st_data.setdefault("images", [])
                    if current_images:
                        image_cols = st.columns(min(4, len(current_images)))
                        for image_index, image_data in enumerate(current_images):
                            normalized = normalize_image(image_data)
                            if not normalized:
                                continue
                            with image_cols[image_index % len(image_cols)]:
                                try:
                                    st.image(base64.b64decode(normalized["data"]), caption=normalized["name"], use_container_width=True)
                                except Exception:
                                    st.warning(f"Không đọc được ảnh: {normalized['name']}")
                                if st.button("Xóa ảnh", key=f"delete_img_{plan['id']}_{day_index}_{stop_index}_{image_index}"):
                                    current_images.pop(image_index)
                                    persist_and_rerun()
                    uploaded_images = st.file_uploader(
                        "Tải thêm một hoặc nhiều ảnh (không làm mất ảnh cũ)",
                        type=["png", "jpg", "jpeg", "webp"],
                        accept_multiple_files=True,
                        key=f"stop_images_{plan['id']}_{day_index}_{stop_index}"
                    )
                    if st.button("💾 Lưu thông tin điểm này", key=f"save_stop_{plan['id']}_{day_index}_{stop_index}"):
                        if st_data.get("arrival_time"):
                            import re
                            if not re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", st_data["arrival_time"].strip()):
                                st.error("Thời gian phải đúng định dạng HH:MM, ví dụ 09:30.")
                                st.stop()
                            st_data["arrival_time"] = st_data["arrival_time"].strip()
                        for uploaded in uploaded_images or []:
                            raw = uploaded.getvalue()
                            st_data["images"].append({
                                "name": uploaded.name,
                                "mime_type": uploaded.type or "image/jpeg",
                                "data": base64.b64encode(raw).decode("utf-8")
                            })
                        st.success("Đã cập nhật thông tin điểm đến.")
                        persist_and_rerun()


# ============================================================
# TAB 3 - THU VIEN DIA DIEM
# ============================================================

with tab_places:

    st.subheader("Thư viện địa điểm Hà Giang")

    st.caption(
        "Địa điểm trong thư viện có thể được sử dụng "
        "ở nhiều phương án lịch trình khác nhau."
    )

    # Them dia diem
    with st.expander(
        "➕ Thêm địa điểm mới",
        expanded=False
    ):

        with st.form("add_place_form"):

            new_name = st.text_input(
                "Tên địa điểm"
            )

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

            new_description = st.text_area(
                "Mô tả"
            )

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

                    st.success(
                        "Đã thêm địa điểm."
                    )

                    persist_and_rerun()

                else:
                    st.error(
                        "Vui lòng nhập tên địa điểm."
                    )


    # Sua dia diem
    with st.expander(
        "✏️ Chỉnh sửa địa điểm",
        expanded=False
    ):

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

                    st.success(
                        "Đã cập nhật địa điểm."
                    )

                    persist_and_rerun()


    # Xoa dia diem
    with st.expander(
        "🗑️ Xóa địa điểm",
        expanded=False
    ):

        if places:

            delete_id = st.selectbox(
                "Chọn địa điểm cần xóa",
                [p["id"] for p in places],
                format_func=lambda x: get_place(x)["name"],
                key="delete_place_id"
            )

            if st.button(
                "Xóa địa điểm khỏi thư viện"
            ):

                data["places"] = [
                    p for p in data["places"]
                    if p["id"] != delete_id
                ]

                for p in data["plans"]:

                    for d in p["days"]:

                        d["stops"] = [
                            x for x in d["stops"]
                            if (x.get("place_id") if isinstance(x, dict) else x) != delete_id
                        ]

                persist_and_rerun()


    # Danh sach dia diem
    st.divider()

    place_rows = []

    for p in data["places"]:

        place_rows.append({
            "Địa điểm": p["name"],
            "Phân loại": p["category"],
            "Latitude": p["lat"],
            "Longitude": p["lon"]
        })

    st.dataframe(
        pd.DataFrame(place_rows),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TAB 4 - CHIA SE VA XUAT DU LIEU
# ============================================================

with tab_export:

    st.subheader("Chia sẻ lịch trình")

    st.markdown(
        "Để mở chế độ chia sẻ, thêm **?view=share** "
        "vào cuối URL ứng dụng."
    )

    try:

        current_url = st.context.url.split("?")[0]
        share_url = current_url + "?view=share"

        st.code(
            share_url,
            language=None
        )

    except Exception:

        st.info(
            "Sau khi deploy trên Streamlit Cloud, "
            "thêm ?view=share vào cuối URL ứng dụng."
        )


    st.divider()

    st.subheader("Xuất Excel")

    excel_rows = []

    for day in plan["days"]:

        route_data = calculate_day_routes(
            day,
            places
        )

        for stop_index, place in enumerate(
            route_data["stops"]
        ):

            stop_data = place.get("_stop", {})
            excel_rows.append({
                "Ngày": day["name"],
                "Thứ tự": stop_index + 1,
                "Thời gian đến": stop_data.get("arrival_time", ""),
                "Địa điểm": place["name"],
                "Phân loại": place["category"],
                "Latitude": place["lat"],
                "Longitude": place["lon"],
                "Mô tả": place.get("description", ""),
                "Ghi chú": stop_data.get("note", ""),
                "Số ảnh": len(stop_data.get("images", []))
            })

    excel_df = pd.DataFrame(excel_rows)

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

        pd.DataFrame(
            data["places"]
        ).drop(
            columns=["image"],
            errors="ignore"
        ).to_excel(
            writer,
            index=False,
            sheet_name="Thu vien dia diem"
        )

    st.download_button(
        "⬇️ Tải lịch trình Excel",
        data=excel_buffer.getvalue(),
        file_name="lich_trinh_ha_giang.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
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
# O. CUOI TRANG
# ============================================================

st.divider()

st.caption(
    "Ha Giang Trip Planner | "
    "Map tiles © Esri | "
    "Routing by OSRM / OpenStreetMap. "
    "Khoảng cách và thời gian chỉ mang tính tham khảo."
)

# Tự động đồng bộ mọi thay đổi phát sinh từ widget (tên ngày, thời gian, ghi chú,...)
# sau khi render xong. Các thao tác có st.rerun() đã lưu trước khi rerun.
try:
    save_if_changed(data)
except Exception as exc:
    st.error(str(exc))
