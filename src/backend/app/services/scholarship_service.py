from . import database as db
from datetime import datetime, date
import re

def list_scholarships(limit=50, categories=None, status=None):
    conn = db.get_db()
    conditions = []
    params = []
    if categories:
        conditions.append("category IN (" + ",".join(["?"] * len(categories)) + ")")
        params.extend(categories)
    if status:
        conditions.append("status IN (" + ",".join(["?"] * len(status)) + ")")
        params.extend(status)
    clause = "WHERE 1=1"
    if conditions:
        clause += " AND " + " AND ".join(conditions)
    sql = f"SELECT * FROM scholarships {clause} ORDER BY deadline ASC LIMIT ?"
    params.append(limit)
    rows = conn.execute(sql, params).fetchall()
    return [dict(row) for row in rows]


def get_scholarship(scholarship_id):
    conn = db.get_db()
    row = conn.execute("SELECT * FROM scholarships WHERE id = ?", (scholarship_id,)).fetchone()
    return dict(row) if row else None


def create_scholarship(data):
    conn = db.get_db()
    cur = conn.execute(
        "INSERT INTO scholarships (name, org, category, eligibility_criteria, deadline, documents, url) VALUES (?,?,?,?,?,?,?)",
        (
            data.get("name", ""),
            data.get("org", ""),
            data.get("category", ""),
            data.get("eligibility_criteria", ""),
            data.get("deadline", ""),
            data.get("documents", ""),
            data.get("url", ""),
        ),
    )
    conn.commit()
    return cur.lastrowid


def seed_sample():
    conn = db.get_db()
    conn.execute("DELETE FROM scholarships")
    conn.execute(
        """
        INSERT INTO scholarships
        (name, org, category, eligibility_criteria, deadline, documents, url)
        VALUES
        (
            ("Central Sector Scheme - College & University", "MHRD / AICTE", "CENTRAL_GENERAL",
             "Class 12 pass. Min 80% aggregate. Family annual income < INR 4.5 lakh.", "2026-10-31",
             "income_certificate, marksheets, admission_letter, caste_certificate", "https://scholarships.gov.in"),
            ("National Means Cum Merit - NMMSS", "MHRD", "CENTRAL_GENERAL",
             "Class 9-10. Min 55% Class 8. Income < INR 3.5 lakh.", "2026-11-15",
             "income_certificate, last_marksheet, caste_certificate_if_applicable", "https://scholarships.gov.in/nmmss"),
            ("Post-Matric Scholarship - SC State", "State SWDs", "SOCIAL_SC",
             "SC student. Class 9-12 / Diploma / College. Income ceiling varies.", "2026-09-30",
             "income_certificate, caste_certificate, admission_proof, marksheet", "https://nafdc.nic.in"),
            ("Pragati Scholarship - Girls", "AICTE", "GENERAL_GIRLS",
             "Girl child single parent. Income < INR 8 lakh.", "2026-10-31",
             "income_certificate, parent_documents, admit_card, marksheet", "https://aicte-india.org"),
            ("AICTE Saksham - PwD", "AICTE", "SOCIAL_PWD",
             "40% disability. Income < INR 8 lakh. 1st year diploma/tech.", "2026-10-31",
             "disability_certificate, income_certificate, ID_proof, admission_letter", "https://aicte-india.org")
        )
    """
    )
    conn.commit()
    print("Seeded", conn.total_changes, "scholarships")
