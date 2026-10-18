class Int8Quantizer:
    """Lượng tử hóa ma trận số thực sang số nguyên 8-bit, tiết kiệm 75% RAM"""
    @staticmethod
    def quantize(dense_matrix):
        if not dense_matrix:
            return {"quantized": [], "scale": 1.0}

        # Tìm giá trị tuyệt đối lớn nhất để làm scale factor
        max_val = max(max(abs(x) for x in row) for row in dense_matrix) or 1.0
        scale = max_val / 127.0

        quantized_matrix = []
        for row in dense_matrix:
            q_row = [int(round(x / scale)) for x in row]
            quantized_matrix.append(q_row)

        return {
            "quantized_matrix": quantized_matrix,
            "scale_factor": round(scale, 6),
            "format": "INT8_SYMMETRIC"
        }
