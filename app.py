
import streamlit as st
import pandas as pd
import folium
import requests
import json
import copy
import uuid
import base64
import math
import io
from pathlib import Path
from streamlit_folium import st_folium

# ============================================================
# PHẦN A. DANH SÁCH ĐỊA ĐIỂM
# Bạn có thể thêm / sửa / xóa địa điểm tại đây
# ============================================================

PLACES = [
    {
        "id": "HG001",
        "name": "Lô Lô Chải",
        "category": "Làng bản",
        "lat": 23.3575,
        "lon": 105.3040,
        "description": "Làng văn hóa người Lô Lô dưới chân cột cờ Lũng Cú.",
        "image": ""
    },
    {
        "id": "HG002",
        "name": "Cột cờ Lũng Cú",
        "category": "Check-in",
        "lat": 23.3619,
        "lon": 105.3150,
        "description": "Điểm tham quan nổi tiếng tại cực Bắc Việt Nam.",
        "image": ""
    },
    {
        "id": "HG003",
        "name": "Phố cổ Đồng Văn",
        "category": "Tham quan",
        "lat": 23.2770,
        "lon": 105.3600,
        "description": "Khu phố cổ với kiến trúc và không gian văn hóa vùng cao.",
        "image": ""
    },
    {
        "id": "HG004",
        "name": "Đèo Mã Pí Lèng",
        "category": "Check-in",
        "lat": 23.2060,
        "lon": 105.4050,
        "description": "Cung đèo nổi tiếng trên cao nguyên đá.",
        "image": ""
    },
    {
        "id": "HG005",
        "name": "Sông Nho Quế",
        "category": "Trải nghiệm",
        "lat": 23.1900,
        "lon": 105.4100,
        "description": "Trải nghiệm đi thuyền trên sông Nho Quế.",
        "image": ""
    },
    {
        "id": "HG006",
        "name": "Hẻm Tu Sản",
        "category": "Check-in",
        "lat": 23.1850,
        "lon": 105.4050,
        "description": "Hẻm vực nổi tiếng trên dòng Nho Quế.",
        "image": ""
    },
    {
        "id": "HG007",
        "name": "Nhà của Pao",
        "category": "Văn hóa",
        "lat": 23.2560,
        "lon": 105.2880,
        "description": "Ngôi nhà truyền thống tại thung lũng Sủng Là.",
        "image": ""
    },
    {
        "id": "HG008",
        "name": "Dinh thự họ Vương",
        "category": "Văn hóa",
        "lat": 23.2570,
        "lon": 105.2820,
        "description": "Công trình kiến trúc lịch sử nổi tiếng.",
        "image": ""
    },
    {
        "id": "HG009",
        "name": "Rừng thông Yên Minh",
        "category": "Thiên nhiên",
        "lat": 23.1000,
        "lon": 105.1500,
        "description": "Khu vực rừng thông và cảnh quan núi rừng.",
        "image": ""
    },
    {
        "id": "HG010",
        "name": "Núi Đôi Quản Bạ",
        "category": "Thiên nhiên",
        "lat": 23.0670,
        "lon": 104.9910,
        "description": "Điểm ngắm cảnh nổi tiếng tại Quản Bạ.",
        "image": ""
    },
    {
        "id": "HG011",
        "name": "Cổng trời Quản Bạ",
        "category": "Check-in",
        "lat": 23.0640,
        "lon": 104.9800,
        "description": "Điểm ngắm toàn cảnh thung lũng Tam Sơn.",
        "image": ""
    },
    {
        "id": "HG012",
        "name": "Hoàng Su Phì",
        "category": "Thiên nhiên",
        "lat": 22.7500,
        "lon": 104.6800,
        "description": "Khu vực ruộng bậc thang nổi tiếng.",
        "image": ""
    },
    {
        "id": "HG013",
        "name": "Chiêu Lầu Thi",
        "category": "Leo núi",
        "lat": 22.7200,
        "lon": 104.7200,
        "description": "Điểm trekking và săn mây.",
        "image": ""
    },
    {
        "id": "HG014",
        "name": "Thác Tiên",
        "category": "Thác nước",
        "lat": 22.6500,
        "lon": 104.7000,
        "description": "Điểm tham quan thiên nhiên tại Hoàng Su Phì.",
        "image": ""
    },
    {
        "id": "HG015",
        "name": "Thành phố Hà Giang",
        "category": "Đô thị",
        "lat": 22.8230,
        "lon": 104.9830,
        "description": "Điểm xuất phát phổ biến của hành trình.",
        "image": ""
    },
    {
        "id": "HG016",
        "name": "Làng H'Mông Pả Vi",
        "category": "Làng bản",
        "lat": 23.2130,
        "lon": 105.4160,
        "description": "Làng văn hóa người Mông, nổi bật với nhà trình tường và homestay.",
        "image": ""
    },
    {
        "id": "HG017",
        "name": "Mèo Vạc",
        "category": "Đô thị",
        "lat": 23.2180,
        "lon": 105.4130,
        "description": "Trung tâm khu vực Mèo Vạc.",
        "image": ""
    },
    {
        "id": "HG018",
        "name": "Mèo Vạc Panorama Cafe",
        "category": "Ăn uống",
        "lat": 23.2150,
        "lon": 105.4070,
        "description": "Điểm cà phê ngắm cảnh khu vực Mèo Vạc. Cần xác minh tọa độ.",
        "image": ""
    },
    {
        "id": "HG019",
        "name": "Yên Minh",
        "category": "Đô thị",
        "lat": 23.1320,
        "lon": 105.1500,
        "description": "Thị trấn Yên Minh, điểm nghỉ chân trên cung đường.",
        "image": ""
    },
    {
        "id": "HG020",
        "name": "Du Già",
        "category": "Làng bản",
        "lat": 22.7300,
        "lon": 105.2000,
        "description": "Khu vực Du Già với cảnh quan núi rừng và homestay.",
        "image": ""
    },
    {
        "id": "HG021",
        "name": "Thác Du Già",
        "category": "Thác nước",
        "lat": 22.7250,
        "lon": 105.2050,
        "description": "Thác nước tại khu vực Du Già.",
        "image": ""
    },
    {
        "id": "HG022",
        "name": "Mậu Duệ",
        "category": "Đô thị",
        "lat": 22.9800,
        "lon": 105.2000,
        "description": "Khu vực trên cung đường nối Mèo Vạc, Yên Minh và Du Già.",
        "image": ""
    },
    {
        "id": "HG023",
        "name": "Thuận Hòa",
        "category": "Cung đường",
        "lat": 22.8500,
        "lon": 104.9500,
        "description": "Điểm thuộc khu vực tuyến đường Thuận Hòa - Thái An.",
        "image": ""
    },
    {
        "id": "HG024",
        "name": "Thái An",
        "category": "Cung đường",
        "lat": 23.0200,
        "lon": 105.0000,
        "description": "Điểm thuộc khu vực tuyến đường Thuận Hòa - Thái An.",
        "image": ""
    }
]

