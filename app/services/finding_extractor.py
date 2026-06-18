import re


COMMON_TESTS = [
    "hemoglobin",
    "haemoglobin",
    "wbc",
    "rbc",
    "platelet",
    "platelets",
    "glucose",
    "creatinine",
    "urea",
    "cholesterol",
    "triglycerides",
    "hdl",
    "ldl",
    "tsh",
    "t3",
    "t4",
    "bilirubin",
    "sgpt",
    "sgot",
    "sodium",
    "potassium"
]


def extract_findings_from_text(text: str):
    findings = []

    lines = text.splitlines()

    for line in lines:
        clean_line = " ".join(line.split())
        lower_line = clean_line.lower()

        for test in COMMON_TESTS:
            if test in lower_line:
                numbers = re.findall(r"\d+(?:\.\d+)?", clean_line)

                if numbers:
                    value = numbers[0]

                    reference_range = None

                    if len(numbers) >= 3:
                        reference_range = f"{numbers[1]} - {numbers[2]}"

                    findings.append({
                        "test_name": test.title(),
                        "value": value,
                        "unit": None,
                        "reference_range": reference_range,
                        "source_text": clean_line
                    })

                    break

    return findings