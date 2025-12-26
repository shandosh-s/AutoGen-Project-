# AI for Product Managers

**An Agentic AI Platform for Product Management Intelligence**

Built with Microsoft AutoGen multi-agent architecture.

## 🚀 Features

### Multi-Agent System
- **Agent 1: Trend Discovery** - Collects content from Google Trends, Reddit, YouTube, Quora, and PM forums
- **Agent 2: Content Generation** - Generates 2000-3000 word articles with insights and comparisons
- **Agent 3: SEO & Plagiarism** - 30+ SEO checks, quality analysis, and mandatory plagiarism detection

### Key Capabilities
- ✅ Multi-source content discovery
- ✅ Keyword extraction and clustering
- ✅ Organization size comparisons (Enterprise/Mid-Size/Startup)
- ✅ Comprehensive SEO analysis (30+ checks)
- ✅ Content quality scoring
- ✅ **Mandatory plagiarism detection** (80% originality threshold)
- ✅ PDF export (blocked until originality passes)

## 📦 Installation

### Prerequisites
- Python 3.9+
- pip

### Setup

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

## 🔧 Project Structure

```
ai_for_product_managers/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── config.py                       # Configuration settings
├── agents/
│   ├── __init__.py                 # Agent exports
│   ├── trend_discovery_agent.py    # Agent 1: Source collection
│   ├── content_generation_agent.py # Agent 2: Article generation
│   └── seo_plagiarism_agent.py     # Agent 3: SEO & plagiarism
├── utils/
│   ├── __init__.py
│   ├── dummy_data.py               # Sample data for testing
│   └── pdf_export.py               # PDF generation module
└── exports/                        # Generated PDF output directory
```

## 🛡️ Plagiarism Enforcement

The platform enforces strict originality requirements:

- **Threshold**: 95% originality required
- **Methods**: N-gram similarity, TF-IDF cosine similarity, sentence-level duplication
- **Gate**: PDF export is **BLOCKED** until content passes plagiarism check
- **Auto-flagging**: Similar sections are highlighted for rewriting

## 📊 SEO Checks (30+)

1. Word count optimization (2000-3000 words)
2. Keyword density (1-3%)
3. Keyword in title
4. Keyword in introduction
5. Heading structure (H1, H2 hierarchy)
6. Keyword in headings
7. Meta title length (50-60 chars)
8. Meta description (150-160 chars)
9. URL slug optimization
10. Internal linking
11. External linking
12. Image alt text optimization
13. Paragraph length
14. Sentence length
15. Flesch readability score
16. Content freshness signals
17. LSI keywords coverage
18. Question-based content
19. Bullet list usage
20. Numbered list usage
21. Bold/emphasis usage
22. Content depth
23. Topic coverage
24. Call-to-action presence
25. Mobile friendliness
26. Featured snippet readiness
27. FAQ schema readiness
28. Semantic structure
29. Vocabulary diversity
30. SERP competitiveness

## 🔌 API Configuration (Optional)

For real API integrations, set these environment variables:

```bash
# Reddit API
export REDDIT_CLIENT_ID=your_client_id
export REDDIT_CLIENT_SECRET=your_client_secret
export REDDIT_USER_AGENT=AI4PM/1.0

# YouTube API (optional)
export YOUTUBE_API_KEY=your_api_key
```

Without API keys, the platform uses simulated data.

## 📖 Usage Guide

1. **Launch the app**: `streamlit run app.py`
2. **Fetch Content**: Click "Fetch Trending Content" to discover AI + PM topics
3. **Browse Content**: View collected items with source metadata
4. **Select Keyword**: Click a keyword in the sidebar to drill down
5. **View Insights**: See AI summary and organization comparisons
6. **Generate Article**: Create a full 2000-3000 word article
7. **Review Analysis**: Check SEO, quality, and plagiarism scores
8. **Export PDF**: Download if all checks pass (originality ≥ 95%)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit UI                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Agent 1    │  │   Agent 2    │  │   Agent 3    │  │
│  │   Trend      │  │   Content    │  │    SEO &     │  │
│  │  Discovery   │→ │  Generation  │→ │  Plagiarism  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│         │                │                   │         │
│         ▼                ▼                   ▼         │
│  ┌──────────────────────────────────────────────────┐  │
│  │                 Data Layer                       │  │
│  │  Content Items │ Keywords │ Articles │ Reports   │  │
│  └──────────────────────────────────────────────────┘  │
│                          │                             │
│                          ▼                             │
│  ┌──────────────────────────────────────────────────┐  │
│  │              PDF Export Module                   │  │
│  │           (Plagiarism Gate Enforced)             │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 📄 License

MIT License

## 🤝 Credits

- Built with [Microsoft AutoGen](https://microsoft.github.io/autogen/)
- UI powered by [Streamlit](https://streamlit.io)
- Inspired by modern agentic AI architectures

