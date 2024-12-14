import subprocess
from pytube import YouTube
import requests
from datetime import datetime, date
from time import sleep
from tqdm import tqdm
import os

# **Cài đặt thư viện nếu chưa có**
def install_pytube():
    try:
        subprocess.check_call(["pip", "install", "pytube"])
        print("\033[1;32mCài đặt thành công pytube!\033[0m")
    except subprocess.CalledProcessError:
        print("\033[1;31mLỗi khi cài đặt pytube!\033[0m")
install_pytube()

# **Hàm tạo loading bar**
def loading_bar():
    for _ in tqdm(range(100), desc="\033[1;36mĐang tải\033[0m", bar_format="{l_bar}{bar}| {percentage:3.0f}% ", ncols=100, colour="green"):
        sleep(0.05)

# **Kiểm tra kết nối Internet**
def check_internet_connection():
    try:
        requests.get("http://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

if not check_internet_connection():
    print("\033[1;31mVui lòng kiểm tra kết nối Internet!\033[0m")
    exit()

# **Hàm lấy thông tin vị trí**
def get_location_info():
    try:
        response = requests.get("https://ipinfo.io")
        data = response.json()
        city, region, country = data.get("city"), data.get("region"), data.get("country")
        return f"🌍 Bạn đang ở: {city}, {region}, {country}."
    except Exception:
        return "🌍 Không thể xác định vị trí."

# **Hàm lấy thời tiết**
def get_weather():
    try:
        response = requests.get("https://wttr.in/?format=%t")
        return f"⛅ Nhiệt độ hiện tại: {response.text.strip()}."
    except Exception:
        return "⛅ Không thể lấy thông tin thời tiết."

# **Hàm tạo hiệu ứng màu gradient**
def rgb_gradient(text, colors):
    gradient = ""
    length = len(text)
    for i, char in enumerate(text):
        ratio = i / length
        r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
        g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
        b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
        gradient += f"\033[38;2;{r};{g};{b}m{char}\033[0m"
    return gradient

# **Banner giới thiệu**
def display_banner():
    logo = """
    ██████████████████████████████████████████████████████████████████████
    █                                                                   █
    █    ███████╗██╗   ██╗ ██████╗ ████████╗ ██████╗ ██╗    ██╗███████╗  █
    █    ██╔════╝██║   ██║██╔═══██╗╚══██╔══╝██╔═══██╗██║    ██║██╔════╝  █
    █    █████╗  ██║   ██║██║   ██║   ██║   ██║   ██║██║ █╗ ██║█████╗    █
    █    ██╔══╝  ██║   ██║██║   ██║   ██║   ██║   ██║██║███╗██║██╔══╝    █
    █    ██║     ╚██████╔╝╚██████╔╝   ██║   ╚██████╔╝╚███╔███╔╝███████╗  █
    █    ╚═╝      ╚═════╝  ╚═════╝    ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚══════╝  █
    █                                                                   █
    ██████████████████████████████████████████████████████████████████████
    🔥               YouTube Video Downloader | Version 1.2               🔥
    """
    print(rgb_gradient(logo, [(255, 0, 255), (0, 255, 255)]))

# **Thông tin công cụ**
def show_info():
    print(rgb_gradient("=" * 60, [(0, 255, 255), (255, 255, 0)]))
    print(f"\033[1;33m[INFO] Tool Python Downloader - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\033[0m")
    print(f"\033[1;36m{get_location_info()}\033[0m")
    print(f"\033[1;36m{get_weather()}\033[0m")
    print(rgb_gradient("=" * 60, [(0, 255, 255), (255, 255, 0)]))

# **Hàm tải video**
def download_video(url, output_folder):
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        print(f"\033[1;35mĐang tải xuống: {yt.title}\033[0m")
        video.download(output_path=output_folder)
        print(f"\033[1;32mVideo đã được tải xuống thành công tại: {os.path.join(output_folder, yt.title)}\033[0m")
    except Exception as e:
        print(f"\033[1;31mLỗi khi tải video: {e}\033[0m")

# **Chương trình chính**
if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    display_banner()
    show_info()
    video_url = input("\n\033[1;34mNhập link video YouTube cần tải: \033[1;33m").strip()
    loading_bar()
    output_dir = "Downloaded_Videos"
    os.makedirs(output_dir, exist_ok=True)
    download_video(video_url, output_dir)