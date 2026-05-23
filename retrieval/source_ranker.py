SOURCE_WEIGHTS = {
    "pib.gov.in": 0.95,
    "factcheck.afp.com": 0.93,
    "altnews.in": 0.90,
    "boomlive.in": 0.88,
    "thehindu.com": 0.85,
    "indianexpress.com": 0.82,
    "ndtv.com": 0.78,
    "timesofindia.com": 0.70,
    "local KB": 0.75
}

def score_evidence(evidence: str) -> float:

    evidence_lower = evidence.lower()

    for domain, score in SOURCE_WEIGHTS.items():

        if domain in evidence_lower:
            return score

    return 0.50