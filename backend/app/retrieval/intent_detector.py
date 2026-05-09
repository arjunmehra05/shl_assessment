def detect_intents(query: str):
    query = query.lower()

    return {
        "leadership": any(
            word in query
            for word in [
                "leadership",
                "executive",
                "director",
                "cxo",
                "manager"
            ]
        ),

        "personality": any(
            word in query
            for word in [
                "personality",
                "behavior",
                "behaviour",
                "culture"
            ]
        ),

        "cognitive": any(
            word in query
            for word in [
                "cognitive",
                "reasoning",
                "numerical",
                "logical",
                "aptitude"
            ]
        ),

        "technical": any(
            word in query
            for word in [
                "java",
                "python",
                "sql",
                "backend",
                "developer",
                "coding"
            ]
        )
    }