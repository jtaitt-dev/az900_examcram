# 🧪 AZ-900 Exam Simulator — OnVUE Style (PyQt6)

This is a fully offline, self-contained **Microsoft Azure Fundamentals (AZ-900)** exam simulator that replicates the official **OnVUE** exam experience. Built with Python and PyQt6, it's perfect for prepping under real-world test conditions.

---

## 🎯 Features

- ✅ **Full 50-Question AZ-900 Bank**  
  Questions are randomized each session, grouped by exam domain.

- 💻 **OnVUE-Inspired UI/UX**  
  Replicates the layout, flow, and pressure of the real Pearson exam.

- 🌗 **Dark/Light Mode Toggle**  
  Switch seamlessly using `Ctrl + D`.

- 🏁 **Flag Questions for Review**  
  Mark questions to revisit before submitting.

- ⏱️ **Countdown Timer**  
  60-minute exam timer with red flashing warning in the last 5 minutes.

- 📊 **Scoring System**  
  Final score out of **1000**, with **700** as the pass threshold.

- 🔁 **Review + Edit Answers Before Submission**  
  Review all questions and answers before grading.

- 📦 **Self-Contained Resources**  
  Base64-encoded Fluent UI icons – no internet or image assets required.

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/az900-exam-simulator.git
cd az900-exam-simulator


🧠 Keyboard Shortcuts

| Shortcut   | Action                 |
| ---------- | ---------------------- |
| `Ctrl + D` | Toggle Dark/Light Mode |
| `← / →`    | Navigate Questions     |
| `F`        | Flag/Unflag Question   |

📷 Screenshots

| Exam Screen                   | Review Screen                     | Results Screen                      |
| ----------------------------- | --------------------------------- | ----------------------------------- |
| ![exam](screenshots/exam.png) | ![review](screenshots/review.png) | ![results](screenshots/results.png) |

(Make sure to add screenshots in a screenshots/ folder.)

📁 Folder Structure

az900-exam-simulator/
│
├── main.py                # Entry point
├── README.md              # This file
├── screenshots/           # UI images (optional)
└── .venv/                 # Virtual env (optional)

📜 License
MIT License.
Feel free to fork, modify, or use in your own certification prep tools.

💡 Credit
Questions adapted to reflect Microsoft’s AZ-900 exam domains.

Icons: Fluent UI System Icons

Simulator inspired by the real Pearson OnVUE interface.



