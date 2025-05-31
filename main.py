from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
import json
from salesforce_agent import get_case_id_from_case_number, get_tickets_id, update_case
from triage_agent import get_triage_response, triage_prompt
import uvicorn

load_dotenv()
app = FastAPI()

@app.get("/triage/{case_number}")
def triage(case_number:str):
    try:
        case_id = get_case_id_from_case_number(case_number)
        if not case_id:
            raise HTTPException(status_code=404, detail="Case not found")
        ticket = get_tickets_id(case_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        prompt= triage_prompt(ticket['subject'], ticket['description'])
        result = get_triage_response(prompt,ticket['subject'], ticket['description'])
        # print(f"Triage response: {result}")
        if not result:
            raise HTTPException(status_code=500, detail="Failed to get triage response")
        success=update_case(case_id, result['Priority'], result['Category'])
        print(success)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update case")
        return {
            "case_id": case_id,
            "priority": result['Priority'],
            "category": result['Category']
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8100, reload=True)





# To run this file user python -m uvicorn main:app --reload --port 8100