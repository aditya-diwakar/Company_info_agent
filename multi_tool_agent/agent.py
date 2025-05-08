import pandas as pd
from google.adk.agents import Agent

# Load the CSV data
df = pd.read_csv("/home/aditya/Desktop/progs/companies.csv")

# Tool 1: Get full company info
def get_company_info(name: str) -> dict:
    match = df[df["name"].str.lower() == name.lower()]
    if match.empty:
        return {"status": "error", "error_message": f"No data found for '{name}'."}
    else:
        info = match.iloc[0].to_dict()
        result = (
            f"{info['name']} is a {info['industry']} company based in {info['location']} "
            f"with {info['employees']} employees and annual revenue of ${info['revenue']}."
        )
        return {"status": "success", "result": result}

# Tool 2: Get number of employees
def get_employee_count(name: str) -> dict:
    match = df[df["name"].str.lower() == name.lower()]
    if match.empty:
        return {"status": "error", "error_message": f"No data found for '{name}'."}
    else:
        employees = match.iloc[0]["employees"]
        return {"status": "success", "result": f"{name} has {employees} employees."}

# Root agent with both tools
root_agent = Agent(
    name="company_info_agent",
    model="gemini-2.0-flash",
    description="Agent that can answer questions about companies from a CSV file.",
    instruction="Answer questions about companies based on their information from the CSV.",
    tools=[get_company_info, get_employee_count],
)
