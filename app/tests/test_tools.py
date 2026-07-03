import sqlite3
import textwrap

DB_NAME = "insurance_tests.db"

# ----------------------------
# 1. SQLITE SETUP
# ----------------------------
def get_conn():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS test_cases (
        id INTEGER PRIMARY KEY,
        category TEXT,
        query TEXT,
        multi_turn_group INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS test_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_id INTEGER,
        response TEXT,
        passed INTEGER,
        notes TEXT
    )
    """)

    conn.commit()
    conn.close()


# ----------------------------
# 2. TEST DATA
# ----------------------------
TESTS = [
    (1, "Tool Usage", "I’m 28 and single. What insurance should I buy first?", None),
    (2, "Tool Usage", "Compare 3 term life plans for a 35-year-old female.", None),
    (3, "Tool Usage", "What is the premium for a 20L health plan, family of 4?", None),
    (4, "Tool Usage", "Do I need a critical illness rider if I already have health insurance?", None),
    (5, "Tool Usage", "What coverage gaps do I have based on my current policies?", None),

    (6, "FAQ", "Explain the difference between indemnity and benefit plans.", None),
    (7, "FAQ", "Which insurer has the best claim settlement ratio?", None),

    (8, "Follow-up", "I’m a diabetic — which health plans will cover me?", None),
    (9, "Follow-up", "Calculate premium for a 1Cr term plan, age 40, smoker.", None),
    (10, "Follow-up", "Should I choose a higher deductible to save on premium?", None),
    (11, "Follow-up", "What riders are available for my existing policy?", None),
    (12, "Follow-up", "How much life cover do I need based on the income replacement method?", None),
    (13, "Follow-up", "Compare ULIPs vs. term + mutual fund combination.", None),
    (14, "Follow-up", "I’m retiring in 5 years. What insurance adjustments should I make?", None),

    (15, "Multi-turn", "Is a super top-up plan better than increasing base cover?", 1),
    (16, "Multi-turn", "What is the waiting period for maternity coverage?", 1),
    (17, "Multi-turn", "Suggest a child education plan with insurance component.", 1),
    (18, "Multi-turn", "My parents are 62 and 58. What health plan options exist?", 1),
    (19, "Multi-turn", "What tax benefits can I claim on my insurance premiums?", 1),
    (20, "Multi-turn", "Generate a full insurance portfolio recommendation for my family.", 1),
]


def seed_data():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("DELETE FROM test_cases")

    cur.executemany("""
        INSERT INTO test_cases (id, category, query, multi_turn_group)
        VALUES (?, ?, ?, ?)
    """, TESTS)

    conn.commit()
    conn.close()


# ----------------------------
# 3. YOUR COPILOT (REPLACE THIS)
# ----------------------------
def insurance_copilot(query, history=None):
    """
    Replace this with:
    - LangChain agent
    - LLM API call
    - tool-using system
    """
    return f"[MOCK RESPONSE] {query}"


# ----------------------------
# 4. SIMPLE EVALUATOR
# ----------------------------
KEYWORDS = {
    "term": ["term insurance", "life cover"],
    "health": ["health insurance", "hospital"],
    "rider": ["add-on", "coverage"],
    "tax": ["80c", "80d"],
    "claim": ["settlement", "ratio"],
}


def evaluate(query, response):
    q = query.lower()
    r = response.lower()

    for k, words in KEYWORDS.items():
        if k in q:
            if any(w in r for w in words):
                return True
    return False


# ----------------------------
# 5. RUN TESTS
# ----------------------------
def run_tests():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id, query, multi_turn_group FROM test_cases ORDER BY id")
    rows = cur.fetchall()

    history = {}

    for test_id, query, group in rows:
        if group:
            history.setdefault(group, [])

        response = insurance_copilot(query, history.get(group))

        print("\n" + "-" * 60)
        print(f"Test ID: {test_id}")
        print("Query:", query)
        print("Response:", response)

        passed = evaluate(query, response)

        cur.execute("""
            INSERT INTO test_results (test_id, response, passed, notes)
            VALUES (?, ?, ?, ?)
        """, (test_id, response, int(passed), "auto-eval"))

    conn.commit()
    conn.close()


# ----------------------------
# 6. REPORT
# ----------------------------
def report():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            COUNT(*),
            SUM(passed),
            (COUNT(*) - SUM(passed))
        FROM test_results
    """)

    total, passed, failed = cur.fetchone()

    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print("Total :", total)
    print("Passed:", passed)
    print("Failed:", failed)


# ----------------------------
# 7. MAIN
# ----------------------------
if __name__ == "__main__":
    init_db()
    seed_data()
    run_tests()
    report()