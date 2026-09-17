from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse

app = FastAPI()


class UserRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "message": "Welcome to Veridian IT Support Agent!"
    }


@app.post("/ask")
def ask_agent(request: UserRequest):

    message = request.message.lower()

    response = ""
    category = ""
    action = ""

    # 1. PASSWORD RESET

    if "password" in message or "locked out" in message:

        category = "Password Reset"

        if "6 times" in message or "7 times" in message or "8 times" in message:
            response = (
                "Your account may be locked after more than 5 failed attempts. "
                "Please contact IT to unlock your account manually. "
                "No approval is required."
            )
            action = "Route to IT"

        else:
            response = (
                "You can reset your password using the self-service portal "
                "at any time."
            )
            action = "Self-service"


    # 2. VPN ACCESS

    elif "vpn" in message:

        category = "VPN Access"

        if "contractor" in message:
            response = (
                "Contractors require manager approval submitted through "
                "the access request form."
            )
            action = "Manager approval"

        elif "expired" in message:
            response = (
                "VPN credentials expire every 90 days. "
                "Please renew your credentials."
            )
            action = "Credential renewal"

        else:
            response = (
                "VPN access is granted automatically to all full-time employees."
            )
            action = "Inform employee"


    # 3. LAPTOP REPLACEMENT

    elif "laptop" in message or "computer" in message:

        category = "Laptop Support"

        if "replacement" in message:

            response = (
                "Laptops are eligible for replacement after 3 years of service, "
                "or earlier in case of verified hardware failure. "
                "Requests must be raised at least 2 weeks in advance."
            )

            action = "Check eligibility"

        else:

            response = (
                "Please provide more details about your laptop issue. "
                "If a hardware failure is verified, earlier replacement "
                "may be possible."
            )

            action = "Human IT review"


    # 4. SOFTWARE INSTALLATION

    elif "software" in message or "install" in message:

        category = "Software Installation"

        response = (
            "Standard software in the approved catalog can be self-installed. "
            "Non-catalog software requires IT Security review, "
            "which takes 3–5 business days."
        )

        action = "Security review if non-catalog"


    # 5. PRINTER

    elif "printer" in message:

        category = "Printer Troubleshooting"

        response = (
            "First check the printer queue and restart the print spooler. "
            "If the issue continues, log a ticket with the printer's asset tag."
        )

        action = "Troubleshooting"


    # 6. EMAIL QUOTA

    elif "mailbox" in message or "email storage" in message:

        category = "Email Mailbox Quota"

        response = (
            "The default mailbox quota is 25GB. "
            "You should archive old emails when nearing the quota. "
            "Quota increases require manager approval and are capped at 50GB."
        )

        action = "Manager approval if increase required"


    # 7. GUEST WI-FI

    elif "guest wifi" in message or "guest wi-fi" in message:

        category = "Guest Wi-Fi"

        response = (
            "Guest Wi-Fi credentials are valid for 24 hours. "
            "Any employee can generate credentials using the front-desk kiosk. "
            "No IT ticket is required."
        )

        action = "Self-service"


    # 8. EXPENSE SOFTWARE

    elif "expense" in message:

        category = "Expense Software Access"

        response = (
            "Access to the expense management tool is granted by Finance, "
            "not IT. IT can assist with login or technical issues "
            "once an account already exists."
        )

        action = "Finance or IT technical support"


    # 9. SECURITY INCIDENT

    elif (
        "phishing" in message
        or "malware" in message
        or "unauthorized access" in message
    ):

        category = "Security Incident"

        response = (
            "Report the suspected security incident immediately to "
            "security@veridian-corp.example. "
            "Do not forward the suspicious email to other employees."
        )

        action = "Escalate to Security"


    # 10. WORK FROM HOME

    elif (
        "work from home" in message
        or "home office" in message
        or "monitor" in message
        or "chair" in message
    ):

        category = "Work-From-Home Equipment"

        response = (
            "Employees working remotely more than 3 days per week "
            "are eligible for a one-time home office equipment allowance. "
            "Manager sign-off and Finance processing are required. "
            "IT handles equipment shipping after approval."
        )

        action = "Manager and Finance approval"


    # UNKNOWN REQUEST

    else:

        category = "Unknown"

        response = (
            "I could not find a specific policy for your request. "
            "Please provide more details or route the issue to human IT support."
        )

        action = "Human IT review"


    return {
        "category": category,
        "response": response,
        "recommended_action": action
    }
# Existing Ticket Queue

tickets = [
    {
        "ticket_id": "TK-1042",
        "employee": "R. Verma",
        "issue": "VPN credential expired",
        "status": "Resolved"
    },
    {
        "ticket_id": "TK-1043",
        "employee": "S. Iyer",
        "issue": "Laptop replacement",
        "status": "Approved - Pending Fulfillment"
    },
    {
        "ticket_id": "TK-1044",
        "employee": "A. Khan",
        "issue": "Non-catalog software request",
        "status": "Pending Security Review"
    },
    {
        "ticket_id": "TK-1047",
        "employee": "K. Singh",
        "issue": "Home office equipment request",
        "status": "Pending Finance"
    },
    {
        "ticket_id": "TK-1048",
        "employee": "T. Rao",
        "issue": "Phishing email reported",
        "status": "Escalated to Security"
    }
]


@app.get("/tickets")
def get_tickets():
    return {
        "tickets": tickets
    }
@app.get("/app")
def serve_frontend():
    return FileResponse("index.html")
@app.post("/route-ticket")
def route_ticket(request: UserRequest):

    message = request.message.lower()

    if "phishing" in message or "malware" in message:
        return {
            "category": "Security Incident",
            "assigned_to": "Security Team",
            "priority": "Immediate",
            "status": "Escalated",
            "reason": "Security incidents must be reported immediately."
        }

    elif "expense" in message:
        return {
            "category": "Expense Software",
            "assigned_to": "Finance",
            "priority": "Normal",
            "status": "Routed",
            "reason": "Finance manages expense software access."
        }

    elif "contractor" in message and "vpn" in message:
        return {
            "category": "VPN Access",
            "assigned_to": "Manager",
            "priority": "Normal",
            "status": "Waiting for Approval",
            "reason": "Contractors require manager approval."
        }

    elif "software" in message and "install" in message:
        return {
            "category": "Software Installation",
            "assigned_to": "IT Security",
            "priority": "Normal",
            "status": "Pending Review",
            "reason": "Non-catalog software requires Security review."
        }

    else:
        return {
            "category": "General IT Support",
            "assigned_to": "IT Support",
            "priority": "Normal",
            "status": "Open",
            "reason": "Issue requires further assessment."
        }