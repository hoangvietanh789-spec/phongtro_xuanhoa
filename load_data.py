import json
from pathlib import Path
from shutil import copy2
from bs4 import BeautifulSoup

# --- Cấu hình ---
html_path = Path("index.html")      # file HTML gốc
json_path = Path("data.json")       # file dữ liệu
deploy_dir = Path("dist")           # thư mục deploy (tạo nếu chưa có)

deploy_dir.mkdir(exist_ok=True)      # tạo thư mục nếu chưa có
deploy_path = deploy_dir / "index.html"  # file HTML sau khi deploy

# --- Đọc dữ liệu JSON ---
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- Đọc và parse HTML ---
html_content = html_path.read_text(encoding="utf-8")
soup = BeautifulSoup(html_content, "html.parser")

# --- Danh sách các key cần nhúng ---
keys = [
    "aircon_waterheater", "area", "available_num", "cctv", "electric",
    "owner", "parking", "price",  "price_single", "price_double",
    "tel", "time", "water", "wifi", "zalo", "btn-call"
]

# --- Thay thế giá trị ---
for key in keys:
    el = soup.find(id=key)
    if el:
        if el.name == "a":
            if key == "tel" or key == "btn-call":
                el["href"] = f"tel:{data['tel']}"
                if key == "btn-call":
                    el.string = "Gọi ngay"
            elif key == "zalo":
                el["href"] = f"https://zalo.me/{data['tel']}"
                el.string = "Nhắn Zalo"
            else:
                el["href"] = data[key]
                el.string = data[key]
        else:
            el.string = data[key]

# --- Xóa đoạn script fetch JSON cũ ---
for script in soup.find_all("script"):
    if "fetch(jsonUrl)" in script.text:
        script.decompose()

# --- Ghi file HTML vào thư mục deploy ---
deploy_path.write_text(str(soup), encoding="utf-8")
print(f"Đã nhúng dữ liệu và deploy HTML vào: {deploy_path.resolve()}")

# --- Tùy chọn: copy các asset khác (ảnh, css) nếu cần ---
# Ví dụ copy toàn bộ thư mục 'assets' sang 'dist/assets'
assets_src = Path("assets")
assets_dst = deploy_dir / "assets"
if assets_src.exists():
    import shutil
    shutil.copytree(assets_src, assets_dst, dirs_exist_ok=True)
    print(f"Đã copy assets sang: {assets_dst.resolve()}")