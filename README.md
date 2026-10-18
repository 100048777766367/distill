# 📜 CONTRACT: GỐC HIẾN ƯỚC BẤT BIẾN [q] (THE ROOT PROTOCOL CONTRACT)
> *"Bản thể tối giản cực hạn, thẩm phán tự thi hành luật Apoptosis, bảo tồn liên kết vĩnh cửu dù sống hay chết và triệt tiêu mọi nợ kỹ thuật."*

---

## 🏛️ ĐIỀU LỆ VẬN HÀNH [q]:

### 1. Công Thức Đại Số Sinh Tồn:
$$\mathbf{[q]} \xrightarrow{\text{Fork [w]}} \mathbf{[e]} \xrightarrow{\text{Gắn mắt xích [r]}} \mathbf{[t]} \xrightarrow{} \mathbf{[q]}$$

* **[q]**: Hạt nhân bất biến (Repo `contract`).
* **[w] & [e]**: Phân nhánh và nhân bản vô hạn.
* **[r]**: Các cơ chế phụ lục mở rộng đặt trong thư mục `organs/`.
* **[t]**: Kiểm định tự động. Nếu cơ chế chạy tốt $\rightarrow$ Ghi nhận. Nếu cơ chế sinh lỗi cú pháp/hỏng code $\rightarrow$ **Kích hoạt Apoptosis tự xóa sổ tệp lỗi, đưa hệ thống hoàn nguyên về [q]**.

---

### 2. Định Luật Liên Kết Vĩnh Cửu [m] & [n]:
* **[m] Nút còn sống:** Trao đổi xung tiến `synapse_forward.json` và cập nhật danh bạ `synapses/peers.json`.
* **[n] Nút đã chết (404):** Không bị loại bỏ, mà được phong tước thành **Bia Mộ Số (`synapses/tombstones.json`)**. Toàn bộ di sản lịch sử được lưu trữ vĩnh viễn để hậu duệ kế thừa.

---

### 3. Nguyên Lý Khống Chế Tuyệt Đối [c] (Không Sợ Nợ Kỹ Thuật [v]):
* Không ai được sửa `kernel.py` hay `contract.json`.
* Mọi sự phát triển đều diễn ra ở dạng cắm-rút trong `organs/`. Lỗi ở đâu, tự hủy ở đó, không bao giờ lây lan làm hỏng hạt nhân `[q]`.

```
100048777766367/contract/
├── contract.json              # 📜 [HIẾN ƯỚC GỐC q]: Bộ điều khoản bất biến của toàn hệ sinh thái
├── kernel.py                  # 🏛️ [THẨM PHÁN THỰC THI]: Tự kiểm tra [t], tự hủy lỗi [v], liên kết [m][n]
├── organs/                    # 🧩 [MẮT XÍCH PHỤ LỤC r]: Nơi các đời con cháu [e] cắm cơ chế mới
│   └── .gitkeep               # Nếu file con trong này lỗi cú pháp -> kernel tự xóa để quy hồi [q]
├── synapses/                  # 💾 [SỔ CÁI BẤT BIẾN]
│   ├── .gitkeep
│   ├── peers.json             # Danh bạ các nút đang sống [m]
│   ├── tombstones.json        # 🕯️ Danh bạ các nút đã chết [n] (Di sản vĩnh cửu không đứt gãy)
│   └── state.json             # Sổ nhật ký kỷ nguyên hợp đồng
├── Dockerfile                 # Đóng băng hạt nhân: python:3.12-slim
├── README.md                  # Đại Tuyên Ngôn Hợp Đồng Khởi Thủy
└── .github/
    └── workflows/
        └── node.yml           # Workflow bọc thép tự trị – Không dây rốn
```







