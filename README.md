# AI Data Analysis Chatbot

A Python chatbot built on the Google Gemini API, developed incrementally with a focus on persistent memory, structured responses, and conversation management.

Built as a learning project while transitioning into data engineering/data analysis — this repo tracks the chatbot's development commit by commit, from a basic API call to a chatbot with automatic, persistent memory.

## Features

- **Gemini-powered chat** — conversational responses via the Google Gemini API
- **Commands** — built-in commands for controlling the chatbot's behavior
- **Conversation saving** — chat sessions are saved locally for later reference
- **Persistent memory** — the chatbot remembers facts about the user across sessions (e.g. name, goals, ongoing projects)
- **Automatic memory detection** — the chatbot decides on its own when something is worth remembering, without needing an explicit "remember this" command
- **Structured model responses** — uses structured JSON output from the model rather than parsing free-form text

## Project structure

```
AI_DataAnalysis_Chatbot/
│
├── chatbot.py          # Main chatbot application
├── memory_test.py       # Standalone script for testing memory behavior
├── requirements.txt     # Python dependencies
├── .gitignore
└── README.md
```

Note: `.env`, `venv/`, `memory.txt`, and `conversations/` are intentionally excluded from this repo (see `.gitignore`) — they hold your local API key and personal chat data and should never be committed.

## Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/30JT004/AI_DataAnalysis_Chatbot.git
   cd AI_DataAnalysis_Chatbot
   ```

2. **Create and activate a virtual environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your Gemini API key**

   Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

5. **Run the chatbot**
   ```bash
   python chatbot.py
   ```

## Development history

This project was built feature by feature, with each step tracked as its own commit rather than pushed as one finished file. Run:
```bash
git log --oneline
```
to see the full build order — from the initial Gemini API call through commands, conversation saving, persistent memory, and automatic memory detection.

## Roadmap

- [ ] Data-analysis features
- [ ] (add more as you go)

## Author

Built by [30JT004](https://github.com/30JT004)
