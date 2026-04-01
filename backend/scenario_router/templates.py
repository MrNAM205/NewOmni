TRAFFIC_TEMPLATE = """
Here’s a neutral, procedural outline for handling a traffic-related situation:

1. Locate the citation and note:
   - citation number
   - date issued
   - deadline or court date
   - issuing agency

2. Read the instructions printed on the citation.
   These usually explain:
   - payment options
   - appearance requirements
   - deadlines
   - contact information

3. Keep copies of:
   - the citation
   - any notices received
   - any payment confirmations

4. If unsure about next steps, contact the clerk’s office listed on the citation.
"""

BILLING_TEMPLATE = """
Here’s a neutral, procedural outline for understanding a bill or remittance coupon:

1. Identify:
   - account number
   - billing period
   - due date
   - total amount due

2. Review the remittance coupon:
   - payment address
   - reference numbers
   - detachable portion instructions

3. Keep copies of:
   - the bill
   - payment confirmations
   - any correspondence

4. Use the payment channels listed on the bill:
   - mail
   - online portal
   - phone
   - in-person (if available)
"""

ADMIN_TEMPLATE = """
Here’s a neutral, procedural outline for handling an administrative notice:

1. Identify:
   - issuing office
   - reference number
   - deadline
   - required documents

2. Read the instructions carefully.
   Notices usually explain:
   - what is being requested
   - where to send documents
   - how to contact the office

3. Keep copies of everything.
"""

def detect_domain(text: str) -> str:
    t = text.lower()

    if any(k in t for k in ["ticket", "citation", "court", "traffic", "violation"]):
        return "traffic"

    if any(k in t for k in ["bill", "statement", "invoice", "remittance", "coupon"]):
        return "billing"

    if any(k in t for k in ["notice", "form", "deadline", "office", "agency"]):
        return "administrative"

    return "general"

def build_procedural_outline(domain: str, text: str) -> str:
    if domain == "traffic":
        return TRAFFIC_TEMPLATE
    if domain == "billing":
        return BILLING_TEMPLATE
    if domain == "administrative":
        return ADMIN_TEMPLATE
    return "Here’s a general procedural outline:

1. Capture the key facts.
2. Identify any dates or deadlines.
3. Keep copies of all documents."
