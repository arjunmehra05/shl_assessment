CATEGORY_TO_CODE = {
    "Knowledge & Skills": "K",
    "Personality & Behavior": "P",
    "Ability & Aptitude": "A",
    "Competencies": "C",
    "Development & 360": "D"
}


def map_test_type(categories):

    if not categories:
        return "Unknown"

    for category in categories:

        if category in CATEGORY_TO_CODE:
            return CATEGORY_TO_CODE[category]

    return "Unknown"