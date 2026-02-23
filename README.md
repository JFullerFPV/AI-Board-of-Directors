# AI Board of Directors (CLI)

A Python-based command-line interface (CLI) application that simulates a corporate Board of Directors to critically evaluate your product ideas and pitches.

By leveraging a hybrid AI architecture, the script delegates specific analytical tasks to specialized local models (saving costs and keeping data local) while offloading the final synthesis and decision-making to a highly capable cloud model.

---

## ✨ Features

- **Hybrid AI Processing:** Uses local models via LM Studio for specialized "Officers" (CTO, CFO, CMO, General Opinion) and OpenAI's `gpt-4o-mini` for the "CEO" synthesis.
- **Real-Time Streaming:** The CEO's final executive summary streams directly into your terminal in real-time.
- **Interactive CLI:** Pitch new ideas directly from the command prompt.
- **Session Loading:** Skip the local inference wait times by loading a previously saved session to test the CEO's output directly.
- **Markdown Export:** Automatically saves the entire board meeting (original idea, officer reports, and CEO summary) to a timestamped Markdown file.
- **Dry Run Mode:** Includes a built-in dry run functionality (`--dry-run`) to test the application's logic and token routing without making any actual API calls or waiting for model inference.

---

## 🧰 Tech Stack

- **Language:** Python 3.10+
- **Local AI API:** OpenAI Python SDK (pointed to `localhost:1234`)
- **Cloud AI API:** OpenAI Python SDK

---

## 🚀 Getting Started

### Prerequisites

1. **Python 3.10+** installed on your machine.
2. **LM Studio** installed and running locally.
3. An active **OpenAI API Key**.

---

### Installation

1. Clone the repository:

```bash
git clone https://github.com/JFullerFPV/AI-Board-of-Directors.git
cd AI-Board-of-Directors
```

2. Install the required Python dependencies:

```bash
pip install openai
```

3. Set your OpenAI API key as an environment variable:

- **Mac/Linux:**
```bash
export OPENAI_API_KEY="your_api_key_here"
```

- **Windows:**
```bash
set OPENAI_API_KEY="your_api_key_here"
```

---

## 🖥 Local Server Setup

1. Open LM Studio.
2. Load your preferred local model(s) into memory.
3. Start the Local Server (ensure it is running on the default port: `http://localhost:1234/v1`).

---

## ▶ Usage

Run the script directly from your terminal:

```bash
python openai_hybrid_board.py
```

### Workflow

1. Select whether you want to **Pitch a new idea** or **Evaluate a previous session**.
2. If pitching a new idea, type your business pitch into the prompt.
3. Watch as the local officers evaluate the idea.
4. The CEO then streams the final executive summary in real-time.
5. The script automatically exports the complete meeting to a `.md` file in the same directory.

---

### 🧪 Dry Run Testing

To test the script without hitting the APIs, run the application with the dry run flag:

```bash
python openai_hybrid_board.py --dry-run
```

This allows you to verify application logic and token routing without waiting for model inference or incurring API costs.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

If you want to add new "Officers" to the board, simply update the `OFFICERS` dictionary in the script with a new role and system prompt.

---

## 📝 License

This project is open-source and available under the MIT License.
