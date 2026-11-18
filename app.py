
import streamlit as st
import pandas as pd
import folium
import requests
import json
import os
import copy
import uuid
from pathlib import Path
from streamlit_folium import st_folium

# ============================================================
# PHẦN A. DANH SÁCH ĐỊA ĐIỂM - CHỈNH SỬA TẠI ĐÂY
# ============================================================

PLACES = [
    {
        "id": "HG001",
        "name": "Lô Lô Chải",
        "category": "Làng bản",
        "lat": 23.3575,
        "lon": 105.3040,
        "description": "Làng văn hóa của người Lô Lô dưới chân cột cờ Lũng Cú.",
        "province": "Tuyên Quang",
        "image": ""
    },
    {
        "id": "HG002",
        "name": "Cột cờ Lũng Cú",
        "category": "Tham quan",
        "lat": 23.3619,
        "lon": 105.3150,
        "description": "Điểm cực Bắc nổi tiếng của Việt Nam.",
        "province": "Tuyên Quang",
        "image": ""
    },
    {
        "id": "HG003",
        "name": "Phố cổ Đồng Văn",
        "category": "Phố cổ",
        "lat": 23.2770,
        "lon": 105.3600,
        "description": "Khu phố cổ với kiến trúc nhà cổ và không gian văn hóa vùng cao.",
        "province": "Tuyên Quang",
        "image": ""
    },
    {
        "id": "HG004",
        "name": "Đèo Mã Pí Lèng",
        "category": "Check-in",
        "lat": 23.2060,
        "lon": 105.4050,
        "description": "Một trong những cung đèo nổi tiếng của miền Bắc.",
        "province": "Tuyên Quang",
        "image": ""
    },
    {
        "id": "HG005",
        "name": "Sông Nho Quế",
        "category": "Trải nghiệm",
        "lat": 23.1900,
        "lon": 105.4100,
        "description": "Trải nghiệm đi thuyền trên sông Nho Quế.",
        "province": "Tuyên Quang",
        "image": ""
    },
    {
        "id": "HG006",
        "name": "Hẻm Tu Sản",
        "category": "Check-in",
        "lat": 23.1850,
        "lon": 105.4050,
        "description": "Hẻm vực sâu nổi tiếng trên dòng Nho Quế.",
        "province": "Tuyên Quang",
        "image": ""
    },
    {
        "id": "HG007",
        "name": "Nhà của Pao",
        "category": "Văn hóa",
        "lat": 23.2560,
        "lon": 105.2880,
        "description": "Ngôi nhà truyền thống tại thung lũng Sủng Là.",
        "province": "Tuyên Quang",
        "image": ""
    },
    {
        "id": "HG008",
        "name": "Dinh thự họ Vương",
        "category": "Văn hóa",
        "lat": 23.2570,
        "lon": 105.2820,
        "description": "Công trình kiến trúc lịch sử nổi tiếng.",
        "province": "Tuyên Quang",
        "image": ""
    },
    {
        "id": "HG009",
        "name": "Rừng thông Yên Minh",
        "category": "Thiên nhiên",
        "lat": 23.1000,
        "lon": 105.1500,
        "description": "Khu vực rừng thông và cảnh quan núi rừng.",
        "province": "Tuyên Quang",
        "image": ""
    },
    {
        "id": "HG010",
        "name": "Núi Đôi Quản Bạ",
        "category": "Thiên nhiên",
        "lat": 23.0670,
        "lon": 104.9910,
        "description": "Điểm ngắm cảnh nổi tiếng tại Quản Bạ.",
        "province": "Tuyên Quang",
        "image": ""
    },
    {
        "id": "HG011",
        "name": "Cổng trời Quản Bạ",
        "category": "Check-in",
        "lat": 23.0640,
        "lon": 104.9800,
        "description": "Điểm ngắm toàn cảnh thung lũng Tam Sơn.",
        "province": "Tuyên Quang",
        "image": ""
    },
    {
        "id": "HG012",
        "name": "Hoàng Su Phì",
        "category": "Thiên nhiên",
        "lat": 22.7500,
        "lon": 104.6800,
        "description": "Khu vực ruộng bậc thang nổi tiếng.",
        "province": "Tuyên Quang",
        "image": ""
    },
    {
        "id": "HG013",
        "name": "Chiêu Lầu Thi",
        "category": "Leo núi",
        "lat": 22.7200,
        "lon": 104.7200,
        "description": "Điểm trekking và săn mây.",
        "province": "Tuyên Quang",
        "image": ""
    },
    {
        "id": "HG014",
        "name": "Thác Tiên",
        "category": "Thiên nhiên",
        "lat": 22.6500,
        "lon": 104.7000,
        "description": "Điểm tham quan thiên nhiên tại khu vực Hoàng Su Phì.",
        "province": "Tuyên Quang",
        "image": ""
    },
    {
        "id": "HG015",
        "name": "Thành phố Hà Giang",
        "category": "Đô thị",
        "lat": 22.8230,
        "lon": 104.9830,
        "description": "Điểm xuất phát phổ biến cho hành trình khám phá.",
        "province": "Tuyên Quang",
        "image": ""
    },
]
PLACES.extend([
    {
        "id": "HG016",
        "name": "Làng H'Mông Pả Vi",
        "category": "Làng bản",
        "lat": 23.2130,
        "lon": 105.4160,
        "description": "Làng văn hóa người Mông, nổi bật với nhà trình tường và homestay.",
        "province": "Tuyên Quang",
        "image": ""
    },
    {
        "id": "HG017",
        "name": "Thị trấn Mèo Vạc",
        "category": "Đô thị",
        "lat": 23.2180,
        "lon": 105.4130,
        "description": "Trung tâm khu vực Mèo Vạc, điểm dừng chân trên cung đường Hà Giang Loop.",
        "province": "Tuyên Quang",
        "image": ""
    },
    {
        "id": "HG018",
        "name": "Mèo Vạc Panorama Cafe",
        "category": "Ăn uống",
        "lat": 23.2150,
        "lon": 105.4070,
        "description": "Điểm cà phê/ngắm cảnh khu vực Mèo Vạc. Cần xác minh lại vị trí chính xác.",
        "province": "Tuyên Quang",
        "image": ""
    },
    {
        "id": "HG019",
        "name": "Yên Minh",
        "category": "Đô thị",
        "lat": 23.1320,
        "lon": 105.1500,
        "description": "Thị trấn Yên Minh, điểm nghỉ chân trên cung đường Hà Giang Loop.",
        "province": "Tuyên Quang",
        "image": ""
    },
    {
        "id": "HG020",
        "name": "Du Già",
        "category": "Làng bản",
        "lat": 22.7300,
        "lon": 105.2000,
        "description": "Khu vực Du Già nổi tiếng với cảnh quan núi rừng, bản làng và homestay.",
        "province": "Tuyên Quang",
        "image": ""
    },
    {
        "id": "HG021",
        "name": "Thác Du Già",
        "category": "Thác nước",
        "lat": 22.7250,
        "lon": 105.2050,
        "description": "Thác nước tại khu vực Du Già, phù hợp tham quan và trải nghiệm thiên nhiên.",
        "province": "Tuyên Quang",
        "image": ""
    },
    {
        "id": "HG022",
        "name": "Mậu Duệ",
        "category": "Đô thị",
        "lat": 22.9800,
        "lon": 105.2000,
        "description": "Khu vực ngã rẽ quan trọng trên cung đường nối Mèo Vạc, Yên Minh và Du Già.",
        "province": "Tuyên Quang",
        "image": ""
    },
    {
        "id": "HG023",
        "name": "Thuận Hòa",
        "category": "Cung đường",
        "lat": 22.8500,
        "lon": 104.9500,
        "description": "Điểm thuộc khu vực tuyến đường Thuận Hòa - Thái An.",
        "province": "Tuyên Quang",
        "image": ""
    },
    {
        "id": "HG024",
        "name": "Thái An",
        "category": "Cung đường",
        "lat": 23.0200,
        "lon": 105.0000,
        "description": "Điểm thuộc khu vực tuyến đường Thuận Hòa - Thái An.",
        "province": "Tuyên Quang",
        "image": ""
    }
])
# ============================================================
# PHẦN B. CẤU HÌNH VÀ KHỞI TẠO
# ============================================================

