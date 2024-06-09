import requests
from bs4 import BeautifulSoup
import csv

# Enter a date in format MM/DD/YYYY
date = input("Enter a date in format MM/DD/YYYY: ")  # Corrected the date format

# Correct the URL string formatting
url = f"https://www.yallakora.com/match-center/مركز-المباريات?date={date}#"

# Send a GET request to the webpage
page = requests.get(url)

def main(page):
    scr = page.content
    soup = BeautifulSoup(scr, "lxml")
    match_details = []
    championships = soup.find_all('div', {'class': 'matchesList'})

    def get_match_info(championship):
        championship_title = championship.contents[1].find('h2').text.strip()
        all_matches = championship.contents[3].find_all('div', {'class': 'item future liItem'})
        number_of_matches = len(all_matches)
        for i in range(number_of_matches):
            # Get teams' names
            team_A = all_matches[i].find('div', {'class': 'teams teamA'}).text.strip()
            team_B = all_matches[i].find('div', {'class': 'teams teamB'}).text.strip()

            # Get score
            match_result = all_matches[i].find('div', {'class': 'MResult'}).find_all('span', {'class': "score"})
            score = f"{match_result[0].text.strip()} - {match_result[1].text.strip()}" if match_result else "N/A"

            # Get time
            match_time = all_matches[i].find('div', {'class': 'MResult'}).find('span', {'class': "time"}).text.strip() if all_matches[i].find('div', {'class': 'MResult'}).find('span', {'class': "time"}) else "N/A"
            
            # Get match Status
            match_status=all_matches[i].find('div', {'class': 'matchStatus'}).text.strip()
            
            # Add to info to dictionary
            match_details.append({
                "نوع البطوله": championship_title,
                "الفريق الاول": team_A,
                "الفريق التاني": team_B,
                "ميعاد المباراة": match_time,
                "النتيجه": score,
                "الحاله":match_status
            })
    # Loop through each championship found
    for championship in championships:
        get_match_info(championship)

    # Make CSV file
    keys = match_details[0].keys()
    with open('/Users/compumagic/Downloads/Web Scraping/yalla_kora.csv', 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(match_details)
        print("successfully created!")

main(page)
