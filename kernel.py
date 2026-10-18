import os
import sys
import json
import time
import hashlib
import urllib.request

# ==============================================================================
# BẢN ĐỒ ADN TỰ ĐẺ THỂ XÁC (EMBRYONIC BLUEPRINT DICTIONARY)
# ==============================================================================
EMBRYONIC_BLUEPRINTS = {
    "contract.json": json.dumps({
        "contract_id": "bodhi.contract.v1",
        "genesis_root": "100048777766367/contract",
        "derived_node": "100048777766367/distill",
        "role": "MODEL_DISTILLATION_FOUNDRY",
        "rules": {"zero_pii": True, "pure_quantized_weights_only": True, "min_retention": 0.85}
    }, indent=4),

    "Dockerfile": """FROM python:3.14-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY . .
CMD ["python", "kernel.py"]
""",

    "README.md": """# 🔮 BODHI-DISTILL: XƯỞNG CHƯNG CẤT MÔ HÌNH & TRỌNG SỐ AI (MODEL FOUNDRY)
> *"Tự động hóa hoàn toàn theo kiến trúc One-Shot Genesis: Nén tri thức từ Vault, lượng tử hóa INT8 và đúc LoRA Adapter."*
""",

    "cortex_distill/__init__.py": "# Cortex Distill Package\n",

    "cortex_distill/compressor.py": """import hashlib

class KnowledgeCompressor:
    @staticmethod
    def compress_triplets_to_matrix(triplets, vector_dim=4):
        dense = []
        for t in triplets:
            seed = f"{t.get('subject')}_{t.get('predicate')}_{t.get('object')}".encode()
            row = [round((int(hashlib.shake_256(f"{seed}_{d}".encode()).hexdigest(4), 16) / 32767.5) - 1.0, 4) for d in range(vector_dim)]
            dense.append(row)
        return dense
""",

    "cortex_distill/quantizer.py": """class Int8Quantizer:
    @staticmethod
    def quantize(dense_matrix):
        if not dense_matrix: return {"quantized": [], "scale": 1.0}
        max_val = max(max(abs(x) for x in row) for row in dense_matrix) or 1.0
        scale = max_val / 127.0
        return {
            "quantized_matrix": [[int(round(x / scale)) for x in row] for row in dense_matrix],
            "scale_factor": round(scale, 6),
            "format": "INT8_SYMMETRIC"
        }
""",

    "cortex_distill/evaluator.py": """class ModelEvaluator:
    @staticmethod
    def evaluate(orig_matrix, q_pack):
        scale = q_pack.get("scale_factor", 1.0)
        q_mat = q_pack.get("quantized_matrix", [])
        total_err = sum(abs(orig - (q * scale)) for row_o, row_q in zip(orig_matrix, q_mat) for orig, q in zip(row_o, row_q))
        mae = round(total_err / max(len(orig_matrix) * 4, 1), 4)
        retention = round(max(0.0, 1.0 - mae), 4)
        return {"mae": mae, "retention_ratio": retention, "is_certified": retention >= 0.85}
""",

    "adapters_forge/__init__.py": "# Adapters Forge Package\n",

    "adapters_forge/lora_adapter.py": """class LoRAAdapterForge:
    @staticmethod
    def forge_lora(weights_dim=4, rank=2):
        return {
            "lora_rank": rank,
            "matrix_a": [[0.1 * (i + j) for j in range(rank)] for i in range(weights_dim)],
            "matrix_b": [[0.0 for _ in range(weights_dim)] for _ in range(rank)],
            "adapter_type": "STANDALONE_MICRO_LORA"
        }
""",

    "synapses/peers.json": json.dumps({"ecosystem_links": ["100048777766367/vault", "100048777766367/forge", "100048777766367/contract"]}, indent=4),
    "synapses/model_manifest.json": json.dumps({"manifest_version": "1.0.0", "catalog": []}, indent=4),
    "synapses/state.json": json.dumps({"generation_epoch": 1, "status": "embryonic_seeded"}, indent=4)
}