st.set_page_config(
    page_title="Ha Giang Trip Planner",
    page_icon="🏔️",
    layout="wide"
)

DATA_FILE = Path("ha_giang_data.json")

def new_id():
    return str(uuid.uuid4())[:8]

def default_data():
    return {
        "places": copy.deepcopy(PLACES),
        "plans": [
            {
                "id": new_id(),
                "name": "Phương án 1",
                "days": [
                    {"name": "Ngày 1", "stops": []},
                    {"name": "Ngày 2", "stops": []},
                    {"name": "Ngày 3", "stops": []}
                ]
            }
        ],
        "active_plan": 0
    }

def load_data():
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            if "places" in data and "plans" in data:
                return data
        except Exception:
            pass
    return default_data()

if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data

if not data["plans"]:
    data["plans"] = default_data()["plans"]
    data["active_plan"] = 0

data["active_plan"] = min(
    max(0, data.get("active_plan", 0)),
    len(data["plans"]) - 1
)

plan = data["plans"][data["active_plan"]]

# ============================================================
# PHẦN C. HÀM XỬ LÝ
# ============================================================

def save_data():
    DATA_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def get_place(place_id):
    return next(
        (p for p in data["places"] if p["id"] == place_id),
        None
    )

def route_between(a, b):
    """Lấy tuyến đường lái xe từ OSRM; trả về None nếu lỗi."""
    try:
        url = (
            "https://router.project-osrm.org/route/v1/driving/"
            f"{a['lon']},{a['lat']};{b['lon']},{b['lat']}"
            "?overview=full&geometries=geojson"
        )
        response = requests.get(url, timeout=12)
        response.raise_for_status()
        result = response.json()

        if result.get("routes"):
            route = result["routes"][0]
            return {
                "distance": route["distance"] / 1000,
                "duration": route["duration"] / 60,
                "coordinates": [
                    [lat, lon]
                    for lon, lat in route["geometry"]["coordinates"]
                ]
            }
    except Exception:
        return None
    return None

