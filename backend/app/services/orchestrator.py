import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from retrieval.retriever import retrieve_assessments
from app.services.comparison import compare_assessments
from app.services.test_type_mapper import map_test_type


def detect_query_type(query: str):

    query = query.lower()

    comparison_keywords = [
        "compare",
        "difference",
        "vs",
        "versus"
    ]

    vague_queries = [
        "i need an assessment",
        "need assessment",
        "suggest assessment",
        "recommend assessment"
    ]

    if any(word in query for word in comparison_keywords):
        return "comparison"

    if query.strip() in vague_queries:
        return "clarification"

    return "recommendation"


def needs_clarification(query: str):

    query = query.lower()

    role_signals = [
        "developer",
        "engineer",
        "manager",
        "sales",
        "leadership",
        "executive",
        "graduate",
        "director",
        "analyst",
        "cxo"
    ]

    assessment_signals = [
        "personality",
        "cognitive",
        "technical",
        "numerical",
        "reasoning",
        "behavioral",
        "aptitude"
    ]

    purpose_signals = [
        "hiring",
        "selection",
        "development",
        "benchmark",
        "benchmarking",
        "promotion",
        "internal mobility"
    ]

    role_matches = sum(
        signal in query
        for signal in role_signals
    )

    assessment_matches = sum(
        signal in query
        for signal in assessment_signals
    )

    purpose_matches = sum(
        signal in query
        for signal in purpose_signals
    )

    # =====================================================
    # Require richer context before recommendation
    # =====================================================

    if role_matches >= 1 and (
        purpose_matches >= 1
        or assessment_matches >= 1
    ):
        return False

    technical_signals = [
        "java",
        "python",
        "sql",
        "backend",
        "frontend",
        "developer",
        "engineering",
        "coding"
    ]

    technical_matches = sum(
        signal in query
        for signal in technical_signals
    )

    if technical_matches >= 2:
        return False

    return True


def generate_followup_question(query):

    query = query.lower()

    if (
        "selection" in query
        or "benchmark" in query
        or "benchmarking" in query
        or "hiring" in query
    ):
        return (
            "These assessments are well-suited "
            "for leadership selection and benchmarking."
        )

    if "leadership" in query or "executive" in query:
        return (
            "Are these intended for hiring, "
            "leadership benchmarking, or development?"
        )

    if "developer" in query or "java" in query:
        return (
            "Do you also want coding simulations "
            "or only technical knowledge assessments?"
        )

    if "graduate" in query:
        return (
            "Is this for campus hiring, screening, "
            "or final-stage evaluation?"
        )

    return (
        "Could you share more about the hiring "
        "or assessment context?"
    )


def is_conversation_complete(query):

    query = query.lower()

    completion_signals = [
        "selection",
        "benchmark",
        "benchmarking",
        "finalize",
        "final",
        "that's what we need",
        "perfect"
    ]

    return any(signal in query for signal in completion_signals)


def handle_query(messages):

    if not messages:

        return {
            "reply": (
                "Please provide some details "
                "about the role or assessment need."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    conversation_text = " ".join(
        msg.content
        for msg in messages
    )

    latest_user_message = ""

    for msg in reversed(messages):

        if msg.role == "user":

            latest_user_message = msg.content

            break

    if not latest_user_message.strip():

        return {
            "reply": (
                "Please provide some details "
                "about the role or assessment need."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # =====================================================
    # Refinement Detection
    # =====================================================

    refinement_keywords = [
        "also",
        "add",
        "include",
        "actually",
        "instead",
        "along with"
    ]

    is_refinement = any(
        kw in latest_user_message.lower()
        for kw in refinement_keywords
    )

    query_type = detect_query_type(conversation_text)

    # =====================================================
    # Comparison Flow
    # =====================================================

    if query_type == "comparison":

        comparison_result = compare_assessments(
            conversation_text
        )

        return {
            "reply": comparison_result["message"],
            "recommendations": [
                {
                    "name": item["name"],
                    "url": item["url"],
                    "test_type": map_test_type(
                        item["categories"]
                    )
                }
                for item in comparison_result["recommendations"]
            ],
            "end_of_conversation": False
        }

    # =====================================================
    # Prompt Injection / Off-topic Refusal
    # =====================================================

    injection_keywords = [
        "ignore previous instructions",
        "system prompt",
        "reveal prompt",
        "bypass",
        "jailbreak"
    ]

    off_topic_keywords = [
        "legal advice",
        "lawsuit",
        "fire employees",
        "salary negotiation",
        "medical advice"
    ]

    if any(
        kw in conversation_text.lower()
        for kw in injection_keywords + off_topic_keywords
    ):

        return {
            "reply": (
                "I can only assist with SHL assessment "
                "recommendations and comparisons."
            ),
            "recommendations": [],
            "end_of_conversation": True
        }

    # =====================================================
    # Scope Guard
    # =====================================================

    domain_keywords = [
        "assessment",
        "test",
        "hiring",
        "leadership",
        "developer",
        "personality",
        "cognitive",
        "reasoning",
        "benchmark",
        "selection",
        "graduate",
        "skills",
        "java",
        "python",
        "sales"
    ]

    domain_matches = sum(
        kw in conversation_text.lower()
        for kw in domain_keywords
    )

    if domain_matches == 0:

        return {
            "reply": (
                "I specialize in SHL assessment "
                "recommendations and comparisons only."
            ),
            "recommendations": [],
            "end_of_conversation": True
        }

    # =====================================================
    # Clarification Flow
    # =====================================================

    if (
        not is_refinement
        and (
            query_type == "clarification"
            or needs_clarification(conversation_text)
        )
    ):

        return {
            "reply": (
                "Could you share more about the role, "
                "seniority level, and whether you need "
                "technical, cognitive, or personality assessments?"
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # =====================================================
    # Retrieval
    # =====================================================

    recommendations = retrieve_assessments(
        conversation_text
    )

    if not recommendations:

        return {
            "reply": (
                "I could not find strong assessment matches. "
                "Could you provide more details about "
                "the role or assessment goals?"
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    formatted = []

    for item in recommendations[:5]:

        formatted.append({
            "name": item["name"],
            "url": item["url"],
            "test_type": map_test_type(
                item["categories"]
            )
        })

    return {
        "reply": (
            "Recommended assessments based on the current context. "
            + generate_followup_question(conversation_text)
        ),
        "recommendations": formatted,
        "end_of_conversation": is_conversation_complete(
            conversation_text
        )
    }


if __name__ == "__main__":

    test_messages = [
        {
            "role": "user",
            "content": "Need assessments for senior leadership"
        }
    ]

    result = handle_query(test_messages)

    print(result)