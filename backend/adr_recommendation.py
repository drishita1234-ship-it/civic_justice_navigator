def recommend_resolution(case_type):

    case_type = case_type.lower()

    if "criminal" in case_type:
        return "Litigation recommended (criminal matters must proceed through court)."

    if "family" in case_type:
        return "Mediation may help resolve this dispute before going to court."

    if "property" in case_type:
        return "Arbitration or mediation could resolve this dispute faster than litigation."

    return "Litigation or alternative dispute resolution may both be possible depending on the case."