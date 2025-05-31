from simple_salesforce import Salesforce
from dotenv import load_dotenv
import os

load_dotenv()

sf=Salesforce(
    username=os.getenv('SF_USERNAME'),
    password=os.getenv('SF_PASSWORD'),
    domain=os.getenv('SF_DOMAIN', 'login'),
    security_token=os.getenv('SF_SECURITY_TOKEN'),
)


def get_case_id_from_case_number(case_number: str):
    """"Get Case ID from Case number"""
    try:
        query=f"SELECT Id FROM Case WHERE CaseNumber = '{case_number}'"
        result = sf.query(query)
        case_id = result['records'][0]['Id']
        return case_id
    except Exception as e:
        print(f"Error: {e}")
        return None



def get_tickets_id(case_id:str):
    """"Get the ticket ID from a case ID. And return the case details"""
    try:
        case=sf.Case.get(case_id)
        return{
            "subject":case.get('Subject'),
            "description":case.get('Description'),
            "id": case.get('Id'),
            "status": case.get('Status'),
        }
    except Exception as e:
        print(f"Error retrieving case {case_id}: {e}")
        return None

def update_case(case_id,priority,reason):
    """Update the case with the given ID with the new priority and assignee."""
    try:
        sf.Case.update(case_id, {
            'Priority': priority,
            'Type': reason,
            'Status':'Working'
        })
        print(f"Case {case_id} updated successfully.")
        return True
    except Exception as e:
        print(f"Error updating case {case_id}: {e}")


# if __name__ == "__main__":
#     case_number = "00001524"
#     case_id = get_case_id_from_case_number(case_number)
#     ticket = get_tickets_id(case_id)
#     print(ticket)
#     if ticket:
#         update_case(case_id, "High", "Installation")  # Update th
#         print("Done")