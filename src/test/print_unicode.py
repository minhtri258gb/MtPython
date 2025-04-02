

# ## CÁCH 1
# # -> Ko thể Print khi dùng đa luồng
# import sys
# import io

# # Thiết lập
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# # Print
# print("Xin chào, đây là tiếng Việt!")



# ## CÁCH 2
# # Ko hoạt động
# import locale

# # Thiết lập mã hóa mặc định
# locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  # Hoặc 'vi_VN.UTF-8' nếu hệ thống hỗ trợ

# # In tiếng Việt
# print("Xin chào, đây là tiếng Việt!".encode('utf-8'))