# ============================================================
# PHẦN B. CẤU HÌNH
# ============================================================

st.set_page_config(
    page_title="Ha Giang Trip Planner",
    page_icon="🏔️",
    layout="wide"
)

DATA_FILE = Path("ha_giang_data.json")

DAY_COLORS = [
    "#E53935", "#1976D2", "#2E7D32",
    "#8E24AA", "#EF6C00", "#00838F",
    "#AD1457", "#5D4037", "#455A64"
]

CATEGORY_ICONS = {
    "Check-in": ("camera", "red"),
    "Ăn uống": ("utensils", "orange"),
    "Lưu trú": ("bed", "blue"),
    "Làng bản": ("house", "green"),
    "Tham quan": ("landmark", "purple"),
    "Trải nghiệm": ("person-hiking", "cadetblue"),
    "Thác nước": ("water", "blue"),
    "Thiên nhiên": ("tree", "green"),
    "Văn hóa": ("building-columns", "darkpurple"),
    "Leo núi": ("mountain", "darkgreen"),
    "Đô thị": ("city", "gray"),
    "Cung đường": ("road", "darkred"),
    "Khác": ("map-pin", "gray")
}

def uid():
    return str(uuid.uuid4())[:8]

def default_data():
    return {
        "places": copy.deepcopy(PLACES),
        "plans": [{
            "id": uid(),
            "name": "Phương án 1",
            "days": [
                {"name": "Ngày 1", "stops": []},
                {"name": "Ngày 2", "stops": []},
                {"name": "Ngày 3", "stops": []}
            ]
        }],
        "active_plan": 0
    }

def load_data():
    if DATA_FILE.exists():
        try:
            obj = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            if isinstance(obj, dict) and isinstance(obj.get("places"), list) and isinstance(obj.get("plans"), list):
                # Bổ sung các địa điểm mới trong code nếu chưa có trong file JSON
                existing_ids = {p.get("id") for p in obj["places"]}
                for p in PLACES:
                    if p["id"] not in existing_ids:
                        obj["places"].append(copy.deepcopy(p))
                if not obj["plans"]:
                    obj["plans"] = default_data()["plans"]
                return obj
        except Exception:
            pass
    return default_data()