def add_stop(day_index, place_id):
    stop = {
        "id": new_id(),
        "place_id": place_id,
        "arrival": "08:00",
        "duration": 60,
        "note": ""
    }
    plan["days"][day_index]["stops"].append(stop)

def delete_stop(day_index, stop_id):
    plan["days"][day_index]["stops"] = [
        s for s in plan["days"][day_index]["stops"]
        if s["id"] != stop_id
    ]

def move_stop(day_index, stop_index, direction):
    stops = plan["days"][day_index]["stops"]
    new_index = stop_index + direction

    if 0 <= new_index < len(stops):
        stops[stop_index], stops[new_index] = (
            stops[new_index], stops[stop_index]
        )

# ============================================================
# PHẦN D. GIAO DIỆN
# ============================================================

st.title("🏔️ HA GIANG TRIP PLANNER")
st.caption("Công cụ lập lịch trình và khám phá các địa điểm tại Hà Giang")

tab1, tab2, tab3, tab4 = st.tabs([
    "🗓️ Lịch trình",
    "📍 Bản đồ",
    "🏞️ Thư viện địa điểm",
    "💾 Lưu / Xuất dữ liệu"
])

# ============================================================
# TAB 1 - LỊCH TRÌNH
# ============================================================

with tab1:

    st.subheader("Quản lý phương án")

    c1, c2, c3 = st.columns([3, 1, 1])

    with c1:
        plan_names = [
            p["name"] for p in data["plans"]
        ]
        selected = st.selectbox(
            "Chọn phương án",
            range(len(plan_names)),
            format_func=lambda x: plan_names[x],
            index=data["active_plan"]
        )

        if selected != data["active_plan"]:
            data["active_plan"] = selected
            st.rerun()

    with c2:
        if st.button("➕ Tạo phương án"):
            duplicated = copy.deepcopy(plan)
            duplicated["id"] = new_id()
            duplicated["name"] = f"Phương án {len(data['plans']) + 1}"
            data["plans"].append(duplicated)
            data["active_plan"] = len(data["plans"]) - 1
            st.rerun()

    with c3:
        if st.button("📋 Nhân bản"):
            duplicated = copy.deepcopy(plan)
            duplicated["id"] = new_id()
            duplicated["name"] = plan["name"] + " - Bản sao"
            data["plans"].append(duplicated)
            data["active_plan"] = len(data["plans"]) - 1
            st.rerun()

    plan["name"] = st.text_input(
        "Tên phương án",
        value=plan["name"],
        key=f"plan_name_{plan['id']}"
    )

    st.divider()

    # Thêm ngày
    c1, c2 = st.columns([1, 4])

    with c1:
        if st.button("➕ Thêm ngày"):
            plan["days"].append({
                "name": f"Ngày {len(plan['days']) + 1}",
                "stops": []
            })
            st.rerun()

    if not plan["days"]:
        st.info("Chưa có ngày nào. Hãy thêm ngày để bắt đầu.")

    # Hiển thị từng ngày
    for day_index, day in enumerate(plan["days"]):

        with st.expander(
            f"📅 {day['name']} - {len(day['stops'])} điểm đến",
            expanded=True
        ):

            day["name"] = st.text_input(
                "Tên ngày",
                value=day["name"],
                key=f"day_name_{plan['id']}_{day_index}"
            )

            # Thêm địa điểm
            place_options = {
                f"{p['name']} ({p['category']})": p["id"]
                for p in data["places"]
            }

            if place_options:
                selected_place = st.selectbox(
                    "Chọn địa điểm để thêm",
                    list(place_options.keys()),
                    key=f"add_place_{plan['id']}_{day_index}"
                )

                if st.button(
                    "Thêm vào lịch trình",
                    key=f"add_btn_{plan['id']}_{day_index}"
                ):
                    add_stop(
                        day_index,
                        place_options[selected_place]
                    )
                    st.rerun()

            st.divider()

            if not day["stops"]:
                st.caption("Chưa có điểm đến.")

            for stop_index, stop in enumerate(day["stops"]):

                place = get_place(stop["place_id"])

                if not place:
                    st.warning("Địa điểm không còn tồn tại.")
                    continue

                st.markdown(f"**{stop_index + 1}. {place['name']}**")

                col1, col2, col3, col4 = st.columns(
                    [1.2, 1, 1, 1]
                )

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
                    if st.button(
                        "⬆️",
                        key=f"up_{stop['id']}",
                        disabled=stop_index == 0
                    ):
                        move_stop(day_index, stop_index, -1)
                        st.rerun()

                    if st.button(
                        "⬇️",
                        key=f"down_{stop['id']}",
                        disabled=stop_index == len(day["stops"]) - 1
                    ):
                        move_stop(day_index, stop_index, 1)
                        st.rerun()

                with col4:
                    if st.button(
                        "🗑️ Xóa",
                        key=f"delete_{stop['id']}"
                    ):
                        delete_stop(day_index, stop["id"])
                        st.rerun()

                stop["note"] = st.text_area(
                    "Ghi chú",
                    value=stop.get("note", ""),
                    key=f"note_{stop['id']}",
                    height=70
                )

                # Chuyển điểm đến sang ngày khác
                other_days = [
                    i for i in range(len(plan["days"]))
                    if i != day_index
                ]

                if other_days:
                    target_day = st.selectbox(
                        "Chuyển sang ngày",
                        other_days,
                        format_func=lambda i: plan["days"][i]["name"],
                        key=f"move_day_{stop['id']}"
                    )

                    if st.button(
                        "Chuyển địa điểm",
                        key=f"move_btn_{stop['id']}"
                    ):
                        plan["days"][target_day]["stops"].append(stop)
                        delete_stop(day_index, stop["id"])
                        st.rerun()

                st.divider()

            if st.button(
                f"🗑️ Xóa {day['name']}",
                key=f"delete_day_{plan['id']}_{day_index}"
            ):
                plan["days"].pop(day_index)
                st.rerun()

