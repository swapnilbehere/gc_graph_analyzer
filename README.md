# Chromatogram Analyzer

A modular, scalable, and maintainable application for analyzing GC chromatogram files, detecting peaks, and providing AI-powered diagnosis and troubleshooting using Retrieval-Augmented Generation (RAG).

---

## Features

- Upload and process GC chromatogram `.cdf` files
- Automatic peak detection and area calculation
- Summarize chromatogram data and export as JSON
- RAG-based diagnosis using reference chromatograms
- RAG-based troubleshooting using a knowledge base (PDF)
- Modular codebase for easy extension and testing

---

## Project Structure

```
gc_graph_analyzer/
├── app/
│   ├── __init__.py
│   ├── main.py                # Streamlit entry point
│   ├── config.py              # Configuration and constants
│   ├── chromatogram/
│   │   ├── __init__.py
│   │   ├── processing.py      # Chromatogram processing logic
│   │   └── utils.py           # Helper functions
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── chains.py          # RAG chain management
│   │   └── loaders.py         # Document loading
│   └── ui/
│       ├── __init__.py
│       └── components.py      # Streamlit UI components
├── data/
│   ├── cdf_files/             # Input chromatogram files
│   ├── temp_uploads/          # Temporary uploaded files
│   ├── json_output/           # Output JSON summaries
│   ├── txt_output/            # Reference chromatogram text files
│   └── knowledge_base/        # PDF troubleshooting guides
├── tests/                     # Unit and integration tests
├── .env                       # Environment variables
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/swapnilbehere/chromatogram-analyzer.git
cd chromatogram-analyzer
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your-openai-api-key
```

Add any other configuration as needed (see `app/config.py`).

### 5. Prepare Data Folders

Ensure the following folders exist (create them if missing):

- `data/cdf_files/`
- `data/temp_uploads/`
- `data/json_output/`
- `data/txt_output/`
- `data/knowledge_base/`

Add your chromatogram `.cdf` files, reference `.txt` files, and knowledge base `.pdf` files to the appropriate folders.

---

## Running the Application

### 1. Start the Streamlit App

```bash
streamlit run app/main.py
```

### 2. Using the App

- Upload a `.cdf` chromatogram file
- Enter metadata for the run
- View detected peaks, diagnosis, and troubleshooting advice

---

## Testing

To run unit tests (if implemented):

```bash
pytest tests/
```

---

## Notes

- Make sure your `.env` file is not committed to version control.
- For large files or production use, consider optimizing memory and storage settings.
- For GPU acceleration, install `faiss-gpu` instead of `faiss-cpu`.

---

## License

MIT License
