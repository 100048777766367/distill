class LoRAAdapterForge:
    """Đúc ma trận phân rã rank thấp A x B (Low-Rank Adaptation)"""
    @staticmethod
    def forge_lora(weights_dim=4, rank=2):
        # Ma trận A (Gaussian init mô phỏng) và B (Zero init)
        matrix_a = [[0.1 * (i + j) for j in range(rank)] for i in range(weights_dim)]
        matrix_b = [[0.0 for j in range(weights_dim)] for i in range(rank)]
        
        return {
            "lora_rank": rank,
            "matrix_a": matrix_a,
            "matrix_b": matrix_b,
            "alpha": 1.0,
            "adapter_type": "STANDALONE_MICRO_LORA"
        }
