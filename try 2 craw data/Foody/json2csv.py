import json
import csv

# Đọc dữ liệu từ file JSON
with open("data_version2.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

# Ghi dữ liệu vào file CSV
with open("data_version2.csv", "w", encoding="utf-8", newline="") as csv_file:
    # Định nghĩa bộ ghi CSV
    csv_writer = csv.writer(csv_file)
    
    # Ghi hàng tiêu đề
    csv_writer.writerow(["ID", "Name", "Address", "Latitude", "Longitude", "Image Link", "Detail URL", "Category"])

    # Ghi từng dòng dữ liệu
    for item in data:
        csv_writer.writerow([
            item["id"],
            item["name"],
            item["address"],
            item["latitude"],
            item["longitude"],
            item["imgLink"],
            item["detailUrl"],
            item["category"]
        ])

print("Chuyển đổi từ JSON sang CSV thành công!")
