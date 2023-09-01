from utils import get_all_menus
import pandas as pd

menus = get_all_menus('2022-01-01', '2023-08-31')

menus.to_csv('data/menus.csv', index=False)