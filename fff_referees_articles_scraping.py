import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os
import sys
import config
from mailjet_rest import Client
from unidecode import unidecode

# Proxy settings (remove if not needed)
# os.environ['HTTP_PROXY'] = 'http://localhost:9000/'
# os.environ['HTTPS_PROXY'] = 'http://localhost:9000/'

# Function to fetch articles from the website and return a DataFrame
def get_articles():
    url = "https://www.fff.fr/voir_plus/zd6r96un1_1608044686369.html"
    page = requests.get(url, verify=False)
    soup = BeautifulSoup(page.content, 'html.parser')
        
    # Create an array for al the articles get the titles (//div[@class="actualities-container"]//a//div[@class="item_toute_actu_cadre flex flex_jc_start flex_ai_start"]//figure[@class="flex article_zoom relative margin_b20 flex_ai_start"]//figcaption[@class="small_9 medium_12 large_12 font_14"]//h3) 
    # the date (//div[@class="actualities-container"]//a//div[@class="flex flex_column padding_r font_14 flex_ai_center bold heure_chrono"]) 
    # and the link (//div[@class="actualities-container"]//a/@href)
    # and add them to an array with key value pairs
    articles = []
    for article in soup.find_all('div', class_='actualities-container'):
        for a in article.find_all('a'):
            for div in a.find_all('div', class_='item_toute_actu_cadre flex flex_jc_start flex_ai_start'):
                for fig in div.find_all('figure', class_='flex article_zoom relative margin_b20 flex_ai_start'):
                    for figcaption in fig.find_all('figcaption', class_='small_9 medium_12 large_12 font_14'):
                        for h3 in figcaption.find_all('h3'):
                            for div in a.find_all('div', class_='flex flex_column padding_r font_14 flex_ai_center bold heure_chrono'):
                                articles.append({'title': h3.text, 'date': div.text, 'link': 'https://www.fff.fr'+ a['href']})

    return pd.DataFrame(articles)

def send_email(title, link):
    # Configure the email
    mailjet = Client(auth=(config.API_KEY_MAILJET, config.API_SECRET_MAILJET), version='v3.1', verify=True)
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "no-reply@fff-web-scraping",
                },
                "To": [
                    {
                        "Email": "john.doe@gmail.com",
                        "Name": "John DOE"
                    },
                    {
                        "Email": "jane.doe@gmail.com",
                        "Name": "Jane Doe"
                    }
                ],
                "Subject": "[FFF.FR] Nouveau Résultats/Classements Disponible !",
                "HTMLPart": f"<h4>Bonjour,<br><br>Un nouvel article est disponible: <a href='{link}'>{title}</a><br><br>Sportivement.</h4>",
                "CustomID": "AppGettingStartedTest"
            }
        ]
    }
    # send the email
    result = mailjet.send.create(data=data,verify=False)


def main():
    # Check if there are any CSV files starting with 'results_'
    csv_files = [f for f in os.listdir('.') if f.startswith('results_')]
    
    if not csv_files:
        # If no CSV files found, create an empty DataFrame as a placeholder for 'last'
        last = pd.DataFrame(columns=['title', 'date', 'link'])
    else:
        # If CSV files found, read the most recent one
        last = pd.read_csv(max(csv_files, key=os.path.getctime), parse_dates=['date'])

    # Get today's articles and save them in a Dataframe
    today = get_articles()
    
    # Save the dataframe to a csv file that contains the date of today with time
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    today.to_csv('results_' + date + '.csv', index=False)

    # From the last csv file, get the most recent article name 
    # and compare it to the last article name in the today csv file
    # if they are the same, exit the script
    if not last.empty and not today.empty and last['title'][0] == today['title'][0]:
        with open('fff_results_log.txt', 'a') as f:
            f.write(date +' - LAST ARTICLE: '+ unidecode(today['title'][0]) + ' (' + today['link'][0]+')\n')
    else:
        with open('fff_results_log.txt', 'a') as f:
            f.write(date +' - NEW ARTICLE FOUND : '+ unidecode(today['title'][0]) + ' (' + today['link'][0]+')\n') 
        
        # Send a mail using MailJet API if the new article contains a specific keywords in the title
        keywords = ['evaluation', 'classement', 'resultat']
        if any(keyword in unidecode(today['title'].iloc[0].lower()) for keyword in keywords): 
            send_email(today['title'].iloc[0], today['link'].iloc[0])

    # If there are more than 10 csv files in the directory, delete the oldest one
    csv_files = [f for f in os.listdir('.') if f.startswith('results_')]
    if len(csv_files) >= 10:
        os.remove(min(csv_files, key=os.path.getctime))
    
if __name__ == "__main__":
    main()
    sys.exit()  # Using sys.exit() instead of exit() for better portability
