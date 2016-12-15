import sheets_api_quickstart as sheets
from config import MINNEHACK_ID

service = sheets.get_service()
EXAMPLE_ID = '1cx8xYnIFvoELmbYathI25RXQL70lVwitfgwNBoAu3g0'

# Set to MINNEHACK_ID for production.
sheetID = EXAMPLE_ID

NAMES_COL = 'A1:A'
ATTENDANCE_COL = 'L'

def formatRange(rangeName):
    return 'sheet1!' + rangeName

def set(cell, value):
    rangeName = formatRange(cell)
    body = { 'values': [[ value ]] }
    result = service.update(
        spreadsheetId=sheetID, range=rangeName, valueInputOption='RAW',
        body=body).execute()
    return result

def get (rangeName):
    rangeName = formatRange(rangeName)
    result = service.get(
        spreadsheetId=sheetID, range=rangeName).execute()
    values = result.get('values', [])
    return values

def get_names():
     names = get(NAMES_COL)
     # Sheets returns each cell as a list for some reason.
     unboxed_names = [ name[0] for name in names ]
     return unboxed_names

def check_attendance(index):
    cell = ATTENDANCE_COL + str(index)
    set(cell, True)
