# Simple legal term simplifier

legal_dictionary = {
    "petitioner": "person who filed the case",
    "respondent": "person responding to the case",
    "litigation": "court case",
    "initiate": "start",
    "proceedings": "legal process",
    "competent jurisdiction": "appropriate court",
    "adjournment": "postponement of the hearing",
    "plaintiff": "person bringing the case",
    "defendant": "person being accused"
}


def simplify_legal_text(text):

    simplified = text.lower()

    for term, meaning in legal_dictionary.items():
        simplified = simplified.replace(term, meaning)

    return simplified.capitalize()