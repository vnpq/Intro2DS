import requests
from bs4 import BeautifulSoup
import csv

# URL của trang web bạn muốn parse
url = "https://www.worldweatheronline.com/ho-chi-minh-city-weather-history/vn.aspx"

# Gửi yêu cầu HTTP GET tới URL và lấy nội dung trang web
response = requests.get(url)
response.encoding = 'utf-8' # Đảm bảo mã hóa đúng

# Kiểm tra xem yêu cầu có thành công không (mã trạng thái 200)
if response.status_code == 200:
    # Parse nội dung HTML của trang web
    soup = BeautifulSoup(response.text, "html.parser")

    # Tìm bảng chứa dữ liệu thời tiết
    weather_table = soup.find("table", {"class": "weather_tb"}) # Điều chỉnh lớp bảng nếu cần

    # Nếu bảng không tồn tại, in ra thông báo và thoát
    if not weather_table:
        print("Không tìm thấy bảng dữ liệu thời tiết.")
        exit()

    # Tạo danh sách để lưu dữ liệu
    weather_data = []

    # Duyệt qua từng hàng trong bảng (trừ hàng đầu tiên là tiêu đề)
    rows = weather_table.find_all("tr")[1:]  # Bỏ qua hàng tiêu đề
    for row in rows:
        columns = row.find_all("td")
        # Lấy dữ liệu từ các cột
        date = columns[0].text.strip()  # Cột ngày
        temp = columns[1].text.strip()  # Cột nhiệt độ
        desc = columns[2].text.strip()  # Cột mô tả thời tiết

        # Thêm dữ liệu vào danh sách
        weather_data.append([date, temp, desc])

    # Ghi dữ liệu vào file CSV
    with open("ho_chi_minh_weather_history.csv", "w", newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)
        # Ghi tiêu đề cho các cột
        csvwriter.writerow(["Date", "Temperature", "Description"])
        # Ghi từng hàng dữ liệu
        csvwriter.writerows(weather_data)

    print("Dữ liệu đã được lưu vào ho_chi_minh_weather_history.csv.")
else:
    print(f"Lỗi khi truy cập trang web: {response.status_code}")
