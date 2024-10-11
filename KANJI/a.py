import re
from bs4 import BeautifulSoup

# Đọc nội dung từ file text.txt
with open('text.txt', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Phân tích HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Tìm tất cả các thẻ <a> bên trong thẻ <td> với data-th="Hán Tự"
kanji_list = []

for td in soup.find_all('td', attrs={'data-th': 'Hán Tự'}):
    for a in td.find_all('a'):
        # Lấy chữ Kanji từ nội dung thẻ <a>
        kanji = a.text.strip()
        if re.search(r'[\u4e00-\u9faf]', kanji):  # Kiểm tra xem có ký tự Kanji không
            kanji_list.append(kanji)

# Xuất ra danh sách chữ Kanji theo định dạng yêu cầu
with open('kanji_list.txt', 'w', encoding='utf-8') as output_file:
    for i in range(0, len(kanji_list), 10):
        line = ', '.join(kanji_list[i:i+10])  # Kết hợp 10 từ Kanji, cách nhau bằng dấu phẩy không có dấu cách
        output_file.write(line.replace(' ', '') + '\n')  # Ghi mỗi dòng vào file