# ============================================================
# TAB 2 - BẢN ĐỒ
# ============================================================

with tab2:

    st.subheader("Bản đồ hành trình")

    all_stops = []

    for day_index, day in enumerate(plan["days"]):
        for stop in day["stops"]:
            place = get_place(stop["place_id"])
            if place:
                all_stops.append((day_index, stop, place))

    if not data["places"]:
        st.warning("Chưa có địa điểm.")

    else:
        selected_categories = st.multiselect(
            "Lọc loại địa điểm",
            sorted(set(p["category"] for p in data["places"])),
            default=sorted(set(p["category"] for p in data["places"]))
        )

        map_places = [
            p for p in data["places"]
            if p["category"] in selected_categories
        ]

        center = [22.95, 105.15]

        m = folium.Map(
            location=center,
            zoom_start=9,
            tiles="OpenStreetMap"
        )

        # Marker địa điểm
        for p in map_places:
            popup_html = f"""
            <b>{p['name']}</b><br>
            Loại: {p['category']}<br>
            {p['description']}
            """

            folium.Marker(
                [p["lat"], p["lon"]],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=p["name"],
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)

        # Đường đi theo thứ tự lịch trình từng ngày
        show_routes = st.checkbox(
            "Hiển thị tuyến đường theo lịch trình",
            value=True
        )

        route_summary = []

        if show_routes:
            for day_index, day in enumerate(plan["days"]):

                places = [
                    get_place(s["place_id"])
                    for s in day["stops"]
                ]
                places = [p for p in places if p]

                if len(places) < 2:
                    continue

                for i in range(len(places) - 1):
                    a, b = places[i], places[i + 1]
                    route = route_between(a, b)

                    if route:
                        folium.PolyLine(
                            route["coordinates"],
                            color="red",
                            weight=4,
                            tooltip=(
                                f"{a['name']} → {b['name']}: "
                                f"{route['distance']:.1f} km, "
                                f"{route['duration']:.0f} phút"
                            )
                        ).add_to(m)

                        route_summary.append({
                            "Ngày": day["name"],
                            "Từ": a["name"],
                            "Đến": b["name"],
                            "Khoảng cách (km)": round(route["distance"], 1),
                            "Thời gian (phút)": round(route["duration"])
                        })

                    else:
                        folium.PolyLine(
                            [[a["lat"], a["lon"]], [b["lat"], b["lon"]]],
                            color="gray",
                            weight=2,
                            dash_array="6, 8",
                            tooltip="Không lấy được tuyến đường"
                        ).add_to(m)

        st_folium(m, width=None, height=600, returned_objects=[])

        if route_summary:
            st.markdown("#### Thống kê tuyến đường")
            route_df = pd.DataFrame(route_summary)
            st.dataframe(route_df, use_container_width=True)

            st.caption(
                "Tuyến đường lấy từ OSRM và OpenStreetMap. "
                "Đây là ước tính tham khảo, có thể khác điều kiện thực tế."
            )

