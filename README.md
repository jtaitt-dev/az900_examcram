# 🧪 AZ‑900 Exam Simulator — Pearson OnVUE‑Style (PyQt6)

A **100 % offline** Microsoft Azure Fundamentals (**AZ‑900**) exam simulator that mirrors the official Pearson OnVUE flow. Built with Python + PyQt6, it lets you drill under real‑world pressure without touching the internet.

---

## 🎯 Key Features

| ✔️ | Capability | Details |
|----|------------|---------|
| **54‑Question Bank** | All five exam domains, fully randomized every session |
| **True OnVUE UX** | Palette, flag button, timer, review flow, light/dark theme |
| **Explanations** | Post‑exam feedback screen shows correct answer *and* rationale |
| **Dark ↔ Light Toggle** | Press **Ctrl + D** anytime |
| **Flag for Review** | Press **F** or click the flag icon |
| **1‑Hour Timer** | Red flash below 5 minutes |
| **Scoring** | 0‑1000 scale, 700 to pass |
| **Verbose Logging** | Console logs exam lifecycle & answer saves |

---

## 🚀 Quick Start

```bash
# 1 . Clone
git clone https://github.com/<your‑user>/az900-exam-simulator.git
cd az900-exam-simulator

# 2 . (Optional) create venv
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3 . Install deps
pip install -r requirements.txt        # PyQt6‑based

# 4 . Launch
python main.py


⌨️ Shortcuts
Keys	Action
Ctrl + D	Toggle dark / light mode
← / →	Previous / next question
F	Flag / unflag question

📸 Screenshots
| Exam Screen │ Review Screen │ Results + Feedback |
|-------------|---------------|--------------------|
||||

(Add PNGs to screenshots/ or remove this section.)

📂 Project Layout
az900-exam-simulator/
├─ main.py             # Entry point
├─ requirements.txt    # PyQt6 pin
├─ README.md
└─ screenshots/        # Optional UI captures


📝 License
MIT — free for personal or commercial use. Pull requests welcome.

🙏 Credits
Questions & Domains — curated to reflect Microsoft’s AZ‑900 blueprint (no official material reproduced).

Icons — Programmatically drawn to avoid external assets, inspired by Microsoft Fluent UI.

UX — Heavily modeled on Pearson VUE’s OnVUE interface for muscle‑memory training.