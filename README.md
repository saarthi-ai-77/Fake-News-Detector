# Fake News Detection System

A hybrid Fake News Detection system that combines Deep Learning (LSTM) with Google Search Verification to accuracy assess news credibility.

## 🚀 Features
- **Hybrid Analysis**: Uses LSTM model (70% weight) + Google Verification (30% weight).
- **Deep Learning**: Pre-trained LSTM model using TensorFlow/Keras.
- **Fact-Checking**: Verification against trusted domains via Google Custom Search API.
- **Dual Input**: Analyze raw text or automatically extract content from URLs.
- **Modern UI**: React-based frontend for easy interaction.

## 🛠️ Tech Stack
- **Backend**: Python, FastAPI, TensorFlow, BeautifulSoup
- **Frontend**: React, Vite, TailwindCSS
- **Search**: Google Custom Search JSON API

## 📋 Prerequisites
- **Python** 3.9 or higher
- **Node.js** 16+ & **npm**
- **Google API Key**: For Custom Search JSON API.
- **Google Search Engine ID (CX)**: Created in Google Programmable Search Engine.

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/saarthi-ai-77/FND-LSTM.git
cd FND-LSTM
```

### 2. Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Secrets**:
   Create a file named `credentials.txt` in the `backend/` directory.
   **IMPORTANT**: This file is git-ignored. Do NOT commit it.
   
   Add your keys in the following format:
   ```text
   GOOGLE_API_KEY=your_actual_api_key_here
   GOOGLE_CSE_ID=your_search_engine_id_here
   ```

### 3. Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

---

## ▶️ Running the Application

### Start the Backend
Open a terminal in the root folder:
```bash
# Windows
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# Mac/Linux
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
*Backend runs on: http://localhost:8000*

### Start the Frontend
Open a **new** terminal:
```bash
cd frontend
npm run dev
```
*Frontend runs on: http://localhost:8080 (or port shown in terminal)*

---

## 🧪 Usage
1. Open the frontend URL in your browser.
2. **Text Tab**: Paste a news snippet. The system will predict its credibility and check for keywords on trusted sites (BBC, Reuters, etc.).
3. **URL Tab**: Paste a link to a news article. The system scrapes the text and performs the same analysis.

---

## 🧹 Project Structure
```
FND-LSTM/
├── backend/
│   ├── main.py           # FastAPI entry point
│   ├── model.py          # LSTM model handler
│   ├── verify.py         # Google Search verification logic
│   ├── utils.py          # URL text extraction
│   ├── credentials.txt   # API Keys (Ignored)
│   ├── fake_lstm_saved.keras # Pre-trained Model
│   └── requirements.txt
├── frontend/             # React Application
├── .gitignore            # Git configuration
└── README.md             # This file
```

## 🔒 Security Note
The `backend/credentials.txt` file is added to `.gitignore` to prevent your API keys from being pushed to GitHub. Always keep your keys secret.
