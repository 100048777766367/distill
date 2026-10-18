import os
import sys
import json
import time
import hashlib
import urllib.request

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cortex_distill.compressor import KnowledgeCompressor
from cortex_distill.quantizer import Int8Quantizer
from cortex_distill.evaluator import ModelEvaluator
from adapters_forge.lora_adapter import LoRAAdapterForge

STATE_FILE = "synapses/state.json"
PEERS_FILE = "synapses/peers.json"
MANIFEST_FILE = "synapses/model_manifest.json"

class DistillKernel:
    def __init__(self):
        self.repo_name = os.environ.get("GITHUB_REPOSITORY", "100048777766367/distill")
        self.owner = os.environ.get("REPO_OWNER", "100048777766367")
        self.contract_repo = f"{self.owner}/contract"
        
        self.ensure_skeleton()
        self.epoch = self.load_epoch()
        self.links = self.load_links()

    def ensure_skeleton(self):
        for folder in ["cortex_distill", "adapters_forge", "dist", "organs", "synapses"]:
            os.makedirs(folder, exist_ok=True)

    def load_epoch(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f).get("generation_epoch", 0) + 1
            except Exception: pass
        return 1

    def load_links(self):
        if os.path.exists(PEERS_FILE):
            try:
                with open(PEERS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f).get("ecosystem_links", [])
            except Exception: pass
        return [f"{self.owner}/vault", f"{self.owner}/forge", f"{self.owner}/golem", self.contract_repo]

    def enforce_contract_apoptosis(self):
        """[t] Áp dụng luật Apoptosis của Contract: diệt tệp lỗi cú pháp trong organs/"""
        for root, _, files in os.walk("organs"):
            for f in files:
                if f.endswith(".py"):
                    fp = os.path.join(root, f)
                    try:
                        with open(fp, "r", encoding="utf-8") as cf:
                            compile(cf.read(), fp, "exec")
                    except SyntaxError as se:
                        print(f"🛑 [APOPTOSIS CONTRACT] '{f}' vi phạm hợp đồng ({se})! Tự xóa sổ.")
                        try: os.remove(fp)
                        except Exception: pass

    def harvest_vault_data(self):
        """Lấy dữ liệu tam thức sạch từ kho Vault"""
        vault_url = f"https://raw.githubusercontent.com/{self.owner}/vault/main/dist/bodhi_knowledge_graph.jsonl"
        triplets = []
        try:
            req = urllib.request.Request(vault_url, headers={"User-Agent": "Distill-Engine"})
            with urllib.request.urlopen(req, timeout=3.5) as r:
                if r.status == 200:
                    for line in r.read().decode("utf-8").splitlines():
                        if line.strip():
                            triplets.append(json.loads(line.strip()))
                    print(f"📥 [NGUYÊN LIỆU VAULT] Đã nạp thành công {len(triplets)} tam thức sạch!")
                    return triplets
        except Exception: pass

        # Mẫu mặc định nếu kho vault đang ở epoch đầu
        return [
            {"subject": "BodhiAI", "predicate": "distills", "object": "MicroNeuralWeights"},
            {"subject": "Distill", "predicate": "quantizes", "object": "Int8SymmetricTensor"},
            {"subject": "Golem", "predicate": "executes", "object": "DistilledKnowledge"}
        ]

    def run(self):
        print("=" * 80)
        print(f"🔮 [DISTILL MODEL FOUNDRY] KHỞI ĐỘNG XƯỞNG CHƯNG CẤT #{self.epoch}")
        print(f"🏛️ Mỏ Neo: {self.contract_repo} | Bản Thể: Chưng Cất Trí Tuệ & Lượng Tử Hóa INT8")
        print("=" * 80)

        # 0. Thực thi luật Apoptosis
        self.enforce_contract_apoptosis()

        # 1. Hút nguyên liệu sạch từ Vault
        triplets = self.harvest_vault_data()

        # 2. Phân xưởng 1: Nén tam thức thành ma trận vector cô đặc
        print(f"⚙️ [NÉN TRI THỨC] Đang nén {len(triplets)} tam thức thành ma trận vector...")
        dense_matrix = KnowledgeCompressor.compress_triplets_to_matrix(triplets, vector_dim=4)
        print(f"  └── 📊 Ma trận cô đặc gồm {len(dense_matrix)} hàng x 4 chiều.")

        # 3. Phân xưởng 2: Lượng tử hóa INT8 siêu tiết kiệm RAM
        print("🧊 [LƯỢNG TỬ HÓA INT8] Ép trọng số về số nguyên 8-bit...")
        quantized_pack = Int8Quantizer.quantize(dense_matrix)
        print(f"  └── 🎯 Hệ số co giãn (Scale Factor): {quantized_pack['scale_factor']}")

        # 4. Phân xưởng 3: Kiểm định độ nguyên vẹn tri thức
        eval_result = ModelEvaluator.evaluate(dense_matrix, quantized_pack)
        print(f"🛡️ [KIỂM ĐỊNH MÔ HÌNH]: Độ lưu giữ tri thức={eval_result['retention_ratio']*100:.2f}% | Chứng nhận={eval_result['is_certified']}")

        # 5. Phân xưởng 4: Đúc LoRA Adapter cắm-rút
        print("🧩 [ĐÚC LORA ADAPTER] Khởi tạo ma trận vi chỉnh Low-Rank...")
        lora_pack = LoRAAdapterForge.forge_lora(weights_dim=4, rank=2)

        # 6. Đóng gói xuất kho thành phẩm tại dist/
        model_payload = {
            "model_identity": f"bodhi_slm_epoch_{self.epoch}",
            "epoch": self.epoch,
            "quantized_weights": quantized_pack,
            "lora_adapter": lora_pack,
            "evaluation": eval_result
        }

        output_path = "dist/distilled_model.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(model_payload, f, indent=4)
        print(f"🎁 [KHO THÀNH PHẨM DIST]: Đã xuất kho mô hình hoàn chỉnh tại '{output_path}' ({os.path.getsize(output_path)} bytes)!")

        # 7. Cập nhật Manifest & Chứng thực Quantum CID
        t = int(time.time())
        seed = f"distill_{self.epoch}_{t}_{eval_result['retention_ratio']}".encode()
        cid = hashlib.shake_256(seed).hexdigest(64)

        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "generation_epoch": self.epoch,
                "last_t": t,
                "models_distilled_count": len(dense_matrix),
                "quantum_cid": cid,
                "status": "model_ready_for_golem_and_huggingface"
            }, f, indent=4)

        fwd_packet = {
            "contract": "bodhi.contract.v1",
            "identity": self.repo_name,
            "role": "MODEL_DISTILLATION_FOUNDRY",
            "epoch": self.epoch,
            "timestamp": t,
            "model_metadata": {
                "file": output_path,
                "retention": eval_result["retention_ratio"],
                "format": "INT8"
            },
            "quantum_cid": cid,
            "status": "weights_ready_for_edge_inference"
        }
        with open("synapse_forward.json", "w", encoding="utf-8") as f:
            json.dump(fwd_packet, f, indent=4)

        print("=" * 80)
        print(f"💾 [CHỨNG THỰC CID MÔ HÌNH]: {cid[:24]}...")
        print("✨ [XUẤT XƯỞNG VIÊN MÃN] Mô hình nơ-ron siêu nhẹ đã sẵn sàng nạp cho Golem và bán trên Hugging Face!")
        print("=" * 80)

if __name__ == "__main__":
    DistillKernel().run()