if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data

if not data.get("plans"):
    data["plans"] = default_data()["plans"]

data["active_plan"] = min(
    max(0, int(data.get("active_plan", 0))),
    len(data["plans"]) - 1
)

plan = data["plans"][data["active_plan"]]

def save_data():
    DATA_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def get_place(place_id):
    return next(
        (p for p in data["places"] if p.get("id") == place_id),
        None
    )

def category_icon(category):
    return CATEGORY_ICONS.get(
        category,
        CATEGORY_ICONS["Khác"]
    )

# ============================================================
# PHẦN C. TÍNH TUYẾN ĐƯỜNG
# ============================================================

@st.cache_data(ttl=3600, show_spinner=False)
def get_osrm_route(lon1, lat1, lon2, lat2):
    try:
        url = (
            "https://router.project-osrm.org/route/v1/driving/"
            f"{lon1},{lat1};{lon2},{lat2}"
            "?overview=full&geometries=geojson"
        )
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        result = r.json()

        if result.get("routes"):
            route = result["routes"][0]
            coords = route["geometry"]["coordinates"]
            return {
                "distance": route["distance"] / 1000,
                "duration": route["duration"] / 60,
                "coordinates": [[lat, lon] for lon, lat in coords]
            }
    except Exception:
        return None

    return None

def haversine_km(a, b):
    radius = 6371
    lat1, lon1 = math.radians(a["lat"]), math.radians(a["lon"])
    lat2, lon2 = math.radians(b["lat"]), math.radians(b["lon"])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    h = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    return 2 * radius * math.asin(math.sqrt(h))

def calculate_day(day):
    places = [
        get_place(s["place_id"])
        for s in day["stops"]
    ]
    places = [p for p in places if p]

    total_km = 0
    total_minutes = 0
    route_segments = []
    route_complete = True

    for i in range(len(places) - 1):
        a, b = places[i], places[i + 1]
        route = get_osrm_route(
            a["lon"], a["lat"], b["lon"], b["lat"]
        )

        if route:
            total_km += route["distance"]
            total_minutes += route["duration"]
            route_segments.append({
                "from": a["name"],
                "to": b["name"],
                "route": route,
                "estimated": False
            })
        else:
            route_complete = False
            estimate = haversine_km(a, b)
            route_segments.append({
                "from": a["name"],
                "to": b["name"],
                "route": {
                    "distance": estimate,
                    "duration": 0,
                    "coordinates": [
                        [a["lat"], a["lon"]],
                        [b["lat"], b["lon"]]
                    ]
                },
                "estimated": True
            })

    return {
        "places": places,
        "distance": total_km,
        "driving_minutes": total_minutes,
        "segments": route_segments,
        "route_complete": route_complete
    }

# ============================================================
# PHẦN D. BẢN ĐỒ
# ============================================================

