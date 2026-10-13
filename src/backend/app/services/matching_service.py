import sqlite3
from datetime import datetime, date
from . import database as db


def extract_entities(profile_text):
    """
    Very basic entity extraction — returns keywords.
    Later: replace with spaCy / OpenAI NLP pipeline.
    """
    # Normalize text
    text = profile_text.lower()
    # Known categories (Indian scholarship classification)
    categories = ["general", "sc", "st", "obc", "pwd", "social_sc", "social_st", "social_obc", "general_girls"]
    results = {
        "degree": "",
        "year": 0,
        "institution": "",
        "category": "",
        "min_percentage": 0,
        "income_ceiling": 0.0,
    }
    for cat in categories:
        if cat in text:
            results["category"] = cat
    # crude parsing
    for kw in ["12th", "10th", "9th", "b.tech", "bbe", "diploma"]:
        if kw in text:
            results["degree"] = kw
            break
    for kw in ["first year", "2", "second year", "3rd year", "third year"]:
        if kw in text:
            results["year"] = {"first year": 1, "second year": 2, "2": 2, "3rd year": 3, "third year": 3}.get(kw, 2)
            break
    # extract numeric ranges: income < 4.5 lakh -> 450000
    import re
    m = re.search(r"income\s*\u003c\s*([a-z0-9.]+)\s*(?:lakh|cr|k|rs|rupees?)", text)
    if m:
        val = float(m.group(1).replace("crore", "10000000").replace("cr", "1000000").replace(",", "").strip())
        if "lakh" in text.lower():
            val = val * 100000
        results["income_ceiling"] = val
    # min percentage
    m = re.search(r"(\d+)%+", text)
    if m:
        results["min_percentage"] = int(m.group(1))
    return results


def list_scholarships(limit=50, categories=None, status=None):
    conn = db.get_db()
    conditions = []
    params = []
    if categories:
        conditions.append("category IN (" + ",".join(["?"]*len(categories)) + ")")
        params.extend(categories)
    if status:
        conditions.append("status IN (" + ",".join(["?"]*len(status)) + ")")
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
        (data["name"], data["org"], data.get("category",""), data.get("eligibility_criteria",""),
         data.get("deadline",""), data.get("documents",""), data.get("url",""))
    )
    conn.commit()
    return cur.lastrowid


def check_eligibility(student_id, limit=50):
    """
    Returns top-N scholarships matched to a student.
    Uses hard-rule matching + keyword scoring.
    """
    conn = db.get_db()
    students = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if not students:
        return {"error": "student not found"}, 404
    student = dict(students)
    
    # Fetch relevant scholarships
    scholars = list_scholarships(limit=100)
    
    scored = []
    for sc in scholars:
        score = 0
        criteria = sc.get("eligibility_criteria", "").lower()
        # Hard rules
        if student.get("category") in ("ww", "sc", "st"):
            if "sc" in criteria or "st" in criteria:
                score += 20
        # Category match
        if student.get("category") and student.get("category") in criteria:
            score += 15
        # Income check
        if student.get("annual_income", 0) <= sc.get("income_ceil", 99999999):
            score += 12
        # Year/program check
        if student.get("degree") in criteria:
            score += 10
        # Parse criteria income ceiling
        import re
        m = re.search(r"income\s*\u003c\s*([a-z0-9.]+)\s*(?:lakh|cr)?", criteria)
        if m:
            ce = float(m.group(1).replace("crore","10000000").replace("cr","1000000").replace(",",""))
            if "lakh" in criteria.lower():
                ce = ce * 100000
            if student.get("annual_income", 0) <= ce:
                score += 10
        # Deadline urgency (within 30 days)
        import datetime
        try:
            dl = datetime.datetime.strptime(sc.get("deadline",""), "%Y-%m-%d")
            now = datetime.datetime.now()
            days = (dl - now).days
            if days <= 30 and days > 0:
                score += 8
            elif days < 0:
                score += 2  # overdue warning
        except:
            pass
        # disabled support (wc, etc)
        if "disability" in criteria or "40%" in criteria or "pw" in criteria:
            if student.get("disability_pct", 0) >= 40:
                score += 10
        # female-only
        if "girl" in criteria and student.get("category") == "general_girls":
            score += 10
        # min marks
        if student.get("degree") and student.get("degree") != "10th":
            mm = re.search(r"min\s+(\d+)%", criteria)
            if mm:
                if "9" in str(student.get("degree")) or "12" in str(student.get("degree")):
                    score += 5
        scored.append((sc, score))
    
    # Sort by score desc
    scored.sort(key=lambda x: x[1], reverse=True)
    
    return {
        "student_id": student["id"],
        "student_name": student.get("name"),
        "matches": [
            {"scholarship": s["id"], "score": sc, "details": s}
            for s, sc in scored[:limit]
        ]
    }
