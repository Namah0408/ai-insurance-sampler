from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


OUTPUT_DIR = Path(
    "knowledge_base/documents"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


def create_pdf(
    filename: str,
    title: str,
    lines: list[str],
):

    path = OUTPUT_DIR / filename

    pdf = canvas.Canvas(
        str(path),
        pagesize=A4,
    )

    width, height = A4

    y = height - 60

    pdf.setFont(
        "Helvetica",
        11,
    )

    for line in lines:

        if y < 60:

            pdf.showPage()

            y = height - 60

            pdf.setFont(
                "Helvetica",
                11,
            )

        pdf.drawString(
            60,
            y,
            line,
        )

        y -= 20

    pdf.save()

    print(
        f"Created: {path}"
    )


create_pdf(
    "synthetic_sampling_sop.pdf",
    "Sampling SOP",
    [
        "DEMO KNOWLEDGE DOCUMENT",
        "NOT AN OFFICIAL COMPANY POLICY",
        "",
        "LIFE INSURANCE SAMPLING SOP",
        "",
        "Version: 1.0",
        "Effective Date: 01/01/2026",
        "",
        "1. Purpose",
        "This document is synthetic training material.",
        "It describes a hypothetical sampling workflow.",
        "",
        "2. Document Review",
        "The sampler should verify that required customer",
        "documents are available and readable.",
        "",
        "3. Identity Review",
        "Customer identity information should be checked",
        "for consistency across submitted documents.",
        "",
        "4. Escalation",
        "Cases with missing or inconsistent information",
        "should be referred for human review.",
        "",
        "5. Decision Principle",
        "An automated system should not invent facts.",
        "Missing evidence should be treated as unknown.",
    ],
)


create_pdf(
    "synthetic_kyc_guidelines.pdf",
    "KYC Guidelines",
    [
        "DEMO KNOWLEDGE DOCUMENT",
        "NOT AN OFFICIAL COMPANY POLICY",
        "",
        "KYC VERIFICATION GUIDELINES",
        "",
        "Version: 1.0",
        "",
        "1. PAN Verification",
        "PAN information should be checked for valid",
        "format and consistency with customer details.",
        "",
        "2. Aadhaar Verification",
        "Aadhaar information should be treated as verified",
        "only when an approved verification mechanism",
        "returns a successful result.",
        "",
        "3. Name Consistency",
        "Material differences between identity documents",
        "should be referred for review.",
        "",
        "4. Missing Evidence",
        "Missing identity evidence should not be guessed.",
        "The case should remain unresolved until evidence",
        "is available.",
    ],
)


create_pdf(
    "synthetic_financial_guidelines.pdf",
    "Financial Guidelines",
    [
        "DEMO KNOWLEDGE DOCUMENT",
        "NOT AN OFFICIAL COMPANY POLICY",
        "",
        "FINANCIAL REVIEW GUIDELINES",
        "",
        "Version: 1.0",
        "",
        "1. Income",
        "Declared income should be compared with available",
        "financial evidence.",
        "",
        "2. Premium",
        "Annual premium may be compared with declared",
        "annual income as part of financial analysis.",
        "",
        "3. Sum Assured",
        "Proposed sum assured may be compared with available",
        "financial information.",
        "",
        "4. Bank Account",
        "Account opening date can be considered as one",
        "factor in financial analysis.",
        "",
        "5. Important",
        "The system must not invent financial information.",
        "Company-approved thresholds must be used for",
        "actual underwriting decisions.",
    ],
)


create_pdf(
    "synthetic_bawc_guidelines.pdf",
    "BAWC Guidelines",
    [
        "DEMO KNOWLEDGE DOCUMENT",
        "NOT AN OFFICIAL COMPANY POLICY",
        "",
        "BAWC REVIEW GUIDELINES",
        "",
        "Version: 1.0",
        "",
        "1. Purpose",
        "BAWC evidence may be reviewed for completion",
        "and consistency with proposal information.",
        "",
        "2. Evidence",
        "The system should verify that required BAWC evidence",
        "is available and usable.",
        "",
        "3. Identity",
        "Identity-related information should be compared",
        "with approved customer information.",
        "",
        "4. Video Analysis",
        "Facial expressions should not be treated as direct",
        "evidence of honesty or dishonesty.",
        "",
        "5. Escalation",
        "Unclear or incomplete BAWC evidence should be",
        "referred for human review.",
    ],
)


print()
print("Synthetic knowledge documents created.")