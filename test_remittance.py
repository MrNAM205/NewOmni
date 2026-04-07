import json
from backend.scenario_engine_v2.router import run_scenario_engine

test_input = """
Please return this portion with your payment.

Account Number: 123-456-789
Amount Enclosed: $100.00

Remit to:
PO Box 1234
Anytown, USA 12345

000123456789  4829-3341  0014287
"""

output = run_scenario_engine(test_input)
print(json.dumps(output, indent=2))
