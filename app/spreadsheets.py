import gspread

from oauth2client.service_account import ServiceAccountCredentials


def establish_connection(creds):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name(
            creds,
            scope
        )

    return gspread.authorize(creds)