def create_map(plan, map_mode="Đường phố", show_all_places=False):
    all_plan_places = []

    for day in plan["days"]:
        for stop in day["stops"]:
            p = get_place(stop["place_id"])
            if p:
                all_plan_places.append(p)

    if all_plan_places:
        center = [
            sum(p["lat"] for p in all_plan_places) / len(all_plan_places),
            sum(p["lon"] for p in all_plan_places) / len(all_plan_places)
        ]
    else:
        center = [23.0, 105.2]

    m = folium.Map(
        location=center,
        zoom_start=9,
        control_scale=True,
        tiles=None
    )

    # Lớp bản đồ đường phố
    folium.TileLayer(
        tiles="OpenStreetMap",
        name="Bản đồ đường phố",
        control=True,
        show=(map_mode == "Đường phố")
    ).add_to(m)

    # Lớp bản đồ đường phố kiểu sáng
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Bản đồ Esri",
        control=True,
        show=False
    ).add_to(m)

    # Lớp ảnh vệ tinh
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Imagery",
        name="Ảnh vệ tinh",
        control=True,
        show=(map_mode == "Vệ tinh")
    ).add_to(m)

    # Marker các điểm trong lịch trình
    for day_index, day in enumerate(plan["days"]):
        color = DAY_COLORS[day_index % len(DAY_COLORS)]

        for stop_index, stop in enumerate(day["stops"]):
            p = get_place(stop["place_id"])
            if not p:
                continue

            icon_name, icon_color = category_icon(p["category"])

            popup = f"""
            <div style="width:230px">
                <b>{p['name']}</b><br>
                <span>{p['category']}</span><br>
                <span>{day['name']} - {stop_index + 1}</span><br>
                <span>Giờ đến: {stop.get('arrival','')}</span><br>
                <p>{p.get('description','')}</p>
            </div>
            """

            folium.Marker(
                [p["lat"], p["lon"]],
                tooltip=f"{day['name']} - {p['name']}",
                popup=folium.Popup(popup, max_width=280),
                icon=folium.Icon(
                    color=icon_color,
                    icon=icon_name,
                    prefix="fa"
                )
            ).add_to(m)

    # Marker địa điểm ngoài lịch trình nếu được bật
    if show_all_places:
        planned_ids = {
            s["place_id"]
            for d in plan["days"]
            for s in d["stops"]
        }

        for p in data["places"]:
            if p["id"] in planned_ids:
                continue

            icon_name, icon_color = category_icon(p["category"])

            folium.Marker(
                [p["lat"], p["lon"]],
                tooltip=p["name"],
                popup=folium.Popup(
                    f"<b>{p['name']}</b><br>{p['category']}<br>{p.get('description','')}",
                    max_width=250
                ),
                icon=folium.Icon(
                    color=icon_color,
                    icon=icon_name,
                    prefix="fa"
                )
            ).add_to(m)

    # Tuyến đường từng ngày, màu riêng
    for day_index, day in enumerate(plan["days"]):
        result = calculate_day(day)
        color = DAY_COLORS[day_index % len(DAY_COLORS)]

        for segment in result["segments"]:
            route = segment["route"]

            folium.PolyLine(
                route["coordinates"],
                color=color,
                weight=5,
                opacity=0.85,
                dash_array="8, 5" if segment["estimated"] else None,
                tooltip=(
                    f"{day['name']}: {segment['from']} → {segment['to']} "
                    f"({route['distance']:.1f} km)"
                    + (" - Ước tính đường thẳng" if segment["estimated"] else "")
                )
            ).add_to(m)

    # Chú giải màu các ngày
    legend_items = ""
    for i, day in enumerate(plan["days"]):
        color = DAY_COLORS[i % len(DAY_COLORS)]
        legend_items += f"""
        <div style="margin:4px 0">
            <span style="display:inline-block;width:22px;height:5px;
            background:{color};vertical-align:middle;margin-right:7px"></span>
            {day['name']}
        </div>
        """

    legend_html = f"""
    <div style="
        position: fixed;
        bottom: 25px;
        left: 25px;
        z-index: 9999;
        background: white;
        padding: 10px 14px;
        border: 1px solid #aaa;
        border-radius: 7px;
        font-size: 13px;
        box-shadow: 0 1px 5px #888;
        ">
        <b>MÀU TUYẾN ĐƯỜNG</b>
        {legend_items}
    </div>
    """

    m.get_root().html.add_child(folium.Element(legend_html))
    folium.LayerControl(collapsed=False).add_to(m)

    return m

# ============================================================
# PHẦN E. BẢNG TÓM TẮT LỊCH TRÌNH
# ============================================================

def make_summary(plan):
    rows = []

    for day_index, day in enumerate(plan["days"]):
        result = calculate_day(day)
        places = result["places"]

        if not places:
            place_names = "Chưa có địa điểm"
            time_text = "-"
        else:
            place_names = " → ".join(p["name"] for p in places)
            time_text = " | ".join([
                f"{s.get('arrival','')} {get_place(s['place_id'])['name']}"
                for s in day["stops"]
                if get_place(s["place_id"])
            ])

        distance_text = (
            f"{result['distance']:.1f} km"
            if result["route_complete"]
            else "Chưa lấy đủ tuyến đường"
        )

        rows.append({
            "Ngày": day["name"],
            "Thời gian & địa điểm": time_text,
            "Lịch trình": place_names,
            "Khoảng cách": distance_text
        })

    return pd.DataFrame(rows)

# ============================================================
# PHẦN F. CHẾ ĐỘ CHIA SẺ CHỈ XEM BẢN ĐỒ
# URL chia sẻ có dạng: https://ten-app.streamlit.app/?view=share
# ============================================================

share_mode = st.query_params.get("view", "") == "share"

