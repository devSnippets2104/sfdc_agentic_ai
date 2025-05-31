from dotenv import load_dotenv
import os
from openai import OpenAI
import json
load_dotenv()

OPEN_AI_API_KEY = os.getenv('OPEN_AI_API_KEY')

def triage_prompt(subject:str,description:str) -> str:
    """Prompt to handle the traige of a ticket"""
    return f"""
        You are a support ticket triage agent.
        Based on the ticket's subject and description, assign:

        - Category: One of [Mechanical, Electrical, Electronic, Structural, Others, Installation]
        - Priority: One of [High, Medium, Low]
        - Assignee: One of [billing_team, tech_team, support_team]

        Respond in JSON only.

        Subject: {subject}
        Description: {description}
    """

def get_triage_response(prompt,subject: str, description: str) -> dict:
    """Get the triage response from OpenAI API"""
    try:
        client=OpenAI(
            api_key=OPEN_AI_API_KEY
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a support ticket triage agent."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        # response_json = json.loads(response)
        response_json= json.loads(response.choices[0].message.content)
        # print(f"OpenAI API Response: {response_json}")
        return response_json
    except Exception as e:
        print(f"Error in OpenAI API call: {e}")
        return None


# if __name__ == "__main__":
#     # Example usage
#     subject = "Installation issue with the new device"
#     description = "The device does not power on after installation. Please assist."
#     prompt=triage_prompt(subject, description)
#     response = get_triage_response(prompt,subject, description)
#     if response:
#         print(f"Triage Response: {response}")
#     else:
#         print("Failed to get triage response.")