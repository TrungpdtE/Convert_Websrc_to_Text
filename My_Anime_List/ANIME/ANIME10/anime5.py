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
        'types': [],
        'open_dates': [],
        'end_dates': [],
        'durations': [],
        'opening_songs': [],
        'ending_songs': [],
        'ratings': [],
        'seasons': [],
        'years': []
    }
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tìm tất cả các khối anime
        anime_blocks = soup.find_all('div', class_='js-seasonal-anime')
        
        for block in anime_blocks:
            title_tag = block.find('h2', class_='h2_anime_title').find('a')
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
            date = format_date(date_tag.text.strip()) if date_tag else 'N/A'
            genres = ', '.join(genre.text for genre in block.find_all('span', class_='genre')) if block.find_all('span', class_='genre') else 'N/A'
            episodes = episodes_tag.text.strip().replace(' eps', '') if episodes_tag else 'N/A'

            # Lấy rating từ thẻ js-score
            rating_tag = block.find('span', class_='js-score')
            rating = rating_tag.text.strip() if rating_tag else 'N/A'

            # Truy cập vào trang chi tiết của anime
            anime_link = title_tag['href']
            anime_response = requests.get(anime_link, headers={'User-Agent': 'Mozilla/5.0'})
            if anime_response.status_code == 200:
                anime_soup = BeautifulSoup(anime_response.text, 'html.parser')

                # Lấy loại phim
                type_tag = anime_soup.find('span', class_='dark_text', string='Type:')
                anime_type = type_tag.find_next('a').text.strip() if type_tag else 'N/A'
                
                # Lấy ngày phát sóng
                aired_tag = anime_soup.find('span', class_='dark_text', string='Aired:')
                if aired_tag and aired_tag.find_parent('div'):
                    aired_text = aired_tag.find_parent('div').get_text(strip=True)
                    aired_dates = aired_text.split('to')
                    open_date = aired_dates[0].replace('Aired:', '').strip() if len(aired_dates) > 0 else 'N/A'
                    end_date = aired_dates[1].strip() if len(aired_dates) > 1 else 'N/A'
                else:
                    open_date, end_date = 'N/A', 'N/A'
                
                # Lấy độ dài
                duration_tag = anime_soup.find('span', class_='dark_text', string='Duration:')
                duration = duration_tag.find_next('div').text.strip() if duration_tag else 'N/A'

                # Lấy opening song
                opening_songs = []
                opening_theme = anime_soup.find('div', class_='theme-songs js-theme-songs opening')
                if opening_theme:
                    for song in opening_theme.find_all('tr'):
                        song_td = song.find('td', width='84%')
                        if song_td:
                            song_name = song_td.get_text(strip=True).split(' by ')[0]
                            artist_tag = song_td.find('span', class_='theme-song-artist')
                            artist_name = artist_tag.text.strip() if artist_tag else 'Unknown Artist'
                            opening_songs.append(f"{song_name}({artist_name})")
                opening_song_str = ', '.join(opening_songs) if opening_songs else 'N/A'

                # Lấy ending song
                ending_songs = []
                ending_theme = anime_soup.find('div', class_='theme-songs js-theme-songs ending')
                if ending_theme:
                    for song in ending_theme.find_all('tr'):
                        song_td = song.find('td', width='84%')
                        if song_td:
                            song_name = song_td.get_text(strip=True).split(' by ')[0]
                            artist_tag = song_td.find('span', class_='theme-song-artist')
                            artist_name = artist_tag.text.strip() if artist_tag else 'Unknown Artist'
                            ending_songs.append(f"{song_name}({artist_name})")
                ending_song_str = ', '.join(ending_songs) if ending_songs else 'N/A'
            else:
                anime_type, open_date, end_date, duration, opening_song_str, ending_song_str = 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'

            # Thêm dữ liệu vào dictionary
            anime_data['titles'].append(title)
            anime_data['studios'].append(studio)
            anime_data['sources'].append(source)
            anime_data['genres'].append(genres)
            anime_data['episodes'].append(f'0/{episodes}')
            anime_data['types'].append(anime_type)
            anime_data['open_dates'].append(open_date)
            anime_data['end_dates'].append(end_date)
            anime_data['durations'].append(duration)
            anime_data['opening_songs'].append(opening_song_str)
            anime_data['ending_songs'].append(ending_song_str)
            anime_data['ratings'].append(rating)
            anime_data['seasons'].append(season.capitalize())  # Lưu mùa của anime
            anime_data['years'].append(str(year))  # Lưu năm của anime

    return anime_data

