# Amazon Competitor Analysis

---

## What you need

1. **Python** 3.12 or newer  
2. **[ScraperAPI](https://www.scraperapi.com/) account** — sign up on their site  
3. **API key** — copy it from your ScraperAPI dashboard  
4. **Dependencies** — install from this repo with `uv sync` (or your usual `pip` workflow)
5. **During testing make sure the product ASIN number and domain match**

---

## Setup

1. In the project folder (same level as `main.py`), create a **`.env`** file.  
2. Add:

   ```env
   SCRAPER_API_KEY=paste_your_key_here
   ```

   Do not commit `.env` or share your key.

---

## Run

```bash
cd web_scraping
uv sync
uv run streamlit run main.py
```

Open the URL the terminal shows (usually `http://localhost:8501`).

---

## Legal note

Using Amazon data must follow **Amazon’s terms**, **ScraperAPI’s terms**, and the law in your region.
