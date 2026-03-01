# solicitor/google_importer.py
import os
import datetime
import yaml
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these SCOPES, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly", "https://www.googleapis.com/auth/gmail.readonly"]

def get_credentials():
    """Gets user credentials from a client_secret.json file."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def search_calendar(creds):
    """Searches Google Calendar for past music events."""
    gigs = []
    try:
        service = build("calendar", "v3", credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        
        # Search for events with keywords
        query_keywords = ["gig", "concert", "live at", "presents"]
        for keyword in query_keywords:
            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    q=keyword,
                    timeMax=now,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])

            if not events:
                print(f"No past calendar events found with keyword: {keyword}")
                continue

            for event in events:
                summary = event.get("summary", "").lower()
                location = event.get("location", "")
                start = event.get("start", {}).get("dateTime", event.get("start", {}).get("date"))
                
                # Basic filtering to avoid false positives
                if "gig" in summary or "concert" in summary or "live" in summary:
                    gigs.append({
                        "artist": event["summary"],
                        "date": start.split("T")[0],
                        "venue": location.split(",")[0] if location else "TBA",
                        "city": location.split(",")[1].strip() if "," in location else "TBA",
                        "type": "gig",
                        "source": "google_calendar"
                    })

    except HttpError as error:
        print(f"An error occurred with Google Calendar: {error}")
    
    return gigs

def search_gmail(creds):
    """Searches Gmail for ticket receipts."""
    gigs = []
    try:
        service = build("gmail", "v1", credentials=creds)
        
        # Search for emails from ticket vendors
        query_keywords = [
            'from:ticketmaster "your order"',
            'from:seetickets "order confirmation"',
            'from:eventbrite "your ticket for"',
            'from:livenation "order confirmation"',
            'subject:"Your tickets for"'
        ]
        
        for keyword in query_keywords:
            results = service.users().messages().list(userId="me", q=f"{keyword} after:2000/01/01").execute()
            messages = results.get("messages", [])

            if not messages:
                print(f"No emails found with query: {keyword}")
                continue

            for message in messages:
                msg = service.users().messages().get(userId="me", id=message["id"], format="metadata").execute()
                headers = msg["payload"]["headers"]
                subject = next(h["value"] for h in headers if h["name"] == "Subject")
                date = next(h["value"] for h in headers if h["name"] == "Date")
                
                # Very basic parsing - this is the hardest part and would need refinement
                # For now, we'll just use the subject as the artist and the date
                parsed_date = datetime.datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z").strftime("%Y-%m-%d")

                # Attempt to parse artist from subject
                artist = subject.replace("Your tickets for ", "").replace("Your order for ", "").split(" at ")[0]

                gigs.append({
                    "artist": artist,
                    "date": parsed_date,
                    "venue": "TBA (from email)",
                    "city": "TBA (from email)",
                    "type": "gig",
                    "source": "gmail"
                })

    except HttpError as error:
        print(f"An error occurred with Gmail: {error}")
        
    return gigs

def main():
    """
    Fetches gigs from Google Calendar and Gmail and saves them to a YAML file.
    """
    creds = get_credentials()
    calendar_gigs = search_calendar(creds)
    gmail_gigs = search_gmail(creds)
    
    all_gigs = calendar_gigs + gmail_gigs
    
    # Remove duplicates, giving preference to calendar entries
    seen = set()
    unique_gigs = []
    for gig in all_gigs:
        identifier = (gig["artist"], gig["date"])
        if identifier not in seen:
            seen.add(identifier)
            # Clean up the entry for yaml output
            del gig["source"]
            unique_gigs.append(gig)

    # Sort by date
    unique_gigs.sort(key=lambda x: x["date"])

    output_file = "../data/google_gigs.yaml"
    with open(output_file, "w") as f:
        yaml.dump(unique_gigs, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        
    print(f"Found {len(unique_gigs)} gigs. Saved to {output_file}")

if __name__ == "__main__":
    # Change working directory to the directory of this script
    # so that credentials.json and token.json are in the solicitor directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
