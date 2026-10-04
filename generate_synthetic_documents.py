from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


OUTPUT_DIR = Path("synthetic_data/documents")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def create_pdf(filename: str, lines: list[str]):
    file_path = OUTPUT_DIR / filename

    pdf = canvas.Canvas(str(file_path), pagesize=A4)

    width, height = A4
    y = height - 60

    for line in lines:
        pdf.drawString(60, y, line)
        y -= 22

        if y < 60:
            pdf.showPage()
            y = height - 60

    pdf.save()

    print(f"Created: {file_path}")


# ---------------------------------------------------------
# 1. SYNTHETIC PAN
# ---------------------------------------------------------

create_pdf(
    "synthetic_pan.pdf",
    [
        "==============================================",
        "DEMO DOCUMENT - NOT A REAL PAN CARD",
        "FOR SOFTWARE TESTING ONLY",
        "==============================================",
        "",
        "INCOME TAX DEPARTMENT",
        "",
        "PERMANENT ACCOUNT NUMBER",
        "",
        "Name: Aarav Sharma",
        "PAN: ABCDE1234F",
        "Date of Birth: 15/05/1990",
        "",
        "Document Status: SYNTHETIC TEST DATA",
        "",
        "THIS DOCUMENT IS NOT A REAL GOVERNMENT DOCUMENT.",
        "DO NOT USE FOR IDENTIFICATION OR VERIFICATION.",
    ],
)


# ---------------------------------------------------------
# 2. SYNTHETIC AADHAAR
# ---------------------------------------------------------

create_pdf(
    "synthetic_aadhaar.pdf",
    [
        "==============================================",
        "DEMO DOCUMENT - NOT A REAL AADHAAR",
        "FOR SOFTWARE TESTING ONLY",
        "==============================================",
        "",
        "UNIQUE IDENTIFICATION DOCUMENT - DEMO",
        "",
        "Name: Aarav Sharma",
        "Date of Birth: 15/05/1990",
        "Aadhaar Number: 1234 5678 9012",
        "",
        "Address:",
        "123 Demo Street",
        "Test City",
        "Maharashtra",
        "000000",
        "",
        "Document Status: SYNTHETIC TEST DATA",
        "",
        "THIS DOCUMENT IS NOT A REAL GOVERNMENT DOCUMENT.",
        "DO NOT USE FOR IDENTIFICATION OR VERIFICATION.",
    ],
)


# ---------------------------------------------------------
# 3. SYNTHETIC APPLICATION / PROPOSAL FORM
# ---------------------------------------------------------

create_pdf(
    "synthetic_application.pdf",
    [
        "==============================================",
        "DEMO DOCUMENT - NOT A REAL APPLICATION",
        "FOR SOFTWARE TESTING ONLY",
        "==============================================",
        "",
        "LIFE INSURANCE PROPOSAL FORM",
        "",
        "Proposal Number: DEMO-PROP-000001",
        "",
        "PERSONAL DETAILS",
        "Name: Aarav Sharma",
        "Date of Birth: 15/05/1990",
        "Age: 36",
        "Gender: Male",
        "",
        "CONTACT DETAILS",
        "Mobile: 9000000000",
        "Email: aarav.demo@example.com",
        "",
        "IDENTITY DETAILS",
        "PAN: ABCDE1234F",
        "Aadhaar: 1234 5678 9012",
        "",
        "POLICY DETAILS",
        "Product Name: Demo Life Protection Plan",
        "Sum Assured: INR 5000000",
        "Annual Premium: INR 75000",
        "",
        "EMPLOYMENT DETAILS",
        "Occupation: Software Engineer",
        "Annual Income: INR 1200000",
        "",
        "DECLARATION",
        "This application is synthetic data created for",
        "software development and testing purposes only.",
        "",
        "Document Status: SYNTHETIC TEST DATA",
        "THIS IS NOT A REAL INSURANCE APPLICATION.",
    ],
)


# ---------------------------------------------------------
# 4. SYNTHETIC BANK STATEMENT
# ---------------------------------------------------------

create_pdf(
    "synthetic_bank_statement.pdf",
    [
        "==============================================",
        "DEMO DOCUMENT - NOT A REAL BANK STATEMENT",
        "FOR SOFTWARE TESTING ONLY",
        "==============================================",
        "",
        "DEMO BANK",
        "Synthetic Testing Branch",
        "",
        "ACCOUNT HOLDER",
        "Name: Aarav Sharma",
        "Account Number: XXXX00012345",
        "Account Type: Savings",
        "Account Opening Date: 10/01/2022",
        "",
        "STATEMENT PERIOD",
        "01/01/2026 to 31/03/2026",
        "",
        "TRANSACTION DATE    DESCRIPTION              AMOUNT",
        "---------------------------------------------------",
        "05/01/2026          Salary Credit           100000",
        "10/01/2026          Utility Payment           5000",
        "15/01/2026          Online Transfer           8000",
        "31/01/2026          Balance                 187000",
        "",
        "05/02/2026          Salary Credit           100000",
        "12/02/2026          Rent Payment             20000",
        "20/02/2026          Online Transfer           7000",
        "28/02/2026          Balance                 260000",
        "",
        "05/03/2026          Salary Credit           100000",
        "15/03/2026          Utility Payment           4500",
        "25/03/2026          Online Transfer          10000",
        "31/03/2026          Balance                 345500",
        "",
        "Average Monthly Salary Credit: INR 100000",
        "Account Age: Approximately 4 years",
        "",
        "Document Status: SYNTHETIC TEST DATA",
        "THIS IS NOT A REAL BANK STATEMENT.",
    ],
)


print()
print("==============================================")
print("All synthetic documents created successfully.")
print("==============================================")