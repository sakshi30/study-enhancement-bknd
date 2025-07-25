# 📚 AI-Powered Learning Resource Backend

A Flask-based backend for uploading, parsing, enriching, and indexing PDFs and web links with AI summaries and semantic search, using pdfplumber, Jina Reader, OpenAI, AWS, and Algolia MCP Server.

## Features

* **User Management:** Handles user registration/login and file management with AWS Cognito and S3.
* **PDF Upload & Parsing:** Extracts text from uploaded PDFs using pdfplumber.
* **Web Link Content Extraction:** Crawls and parses web pages/articles using Jina Reader.
* **AI Summarization:** Uses OpenAI (GPT models) to generate concise summaries, key points, and practice questions (returned as JSON).
* **Semantic Search:** Indexes assets and AI-enriched metadata to Algolia MCP Server for fast, smart search across all uploads.

## Tech Stack

| Component | Library/Service    |
|-----------|--------------------|
| Web Framework | Flask              |
| PDF Parsing | pdfplumber         |
| Web Extraction | Jina Reader        |
| Summarization (AI) | OpenAI (GPT)       |
| User/Auth/Storage | AWS RDS            |
| Search/Indexing | Algolia MCP Server |

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/sakshi30/study-enhancement-bknd.git
cd study-enhancement-bknd
```

### 2. Install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file with:

```env
OPENAI_API_KEY=
ALGOLIA_APPLICATION_KEY=
ALGOLIA_WRITE_API_KEY=
JINA_PARSER=
ALGOLIA_INDEX_NAME=
MYSQL_DBHOST=
MYSQL_PASSWORD=
MYSQL_USER=
MYSQL_DBNAME=
```

### 4. Start the server

```bash
flask run
```

## API Endpoints

| Endpoint | Method | Description                         |
|----------|--------|-------------------------------------|
| `/register` | POST | User registration (AWS RDS)         |
| `/login` | POST | User login (AWS RDS)                |
| `//upload-files` | POST | Upload and parse PDF file           |
| `/add-links` | POST | Submit a URL for crawling/extract   |

[//]: # (| `/resources` | GET | List/Search indexed resources &#40;MCP&#41; |)

## Example Workflow

1. **User registers and logs in**.
2. **Uploads a PDF** or **submits a web link**.
3. **Backend pipeline:**
   * PDF → parsed with pdfplumber; Link → extracted with Jina Reader.
   * Extracted text sent to OpenAI API for enrichment.
   * Summary, key points (all JSON) returned/stored.
   * Resource indexed (summary, metadata, download URL) in Algolia MCP Server.
4. **User can search, view, and download resources** with summaries and full metadata.

## Example JSON Output (from AI summarization)

```json
{
  "title": "Understanding Neural Networks",
  "type": "PDF",
  "source": "User Upload",
  "summary": "This document explains the principles of neural networks and their real-world applications...",
  "key_points": [
    "Neural networks mimic the structure of the brain.",
    "Layers of neurons are used for feature extraction and classification.",
    "Learning is achieved by adjusting weights during training."
  ]
}
```

## Requirements

* Python 3.8+
* Flask
* pdfplumber
* jina
* boto3
* openai
* requests
* python-dotenv (for `.env` management)
* Algolia MCP SDK or compatible client

## License

MIT

## Acknowledgments

* [pdfplumber](https://github.com/jsvine/pdfplumber)
* [Jina AI Reader](https://jina.ai/)
* [OpenAI GPT](https://openai.com/)
* [AWS Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
* [Algolia MCP Server](https://www.algolia.com/)

---

***PRs, issues, and feedback are welcome! 🚀***