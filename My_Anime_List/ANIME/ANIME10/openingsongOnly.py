import requests
from bs4 import BeautifulSoup
import time
import os
from datetime import datetime

# Hàm lấy danh sách anime từ một mùa cụ thể
def get_anime_from_season(year, season):
    url = f'https://myanimelist.net/anime/season/{year}/{season}'
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    anime_data = {
        'opening_songs': []
    }
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tìm tất cả các khối anime
        anime_blocks = soup.find_all('div', class_='js-seasonal-anime')
        
        for block in anime_blocks:
            title_tag = block.find('h2', class_='h2_anime_title').find('a')

            # Truy cập vào trang chi tiết của anime
            anime_link = title_tag['href']
            anime_response = requests.get(anime_link, headers={'User-Agent': 'Mozilla/5.0'})
            if anime_response.status_code == 200:
                anime_soup = BeautifulSoup(anime_response.text, 'html.parser')

                # Lấy opening song
                opening_songs = []
                opening_theme = anime_soup.find('div', class_='theme-songs js-theme-songs opnening')
                if opening_theme:
                    for song in opening_theme.find_all('tr'):
                        song_td = song.find('td', width='84%')
                        if song_td:
                            song_name = song_td.get_text(strip=True).split(' by ')[0]
                            artist_tag = song_td.find('span', class_='theme-song-artist')
                            artist_name = artist_tag.text.strip() if artist_tag else 'Unknown Artist'
                            opening_songs.append(f"{song_name} ({artist_name})")
                opening_song_str = ', '.join(opening_songs) if opening_songs else 'N/A'
                anime_data['opening_songs'].append(opening_song_str)

    return anime_data

# Danh sách các mùa
seasons = ['winter', 'spring', 'summer', 'fall']

# Tạo thư mục lưu tệp nếu chưa tồn tại
if not os.path.exists('anime_data'):
    os.makedirs('anime_data')

# Lặp qua các năm từ 2024 đến 1917
for year in range(2001, 1916, -1):
    for season in seasons:
        print(f"Lấy dữ liệu cho mùa {season.capitalize()} {year}...")

        # Lấy danh sách anime của mùa đó
        anime_data = get_anime_from_season(year, season)

        # Ghi dữ liệu opening song vào tệp
        with open(f'anime_data/opening_songs.txt', 'a', encoding='utf-8') as file:
            for opening_song in anime_data['opening_songs']:
                file.write(f"{opening_song}\n")

        time.sleep(1)  # Chờ 1 giây giữa các yêu cầu để tránh bị chặn

print("Danh sách các bài opening song đã được lưu vào tệp 'opening_songs.txt'.")
#2001