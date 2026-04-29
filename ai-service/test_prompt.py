from pathlib import Path

# Load prompt
prompt = Path("prompts/describe_prompt.txt").read_text()

# Sample inputs
test_inputs = [
    "Company dumping chemical waste into river",
    "Employees not provided safety equipment in factory",
    "CEO involved in financial fraud",
    "Excessive carbon emissions from manufacturing plant",
    "Child labor used in supply chain"
]

for i, inp in enumerate(test_inputs, 1):
    print(f"\n--- Test Case {i} ---")
    print(prompt.replace("{input}", inp))