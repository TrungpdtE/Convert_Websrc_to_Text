import requests
from bs4 import BeautifulSoup
import time
import os

# Hàm lấy danh sách anime từ một mùa cụ thể và lưu link
def get_anime_links_from_season(year, season):
    url = f'https://myanimelist.net/anime/season/{year}/{season}'
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tìm tất cả các khối anime
        anime_blocks = soup.find_all('div', class_='js-seasonal-anime')
        
        with open('anime_data/link.txt', 'a', encoding='utf-8') as link_file:
            for block in anime_blocks:
                title_tag = block.find('h2', class_='h2_anime_title').find('a')
                
                # Lấy liên kết của anime
                if title_tag:
                    anime_link = title_tag['href']
                    link_file.write(f"{anime_link}\n")

# Danh sách các mùa
seasons = ['winter', 'spring', 'summer', 'fall']

# Tạo thư mục lưu tệp nếu chưa tồn tại
if not os.path.exists('anime_data'):
    os.makedirs('anime_data')

# Chạy lấy liên kết cho từng mùa và năm từ 2024 đến 1917
for year in range(2024, 1916, -1):
    for season in seasons:
        print(f"Lấy liên kết cho mùa {season.capitalize()} {year}...")
        get_anime_links_from_season(year, season)
        time.sleep(1)  # Để tránh gửi quá nhiều yêu cầu cùng lúc

print("Tất cả các liên kết anime đã được lưu vào 'anime_data/link.txt'.")
