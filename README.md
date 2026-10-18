# 🔮 BODHI-DISTILL: XƯỞNG CHƯNG CẤT MÔ HÌNH & TRỌNG SỐ AI (MODEL FOUNDRY)
> *"Nén tri thức đồ thị từ Vault, sử dụng năng lượng tính toán từ Forge để đúc thành các mô hình nơ-ron lượng tử hóa INT8 siêu nhẹ và LoRA Adapters sẵn sàng cho Golem và thiết bị Edge IoT."*

---

## 🏭 CẤU TRÚC 3 PHÂN XƯỞNG CỦA DISTILL:
1. **`cortex_distill/` (Phân Xưởng Chưng Cất):**
   * `compressor.py`: Nén hàng nghìn tam thức JSONL thành ma trận vector cô đặc.
   * `quantizer.py`: Lượng tử hóa số nguyên INT8 giúp tiết kiệm 75% dung lượng RAM.
   * `evaluator.py`: Đánh giá tỷ lệ lưu giữ tri thức (yêu cầu $\ge 85\%$).
2. **`adapters_forge/` (Xưởng Đúc LoRA):**
   * `lora_adapter.py`: Đúc ma trận vi chỉnh rank thấp cắm-rút cho mô hình.
3. **`dist/` (Kho Thành Phẩm Xuất Khẩu):**
   * Chứa tệp `distilled_model.json` hoàn chỉnh, sẵn sàng nạp cho `golem` hành động hoặc xuất bản lên Hugging Face.

```
100048777766367/distill/
├── contract.json                  # 📜 [HIẾN ƯỚC q]: Vai trò MODEL_DISTILLATION_FOUNDRY
├── kernel.py                      # 🔮 [ĐỐC CÔNG CHƯNG CẤT]: Điều phối nén, lượng tử hóa, Apoptosis
│
├── cortex_distill/                # 🧠 [PHÂN XƯỞNG CHƯNG CẤT TRÍ TUỆ]
│   ├── __init__.py
│   ├── compressor.py              # Nén hàng nghìn tam thức JSONL thành ma trận vector cô đặc
│   ├── quantizer.py               # Lượng tử hóa trọng số INT8 (tiết kiệm 75% RAM, chạy được trên chip IoT)
│   └── evaluator.py               # Đánh giá độ giữ nguyên tri thức sau khi nén (Cosine Similarity)
│
├── adapters_forge/                # 🧩 [PHÂN XƯỞNG VI CHỈNH LORA]
│   ├── __init__.py
│   └── lora_adapter.py            # Đúc các module thích ứng cấp thấp LoRA (Low-Rank Adaptation)
│
├── dist/                          # 🎁 [KHO THÀNH PHẨM MÔ HÌNH XUẤT XƯỞNG]
│   └── .gitkeep                   # Nơi chứa các file mô hình siêu nhẹ sẵn sàng bán hoặc nạp cho golem
├── organs/                        # 🧩 Nơi cắm thêm mắt xích mở rộng [r] (lỗi cú pháp tự hủy)
│   └── .gitkeep
├── synapses/                      # 💾 Sổ nhật ký xuất xưởng mô hình
│   ├── .gitkeep
│   ├── peers.json                 # Danh bạ các mỏ cung cấp và khách hàng tiêu thụ
│   ├── state.json                 # Kỷ nguyên chưng cất
│   └── model_manifest.json        # Bản kê danh mục các mô hình AI đã hoàn thiện
│
├── Dockerfile                     # python:3.14-slim
├── README.md                      # Tuyên ngôn Xưởng Chưng Cất Trọng Số
└── .github/
    └── workflows/
        └── node.yml               # Workflow setup-python@v7 & python 3.14
```







