from retrieval.intent_detector import detect_intents


def tokenize(text):

    return text.lower().split()


def lexical_overlap_score(query, document_text):

    query_tokens = set(tokenize(query))
    doc_tokens = set(tokenize(document_text))

    overlap = query_tokens.intersection(doc_tokens)

    return len(overlap)


def rerank_results(query, results):

    intents = detect_intents(query)

    scored = []

    query_lower = query.lower()

    for item in results:

        text = f"""
        {item['name']}
        {item['description']}
        {' '.join(item['categories'])}
        {' '.join(item['job_levels'])}
        """

        text_lower = text.lower()

        score = lexical_overlap_score(query, text)

        product_type = item.get("product_type", "other")

        # =====================================================
        # Leadership
        # =====================================================

        if intents["leadership"]:

            if (
                intents["leadership"]
                and not intents["cognitive"]
            ):

                if "Ability & Aptitude" in item["categories"]:
                    score -= 20
            
            generic_aptitude_terms = [
                "numerical ability",
                "verbal ability",
                "deductive reasoning",
                "inductive reasoning"
            ]

            for term in generic_aptitude_terms:

                if term in text_lower:
                    score -= 15

            leadership_levels = [
                "Director",
                "Executive",
                "Manager",
                "Front Line Manager"
            ]

            for level in leadership_levels:

                if level in item["job_levels"]:
                    score += 3

            leadership_keywords = [
                "leadership",
                "executive",
                "manager",
                "director",
                "hipo"
            ]

            for kw in leadership_keywords:

                if kw in text_lower:
                    score += 2

            if product_type == "assessment":
                score += 8

            if product_type == "report":
                score += 2

            # =================================================
            # Core Leadership Assessment Boost
            # =================================================

            core_leadership_assessments = [
                "opq32r",
                "occupational personality questionnaire",
                "global skills assessment"
            ]

            secondary_reports = [
                "development action planner",
                "development report",
                "team impact",
                "coaching report",
                "profile report",
                "manager plus",
                "team types",
                "leadership styles profile"
            ]

            # Strong boost for foundational instruments
            for term in core_leadership_assessments:

                if term in text_lower:
                    score += 35

            # Penalize derivative reports slightly
            for term in secondary_reports:

                if term in text_lower:
                    score -= 10

            # Prefer actual assessments over reports
            if product_type == "assessment":
                score += 15

            if product_type == "report":
                score -= 2

            # =================================================
            # Exact leadership boosts
            # =================================================

            if "leadership" in query_lower:

                exact_priority_terms = [
                    "leadership report",
                    "enterprise leadership",
                    "opq leadership"
                ]

                for term in exact_priority_terms:

                    if term in text_lower:
                        score += 10

                core_instruments = [
                    "opq32r",
                    "occupational personality questionnaire"
                ]

                for term in core_instruments:

                    if term in text_lower:
                        score += 15

        # =====================================================
        # Personality
        # =====================================================

        if intents["personality"]:

            if "Personality & Behavior" in item["categories"]:
                score += 8

            personality_keywords = [
                "personality",
                "behavior",
                "behaviour",
                "opq"
            ]

            for kw in personality_keywords:

                if kw in text_lower:
                    score += 2

        # =====================================================
        # Cognitive
        # =====================================================

        if intents["cognitive"]:

            if "Ability & Aptitude" in item["categories"]:
                score += 8

            cognitive_keywords = [
                "reasoning",
                "numerical",
                "logical",
                "aptitude",
                "deductive",
                "inductive",
                "g+"
            ]

            for kw in cognitive_keywords:

                if kw in text_lower:
                    score += 2

            if "cognitive" in query_lower:

                if "Ability & Aptitude" in item["categories"]:
                    score += 12

        # =====================================================
        # Technical
        # =====================================================

        if intents["technical"]:

            if "Knowledge & Skills" in item["categories"]:
                score += 8

            technical_keywords = [
                "java",
                "python",
                "sql",
                "backend",
                "coding",
                "programming",
                "developer"
            ]

            for kw in technical_keywords:

                if kw in query_lower and kw in text_lower:
                    score += 4

            query_words = query_lower.split()

            for word in query_words:

                if word in text_lower:
                    score += 1

        # =====================================================
        # Remote
        # =====================================================

        if "remote" in query_lower:

            if item.get("remote"):
                score += 3

        scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)

    reranked = [item for score, item in scored]

    return reranked