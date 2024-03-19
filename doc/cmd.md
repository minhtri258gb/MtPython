
# PIP

* Package mgr
> pip list (Danh sách đã cài)
> pip list --outdated (Danh sách có thể nâng cấp)
> pip install <package-name> (Cài package)
> pip install <package-name>==<version> (Cài thêm package chọn phiên bản)
> pip uninstall -y <package-name> (Gỡ package)
> pip freeze > requirements.txt (Xuất package ra file)
> pip install -r requirements.txt --upgrade (Update toàn bộ package trong file)

Exam: pip install Flask==3.0.2

* Update pip itself
> pip3 install --upgrade pip
> python.exe -m pip install --upgrade pip
