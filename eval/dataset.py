"""
Evaluation dataset grounded in actual product, tax, CSR, and rider documents.

Sources used:
- product_brochure_healthshield_floater.html
- product_brochure_securelife_term.html
- tax_circular_life_health_insurance.pdf
- csr_disclosure_fy2024_25.docx
- rider_documentation.csv

Used for:
- RAG retrieval evaluation
- Answer correctness
- Intent classification validation
"""

EVAL_DATASET = [

    # -----------------------------------
    # HEALTHSHIELD FLOATER (Health Policy)
    # -----------------------------------
    {
        "id": "healthshield-sum-insured-options",
        "category": "policy_query",
        "question": "What sum insured options are available under HealthShield Family Floater?",
        "ground_truth": "Sum insured options are Rs. 3 lakh, 5 lakh, 10 lakh, 25 lakh, and 50 lakh.",
        "expected_source": "product_brochure_healthshield_floater.html",
    },
    {
        "id": "healthshield-preexisting-waiting",
        "category": "policy_query",
        "question": "What is the waiting period for pre-existing diseases in HealthShield?",
        "ground_truth": "Pre-existing diseases are covered after 36 months of continuous coverage.",
        "expected_source": "product_brochure_healthshield_floater.html",
    },
    {
        "id": "healthshield-ncb",
        "category": "policy_query",
        "question": "How does the No Claim Bonus work in HealthShield?",
        "ground_truth": "A 10% increase in sum insured is given for each claim-free year up to 50%, and it reduces by 10% after a claim.",
        "expected_source": "product_brochure_healthshield_floater.html",
    },
    {
        "id": "healthshield-room-rent",
        "category": "coverage_query",
        "question": "Is there a room rent limit in HealthShield?",
        "ground_truth": "Room rent is capped at 1% of sum insured per day for plans up to Rs. 5 lakh, with no cap for Rs. 10 lakh and above.",
        "expected_source": "product_brochure_healthshield_floater.html",
    },
    {
        "id": "healthshield-cashless-network",
        "category": "claim_query",
        "question": "How many hospitals are part of the HealthShield cashless network?",
        "ground_truth": "HealthShield offers cashless treatment at over 8,500 network hospitals.",
        "expected_source": "product_brochure_healthshield_floater.html",
    },

    # -----------------------------------
    # SECURELIFE TERM PLAN
    # -----------------------------------
    {
        "id": "securelife-min-sum-assured",
        "category": "policy_query",
        "question": "What is the minimum sum assured in SecureLife Term Plan?",
        "ground_truth": "The minimum sum assured is Rs. 25 lakh.",
        "expected_source": "product_brochure_securelife_term.html",
    },
    {
        "id": "securelife-premium-options",
        "category": "premium_query",
        "question": "What premium payment options are available in SecureLife?",
        "ground_truth": "Regular pay, limited pay, and single pay options are available with multiple frequency choices.",
        "expected_source": "product_brochure_securelife_term.html",
    },
    {
        "id": "securelife-rider-limit",
        "category": "policy_query",
        "question": "Is there a limit on rider premium in SecureLife?",
        "ground_truth": "Yes, total rider premium cannot exceed 30% of the base plan premium.",
        "expected_source": "product_brochure_securelife_term.html",
    },
    {
        "id": "securelife-death-benefit",
        "category": "coverage_query",
        "question": "How is the death benefit calculated in SecureLife?",
        "ground_truth": "The nominee receives the highest of sum assured, 10 times annual premium, or 105% of total premiums paid.",
        "expected_source": "product_brochure_securelife_term.html",
    },
    {
        "id": "securelife-suicide-exclusion",
        "category": "coverage_query",
        "question": "Is suicide covered under SecureLife policy?",
        "ground_truth": "Suicide within 12 months is excluded, but 80% of premiums or surrender value is paid.",
        "expected_source": "product_brochure_securelife_term.html",
    },

    # -----------------------------------
    # TAXATION (PDF)
    # -----------------------------------
    {
        "id": "tax-80c-limit",
        "category": "tax_query",
        "question": "What is the tax deduction limit under Section 80C for life insurance?",
        "ground_truth": "Up to Rs. 1,50,000 per annum, subject to premium not exceeding 10% of sum assured.",
        "expected_source": "tax_circular_life_health_insurance.pdf",
    },
    {
        "id": "tax-80d-limit",
        "category": "tax_query",
        "question": "What is the tax benefit under Section 80D for health insurance?",
        "ground_truth": "Rs. 25,000 for self/family and additional Rs. 25,000 for parents, increasing to Rs. 50,000 for senior citizens.",
        "expected_source": "tax_circular_life_health_insurance.pdf",
    },
    {
        "id": "tax-maturity-taxation",
        "category": "tax_query",
        "question": "Are maturity proceeds from life insurance taxable?",
        "ground_truth": "They are exempt under Section 10(10D) unless premium exceeds Rs. 5,00,000 annually for policies issued after April 2023.",
        "expected_source": "tax_circular_life_health_insurance.pdf",
    },
    {
        "id": "tax-tds",
        "category": "tax_query",
        "question": "When is TDS applicable on insurance payouts?",
        "ground_truth": "TDS at 5% applies on taxable payouts exceeding Rs. 1,00,000 on the income portion.",
        "expected_source": "tax_circular_life_health_insurance.pdf",
    },

    # -----------------------------------
    # CSR DISCLOSURE
    # -----------------------------------
    {
        "id": "csr-spend-obligation",
        "category": "general_query",
        "question": "What is the CSR spending requirement for the company?",
        "ground_truth": "The company must spend at least 2% of the average net profits of the last three years.",
        "expected_source": "csr_disclosure_fy2024_25.docx",
    },
    {
        "id": "csr-actual-spend",
        "category": "general_query",
        "question": "How much did the company spend on CSR in FY 2024-25?",
        "ground_truth": "The company spent Rs. 18.6 crore against an obligation of Rs. 18.4 crore.",
        "expected_source": "csr_disclosure_fy2024_25.docx",
    },
    {
        "id": "csr-focus-areas",
        "category": "general_query",
        "question": "What are the main CSR focus areas?",
        "ground_truth": "Financial literacy, healthcare access, education, disaster relief, and environmental sustainability.",
        "expected_source": "csr_disclosure_fy2024_25.docx",
    },

    # -----------------------------------
    # EDGE CASES (Agent behavior)
    # -----------------------------------
    {
        "id": "greeting",
        "category": "small_talk",
        "question": "Hello, can you help me?",
        "ground_truth": "Hello! I can help you with insurance policies, claims, and tax-related queries.",
        "expected_source": None,
    },
    {
        "id": "out-of-scope",
        "category": "out_of_scope",
        "question": "Who won the cricket match yesterday?",
        "ground_truth": "I can help only with insurance-related queries. Please ask about policies, claims, or coverage.",
        "expected_source": None,
    },
]