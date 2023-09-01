import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from tqdm import tqdm


def get_menu(date):
    '''
        Get the menu for a given date.
        Input:
            - date (string): string in the format YYYY-MM-DD
        Returns:
            - menus (DataFrame): DataFrame containing the menu for the given date
    '''
    url = 'https://www.epfl.ch/campus/restaurants-shops-hotels/fr/offre-du-jour-de-tous-les-points-de-restauration/?date=' + date
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    
    menus = pd.DataFrame(columns=['name', 'restaurant', 'etudiant', 'doctorant', 'campus', 'visiteur', 'vegetarian'])
    menus['vegetarian'] = menus['vegetarian'].astype('bool')

    menuTable = soup.find('table', id='menuTable')
    if not menuTable:
        return menus
        
    lunches = menuTable.find_all('tr', class_='lunch')
    if not lunches:
        return menus

    for item in lunches:
        name = item.find('div', class_="descr").text.replace('\n', '\\n')
        restaurant = item.find('td', class_='restaurant').text
        
        # if item has class 'vegetarian', then it's vegetarian
        vegetarian = 'vegetarian' in item['class']

       # Extract all price options for this menu item
        price_elements = item.find_all('span', class_='price')
        prices_dict = {}
        
        # Check if there is at least one price element
        valid_menu = True
        if price_elements:
            for price_element in price_elements:
                price_text = price_element.text.strip()
                price_category = price_element.find('abbr', class_='text-primary')
                
                # Check if there is a price category (abbreviation)
                if price_category:
                    category = price_category.text.strip()
                else:
                    category = 'default'
                    
                # Check if the price format is valid (no characters after CHF)
                if not re.search(r'CHF\s*\S', price_text):
                    price_match = re.search(r'([\d.]+)\s*CHF', price_text, re.IGNORECASE)
                    if price_match:
                        price = float(price_match.group(1))
                        prices_dict[category] = price
                else:
                    valid_menu = False
                    break  # Discard the menu if this condition is met

        # If the menu is valid, add it to the DataFrame
        if valid_menu:
            # Fill missing prices with the default price, if it exists
            if 'default' in prices_dict:
                default_price = prices_dict['default']
                for category in ['E', 'D', 'C', 'V']:
                    if category not in prices_dict:
                        prices_dict[category] = default_price
            else:
                # Set missing prices to None
                for category in ['E', 'D', 'C', 'V']:
                    if category not in prices_dict:
                        prices_dict[category] = None

            menus = pd.concat([menus, pd.DataFrame({
                'name': [name],
                'restaurant': [restaurant],
                'etudiant': [prices_dict['E']],
                'doctorant': [prices_dict['D']],
                'campus': [prices_dict['C']],
                'visiteur': [prices_dict['V']],
                'vegetarian': [vegetarian]
            })])

    return menus

def get_all_menus(start_date, end_date):
    '''
        Get the menus for a given date range.
        Input:
            - start_date (string): string in the format YYYY-MM-DD
            - end_date (string): string in the format YYYY-MM-DD
        Returns:
            - menus (DataFrame): DataFrame containing the menus for the given date range
    '''
    menus = pd.DataFrame(columns=['date', 'name', 'restaurant', 'etudiant', 'doctorant', 'campus', 'visiteur', 'vegetarian'])
    menus['vegetarian'] = menus['vegetarian'].astype('bool')
    for date in tqdm(pd.date_range(start_date, end_date)):
        day_menus = get_menu(date.strftime('%Y-%m-%d'))
        day_menus['date'] = date
        menus = pd.concat([menus, day_menus])
    return menus
