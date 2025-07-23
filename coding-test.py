import requests
import sys
from bs4 import BeautifulSoup
from operator import attrgetter
from termcolor import colored

class CharacterGridItem:
    def __init__(self, x, char, y):
        self.x = x
        self.char = char
        self.y = y

def main():
    validate_user_input()
    decode_secret_message(sys.argv[1])

def decode_secret_message(doc_url):
    grid, max_x, max_y = get_character_grid(doc_url)
    sorted_grid = sorted(grid, key=attrgetter("y", "x"))
    
    for y in range(max_y, -1, -1):
        for x in range(max_x + 1):
            try:
                grid_item = next(item for item in sorted_grid if item.x == x and item.y == y)
                print(grid_item.char, end="")
                
            except StopIteration:
                print(" ", end="")
                
        print()
            
def get_character_grid(doc_url):
    try:
        response = requests.get(doc_url)
    except:
        print(colored("An error occured while attempting to download the specified URL.", "red"))
        sys.exit(1)
        
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    grid = []
    max_x = 0
    max_y = 0
    
    tables = soup.find_all('table')
    
    for table in tables:
        rows = table.find_all('tr')
        
        for row in rows:
            cells = row.find_all('td')
            
            x = cells[0].get_text(strip=True)
            char = cells[1].get_text(strip=True)
            y = cells[2].get_text(strip=True)
            
            if not x.isnumeric() or not y.isnumeric():
                continue
            
            x = int(x)
            if x > max_x: max_x = x
            
            y = int(y)
            if y > max_y: max_y = y
            
            grid.append(CharacterGridItem(x, char, y))

    return grid, max_x, max_y

def validate_user_input():
    if len(sys.argv) == 1:
        print(colored("No arguments specified. Please pass 1 argument that is a valid url.", "red"))
        sys.exit(1);
        
    doc_url = sys.argv[1]
    
    if not doc_url.startswith("http://") and not doc_url.startswith("https://"):
        print(colored("Invalid arguments: Please pass 1 argument that is a valid url.", "red"))
        sys.exit(1)

if __name__ == "__main__":
    main()