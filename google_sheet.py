import os
import json
from typing import List

from config import google_sheet_key
from logger import get_logger

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

log = get_logger(__name__)

def append_values(
    spreadsheet_id: str,
    range_name: str,
    value_input_option: str,
    values_to_append: List,
):
    try:
        credentials = Credentials.from_service_account_file("key.json", scopes=SCOPES)
        service = build("sheets", "v4", credentials=credentials)

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
    try:
        if data_to_insert:
            range_name = "Tracking Main!A1"
            value_input_option = "USER_ENTERED"
            _, success = append_values(
                spreadsheet_id=spreadseet_id,
                range_name=range_name,
                value_input_option=value_input_option,
                values_to_append=data_to_insert,
            )
    except Exception as error:
        log.error(error)
    return success
