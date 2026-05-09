import json
import re

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

CATALOG_PATH = BASE_DIR / "data" / "catalog.json"


with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    catalog = json.load(f)


KNOWN_ENTITIES = {
    "opq": [
        "occupational personality questionnaire",
        "opq32r",
        "opq"
    ],

    "gsa": [
        "global skills assessment",
        "gsa"
    ],

    "verify": [
        "verify"
    ]
}


def normalize(text):

    text = text.lower()

    text = re.sub(r"[^a-z0-9\s]", " ", text)

    return text.strip()


def extract_entities(query):

    query = normalize(query)

    found = []

    for entity, aliases in KNOWN_ENTITIES.items():

        for alias in aliases:

            if alias in query:
                found.append(entity)
                break

    return found


def lookup_assessments(query):

    entities = extract_entities(query)

    matched = []

    for entity in entities:

        for item in catalog:

            name = normalize(item["name"])

            if entity == "opq":

                if (
                    "opq32r" in name
                    or "occupational personality questionnaire" in name
                ):
                    matched.append(item)

            elif entity == "gsa":

                if "global skills assessment" in name:
                    matched.append(item)

            elif entity == "verify":

                if "verify" in name:
                    matched.append(item)

    # remove duplicates
    unique = []

    seen = set()

    for item in matched:

        if item["name"] not in seen:

            unique.append(item)

            seen.add(item["name"])

    return unique[:2]