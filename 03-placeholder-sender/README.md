# Placeholder Meeting Sender (Multiple Time Slots)

This demo sends **multiple placeholder meeting invites** to a list of participants, one invite per candidate time slot, 
using the Microsoft Graph Python SDK and delegated authentication. It’s useful when you want to propose several possible times and let attendees accept/decline each one.

## What it does

- Reads attendees from `./input/attendees.csv`
- Reads candidate time slots from `./input/times.csv`
- Reads meeting subject/body from `./input/placeholder_info.txt`
- Creates an Outlook calendar event for each time slot using `POST /me/events` (delegated), inviting all attendees

## Folder structure

Recommended layout:

placeholder-sender/
├─ demo.py
├─ auth_delegated.py
├─ config.py
├─ requirements.txt
├─ input/
│ ├─ attendees.csv
│ ├─ times.csv
│ └─ placeholder_info.txt
└─ .env.example


## Prerequisites

- Python 3.10+ recommended
- A Microsoft 365 tenant user account to sign in with
- An app registration in Microsoft Entra ID configured for **delegated** auth (public client)

## Entra ID app registration (delegated)

1. Entra ID → **App registrations** → **New registration**
2. Create an app (single-tenant is fine for a demo)
3. Go to **Authentication**
   - Enable **Allow public client flows** (required for device code / interactive browser flows)
4. Go to **API permissions** → add **Microsoft Graph (Delegated)**:
   - `User.Read`
   - `Calendars.ReadWrite`

### Consent note (important)

- Depending on your tenant’s “User consent settings”, non-admin users may not be allowed to consent to `Calendars.ReadWrite` and will only see **Request admin approval**.
- If you want every user to decide, your tenant must allow user consent for that permission; otherwise an admin must grant consent once for the tenant.

## Configuration

### `.env.example`

Create a `.env.example` (commit this) and `.env` (do not commit) like:

```ini
CLIENT_ID=your-app-client-id
TENANT_ID=your-tenant-id
GRAPH_SCOPES=User.Read Calendars.ReadWrite
```

**GRAPH_SCOPES** must be space-separated, since your config.py typically splits it into a list.

```markdown
## Input files

### 1) `./input/attendees.csv`
CSV format (no header), one attendee per line:

```csv
Grady Archie,GradyA@contoso.com
Lidia Holloway,LidiaH@contoso.com
Diego Siciliani,DiegoS@contoso.com
```

### 2) `./input/times.csv`
CSV format (no header), one time slot per line:

```csv
2026-02-20T10:00:00,2026-02-20T11:00:00,Slot 1
2026-02-20T14:00:00,2026-02-20T15:00:00,Slot 2
2026-02-20T16:00:00,2026-02-20T17:00:00,Slot 3
```

Notes:
- Use ISO-like local date-time strings as shown.
- The demo applies a single `TIME_ZONE` to all slots.

### 3) `./input/placeholder_info.txt`
The script reads:
- Line 1 = subject
- Line 2 = body (HTML)

Example:

```text
PLACEHOLDER - VERY IMPORTANT CLIENT
<h2>PLACEHOLDER - VERY IMPORTANT CLIENT</h2><p>Waiting the client to reply</p>
```

Tip: Keep subject and body on a single line each (the current reader stops after line 2).

## Time zone

The demo uses:

```python
TIME_ZONE = "Pacific Standard Time"
```

It sets:
- `DateTimeTimeZone.time_zone = TIME_ZONE`
- Header `Prefer: outlook.timezone="Pacific Standard Time"`

If you prefer your local time zone, change `TIME_ZONE` to the appropriate Outlook time zone name.

## Install & run

From your repo root (with venv activated):

```bash
pip install -r requirements.txt
python demo.py
```

On first run you’ll be prompted to sign in (device code or browser, depending on your `DelegatedAuthProvider` implementation).

## Expected output

The script:
- Loads attendees and time slots from the CSV files
- Creates one meeting per slot
- Prints a web link for each created event

Example:

```text
Slot 1: https://outlook.office.com/calendar/item/...
Slot 2: https://outlook.office.com/calendar/item/...
Slot 3: https://outlook.office.com/calendar/item/...
All placeholders sent! Recipients will receive multiple invites.
```

Recipients will receive multiple invitations (one per slot) and can accept/decline individually.

## Troubleshooting

**“Need admin approval” / only “Request admin approval”**

Your tenant does not allow user consent for the requested permission(s), or the permission is considered higher impact by policy. Ask an admin to grant consent for the app, or adjust tenant consent settings.

**AADSTS7000218 (asks for `client_secret` / `client_assertion`)**

Your app is not configured as a public client. Enable **Allow public client flows** in the app registration and ensure you’re using a delegated credential (Device Code / Interactive Browser) without a client secret.

**Past dates**

If you use dates in the past, Outlook may behave unexpectedly. Use future time slots.

---