# ============================================================
# TAB 3 - THƯ VIỆN ĐỊA ĐIỂM
# ============================================================

with tab3:

    st.subheader("Thư viện địa điểm")

    search = st.text_input("Tìm kiếm địa điểm")

    categories = sorted(
        set(p["category"] for p in data["places"])
    )

    category_filter = st.selectbox(
        "Lọc theo loại",
        ["Tất cả"] + categories
    )

    filtered = [
        p for p in data["places"]
        if search.lower() in p["name"].lower()
        and (
            category_filter == "Tất cả"
            or p["category"] == category_filter
        )
    ]

    st.dataframe(
        pd.DataFrame([
            {
                "Tên": p["name"],
                "Loại": p["category"],
                "Vĩ độ": p["lat"],
                "Kinh độ": p["lon"],
                "Mô tả": p["description"]
            }
            for p in filtered
        ]),
        use_container_width=True
    )

    st.divider()
    st.markdown("#### Thêm địa điểm mới")

    with st.form("add_place_form"):
        name = st.text_input("Tên địa điểm")
        category = st.selectbox(
            "Phân loại",
            [
                "Check-in", "Tham quan", "Ăn uống",
                "Lưu trú", "Trải nghiệm", "Thiên nhiên",
                "Văn hóa", "Làng bản", "Leo núi", "Khác"
            ]
        )

        col1, col2 = st.columns(2)
        with col1:
            lat = st.number_input(
                "Vĩ độ",
                value=22.95,
                format="%.6f"
            )
        with col2:
            lon = st.number_input(
                "Kinh độ",
                value=105.15,
                format="%.6f"
            )

        description = st.text_area("Mô tả")
        image_url = st.text_input("Link ảnh (nếu có)")

        submitted = st.form_submit_button("Thêm địa điểm")

        if submitted:
            if name.strip():
                data["places"].append({
                    "id": new_id(),
                    "name": name.strip(),
                    "category": category,
                    "lat": lat,
                    "lon": lon,
                    "description": description,
                    "province": "Tuyên Quang",
                    "image": image_url
                })
                st.success("Đã thêm địa điểm. Nhấn Lưu dữ liệu để lưu lâu dài.")
                st.rerun()
            else:
                st.error("Bạn cần nhập tên địa điểm.")

    st.divider()
    st.markdown("#### Chỉnh sửa / xóa địa điểm")

    if data["places"]:
        place_ids = [p["id"] for p in data["places"]]

        selected_id = st.selectbox(
            "Chọn địa điểm",
            place_ids,
            format_func=lambda x: get_place(x)["name"]
        )

        selected_place = get_place(selected_id)

        with st.form("edit_place_form"):
            edit_name = st.text_input(
                "Tên",
                value=selected_place["name"]
            )
            edit_category = st.text_input(
                "Phân loại",
                value=selected_place["category"]
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
            edit_image = st.text_input(
                "Link ảnh",
                value=selected_place.get("image", "")
            )

            update = st.form_submit_button("Cập nhật")

            if update:
                selected_place.update({
                    "name": edit_name,
                    "category": edit_category,
                    "lat": edit_lat,
                    "lon": edit_lon,
                    "description": edit_description,
                    "image": edit_image
                })
                st.success("Đã cập nhật.")
                st.rerun()

        if st.button("🗑️ Xóa địa điểm đang chọn"):
            data["places"] = [
                p for p in data["places"]
                if p["id"] != selected_id
            ]

            # Loại bỏ các điểm đã xóa khỏi lịch trình
            for p_plan in data["plans"]:
                for day in p_plan["days"]:
                    day["stops"] = [
                        s for s in day["stops"]
                        if s["place_id"] != selected_id
                    ]

            st.rerun()

# ============================================================
# TAB 4 - LƯU / XUẤT / NHẬP DỮ LIỆU
# ============================================================

with tab4:

    st.subheader("Lưu và quản lý dữ liệu")

    st.warning(
        "Các thay đổi chỉ được ghi vào file khi bạn nhấn Lưu dữ liệu."
    )

    if st.button("💾 LƯU DỮ LIỆU", type="primary"):
        save_data()
        st.success("Đã lưu dữ liệu vào ha_giang_data.json")

    st.divider()

    # Xuất JSON
    json_bytes = json.dumps(
        data,
        ensure_ascii=False,
        indent=2
    ).encode("utf-8")

    st.download_button(
        "⬇️ Xuất toàn bộ dữ liệu JSON",
        data=json_bytes,
        file_name="ha_giang_data.json",
        mime="application/json"
    )

    # Xuất Excel
    rows = []

    for p_plan in data["plans"]:
        for day in p_plan["days"]:
            for stop in day["stops"]:
                place = get_place(stop["place_id"])
                if place:
                    rows.append({
                        "Phương án": p_plan["name"],
                        "Ngày": day["name"],
                        "Địa điểm": place["name"],
                        "Phân loại": place["category"],
                        "Giờ đến": stop["arrival"],
                        "Thời gian (phút)": stop["duration"],
                        "Ghi chú": stop["note"]
                    })

    excel_df = pd.DataFrame(rows)

    import io
    excel_buffer = io.BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:
        excel_df.to_excel(
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

    # Nhập JSON
    st.markdown("#### Nhập dữ liệu từ JSON")

    uploaded = st.file_uploader(
        "Chọn file ha_giang_data.json",
        type=["json"]
    )

    if uploaded is not None:
        if st.button("Nhập và thay thế dữ liệu hiện tại"):
            try:
                imported = json.load(uploaded)

                if (
                    isinstance(imported, dict)
                    and isinstance(imported.get("places"), list)
                    and isinstance(imported.get("plans"), list)
                    and len(imported["plans"]) > 0
                ):
                    data.clear()
                    data.update(imported)
                    save_data()
                    st.success("Đã nhập dữ liệu.")
                    st.rerun()
                else:
                    st.error("File JSON không đúng cấu trúc.")

            except Exception as e:
                st.error(f"Không thể nhập file: {e}")

    st.divider()

    st.markdown("#### Xóa phương án")

    if len(data["plans"]) > 1:
        delete_plan_index = st.selectbox(
            "Chọn phương án cần xóa",
            range(len(data["plans"])),
            format_func=lambda i: data["plans"][i]["name"]
        )

        if st.button("Xóa phương án đã chọn"):
            data["plans"].pop(delete_plan_index)
            data["active_plan"] = min(
                data["active_plan"],
                len(data["plans"]) - 1
            )
            st.rerun()
    else:
        st.caption("Cần giữ lại ít nhất một phương án.")

st.divider()
st.caption(
    "Ha Giang Trip Planner | Dữ liệu mẫu cần được kiểm tra tọa độ "
    "trước khi sử dụng cho chuyến đi thực tế."
)
