"""Demo script for placeholder meeting sender (Multiple Time Slots)."""
import asyncio
from auth_delegated import DelegatedAuthProvider
from msgraph.generated.models.event import Event
from msgraph.generated.models.item_body import ItemBody
from msgraph.generated.models.body_type import BodyType
from msgraph.generated.models.date_time_time_zone import DateTimeTimeZone
from msgraph.generated.models.attendee import Attendee
from msgraph.generated.models.email_address import EmailAddress
from msgraph.generated.models.attendee_type import AttendeeType
from kiota_abstractions.base_request_configuration import RequestConfiguration

# =======================================================
# INPUT VARIABLES - CHANGE THESE FOR YOUR MEETINGS
# =======================================================
ATTENDEES_LIST = [
    ("Grady Archie", "GradyA@M365x89922257.onmicrosoft.com"),
    ("Lidia Holloway", "LidiaH@M365x89922257.onmicrosoft.com"),
    ("Diego Siciliani", "DiegoS@M365x89922257.onmicrosoft.com")
]

MEETING_SUBJECT = "PLACEHOLDER - VERY IMPORTANT CLIENT"
MEETING_BODY = """
<h2>PLACEHOLDER - VERY IMPORTANT CLIENT</h2>
<p>Waiting for client confirmation.</p>
"""

# MULTIPLE TIME SLOTS - Recipients get ALL these invites
TIME_SLOTS = [
    {"start": "2026-02-20T10:00:00", "end": "2026-02-20T11:00:00", "label": "Slot 1"},
    {"start": "2026-02-20T14:00:00", "end": "2026-02-20T15:00:00", "label": "Slot 2"}, 
    {"start": "2026-02-20T16:00:00", "end": "2026-02-20T17:00:00", "label": "Slot 3"},
]

TIME_ZONE = "Pacific Standard Time"
# =======================================================

async def send_placeholder(client, content, attendees, start_time, end_time, slot_label):
    """Send placeholder meeting invite to attendees."""
    request_body = Event(
        subject=f"{MEETING_SUBJECT} ({slot_label})",
        body=ItemBody(
            content_type=BodyType.Html,
            content=f"{content}<p><strong>Time Slot: {slot_label}</strong></p>",
        ),
        start=start_time,
        end=end_time,
        attendees=attendees,
        allow_new_time_proposals=True,
        is_reminder_on=True,
    )

    request_configuration = RequestConfiguration()
    request_configuration.headers.add("Prefer", f'outlook.timezone="{TIME_ZONE}"')

    result = await client.me.events.post(request_body, request_configuration=request_configuration)
    print(f" {slot_label}: {result.web_link}")
    return result

def get_attendees(attendees_list):
    """Convert attendees list to Graph Attendee objects."""
    attendees = []
    for name, mail in attendees_list:
        attendee = Attendee(
            email_address=EmailAddress(
                address=mail,
                name=name,
            ),
            type=AttendeeType.Required,
        )
        attendees.append(attendee)
    return attendees

async def main():
    """Main demo function."""
    print("=" * 70)
    print(" MULTIPLE PLACEHOLDER MEETING SENDER")
    print("=" * 70)
    print(f" Recipients: {len(ATTENDEES_LIST)}")
    print(f" Time slots: {len(TIME_SLOTS)}")
    print()

    attendees = get_attendees(ATTENDEES_LIST)

    try:
        # Setup delegated authentication
        auth = DelegatedAuthProvider()
        client = auth.get_client()

        # Send ALL placeholder meetings
        print(" Sending meeting invites...\n")
        for slot in TIME_SLOTS:
            start_time = DateTimeTimeZone(
                date_time=slot["start"],
                time_zone=TIME_ZONE,
            )
            end_time = DateTimeTimeZone(
                date_time=slot["end"],
                time_zone=TIME_ZONE,
            )
            
            await send_placeholder(
                client, 
                MEETING_BODY, 
                attendees, 
                start_time, 
                end_time, 
                slot["label"]
            )

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

    print("\n All placeholders sent! Recipients will receive multiple invites.")
    print("They can Accept/Decline each one independently.")
    return 0

if __name__ == "__main__":
    exit(asyncio.run(main()))
