import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']


GOOGLE_SHEET_CREDS = ServiceAccountCredentials.from_json_keyfile_name(
    'medical supplies-3abda9c4c6a3.json',scope
    )


def get_sheet(sheet_name):
    client = gspread.authorize(GOOGLE_SHEET_CREDS)
    sheet = client.open('med supplies')
    return sheet.worksheet(sheet_name)


def process_submissions(submissions):
    processed_submissions = {}
    for submission in submissions:
        submission_qty = submissions[submission]

        if submission_qty and all([x in '0123456789' for x in str(submission_qty)]):
            processed_submissions[submission] = submission_qty

    return processed_submissions


def flash_errors(form):
    for field, errors in form.errors.items():
        if field != "recaptcha":
            for error in errors:
                flash(error)
