def detect_report_type(text: str):
    text = text.lower()

    if any(word in text for word in ["hemoglobin","haemoglobin","platelet","platelets","wbc","rbc","cbc","blood count","complete blood count",
"hematology",
    "differential count"]):
        return "Blood Test"

    if any(word in text for word in ["mri",
    "magnetic resonance imaging",
    "mr study",
    "brain",
    "cervical spine",
    "spinal cord",
    "radiology",
    "main findings",
    "impression"]):
        return "MRI"

    if any(word in text for word in ["ct scan", "computed tomography"]):
        return "CT Scan"

    if any(word in text for word in ["prescription", "rx", "tablet", "capsule", "dosage"]):
        return "Prescription"

    if any(word in text for word in ["discharge summary", "admission date", "discharge date"]):
        return "Discharge Summary"

    return "General Medical Report"