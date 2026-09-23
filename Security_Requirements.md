# Security Requirements cho json_search()

## 1. Mục tiêu

Hàm `json_search()` được sử dụng để tìm kiếm thông tin trong dữ liệu JSON
trả về từ API giám sát hạ tầng mạng.

Do dữ liệu có thể chứa các thông tin nhạy cảm, hàm cần kiểm tra quyền của
người dùng trước khi trả về kết quả.

## 2. Các role

Hệ thống có các role:

- `admin`: quản trị hệ thống, có quyền truy cập cao nhất.
- `operator`: vận hành và giám sát hệ thống.
- `viewer`: chỉ được xem các thông tin thông thường.

Quyền truy cập cụ thể của từng role được xác định trong `policy.py`.

## 3. Security Requirements

### SR-01: Kiểm tra role

Hàm `json_search()` phải kiểm tra role của người gọi trước khi trả về
kết quả tìm kiếm.

### SR-02: Kiểm soát quyền truy cập

Hệ thống chỉ trả về giá trị của một trường nếu role của người dùng được
phép truy cập trường đó theo `policy.py`.

### SR-03: Bảo vệ dữ liệu nhạy cảm

Các thông tin nhạy cảm như API key, thông tin xác thực, SNMP credential
hoặc thông tin định danh thiết bị không được trả về cho role không có quyền.

Ví dụ, nếu `viewer` không có quyền đọc `apiKey`:

    json_search("apiKey", data, role="viewer")

phải trả về:

    []

### SR-04: Từ chối role không hợp lệ

Nếu role không tồn tại hoặc không được phép truy cập trường được yêu cầu,
hàm phải trả về kết quả rỗng thay vì trả về dữ liệu.

### SR-05: Kiểm tra quyền khi tìm kiếm đệ quy

Việc kiểm tra quyền phải được áp dụng cho cả dữ liệu nằm bên trong các
dictionary hoặc list lồng nhau.
