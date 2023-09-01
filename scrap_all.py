from utils import get_all_menus
import pandas as pd

range_menus = get_all_menus('2023-08-28', '2023-08-31')

# Read the menus from the CSV file
menus = pd.read_csv('data/menus.csv')

# Filter out the menus where dates are already in the CSV file
range_menus = range_menus[~range_menus['date'].isin(menus['date'])]

print(f'{len(range_menus)} new days of menus found.')

# Append the new menus to the CSV file
menus = pd.concat([menus, range_menus])

# Save the CSV file
menus.to_csv('data/menus.csv', index=False)