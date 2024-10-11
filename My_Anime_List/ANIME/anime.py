import requests
from bs4 import BeautifulSoup
import time
import os
from datetime import datetime

# Hàm chuyển đổi định dạng ngày
def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%Y%m%d')
        return date_obj.strftime('%d/%m/%Y')
    except ValueError:
        return 'N/A'

# Hàm lấy danh sách anime từ một mùa cụ thể
def get_anime_from_season(year, season):
    url = f'https://myanimelist.net/anime/season/{year}/{season}'
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    anime_data = {
        'titles': [],
        'studios': [],
        'genres': [],
        'sources': [],
        'episodes': [],
        'dates': [],
        'ratings': []
    }
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tìm tất cả các khối anime
        anime_blocks = soup.find_all('div', class_='js-seasonal-anime')
        
        for block in anime_blocks:
            title_tag = block.find('h2', class_='h2_anime_title').find('a')
            rating_tag = block.find('span', class_='js-score')
            date_tag = block.find('span', class_='js-start_date')
            episodes_tag = block.find('span', string=lambda x: x and 'eps' in x)

            # Lấy thông tin studio và source từ phần properties
            properties = block.find('div', class_='properties')
            studio, source = 'N/A', 'N/A'
            if properties:
                studio_tag = properties.find('span', class_='caption', string='Studio')
                source_tag = properties.find('span', class_='caption', string='Source')
                if studio_tag and studio_tag.find_next_sibling('span'):
                    studio = studio_tag.find_next_sibling('span').text.strip()
                if source_tag and source_tag.find_next_sibling('span'):
                    source = source_tag.find_next_sibling('span').text.strip()

            # Lấy thông tin
            title = title_tag.text.strip() if title_tag else 'N/A'
            rating = rating_tag.text.strip() if rating_tag else 'N/A'
            date = format_date(date_tag.text.strip()) if date_tag else 'N/A'
            genres = ' '.join(genre.text for genre in block.find_all('span', class_='genre')) if block.find_all('span', class_='genre') else 'N/A'
            episodes = episodes_tag.text.strip().replace(' eps', '') if episodes_tag else 'N/A'
            episodes = f"0/{episodes}"  # Đổi định dạng thành 0/x

            # Thêm dữ liệu vào dictionary
            anime_data['titles'].append(title)
            anime_data['ratings'].append(rating)
            anime_data['dates'].append(date)
            anime_data['studios'].append(studio)
            anime_data['sources'].append(source)
            anime_data['genres'].append(genres)
            anime_data['episodes'].append(episodes)
    
    return anime_data

# Danh sách các mùa
seasons = ['winter', 'spring', 'summer', 'fall']

# Tạo thư mục lưu tệp nếu chưa tồn tại
if not os.path.exists('anime_data'):
    os.makedirs('anime_data')

# Lặp qua các năm từ 2024 đến 1917
for year in range(2024, 1916, -1):
    for season in seasons:
        print(f"Lấy dữ liệu cho mùa {season.capitalize()} {year}...")

        # Lấy danh sách anime của mùa đó
        anime_data = get_anime_from_season(year, season)

        # Ghi dữ liệu vào tệp titles.txt
        with open('anime_data/titles.txt', 'a', encoding='utf-8') as title_file:
            for title in anime_data['titles']:
                title_file.write(f"{title} ({season.capitalize()}) [{year}]\n")

        # Ghi dữ liệu vào các tệp khác
        for key, values in anime_data.items():
            if key != 'titles':  # Không ghi lại tiêu đề
                with open(f'anime_data/{key}.txt', 'a', encoding='utf-8') as file:
                    for value in values:
                        file.write(f"{value}\n")  # Ghi mỗi giá trị trên một dòng

        time.sleep(1)  # Chờ 1 giây giữa các yêu cầu để tránh bị chặn

print("Dữ liệu anime đã được lưu vào các tệp riêng biệt trong thư mục 'anime_data'.")
