import re
from bs4 import BeautifulSoup

# Đọc nội dung từ file text.txt
with open('text.txt', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Phân tích HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Danh sách để lưu kết quả
output_list = []

# Tìm tất cả các hàng trong bảng
for tr in soup.find_all('tr'):
    # Trích xuất dữ liệu từ các ô trong hàng
    han_viet = tr.find('td', attrs={'data-th': 'Hán Việt'}).text.strip() if tr.find('td', attrs={'data-th': 'Hán Việt'}) else ''
    tieng_viet = tr.find('td', attrs={'data-th': 'Tiếng Việt'}).text.strip() if tr.find('td', attrs={'data-th': 'Tiếng Việt'}) else ''
    
    # Kết hợp các giá trị theo định dạng yêu cầu
    if han_viet and tieng_viet:
        combined = f"{han_viet} ({tieng_viet})"
        output_list.append(combined)

# Xuất ra danh sách vào file
with open('output_list.txt', 'w', encoding='utf-8') as output_file:
    for i in range(0, len(output_list), 10):
        line = ' / '.join(output_list[i:i+10])  # Kết hợp 10 thẻ cách nhau bằng dấu '/'
        output_file.write(line + '\n')  # Ghi mỗi dòng vào file
