# Threat Model cho json_search()

## 1. Actor / Role

Hàm `json_search()` có thể được gọi bởi các role:

- `admin`: quản trị hệ thống.
- `operator`: vận hành và giám sát hệ thống.
- `viewer`: xem các thông tin được cho phép.

Mỗi role chỉ được truy cập các trường dữ liệu được quy định trong
`policy.py`.

## 2. Asset cần bảo vệ

Dữ liệu JSON có thể chứa các thông tin nhạy cảm như:

- Thông tin định danh thiết bị.
- Địa chỉ và thông tin hạ tầng mạng.
- API key.
- SNMP credential hoặc chuỗi xác thực.
- Các thông tin nhạy cảm khác của hệ thống.

Các dữ liệu này không được trả về cho người dùng không có quyền.

## 3. Trust Boundary

Trust boundary nằm giữa người gọi hàm và dữ liệu trả về từ API:

    User
      |
      | role
      v
    json_search()
      |
      | kiểm tra quyền
      v
    policy.py
      |
      v
    JSON Data

Nếu `json_search()` không kiểm tra role trước khi trả về kết quả thì
trust boundary này bị bỏ qua.

Khi đó người dùng có quyền thấp vẫn có thể tìm kiếm và đọc các trường
dữ liệu nhạy cảm.

## 4. Threats

### T-01: Information Disclosure

Người dùng có quyền thấp, ví dụ `viewer`, có thể tìm kiếm các trường
nhạy cảm như `apiKey`.

Nếu hàm không kiểm tra role, giá trị của trường có thể bị trả về cho
người dùng không có quyền.

Ví dụ:

    json_search("apiKey", data, role="viewer")

Nếu `viewer` không được phép đọc `apiKey` nhưng hàm vẫn trả về giá trị,
thông tin nhạy cảm đã bị lộ.

Biện pháp:

- Kiểm tra role trước khi trả về kết quả.
- Nếu role không có quyền thì trả về `[]`.

### T-02: Elevation of Privilege

Người dùng có role thấp có thể cố truy cập dữ liệu dành cho role có
quyền cao hơn.

Nếu hàm không kiểm tra quyền, `viewer` hoặc `operator` có thể truy cập
các trường chỉ dành cho role có quyền cao hơn.

Biện pháp:

- Kiểm tra quyền dựa trên `policy.py`.
- Chỉ trả về dữ liệu khi role được phép truy cập trường đó.

## 5. Kết luận

`json_search()` phải kiểm tra role trước khi trả về kết quả.

Nếu role không có quyền truy cập trường được yêu cầu, hàm phải trả về
danh sách rỗng `[]`.

Các yêu cầu này sẽ được sử dụng để xây dựng security test cho
`json_search()` ở bước tiếp theo.
