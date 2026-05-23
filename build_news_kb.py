"""
build_indian_news_kb.py
=======================
Builds the indian_news/ knowledge base folder for the
Multi-Agent Fact Verification project.

Scrapes articles from trusted Indian fact-checking sources
and saves them as clean .txt files ready for FAISS ingestion.

Usage:
    pip install requests beautifulsoup4 trafilatura tqdm
    python build_indian_news_kb.py

Output:
    indian_news/
    ├── boomlive/       ← Boom Live fact-checks
    ├── altnews/        ← Alt News fact-checks
    ├── pib/            ← PIB government press releases
    ├── thehindu/       ← The Hindu articles
    └── manual/         ← Drop any PDFs/txts here manually
"""

import os
import time
import json
import requests
from bs4 import BeautifulSoup
import trafilatura
from tqdm import tqdm
from datetime import datetime

# ── Output folder ──────────────────────────────────────────
BASE_DIR = "indian_news"
os.makedirs(BASE_DIR, exist_ok=True)
SOURCES = ["boomlive", "altnews", "pib", "thehindu", "manual"]
for s in SOURCES:
    os.makedirs(os.path.join(BASE_DIR, s), exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# ── Utility: extract clean text from a URL ─────────────────
def extract_text(url: str) -> str | None:
    """Use trafilatura for clean article text extraction."""
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            text = trafilatura.extract(
                downloaded,
                include_comments=False,
                include_tables=True,
                no_fallback=False
            )
            return text
    except Exception as e:
        print(f"  [!] trafilatura failed for {url}: {e}")
    return None


def save_article(text: str, folder: str, filename: str, url: str):
    """Save article text with metadata header."""
    filepath = os.path.join(BASE_DIR, folder, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"SOURCE: {url}\n")
        f.write(f"SCRAPED: {datetime.now().isoformat()}\n")
        f.write("=" * 60 + "\n\n")
        f.write(text)
    return filepath


# ══════════════════════════════════════════════════════════
# 1. BOOM LIVE — India's premier fact-checking site
# ══════════════════════════════════════════════════════════

# Curated high-value Boom Live URLs covering major Indian controversies
BOOMLIVE_URLS = [
    "https://www.boomlive.in/fact-check/unrelated-photo-peddled-as-edu-minister-dharmendra-pradhan-with-neet-leak-accused-31596",
    "https://www.boomlive.in/fact-check/video-of-eviction-from-bangladesh-falsely-linked-to-west-bengal-31602",
    "https://www.boomlive.in/fact-check/fake-news-viral-video-helle-lyngs-question-to-modi-on-press-freedom-pak-handles-operation-sindoor-question-31598",
    "https://www.boomlive.in/fact-check/fake-news-viral-video-people-removing-tvk-flags-anti-sanatana-remarks-old-video-tamil-nadu-election-factcheck-31595",
    "https://www.boomlive.in/fact-check/fake-news-viral-videos-s-jaishankar-pakistan-retaliation-caught-india-off-guard-army-general-saying-india-paid-taliban-31593",
    "https://www.boomlive.in/fact-check/video-bulldozer-demolition-drive-west-bengal-claim-fact-check-31591",
    "https://www.boomlive.in/fact-check/nashik-assault-video-shared-with-false-communal-claim-as-bengal-muslim-woman-31556",
    "https://www.boomlive.in/fact-check/fake-news-bihar-education-minister-mithilesh-tiwari-girls-education-statement-misreported-girls-protests-government-31549",
    "https://www.boomlive.in/fact-check/video-tmc-worker-attack-bjp-post-poll-violence-west-bengal-fact-check-31533",
    "https://www.boomlive.in/fact-check/video-of-drdo-chairman-on-washing-missiles-with-cow-urine-is-a-deepfake-31143",
    "https://www.boomlive.in/fact-check/fake-news-viral-image-passport-wife-cole-thomas-allen-indian-priyanka-rao-31080",
    "https://www.boomlive.in/fact-check/fake-news-viral-videos-ai-deepfakes-indian-army-officers-criticize-trump-indian-government-factcheck-31059",
    "https://www.boomlive.in/fact-check/fake-news-jd-vance-plane-iran-us-ceasefire-talks-pakistan-factcheck-31000",
    "https://www.boomlive.in/fact-check/fact-check-noida-police-assaulting-women-viral-video-is-real-31038",
    "https://www.boomlive.in/fact-check/fake-news-viral-video-indian-navy-attack-iran-ship-fact-checkn-30938",
]


def scrape_boomlive():
    print("\n[1/4] Scraping Boom Live...")

    # Also scrape their fact-check listing page to get more URLs
    listing_url = "https://www.boomlive.in/fact-check"
    try:
        resp = requests.get(listing_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        # Extract article links from listing
        links = soup.find_all("a", href=True)
        extra_urls = [
            "https://www.boomlive.in" + a["href"]
            for a in links
            if "/fact-check/" in a["href"]
            and "boomlive.in" not in a["href"]
        ][:20]  # grab top 20 from listing
        all_urls = list(set(BOOMLIVE_URLS + extra_urls))
    except Exception:
        all_urls = BOOMLIVE_URLS

    saved = 0
    for i, url in enumerate(tqdm(all_urls, desc="Boom Live")):
        text = extract_text(url)
        if text and len(text) > 200:
            slug = url.rstrip("/").split("/")[-1][:60]
            filename = f"boomlive_{i:03d}_{slug}.txt"
            save_article(text, "boomlive", filename, url)
            saved += 1
        time.sleep(1.5)  # polite scraping delay

    print(f"  ✓ Saved {saved} Boom Live articles")


# ══════════════════════════════════════════════════════════
# 2. ALT NEWS — India's oldest fact-checking org
# ══════════════════════════════════════════════════════════

ALTNEWS_URLS = [
    "https://www.altnews.in/cockroach-janata-partys-majority-followers-pakistani-bjym-secretary-tajinder-bagga-others-amplify-misleading-claim/",
    "https://www.altnews.in/rare-earths-and-rebel-armies-how-a-conspiracy-story-with-no-evidence-jumped-from-fringe-sites-to-newsrooms/",
    "https://www.altnews.in/tamil-nadu-anti-hindi-protests-from-march-falsely-linked-to-tvk-assuming-power/",
    "https://www.altnews.in/convoy-controversy-rajasthan-mlas-cavalcade-video-falsely-linked-to-bjp-pm-modi/",
    "https://www.altnews.in/fake-video-clip-showing-suvendu-adhikari-talking-about-finishing-muslims-is-ai-generated/",
    "https://www.altnews.in/mosques-vandalized-muslim-homes-burnt-down-in-meerut-no-hapur-video-falsely-viral/",
    "https://www.altnews.in/bihar-education-minister-mithilesh-tiwari-didnt-say-girls-dont-need-education/",
    "https://www.altnews.in/fact-check-edited-the-hindu-clip-shared-claiming-indira-gandhi-appeal-to-indians-to-stop-buying-gold-in-1967/",
    "https://www.altnews.in/india-is-not-the-fourth-largest-or-a-4-trillion-economy-yet-niti-aayog-ceos-claim-citing-imf-data-misleading/",
    "https://www.altnews.in/media-misreports-nirmala-sitharaman-claimed-demonetisation-had-no-impact-on-economy/",
    "https://www.altnews.in/did-indias-economy-plummet-from-3rd-largest-in-the-world-in-2011-to-6th-largest-in-2017/",
    "https://www.altnews.in/did-chandrababu-naidu-claim-23-lakh-crore-jobs-were-created-in-18-months-edited-clip-goes-viral/",
    "https://www.altnews.in/political-misinformation-in-2025-who-shared-who-was-targeted-how-did-it-shape-narratives/",
]


def scrape_altnews():
    print("\n[2/4] Scraping Alt News...")

    # Scrape listing page too
    listing_url = "https://www.altnews.in"
    try:
        resp = requests.get(listing_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        links = soup.find_all("a", href=True)
        extra_urls = [
            a["href"] for a in links
            if "altnews.in/" in a.get("href", "")
            and len(a["href"]) > 30
            and not a["href"].endswith("altnews.in/")
        ][:20]
        all_urls = list(set(ALTNEWS_URLS + extra_urls))
    except Exception:
        all_urls = ALTNEWS_URLS

    saved = 0
    for i, url in enumerate(tqdm(all_urls, desc="Alt News")):
        text = extract_text(url)
        if text and len(text) > 200:
            slug = url.rstrip("/").split("/")[-1][:60]
            filename = f"altnews_{i:03d}_{slug}.txt"
            save_article(text, "altnews", filename, url)
            saved += 1
        time.sleep(1.5)

    print(f"  ✓ Saved {saved} Alt News articles")


# ══════════════════════════════════════════════════════════
# 3. PIB FACT CHECK — Official Government of India
# ══════════════════════════════════════════════════════════

PIB_URLS = [
    # PIB Fact Check main page
    "https://pib.gov.in/FactCheck.aspx",

    # Direct PIB press releases on key topics
    "https://www.pib.gov.in/PressReleasePage.aspx?PRID=1999956&reg=3&lang=2"
    "https://pib.gov.in/PressReleasePage.aspx?PRID=2000001",  # economy
    "https://pib.gov.in/PressReleasePage.aspx?PRID=1999999",  # schemes
    "https://factcheck.pib.gov.in/",                           # fact check portal

    # Government data sources
    "https://mospi.gov.in/gdp-data-release",                  # GDP data
    "https://data.gov.in/",                                    # open data portal
]

PIB_FACT_CHECK_API = "https://factcheck.pib.gov.in/api/fact-checks"


def scrape_pib():
    print("\n[3/4] Scraping PIB Fact Check...")
    saved = 0

    for i, url in enumerate(tqdm(PIB_URLS, desc="PIB")):
        text = extract_text(url)
        if text and len(text) > 200:
            slug = f"pib_{i:03d}_factcheck"
            filename = f"{slug}.txt"
            save_article(text, "pib", filename, url)
            saved += 1
        time.sleep(1.5)

    print(f"  ✓ Saved {saved} PIB articles")



# ══════════════════════════════════════════════════════════
# 5. MANUAL SOURCES — Wikipedia + open data
#    These are guaranteed to work (no paywall/blocking)
# ══════════════════════════════════════════════════════════

WIKIPEDIA_URLS = [
    # Major Indian controversies — all open access
    ("2024_NEET_controversy",         "neet_2024_controversy"),
    ("2024_Indian_general_election",  "lok_sabha_2024"),
    ("UGC-NET_2024_controversy",      "ugc_net_2024"),
    ("Pegasus_Project_(India)",        "pegasus_india"),
    ("Electoral_bonds_scheme",         "electoral_bonds"),
    ("Demonetisation_in_India",        "demonetisation_india"),
    ("Ayushman_Bharat",                "ayushman_bharat"),
    ("Make_in_India",                  "make_in_india"),
    ("India–China_relations",          "india_china_relations"),
    ("Manipur_violence_(2023)",        "manipur_violence_2023"),
    ("National_Register_of_Citizens",  "nrc_india"),
    ("Citizenship_Amendment_Act_2019", "caa_india"),
    ("Farm_laws_repeal_India",         "farm_laws_india"),
    ("COVID-19_pandemic_in_India",     "covid_india"),
    ("Indian_Premier_League",          "ipl_controversies"),
]

WIKIPEDIA_API = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"
WIKIPEDIA_FULL = "https://en.wikipedia.org/w/api.php"


def scrape_wikipedia():
    print("\n[5/5] Scraping Wikipedia (guaranteed open access)...")
    saved = 0

    for page_title, filename_slug in tqdm(WIKIPEDIA_URLS, desc="Wikipedia"):
        try:
            # Get full article text via Wikipedia API
            params = {
                "action": "query",
                "prop": "extracts",
                "explaintext": True,
                "titles": page_title,
                "format": "json",
                "exsectionformat": "plain"
            }
            resp = requests.get(WIKIPEDIA_FULL, params=params,
                                headers=HEADERS, timeout=10)
            data = resp.json()
            pages = data["query"]["pages"]
            page = next(iter(pages.values()))

            if "extract" in page and len(page["extract"]) > 300:
                url = f"https://en.wikipedia.org/wiki/{page_title}"
                filename = f"wiki_{filename_slug}.txt"
                save_article(page["extract"], "manual", filename, url)
                saved += 1

            time.sleep(0.5)

        except Exception as e:
            print(f"  [!] Wikipedia failed for {page_title}: {e}")

    print(f"  ✓ Saved {saved} Wikipedia articles")


# ══════════════════════════════════════════════════════════
# 6. NEET SPECIFIC — guaranteed sources
# ══════════════════════════════════════════════════════════

NEET_SPECIFIC_URLS = [
    "https://en.wikipedia.org/wiki/2024_NEET_controversy",
    "https://en.wikipedia.org/wiki/National_Eligibility_cum_Entrance_Test",
    "https://en.wikipedia.org/wiki/National_Testing_Agency",
    "https://pib.gov.in/PressReleasePage.aspx?PRID=2026581",
    "https://www.thehindu.com/topic/neet/",
    "https://www.ndtv.com/topic/neet-paper-leak",
]


def scrape_neet_specific():
    print("\n[Bonus] Scraping NEET-specific pages...")
    saved = 0

    for i, url in enumerate(tqdm(NEET_SPECIFIC_URLS, desc="NEET")):
        text = extract_text(url)
        if text and len(text) > 200:
            filename = f"neet_{i:03d}_{url.split('/')[-1][:50]}.txt"
            save_article(text, "manual", filename, url)
            saved += 1
        time.sleep(1)

    print(f"  ✓ Saved {saved} NEET-specific articles")


# ══════════════════════════════════════════════════════════
# MAIN — run everything
# ══════════════════════════════════════════════════════════

def count_files():
    total = 0
    for folder in SOURCES:
        path = os.path.join(BASE_DIR, folder)
        n = len([f for f in os.listdir(path) if f.endswith(".txt")])
        print(f"  {folder:12s}: {n} files")
        total += n
    print(f"  {'TOTAL':12s}: {total} files")
    return total


if __name__ == "__main__":
    print("=" * 60)
    print("Building indian_news/ knowledge base")
    print("=" * 60)

    # Wikipedia is 100% reliable — always run this first
    scrape_wikipedia()
    scrape_neet_specific()

    # These may partially fail due to paywalls/blocking — that's OK
    scrape_boomlive()
    scrape_altnews()
    scrape_pib()

    print("\n" + "=" * 60)
    print("FINAL COUNT:")
    total = count_files()
    print("=" * 60)

    if total >= 20:
        print(f"\n✅ Knowledge base ready! {total} documents in indian_news/")
        print("Next step: run ingest.py to build your FAISS index")
    else:
        print(f"\n⚠️  Only {total} documents saved.")
        print("Some sources may be blocked. Use manual/ folder to add PDFs.")
        print("Wikipedia articles alone are enough to get started.")