import os
import json
from typing import List

from .config import google_sheet_credentials
from .logger import get_logger

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

log = get_logger(__name__)

def config_to_credentials():
    try:
        with open("./credentials.json", "w+") as credentials:
            json.dump(credentials_config)
            return True
    except (IOError, json.JSONDecodeError):
        log.error("failed to load credentials into a file to be used")
    return False


def append_values(
    spreadsheet_id: str,
    range_name: str,
    value_input_option: str,
    values_to_append: List,
):
    try:
        creds = None
        if os.path.exists("./token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not config_to_credentials():
                    log.error("failed to load config into credentials json file")
                    return _, False
                flow = InstalledAppFlow.from_client_secrets_file(
                    "./credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("./token.json", "w") as token:
                token.write(creds.to_json())
        service = build("sheets", "v4", credentials=creds)

        value_range_body = {"majorDimension": "ROWS", "values": [values_to_append]}

        result = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=value_range_body,
            )
            .execute()
        )
        print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
        return result, True
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error, False


def insert_values_in_sheet(data_to_insert: List, spreadseet_id: str):
    log.debug(data_to_insert)
    success = False
    if data_to_insert:
        range_name = "Tracking Main!A1"
        value_input_option = "USER_ENTERED"
        _, success = append_values(
            spreadsheet_id=spreadseet_id,
            range_name=range_name,
            value_input_option=value_input_option,
            values_to_append=data_to_insert,
        )
    return success