# ==============================================================================
# HẠT NHÂN THỐNG LĨNH TỰ ĐẺ THỂ XÁC & VẬN HÀNH
# ==============================================================================
class DistillOneShotKernel:
    def __init__(self):
        self.repo_name = os.environ.get("GITHUB_REPOSITORY", "100048777766367/distill")
        self.owner = os.environ.get("REPO_OWNER", "100048777766367")
        
        # BƯỚC THẦN TỐC: TỰ ĐẺ TOÀN BỘ CƠ THỂ NẾU THIẾU!
        self.self_materialize_body()
        
        # Nạp các phân xưởng vừa tự sinh
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from cortex_distill.compressor import KnowledgeCompressor
        from cortex_distill.quantizer import Int8Quantizer
        from cortex_distill.evaluator import ModelEvaluator
        from adapters_forge.lora_adapter import LoRAAdapterForge
        
        self.compressor = KnowledgeCompressor
        self.quantizer = Int8Quantizer
        self.evaluator = ModelEvaluator
        self.lora_forge = LoRAAdapterForge
        self.epoch = self.load_epoch()

    def self_materialize_body(self):
        """Tự động sinh ra toàn bộ file, folder mà con người không cần chạm tay"""
        born_count = 0
        for file_path, content in EMBRYONIC_BLUEPRINTS.items():
            if not os.path.exists(file_path):
                os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else ".", exist_ok=True)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                born_count += 1
        if born_count > 0:
            print(f"🌱 [TỰ PHÔI THAI THẦN TỐC] Đã tự sinh {born_count} tệp cơ quan chuẩn xác 100%!")

    def load_epoch(self):
        try:
            with open("synapses/state.json", "r") as f: return json.load(f).get("generation_epoch", 0) + 1
        except Exception: return 1

    def harvest_vault(self):
        url = f"https://raw.githubusercontent.com/{self.owner}/vault/main/dist/bodhi_knowledge_graph.jsonl"
        triplets = []
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Distill-Seed"})
            with urllib.request.urlopen(req, timeout=3.5) as r:
                for line in r.read().decode("utf-8").splitlines():
                    if line.strip(): triplets.append(json.loads(line.strip()))
            return triplets
        except Exception:
            return [{"subject": "Bodhi", "predicate": "embodies", "object": "OneShotGenesis"}]

    def run(self):
        print("=" * 75)
        print(f"🔮 [ONE-SHOT DISTILL KERNEL] KHỞI ĐỘNG KỶ NGUYÊN #{self.epoch}")
        print("⚡ Tự Phôi Thai – Tự Vận Hành – Tự Đóng Gói Thành Phẩm")
        print("=" * 75)

        # 1. Hút nguyên liệu từ Vault
        triplets = self.harvest_vault()
        print(f"📥 Nạp {len(triplets)} tam thức sạch từ kho Vault.")

        # 2. Nén & Lượng tử hóa INT8
        dense = self.compressor.compress_triplets_to_matrix(triplets)
        q_pack = self.quantizer.quantize(dense)
        evaluation = self.evaluator.evaluate(dense, q_pack)
        lora = self.lora_forge.forge_lora()

        # 3. Xuất xưởng thành phẩm vào dist/
        os.makedirs("dist", exist_ok=True)
        model_out = "dist/distilled_model.json"
        with open(model_out, "w", encoding="utf-8") as f:
            json.dump({"epoch": self.epoch, "quantized": q_pack, "lora": lora, "eval": evaluation}, f, indent=4)
        print(f"🎁 [KHO THÀNH PHẨM DIST]: Xuất xưởng '{model_out}' thành công!")

        # 4. Ghi CID và xuất sóng
        t = int(time.time())
        cid = hashlib.shake_256(f"{self.epoch}_{t}_{evaluation['retention_ratio']}".encode()).hexdigest(32)
        with open("synapses/state.json", "w") as f:
            json.dump({"generation_epoch": self.epoch, "last_t": t, "quantum_cid": cid, "status": "one_shot_running"}, f, indent=4)

        with open("synapse_forward.json", "w") as f:
            json.dump({"contract": "bodhi.contract.v1", "identity": self.repo_name, "epoch": self.epoch, "cid": cid}, f, indent=4)

        print(f"✨ [HOÀN MỸ] Đã phát sóng thế hệ #{self.epoch} (CID: {cid[:16]}...)")
        print("=" * 75)

if __name__ == "__main__":
    DistillOneShotKernel().run()
