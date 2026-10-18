import math

class ModelEvaluator:
    """Đo lường độ thất thoát tri thức sau khi lượng tử hóa"""
    @staticmethod
    def evaluate(original_matrix, quantized_pack):
        scale = quantized_pack.get("scale_factor", 1.0)
        q_matrix = quantized_pack.get("quantized_matrix", [])
        
        total_error = 0.0
        count = 0

        for orig_row, q_row in zip(original_matrix, q_matrix):
            for orig, q in zip(orig_row, q_row):
                dequantized = q * scale
                total_error += abs(orig - dequantized)
                count += 1

        mean_abs_error = round(total_error / max(count, 1), 4)
        retention_ratio = round(max(0.0, 1.0 - mean_abs_error), 4)

        return {
            "mean_absolute_error": mean_abs_error,
            "retention_ratio": retention_ratio,
            "is_certified": retention_ratio >= 0.85
        }