if share_mode:
    st.title("🏔️ " + plan["name"])
    st.caption("Lịch trình khám phá Hà Giang")

    st.info(
        "Đây là chế độ xem lịch trình. "
        "Bản đồ hiển thị tuyến đường theo màu riêng của từng ngày."
    )

    map_mode = st.radio(
        "Kiểu bản đồ",
        ["Đường phố", "Vệ tinh"],
        horizontal=True
    )

    map_object = create_map(plan, map_mode=map_mode)

    st_folium(
        map_object,
        width=None,
        height=650,
        returned_objects=[]
    )

    st.subheader("Tóm tắt lịch trình")
    st.dataframe(
        make_summary(plan),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Khoảng cách là tổng các đoạn đường OSRM lấy được. "
        "Nếu một đoạn không lấy được tuyến đường, khoảng cách ngày đó "
        "sẽ hiển thị chưa đầy đủ."
    )

    st.stop()

# ============================================================
# PHẦN G. GIAO DIỆN CHÍNH
# ============================================================

st.title("🏔️ HA GIANG TRIP PLANNER")
st.caption("Công cụ lập lịch trình và khám phá Hà Giang")

tab1, tab2, tab3, tab4 = st.tabs([
    "🗓️ Lịch trình",
    "🗺️ Bản đồ",
    "📍 Thư viện địa điểm",
    "💾 Lưu / Chia sẻ"
])

# ============================================================
# TAB 1 - LỊCH TRÌNH
# ============================================================

with tab1:

    st.subheader("Quản lý phương án")

    c1, c2, c3 = st.columns([3, 1, 1])

    with c1:
        selected_plan = st.selectbox(
            "Chọn phương án",
            range(len(data["plans"])),
            format_func=lambda i: data["plans"][i]["name"],
            index=data["active_plan"]
        )

        if selected_plan != data["active_plan"]:
            data["active_plan"] = selected_plan
            st.rerun()

    with c2:
        if st.button("➕ Tạo mới"):
            new_plan = {
                "id": uid(),
                "name": f"Phương án {len(data['plans']) + 1}",
                "days": [
                    {"name": "Ngày 1", "stops": []},
                    {"name": "Ngày 2", "stops": []},
                    {"name": "Ngày 3", "stops": []}
                ]
            }
            data["plans"].append(new_plan)
            data["active_plan"] = len(data["plans"]) - 1
            st.rerun()

    with c3:
        if st.button("📋 Nhân bản"):
            duplicate = copy.deepcopy(plan)
            duplicate["id"] = uid()
            duplicate["name"] = plan["name"] + " - Bản sao"
            data["plans"].append(duplicate)
            data["active_plan"] = len(data["plans"]) - 1
            st.rerun()

    plan["name"] = st.text_input(
        "Tên phương án",
        value=plan["name"],
        key=f"plan_name_{plan['id']}"
    )

    st.divider()

    if st.button("➕ Thêm ngày"):
        plan["days"].append({
            "name": f"Ngày {len(plan['days']) + 1}",
            "stops": []
        })
        st.rerun()

    if not plan["days"]:
        st.info("Chưa có ngày. Hãy thêm ngày.")

    for day_index, day in enumerate(plan["days"]):

        with st.expander(
            f"📅 {day['name']} ({len(day['stops'])} điểm)",
            expanded=True
        ):

            day["name"] = st.text_input(
                "Tên ngày",
                value=day["name"],
                key=f"day_name_{plan['id']}_{day_index}"
            )

            place_options = {
                f"{p['name']} ({p['category']})": p["id"]
                for p in data["places"]
            }

            if place_options:
                chosen = st.selectbox(
                    "Chọn địa điểm",
                    list(place_options.keys()),
                    key=f"place_{plan['id']}_{day_index}"
                )

                if st.button(
                    "Thêm địa điểm vào ngày",
                    key=f"add_{plan['id']}_{day_index}"
                ):
                    place_id = place_options[chosen]
                    day["stops"].append({
                        "id": uid(),
                        "place_id": place_id,
                        "arrival": "08:00",
                        "duration": 60,
                        "note": "",
                        "image": ""
                    })
                    st.rerun()

            st.divider()

            for stop_index, stop in enumerate(day["stops"]):
                p = get_place(stop["place_id"])

                if not p:
                    st.warning("Địa điểm không còn trong thư viện.")
                    continue

                st.markdown(
                    f"**{stop_index + 1}. {p['name']}** · {p['category']}"
                )

                col1, col2, col3 = st.columns([1, 1, 1])

                with col1:
                    stop["arrival"] = st.text_input(
                        "Giờ đến",
                        value=stop.get("arrival", "08:00"),
                        key=f"arrival_{stop['id']}"
                    )

                with col2:
                    stop["duration"] = st.number_input(
                        "Thời gian (phút)",
                        min_value=0,
                        max_value=1440,
                        value=int(stop.get("duration", 60)),
                        key=f"duration_{stop['id']}"
                    )

                with col3:
                    st.caption("Sắp xếp")
                    c_up, c_down = st.columns(2)

                    with c_up:
                        if st.button(
                            "⬆️",
                            key=f"up_{stop['id']}",
                            disabled=stop_index == 0
                        ):
                            day["stops"][stop_index - 1], day["stops"][stop_index] = (
                                day["stops"][stop_index],
                                day["stops"][stop_index - 1]
                            )
                            st.rerun()

                    with c_down:
                        if st.button(
                            "⬇️",
                            key=f"down_{stop['id']}",
                            disabled=stop_index == len(day["stops"]) - 1
                        ):
                            day["stops"][stop_index + 1], day["stops"][stop_index] = (
                                day["stops"][stop_index],
                                day["stops"][stop_index + 1]
                            )
                            st.rerun()

                stop["note"] = st.text_area(
                    "Ghi chú",
                    value=stop.get("note", ""),
                    key=f"note_{stop['id']}"
                )

                st.caption("Ảnh minh họa cho điểm đến / ghi chú")

                uploaded_image = st.file_uploader(
                    "Tải ảnh lên",
                    type=["png", "jpg", "jpeg", "webp"],
                    key=f"image_{stop['id']}"
                )

                if uploaded_image is not None:
                    stop["image"] = base64.b64encode(
                        uploaded_image.getvalue()
                    ).decode("utf-8")
                    stop["image_type"] = uploaded_image.type

                if stop.get("image"):
                    try:
                        image_bytes = base64.b64decode(stop["image"])
                        st.image(
                            image_bytes,
                            caption="Ảnh đã thêm",
                            width=300
                        )
                    except Exception:
                        pass

                other_days = [
                    i for i in range(len(plan["days"]))
                    if i != day_index
                ]

                if other_days:
                    target = st.selectbox(
                        "Chuyển sang ngày",
                        other_days,
                        format_func=lambda i: plan["days"][i]["name"],
                        key=f"target_{stop['id']}"
                    )

                    if st.button(
                        "Chuyển điểm đến",
                        key=f"move_{stop['id']}"
                    ):
                        plan["days"][target]["stops"].append(stop)
                        day["stops"].pop(stop_index)
                        st.rerun()

                if st.button(
                    "🗑️ Xóa điểm đến",
                    key=f"delete_{stop['id']}"
                ):
                    day["stops"].pop(stop_index)
                    st.rerun()

                st.divider()

            if st.button(
                f"🗑️ Xóa ngày {day['name']}",
                key=f"delete_day_{plan['id']}_{day_index}"
            ):
                plan["days"].pop(day_index)
                st.rerun()

