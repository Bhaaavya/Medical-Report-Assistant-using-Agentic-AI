def extract_clinical_findings(text: str):
    findings = []

    lines = text.splitlines()
    capture = False

    for line in lines:
        clean_line = line.strip()

        if not clean_line:
            continue

        lower_line = clean_line.lower()

        if "main findings" in lower_line:
            capture = True
            continue

        if capture and (
            "conclusion" in lower_line
            or "recommendations" in lower_line
            or "impression" in lower_line
        ):
            break

        if capture and clean_line.startswith("-"):
            finding_text = clean_line.lstrip("-").strip()

            severity = None
            if any(word in finding_text.lower() for word in ["severe", "marked", "large"]):
                severity = "High"
            elif any(word in finding_text.lower() for word in ["mild", "small"]):
                severity = "Low"
            elif any(word in finding_text.lower() for word in ["moderate"]):
                severity = "Medium"

            findings.append({
                "finding_text": finding_text,
                "body_area": None,
                "severity": severity,
                "source_section": "Main Findings"
            })

    return findings