import hashlib

class KnowledgeCompressor:
    """Nén các bộ ba tam thức trừu tượng thành ma trận trọng số cô đặc"""
    @staticmethod
    def compress_triplets_to_matrix(triplets, vector_dim=4):
        dense_matrix = []
        
        for item in triplets:
            subj = str(item.get("subject", ""))
            pred = str(item.get("predicate", ""))
            obj = str(item.get("object", ""))
            
            # Băm bọt biển SHAKE-256 nén chuỗi quan hệ thành vector chuẩn hóa [-1.0, 1.0]
            row = []
            for d in range(vector_dim):
                seed = f"{subj}_{pred}_{obj}_{d}".encode()
                val = (int(hashlib.shake_256(seed).hexdigest(4), 16) / 32767.5) - 1.0
                row.append(round(val, 4))
            dense_matrix.append(row)

        return dense_matrix
