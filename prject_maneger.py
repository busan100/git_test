import gspread
# import pyautogui

# keyword = pyautogui.prompt("파일명 넣어주세요")

gc = gspread.service_account(filename="keys.json")

sh = gc.create('33333keyword')

worksheet = sh.add_worksheet(title="A wgggggg00", rows=100, cols=20)

# But that new spreadsheet will be visible only to your script's account.
# To be able to access newly created spreadsheet you *must* share it
# with your email. Which brings us to…

sh.share('busan100@gmail.com', perm_type='user', role='writer')
