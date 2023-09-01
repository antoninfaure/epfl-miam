from utils import get_menu
import pandas as pd
import datetime

# Get today's date
today = datetime.date.today().strftime('%Y-%m-%d')

# Get the menu for today
today_menus = get_menu(today)

# Read the existing menus
menus = pd.read_csv('data/menus.csv')

# If date not in menus, add it
if today not in menus['date'].values:
    today_menus['date'] = today
    menus = pd.concat([menus, today_menus])
    menus.to_csv('data/menus.csv', index=False)