# Hàm ghi log vị trí hiện tại
def write_log(year, season):
    with open('anime_data/log.txt', 'w') as log_file:
        log_file.write(f"{year},{season}\n")

# Hàm đọc log để tiếp tục từ vị trí cuối cùng
def read_log():
    try:
        with open('anime_data/log.txt', 'r') as log_file:
            last_position = log_file.readline().strip().split(',')
            return int(last_position[0]), last_position[1]
    except FileNotFoundError:
        return None  # Nếu không có tệp log thì bắt đầu từ đầu

# Danh sách các mùa
seasons = ['winter', 'spring', 'summer', 'fall']

# Tạo thư mục lưu tệp nếu chưa tồn tại
if not os.path.exists('anime_data'):
    os.makedirs('anime_data')

# Đọc vị trí từ log nếu có
last_year_season = read_log()

# Nếu có vị trí trong log, bắt đầu từ đó, nếu không thì bắt đầu từ 2024
start_year = last_year_season[0] if last_year_season else 2024
start_season = last_year_season[1] if last_year_season else 'winter'

# Lặp qua các năm từ 2024 đến 1917
for year in range(start_year, 1916, -1):
    for season in seasons:
        # Bỏ qua các mùa đã chạy trước đó nếu có log
        if year == start_year and seasons.index(season) < seasons.index(start_season):
            continue

        print(f"Lấy dữ liệu cho mùa {season.capitalize()} {year}...")

        # Lấy danh sách anime của mùa đó
        anime_data = get_anime_from_season(year, season)

        # Ghi dữ liệu vào các tệp riêng biệt và ghi mùa/năm đồng thời
        for i in range(len(anime_data['titles'])):
            # Ghi thông tin từng bộ anime vào các tệp
            with open('anime_data/titles.txt', 'a', encoding='utf-8') as file:
                file.write(f"{anime_data['titles'][i]}\n")
            with open('anime_data/studios.txt', 'a', encoding='utf-8') as file:
                file.write(f"{anime_data['studios'][i]}\n")
            with open('anime_data/genres.txt', 'a', encoding='utf-8') as file:
                file.write(f"{anime_data['genres'][i]}\n")
            with open('anime_data/sources.txt', 'a', encoding='utf-8') as file:
                file.write(f"{anime_data['sources'][i]}\n")
            with open('anime_data/episodes.txt', 'a', encoding='utf-8') as file:
                file.write(f"{anime_data['episodes'][i]}\n")
            with open('anime_data/types.txt', 'a', encoding='utf-8') as file:
                file.write(f"{anime_data['types'][i]}\n")
            with open('anime_data/open_dates.txt', 'a', encoding='utf-8') as file:
                file.write(f"{anime_data['open_dates'][i]}\n")
            with open('anime_data/end_dates.txt', 'a', encoding='utf-8') as file:
                file.write(f"{anime_data['end_dates'][i]}\n")
            with open('anime_data/durations.txt', 'a', encoding='utf-8') as file:
                file.write(f"{anime_data['durations'][i]}\n")
            with open('anime_data/opening_songs.txt', 'a', encoding='utf-8') as file:
                file.write(f"{anime_data['opening_songs'][i]}\n")
            with open('anime_data/ending_songs.txt', 'a', encoding='utf-8') as file:
                file.write(f"{anime_data['ending_songs'][i]}\n")
            with open('anime_data/ratings.txt', 'a', encoding='utf-8') as file:
                file.write(f"{anime_data['ratings'][i]}\n")
            with open('anime_data/mua.txt', 'a', encoding='utf-8') as file:
                file.write(f"{anime_data['seasons'][i]}\n")  # Ghi mùa cho mỗi anime
            with open('anime_data/year.txt', 'a', encoding='utf-8') as file:
                file.write(f"{anime_data['years'][i]}\n")  # Ghi năm cho mỗi anime

        # Ghi log sau khi xong một mùa
        write_log(year, season)

        # Để tránh gửi quá nhiều yêu cầu trong thời gian ngắn
        time.sleep(1)

print("Dữ liệu anime đã được lưu vào các tệp riêng biệt trong thư mục 'anime_data'.")
