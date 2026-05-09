import json

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_PATH = (
    BASE_DIR /
    "data" /
    "raw" /
    "catalog" /
    "shl_catalog.json"
)

OUTPUT_PATH = (
    BASE_DIR /
    "data" /
    "catalog.json"
)

def detect_product_type(name: str):

    name = name.lower()

    report_keywords = [
        "report",
        "profile",
        "planner"
    ]

    assessment_keywords = [
        "questionnaire",
        "assessment",
        "test",
        "verify",
        "simulation"
    ]

    for kw in report_keywords:
        if kw in name:
            return "report"

    for kw in assessment_keywords:
        if kw in name:
            return "assessment"

    return "other"

def normalize_record(item):
    return {
        "id": item.get("entity_id", ""),
        "name": item.get("name", "").strip(),
        "url": item.get("link", "").strip(),
        "description": item.get("description", "").strip(),

        "job_levels": item.get("job_levels", []),

        "languages": item.get("languages", []),

        "duration": item.get("duration", "").strip(),

        "remote": item.get("remote", "").lower() == "yes",

        "adaptive": item.get("adaptive", "").lower() == "yes",

        "categories": item.get("keys", []),

        "product_type": detect_product_type(
            item.get("name", "")
        ),
    }


def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    normalized = []

    seen_urls = set()

    for item in raw_data:
        url = item.get("link", "").strip()

        if not url:
            continue

        if "/job-solutions/" in url.lower():
            continue

        if url in seen_urls:
            continue

        seen_urls.add(url)

        normalized.append(normalize_record(item))

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(normalized, f, indent=2, ensure_ascii=False)

    print(f"Normalized {len(normalized)} assessments")


if __name__ == "__main__":
    main()