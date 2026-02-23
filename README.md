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
## Example Output:

Input Prompt: The pizza compass. It is a compass that points to the nearest pizza restraunt.

## Executive Summary: The Pizza Compass Proposal

The Pizza Compass is a unique concept designed to point users to the nearest pizza restaurants, combining modern technology with a playful, nostalgic appeal. The idea has garnered interest from our Board of Directors, with both opportunities and challenges identified in the evaluations.

## Combined Feedback from the Board

**Technology Feasibility:**
The technology behind the Pizza Compass is technically feasible, but it presents several critical challenges:
- **Hardware:** GPS accuracy in urban environments may be compromised, requiring hybrid positioning solutions (Wi-Fi, BLE) that add complexity. Power management is crucial to ensure usability without frequent recharging.
- **Software:** A robust software architecture is needed to handle real-time data processing and geofencing. The integration of a global database for pizza restaurants poses a significant development challenge.

**Financial Viability:**
The financial analysis indicates a strong market opportunity for both B2C and B2B segments. Potential revenue streams include hardware sales, subscription models, partnerships with pizza chains, and data monetization. Initial investment estimates range from $300K to $900K, with projected revenues potentially reaching $40M by Year 3.

**Marketing Strategy:**
The marketing plan emphasizes a playful, gamified experience, targeting pizza lovers and tech enthusiasts. A phased go-to-market strategy involves leveraging influencer partnerships, crowdfunding, and localized promotions to create buzz. Potential user engagement through social media and community challenges could drive adoption.

**General Considerations:**
While the idea is whimsical and engaging, concerns about practicality, market saturation, and privacy must be addressed. The product needs to offer tangible benefits beyond novelty to ensure user retention and satisfaction.

### Go/No-Go Decision: Go

**Final Decision:** The Pizza Compass will proceed to the prototype phase. The combination of technological feasibility, potential market demand, and strong financial projections support the decision to move forward, albeit with caution regarding the highlighted risks.

### Immediate Next Steps

1. **Prototype Development:**
   - Initiate a prototype using a Raspberry Pi or ESP32 with GPS capabilities to test hardware feasibility and user experience.
   - Focus on developing the positioning algorithm and battery management solutions.

2. **Partnership Outreach:**
   - Begin discussions with potential partners in the pizza industry, including local pizzerias and larger chains like Domino's and Pizza Hut, to establish initial collaborations.

3. **Market Research:**
   - Conduct surveys and focus groups with target demographics to validate features and identify additional user needs.
   - Explore potential crowdfunding platforms and prepare a campaign strategy to gauge market interest.

4. **Software Development Planning:**
   - Assemble a dedicated team for software architecture, focusing on building a robust backend that supports real-time updates and geospatial queries.
   - Outline the requirements for the mobile app, considering user permissions and ease of use.

5. **Marketing Strategy Refinement:**
   - Develop a comprehensive marketing plan, including potential viral campaigns, influencer partnerships, and community engagement strategies.
   - Create branding materials to establish a visual identity and messaging framework before the official launch.

By following these steps, we aim to optimize the Pizza Compass concept for market entry and ensure its success in a competitive landscape.

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
