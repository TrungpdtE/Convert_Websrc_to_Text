import requests
from bs4 import BeautifulSoup

# URL của trang manga
url = 'https://myanimelist.net/topmanga.php'

# Danh sách để lưu thông tin
manga_list = []
date_list = []
rate_list = []
type_list = []
volume_list = []

# Lặp qua nhiều trang
limit = 50  # Mỗi trang hiển thị 50 manga
offset = 0  # Bắt đầu từ trang đầu

while True:
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, params={'limit': limit, 'offset': offset})
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tìm tất cả các mục manga
        manga_items = soup.find_all('tr', class_='ranking-list')

        if not manga_items:
            break  # Dừng nếu không còn mục nào

        for manga in manga_items:
            title_tag = manga.find('h3', class_='manga_h3').find('a')
            title = title_tag.text.strip() if title_tag else "N/A"  # Lấy tiêu đề từ thẻ <a>

            # Lấy điểm đánh giá
            score_tag = manga.find('td', class_='score')
            score = score_tag.find('span', class_='score-label').text.strip() if score_tag else "N/A"

            # Lấy năm sản xuất
            info_div = manga.find('div', class_='information')
            if info_div:
                year_info = info_div.text.strip().split('\n')[1]  # Lấy dòng thứ 2 (năm)
                year = year_info.split('-')[0].strip()  # Chỉ lấy năm bắt đầu
            else:
                year = "N/A"

            # Lấy thông tin loại và số lượng tập
            if info_div:
                type_text = "Manga" if "Manga" in info_div.text else "Light Novel"
                type_list.append(type_text)

                volume_text = info_div.text.split('(')[1].split(')')[0].strip() if '(' in info_div.text else "N/A"
                volume_list.append(volume_text)
            else:
                type_list.append("N/A")
                volume_list.append("N/A")

            # Thêm thông tin vào danh sách
            manga_list.append(title)
            date_list.append(year)
            rate_list.append(score)

        offset += limit  # Tăng offset để lấy trang tiếp theo
    else:
        print(f"Error: {response.status_code}")
        break

# Xuất danh sách vào các tệp
with open('manga.txt', 'w', encoding='utf-8') as manga_file, \
     open('date.txt', 'w', encoding='utf-8') as date_file, \
     open('rate.txt', 'w', encoding='utf-8') as rate_file, \
     open('type.txt', 'w', encoding='utf-8') as type_file, \
     open('volume.txt', 'w', encoding='utf-8') as volume_file:

    for title, year, score, manga_type, volume in zip(manga_list, date_list, rate_list, type_list, volume_list):
        manga_file.write(f"{title}\n")
        date_file.write(f"{year}\n")
        rate_file.write(f"{score}\n")
        type_file.write(f"{manga_type}\n")
        volume_file.write(f"{volume}\n")

print("Danh sách đã được xuất vào manga.txt, date.txt, rate.txt, type.txt và volume.txt")
