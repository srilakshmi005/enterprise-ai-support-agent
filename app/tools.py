import uuid


def create_support_ticket(issue):
    """Create a support ticket for issues requiring human assistance."""

    ticket_id = "IT-" + str(uuid.uuid4())[:8].upper()

    return {
        "ticket_id": ticket_id,
        "status": "Created",
        "issue": issue,
        "message": "Your issue has been escalated to human IT support."
    }
