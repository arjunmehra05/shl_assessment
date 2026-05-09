from app.services.catalog_lookup import lookup_assessments


def compare_assessments(query: str):

    results = lookup_assessments(query)

    if len(results) < 2:

        return {
            "type": "comparison",
            "message": (
                "I could not confidently identify both assessments. "
                "Please specify the exact assessment names."
            ),
            "recommendations": []
        }

    comparison_parts = []

    for item in results:

        summary = (
            f"{item['name']} focuses on "
            f"{', '.join(item['categories'])} "
            f"and is commonly used for "
            f"{', '.join(item['job_levels'][:3])} roles."
        )

        comparison_parts.append(summary)

    return {
        "type": "comparison",
        "message": " ".join(comparison_parts),
        "recommendations": results
    }