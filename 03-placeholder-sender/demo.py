"""Demo script for placeholder meeting sender (Multiple Time Slots)."""
import asyncio
import csv
from auth_delegated import DelegatedAuthProvider
from msgraph.generated.models.event import Event
from msgraph.generated.models.item_body import ItemBody
from msgraph.generated.models.body_type import BodyType
from msgraph.generated.models.date_time_time_zone import DateTimeTimeZone
from msgraph.generated.models.attendee import Attendee
from msgraph.generated.models.email_address import EmailAddress
from msgraph.generated.models.attendee_type import AttendeeType
from kiota_abstractions.base_request_configuration import RequestConfiguration


# ======================================================
# UTILITY FUNCTIONS - READ INPUTS
# ======================================================

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


def read_attendees(filename):
    attendees_list = []

    with open(file=filename, mode = "r") as file:
        csvFile = csv.reader(file)
        for attendee_info in csvFile:
            name = attendee_info[0]
            mail = attendee_info[1]
            attendees_list.append((name, mail))
    
    attendee_objs = get_attendees(attendees_list)

    return attendee_objs

def read_times(filename):
    time_slots = []

    with open(file=filename, mode = "r") as file:
        csvFile = csv.reader(file)
        for times_info in csvFile:
            start = times_info[0]
            end = times_info[1]
            label = times_info[2]
            time_slots.append({
                "start": start,
                "end": end,
                "label": label
            })
    return time_slots

def read_meeting_info(filename):
    subject = ""
    body = ""
    
    with open(file = filename, mode = "r") as file:
        for i, line in enumerate(file):
            if i == 0:
                subject = line
            elif i == 1:
                body = line
            else:
                break
    
    return subject, body 


# =======================================================
# OTHER INPUT VARIABLES  
# =======================================================


TIME_ZONE = "Pacific Standard Time"

# =======================================================
# SEND PLACEHOLDER FUNCTION 
# =======================================================


async def send_placeholder(client, meeting_subject, content, attendees, start_time, end_time, slot_label):
    """Send placeholder meeting invite to attendees."""
    request_body = Event(
        subject=f"{meeting_subject} ({slot_label})",
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

# =======================================================
# MAIN FUNCTION
# =======================================================


async def main():
    """Main demo function."""

    # READ INPUT VARIABLES - CHANGE FILES IN ./input FOLDER

    # Attendees
    ATTENDEES_LIST = read_attendees("./input/attendees.csv")
    print(ATTENDEES_LIST)

    # Time slots
    TIME_SLOTS = read_times("./input/times.csv")
    print(TIME_SLOTS)

    # Meeting info
    MEETING_SUBJECT, MEETING_BODY = read_meeting_info("./input/placeholder_info.txt")

    print("=" * 70)
    print(" MULTIPLE PLACEHOLDER MEETING SENDER")
    print("=" * 70)
    print(f" Recipients: {len(ATTENDEES_LIST)}")
    print(f" Time slots: {len(TIME_SLOTS)}")
    print()

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
                MEETING_SUBJECT,
                MEETING_BODY, 
                ATTENDEES_LIST, 
                start_time, 
                end_time, 
                slot["label"]
            )

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

    print("\n All placeholders sent! Recipients will receive multiple invites.")

    return 0

if __name__ == "__main__":
    exit(asyncio.run(main()))
