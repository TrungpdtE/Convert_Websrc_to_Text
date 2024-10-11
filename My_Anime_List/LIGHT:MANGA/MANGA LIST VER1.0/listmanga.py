from bs4 import BeautifulSoup

# Mở file và đọc nội dung
with open('textmanga.txt', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Phân tích cú pháp HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Tìm tất cả các phần tử h3 có class là "manga_h3"
manga_titles = soup.find_all('h3', class_='manga_h3')

# Tạo một tập hợp để loại bỏ các tên trùng lặp
unique_manga_titles = set()

# Mở file out.txt để ghi kết quả
with open('out.txt', 'w', encoding='utf-8') as out_file:
    for title in manga_titles:
        # Lấy tên manga từ thẻ a bên trong thẻ h3 và loại bỏ khoảng trắng
        manga_name = title.find('a').get_text(strip=True)
        # Thêm vào tập hợp nếu chưa có
        if manga_name not in unique_manga_titles:
            unique_manga_titles.add(manga_name)
            out_file.write(manga_name + '\n')

print("Đã xuất tên manga vào file out.txt, loại bỏ các tên trùng lặp.")
