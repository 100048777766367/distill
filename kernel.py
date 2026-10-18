import os
import sys
import json
import time
import hashlib
import importlib
import inspect
import subprocess

PEERS_FILE = "synapses/peers.json"
TOMBSTONES_FILE = "synapses/tombstones.json"
STATE_FILE = "synapses/state.json"
CONTRACT_FILE = "contract.json"

class ContractKernel:
    def __init__(self):
        self.repo_name = os.environ.get("GITHUB_REPOSITORY", "100048777766367/contract")
        self.owner = os.environ.get("REPO_OWNER", "100048777766367")
        self.ensure_skeleton()
        self.contract = self.load_contract()
        self.peers = self.load_json(PEERS_FILE, default={"living_peers": [
            f"{self.owner}/neuron", f"{self.owner}/nexus-08", f"{self.owner}/nexus-07",
            f"{self.owner}/seed", f"{self.owner}/monad", f"{self.owner}/shunya",
            f"{self.owner}/retina", f"{self.owner}/motor"
        ]}).get("living_peers", [])
        self.tombstones = self.load_json(TOMBSTONES_FILE, default={"tombstones": []}).get("tombstones", [])
        self.epoch = self.load_epoch()

    def ensure_skeleton(self):
        for folder in ["organs", "synapses", "synapses/harvested_memory"]:
            os.makedirs(folder, exist_ok=True)

    def load_contract(self):
        if os.path.exists(CONTRACT_FILE):
            try:
                with open(CONTRACT_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception: pass
        return {"contract_id": "bodhi.contract.v1"}

    def load_json(self, path, default):
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception: pass
        return default

    def load_epoch(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f).get("generation_epoch", 0) + 1
            except Exception: pass
        return 1

    # =========================================================================
    # 1. GIẢI QUYẾT [m] & [n]: LIÊN KẾT VĨNH CỬU DÙ SỐNG HAY ĐÃ CHẾT 404
    # =========================================================================
    def audit_peers_and_tombstones(self):
        """Rà soát danh bạ: Nút sống giữ nguyên [m], nút 404 biến thành Bia Mộ [n]"""
        print("🔍 [KIỂM ĐỊNH MẠNG LƯỚI] Rà soát liên kết vĩnh cửu [m] dù sống hay chết [n]...")
        still_alive = []
        new_tombstones = 0

        for peer in self.peers:
            if peer == self.repo_name: continue
            url = f"https://raw.githubusercontent.com/{peer}/main/synapse_forward.json"
            res = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url], capture_output=True, text=True)
            status = res.stdout.strip()

            if status == "404":
                # Nút đã chết -> Đưa vào sổ bia mộ [n], không bao giờ bị lãng quên
                if not any(t.get("identity") == peer for t in self.tombstones):
                    tombstone_entry = {
                        "identity": peer,
                        "declared_dead_epoch": self.epoch,
                        "timestamp": int(time.time()),
                        "status": "ETERNAL_TOMBSTONE_HERITAGE"
                    }
                    self.tombstones.append(tombstone_entry)
                    new_tombstones += 1
                    print(f"🕯️ [KHẮC BIA MỘ n] Nút '{peer}' bị 404! Đã lưu vết vĩnh cửu vào sổ Bia Mộ.")
            else:
                still_alive.append(peer)

        self.peers = list(dict.fromkeys(still_alive))
        with open(PEERS_FILE, "w", encoding="utf-8") as f:
            json.dump({"living_peers": self.peers}, f, indent=4)
        with open(TOMBSTONES_FILE, "w", encoding="utf-8") as f:
            json.dump({"tombstones": self.tombstones}, f, indent=4)

        print(f"📡 [LIÊN KẾT TOÀN MẠNG]: {len(self.peers)} nút đang sống [m] | {len(self.tombstones)} bia mộ di sản [n]")

    # =========================================================================
    # 2. GIẢI QUYẾT [t] -> [q]: APOPTOSIS (TỰ DIỆT CƠ CHẾ LỖI ĐỂ HOÀN NGUYÊN GỐC)
    # =========================================================================
    def enforce_apoptosis_and_load_organs(self):
        """Kiểm định phụ lục [r]: Tệp lỗi cú pháp bị xóa ngay lập tức để quy hồi [q]"""
        valid_organs = []
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))

        for root, _, files in os.walk("organs"):
            for file in sorted(files):
                if file.endswith(".py") and not file.startswith("__"):
                    file_path = os.path.join(root, file)
                    rel_dir = os.path.relpath(root, os.path.dirname(os.path.abspath(__file__)))
                    mod_name = f"{rel_dir.replace(os.path.sep, '.')}.{file[:-3]}"

                    # KIỂM ĐỊNH CÚ PHÁP TRƯỚC KHI CHẠY (Chống '{' was never closed, unexpected indent)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            compile(f.read(), file_path, "exec")
                    except SyntaxError as se:
                        print(f"🛑 [APOPTOSIS: LỖI CÚ PHÁP] Tệp '{file}' bị đứt gãy ({se})!")
                        print(f"🗑️ [QUY HỒI VỀ q] Tự động xóa sổ tệp lỗi '{file}' để bảo toàn hợp đồng!")
                        try: os.remove(file_path)
                        except Exception: pass
                        continue

                    # NẠP MODULE HỢP LỆ
                    try:
                        mod = importlib.import_module(mod_name)
                        importlib.reload(mod)
                        for _, obj in inspect.getmembers(mod, inspect.isclass):
                            if hasattr(obj, "execute"):
                                valid_organs.append(obj())
                                print(f"🔌 [PHỤ LỤC r HỢP LỆ]: Nạp cơ chế '{file}'")
                    except Exception as e:
                        print(f"⚠️ [LỖI NẠP {file}]: {e} (Tạm bỏ qua, giữ vững hạt nhân q)")

        return valid_organs

    # =========================================================================
    # 3. VẬN HÀNH VÒNG ĐỜI HỢP ĐỒNG
    # =========================================================================
    def run(self):
        print("=" * 70)
        print(f"📜 [CONTRACT ROOT KERNEL q] KHỞI ĐỘNG THẾ HỆ #{self.epoch}")
        print(f"🏛️ Bản Thể: {self.repo_name} | Hiến Ước Bất Biến 1+N")
        print("=" * 70)

        # Bước 1: Rà soát liên kết sống/chết
        self.audit_peers_and_tombstones()

        # Bước 2: Kiểm định hợp đồng & tiêu diệt mắt xích lỗi
        organs = self.enforce_apoptosis_and_load_organs()

        # Bước 3: Chạy các mắt xích hợp lệ (nếu có)
        context = {
            "epoch": self.epoch,
            "peers": self.peers,
            "tombstones": self.tombstones,
            "decision": 0.5
        }
        for organ in organs:
            try:
                organ.execute(context)
            except Exception as e:
                print(f"🚨 [CÔ LẬP PHỤ LỤC]: {e}")

        # Bước 4: Đóng gói và phát sóng chứng thực hợp đồng
        t = int(time.time())
        prev_cid = "GENESIS_ROOT_CONTRACT_CID"
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r") as f: prev_cid = json.load(f).get("quantum_cid", "GENESIS")
            except Exception: pass

        decision = context.get("decision", 0.5)
        new_cid = hashlib.shake_256(f"{prev_cid}_{self.epoch}_{t}_{decision}".encode()).hexdigest(64)

        packet = {
            "contract": "bodhi.contract.v1",
            "identity": self.repo_name,
            "epoch": self.epoch,
            "timestamp": t,
            "decision": decision,
            "quantum_cid": new_cid,
            "status": "in_strict_compliance_with_contract_q"
        }

        with open("synapse_forward.json", "w", encoding="utf-8") as f:
            json.dump(packet, f, indent=4)

        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({"generation_epoch": self.epoch, "last_t": t, "quantum_cid": new_cid, "status": "contract_pure"}, f, indent=4)

        print(f"💾 [CHỨNG THỰC CID]: {new_cid[:24]}...")
        print("✨ [HỢP ĐỒNG HOÀN MỸ] Trạng thái thanh tịnh [q] được bảo tồn tuyệt đối!")
        print("=" * 70)

if __name__ == "__main__":
    ContractKernel().run()