# ============================================================
# TAB 2 - BẢN ĐỒ
# ============================================================

with tab2:

    st.subheader("Bản đồ hành trình")

    map_mode = st.radio(
        "Chọn nền bản đồ",
        ["Đường phố", "Vệ tinh"],
        horizontal=True
    )

    show_all = st.checkbox(
        "Hiển thị tất cả địa điểm trong thư viện",
        value=False
    )

    with st.spinner("Đang tải bản đồ và tính tuyến đường..."):
        map_object = create_map(
            plan,
            map_mode=map_mode,
            show_all_places=show_all
        )

        st_folium(
            map_object,
            width=None,
            height=650,
            returned_objects=[]
        )

    st.markdown("### Tóm tắt lịch trình theo ngày")

    summary = make_summary(plan)

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Các tuyến đường được lấy từ dịch vụ OSRM. "
        "Đường nét đứt là đường nối ước tính khi không lấy được dữ liệu "
        "tuyến đường. Khoảng cách tổng chỉ cộng các đoạn OSRM lấy thành công."
    )

    st.markdown("### Chú giải tuyến đường")

    legend_cols = st.columns(min(max(len(plan["days"]), 1), 4))

    for i, day in enumerate(plan["days"]):
        color = DAY_COLORS[i % len(DAY_COLORS)]
        with legend_cols[i % len(legend_cols)]:
            st.markdown(
                f"<span style='color:{color};font-size:25px'>━━</span> "
                f"**{day['name']}**",
                unsafe_allow_html=True
            )

# ============================================================
# TAB 3 - THƯ VIỆN ĐỊA ĐIỂM
# ============================================================

