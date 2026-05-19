
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os

load_dotenv()

SPREADSHEET_NAME = os.getenv("SPREADSHEET_NAME")
WORKSHEET_NAME = os.getenv("WORKSHEET_NAME")

def authorize_gsheet():
    scope = [
        "https://spreadsheetsxxxx",
        "https://www.googleapis.xxxx",
        "https://www.googleapis.xxxxx",
        "https://www.googleapis.xxxxx"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    return client


def save_data_to_sheet(data: list[dict]):
    client = authorize_gsheet()
    sheet = client.open(SPREADSHEET_NAME).worksheet(WORKSHEET_NAME)
    all_values = sheet.get_all_values()

    headers = ["title", "username", "viewers", "timestamp"]

    # Set header if sheet is empty
    if not all_values:
        sheet.append_row(headers)
        all_values = [headers]

    existing_rows = all_values[1:]

    updated_indices = set()
    new_rows = []

    for row in data:
        found = False
        for idx, existing in enumerate(existing_rows):
            if row["username"] == existing[1] and row["title"] == existing[0]:
                # Update viewers and timestamp
                sheet.update(f"C{idx + 2}", [[row["viewers"]]])     # viewers
                sheet.update(f"D{idx + 2}", [[row["timestamp"]]])   # timestamp
                updated_indices.add(idx + 2)
                found = True
                break
        if not found:
            new_rows.append([
                row["title"],
                row["username"],
                row["viewers"],
                row["timestamp"]
            ])

    # Append unique new data
    for row in new_rows:
        sheet.append_row(row)

    # Keep only 500 latest rows (plus 1 header)
    final_data = sheet.get_all_values()
    if len(final_data) > 501:
        excess = len(final_data) - 501
        sheet.delete_rows(2, 2 + excess - 1) 
