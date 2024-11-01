import requests
import json

category = {
    "food": [["sang-trong", 12], ["buffet", 39], ["nha-hang", 1], ["an-vat-via-he", 11], ["an-chay", 56], ["cafe", 2], ["quan-an", 3], 
             ["bar-pub", 4], ["quan-nhau", 54], ["beer-club", 43], ["tiem-banh", 6], ["foodcourt", 79]],
    "travel": [["khu-du-lich", 7], ["cong-vien-vui-choi", 24], ["bao-tang-di-tich", 64]],
    # "restaurant": [["bao-tang-di-tich", 64]],
    "entertain": [["karaoke", 5], ["billiards", 8], ["giai-tri", 13], ["san-khau", 23], ["khu-choi-game", 25]],
    "shop": [["trung-tam-thuong-mai", 31]]
}

# mongodb+srv://5CLCsCan:5clcscan@hcmus.yrgifkc.mongodb.net/?retryWrites=true&w=majority&appName=HCMUS

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Ch-Ua": '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
    "X-Foody-User-Token": "xX1XF0gpGsRKHglxnE4D6gFObARUHNwwOcavRuskhgEHHuN4labexpG4KeWK",
    "X-Requested-With": "XMLHttpRequest"
}


cookies = {
    "flg": "vn",
    "__ondemand_sessionid": "c34r4tkdbcspkagfvancnacf",
    "floc": "217",
    "gcat": "food",
    "__utma": "257500956.258760816.1717010662.1717010662.1717010662.1",
    "__utmc": "257500956",
    "__utmz": "257500956.1717010662.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)",
    "__utmt_UA-33292184-1": "1",
    "_ga": "GA1.2.258760816.1717010662",
    "_gid": "GA1.2.1717508847.1717010663",
    "FOODY.AUTH.UDID": "f1157743-228f-409e-b153-f1cc9d3b7c8f",
    "FOODY.AUTH": "30F2086F91BA1AFEDCCED77C3E699B7B7CAF11191623BA73395743320B83D9DE92A01CB977C493C7948F535EF2203DB1341A6E5C924628DFC3A410E895B4C1F68D40A3C8D6CF1ECE09A7CCF678BDDF6788A05A201E81DED4F7E93A582AFAFF6863DBF72B21070828BBB86286EF515B10F7573C8B829692A7787D04F1DBEFDE392036FBC9E11CEC3A4901C17FBAA7577B26FEA563E3DD3C3F552F53DAA0F3FEBED88D400B0D135D9D0E7C9D1BFA50EB9D005616BD368E085EDA5410C0FB899E7F7FC83ACF5AE6CCE90BC50D25A05DBAC089E6ABB8CF33DAE14A8F7CFD0A3C87CD5BDF077E46BAE887C8CBF07C1F4049E7DBEE727FF3B5CA527FD4070585E5BB05",
    "fd.keys": "",
    "_gat": "1",
    "_ga_6M8E625L9H": "GS1.2.1717010662.1.1.1717011208.45.0.0",
    "__utmb": "257500956.6.10.1717010662"
}


whitelist_url = None
result = []

process_log = open("process_log.txt", "w", encoding='utf-8')

def parse(data, category, sub = False):
    global whitelist_url
    global result
    if (len(data) == 0):
        return sub, 0
    cnt = 0
    for item in data:
        id_ = item["Id"]
        if (id_ in whitelist_url):
            print("Duplicate")
            process_log.write(f"Duplicate\n")
            return False, cnt
        whitelist_url.add(id_)
        address = item["Address"]
        lat = item["Latitude"]
        long = item["Longitude"]
        name = item["Name"]
        imgLink = item["PicturePathLarge"]
        detailUrl = f"https://www.foody.vn{item['DetailUrl']}"
        result.append({
            "id": id_,
            "name": name,
            "address": address,
            "latitude": lat,
            "longitude": long,
            "imgLink": imgLink,
            "detailUrl": detailUrl,
            "category": category
        })
        print(f"Added {name}")
        process_log.write(f"Added {name}\n")
        _, tmp = parse(item["SubItems"], category, True)
        cnt += tmp + 1
    return True, cnt


def crawlData(category1, category2, categoryID, page):
    tmp_cookies = cookies.copy()
    tmp_cookies["gcat"] = category2
    url = f"https://www.foody.vn/ho-chi-minh/{category1}?ds={category2}&vt=row&st=1&c={categoryID}&page={page}&provinceId=217&categoryId={categoryID}&append=true"
    print(f"Crawling data from {url}")
    process_log.write(f"Crawling data from {url}\n")
    cnt = 0
    while (cnt < 10):
        response = requests.get(url, headers=headers, cookies=tmp_cookies)
        if (response.status_code != 200):
            print("Error: ", response.status_code)
            process_log.write(f"Error: {response.status_code}\n")
            print(f"Retry {cnt}")
            process_log.write(f"Retry {cnt}\n")
            cnt += 1
            continue
        return response.json()
    return None
# tmp = crawlData("bao-tang-di-tich", "Travel", 64, 1)
# print(tmp["searchItems"][1]["Name"])

# exit(0)

log_fo = open("log.txt", "w", encoding='utf-8')

# list_cookies = []
# for category2 in category:
#     tmp_cookies = cookies.copy()
#     tmp_cookies["gcat"] = category2
#     list_cookies.append(tmp_cookies)

for category2 in category:
    for category1, categoryID in category[category2]:
        whitelist_url = set()
        
        page = 1
        cnt = 0
        # for cookies in list_cookies:
        while True:
            data = crawlData(category1, category2, categoryID, page)
            if (data == None):
                break
            ok, total = parse(data["searchItems"], f"{category2}/{category1}")
            cnt += total
            if (not ok):
                break
            page += 1
        log_fo.write(f"{category2}/{category1}: {cnt}\n")

log_fo.close()

print(f"Total: {len(result)}")
process_log.write(f"Total: {len(result)}\n")

with open("data_version2.json", "w", encoding='utf-8') as f:
    json.dump(result, f, indent=4, ensure_ascii=False)

process_log.close()