with tab3:

    st.subheader("Thư viện địa điểm")

    search = st.text_input("Tìm kiếm địa điểm")

    categories = sorted(set(
        p["category"] for p in data["places"]
    ))

    selected_category = st.selectbox(
        "Lọc theo phân loại",
        ["Tất cả"] + categories
    )

    filtered_places = [
        p for p in data["places"]
        if search.lower() in p["name"].lower()
        and (
            selected_category == "Tất cả"
            or p["category"] == selected_category
        )
    ]

    for p in filtered_places:
        icon_name, icon_color = category_icon(p["category"])

        with st.expander(
            f"📍 {p['name']} - {p['category']}"
        ):
            st.write(p.get("description", ""))
            st.write(
                f"Tọa độ: {p['lat']}, {p['lon']}"
            )

            if p.get("image"):
                st.image(p["image"], width=300)

    st.divider()
    st.markdown("### Thêm địa điểm")

    with st.form("add_place_form"):
        new_name = st.text_input("Tên địa điểm")

        new_category = st.selectbox(
            "Phân loại",
            [
                "Check-in", "Ăn uống", "Lưu trú",
                "Làng bản", "Tham quan", "Trải nghiệm",
                "Thác nước", "Thiên nhiên", "Văn hóa",
                "Leo núi", "Đô thị", "Cung đường", "Khác"
            ]
        )

        c1, c2 = st.columns(2)

        with c1:
            new_lat = st.number_input(
                "Vĩ độ",
                value=23.0,
                format="%.6f"
            )

        with c2:
            new_lon = st.number_input(
                "Kinh độ",
                value=105.0,
                format="%.6f"
            )

        new_description = st.text_area("Mô tả")
        new_image_url = st.text_input("Link ảnh (nếu có)")

        submitted = st.form_submit_button("Thêm địa điểm")

        if submitted:
            if not new_name.strip():
                st.error("Bạn cần nhập tên địa điểm.")
            else:
                data["places"].append({
                    "id": uid(),
                    "name": new_name.strip(),
                    "category": new_category,
                    "lat": new_lat,
                    "lon": new_lon,
                    "description": new_description,
                    "image": new_image_url
                })
                st.success("Đã thêm địa điểm. Hãy lưu dữ liệu.")
                st.rerun()

    st.divider()
    st.markdown("### Chỉnh sửa / xóa địa điểm")

    if data["places"]:
        selected_id = st.selectbox(
            "Chọn địa điểm cần chỉnh sửa",
            [p["id"] for p in data["places"]],
            format_func=lambda x: get_place(x)["name"]
        )

        selected_place = get_place(selected_id)

        with st.form("edit_place_form"):
            edit_name = st.text_input(
                "Tên",
                value=selected_place["name"]
            )

            edit_category = st.selectbox(
                "Phân loại",
                [
                    "Check-in", "Ăn uống", "Lưu trú",
                    "Làng bản", "Tham quan", "Trải nghiệm",
                    "Thác nước", "Thiên nhiên", "Văn hóa",
                    "Leo núi", "Đô thị", "Cung đường", "Khác"
                ],
                index=(
                    [
                        "Check-in", "Ăn uống", "Lưu trú",
                        "Làng bản", "Tham quan", "Trải nghiệm",
                        "Thác nước", "Thiên nhiên", "Văn hóa",
                        "Leo núi", "Đô thị", "Cung đường", "Khác"
                    ].index(selected_place["category"])
                    if selected_place["category"] in [
                        "Check-in", "Ăn uống", "Lưu trú",
                        "Làng bản", "Tham quan", "Trải nghiệm",
                        "Thác nước", "Thiên nhiên", "Văn hóa",
                        "Leo núi", "Đô thị", "Cung đường", "Khác"
                    ] else 12
                )
            )

            edit_lat = st.number_input(
                "Vĩ độ",
                value=float(selected_place["lat"]),
                format="%.6f"
            )

            edit_lon = st.number_input(
                "Kinh độ",
                value=float(selected_place["lon"]),
                format="%.6f"
            )

            edit_description = st.text_area(
                "Mô tả",
                value=selected_place.get("description", "")
            )

            update = st.form_submit_button("Cập nhật địa điểm")

            if update:
                selected_place.update({
                    "name": edit_name,
                    "category": edit_category,
                    "lat": edit_lat,
                    "lon": edit_lon,
                    "description": edit_description
                })
                st.success("Đã cập nhật.")
                st.rerun()

        if st.button("🗑️ Xóa địa điểm đang chọn"):
            data["places"] = [
                p for p in data["places"]
                if p["id"] != selected_id
            ]

            for p_plan in data["plans"]:
                for d in p_plan["days"]:
                    d["stops"] = [
                        s for s in d["stops"]
                        if s["place_id"] != selected_id
                    ]

            st.rerun()

# ============================================================
# TAB 4 - LƯU / XUẤT / CHIA SẺ
# ============================================================

with tab4:

    st.subheader("Lưu dữ liệu")

    st.warning(
        "Những thay đổi trong ứng dụng chỉ được ghi vào file JSON "
        "khi bạn nhấn nút Lưu dữ liệu."
    )

    if st.button("💾 LƯU DỮ LIỆU", type="primary"):
        save_data()
        st.success("Đã lưu vào ha_giang_data.json")

    st.divider()

    st.markdown("### Xuất dữ liệu JSON")

    json_data = json.dumps(
        data,
        ensure_ascii=False,
        indent=2
    ).encode("utf-8")

    st.download_button(
        "⬇️ Tải toàn bộ dữ liệu JSON",
        data=json_data,
        file_name="ha_giang_data.json",
        mime="application/json"
    )

    st.markdown("### Xuất lịch trình Excel")

    rows = []

    for p_plan in data["plans"]:
        for day in p_plan["days"]:
            for stop in day["stops"]:
                p = get_place(stop["place_id"])
                if p:
                    rows.append({
                        "Phương án": p_plan["name"],
                        "Ngày": day["name"],
                        "Địa điểm": p["name"],
                        "Phân loại": p["category"],
                        "Giờ đến": stop.get("arrival", ""),
                        "Thời gian (phút)": stop.get("duration", 0),
                        "Ghi chú": stop.get("note", "")
                    })

    excel_buffer = io.BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:
        pd.DataFrame(rows).to_excel(
            writer,
            index=False,
            sheet_name="Lich_trinh"
        )

        pd.DataFrame(data["places"]).to_excel(
            writer,
            index=False,
            sheet_name="Dia_diem"
        )

    st.download_button(
        "⬇️ Xuất Excel",
        data=excel_buffer.getvalue(),
        file_name="ha_giang_trip.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.divider()

    st.markdown("### Nhập dữ liệu JSON")

    uploaded_json = st.file_uploader(
        "Chọn file JSON đã xuất trước đó",
        type=["json"]
    )

    if uploaded_json is not None:
        if st.button("Nhập và thay thế dữ liệu hiện tại"):
            try:
                imported = json.load(uploaded_json)

                if (
                    isinstance(imported, dict)
                    and isinstance(imported.get("places"), list)
                    and isinstance(imported.get("plans"), list)
                    and len(imported["plans"]) > 0
                ):
                    data.clear()
                    data.update(imported)
                    data["active_plan"] = min(
                        max(0, int(data.get("active_plan", 0))),
                        len(data["plans"]) - 1
                    )
                    save_data()
                    st.success("Đã nhập dữ liệu.")
                    st.rerun()
                else:
                    st.error("Cấu trúc JSON không hợp lệ.")

            except Exception as e:
                st.error(f"Lỗi nhập dữ liệu: {e}")

    st.divider()

    st.markdown("### Tạo đường dẫn chia sẻ chỉ xem bản đồ")

    app_url = st.text_input(
        "Địa chỉ website Streamlit của bạn",
        placeholder="https://ten-ung-dung.streamlit.app"
    )

    if app_url.strip():
        share_url = (
            app_url.strip().rstrip("/")
            + "?view=share"
        )

        st.code(share_url)

        st.caption(
            "Gửi đường dẫn này cho người khác để họ xem bản đồ "
            "và bảng tóm tắt mà không thấy giao diện chỉnh sửa."
        )

        st.link_button(
            "Mở chế độ xem chia sẻ",
            share_url
        )

    st.divider()

    st.markdown("### Xóa phương án")

    if len(data["plans"]) > 1:
        delete_index = st.selectbox(
            "Chọn phương án cần xóa",
            range(len(data["plans"])),
            format_func=lambda i: data["plans"][i]["name"]
        )

        if st.button("Xóa phương án"):
            data["plans"].pop(delete_index)
            data["active_plan"] = min(
                data["active_plan"],
                len(data["plans"]) - 1
            )
            st.rerun()
    else:
        st.caption("Cần giữ lại ít nhất một phương án.")

st.divider()

st.caption(
    "Ha Giang Trip Planner | Khoảng cách và tuyến đường chỉ mang tính "
    "tham khảo, cần kiểm tra lại trước khi di chuyển."
)
