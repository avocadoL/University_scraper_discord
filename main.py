from dotenv import load_dotenv
import os 
from bs4 import BeautifulSoup
import requests
from datetime import date
from twilio.rest import Client 

#loading enviroment variables
load_dotenv()
univ_url = os.environ.get("url")
account_sid = os.environ.get("twilio_sid")
auth_token =  os.environ.get("twilio_token")
to_phone = os.environ.get('to_phone_number')
from_phone = os.environ.get('from_phone_number')




# ----> First Part : parsing the web page <--- #

# getting today date
today = date.today().strftime("%b-%d-%Y")


#requesting the page url and saving the html in "page_content"
page = requests.get(univ_url)
page_content = page.content

#parssing the page_content with Bs4
page_parsed = BeautifulSoup(page_content,'html5lib')

#gathering the 10 newst news
all_news = page_parsed.findAll('div',attrs={'class':'event media mt-0 no-bg no-border'},limit=10)

# the final list that cotain all result
news_list=[]

#looping oover the 10 news to extract informations
for news in all_news:
    news_content = news.find('div',attrs={'class':'event-content pull-left flip pl-20 pl-xs-10'})
    news_time = news.find('div',attrs={'class':'event-date-new media-left text-center flip bg-theme-colored pl-10'})

    n={}
    n['headline']=news_content.h4.a.text
    n['link']=news_content.h4.a['href']
    time=news_time.ul.findAll('li')
    jour=time[0].text
    mois=time[1].text
    annee=time[2].text
    n['time']=f'{mois.strip()}-{jour.strip()}-20{annee.strip()}'

    #cheking if the news collected is from today if yes , if not we get out of the loop.
    news_list.append(n)
    # # if (n['time'] == today):
    #     news_list.append(n)
    # else:
    #     break

# her we are we collected all news and stored them in news_list 


# ----> Second Part : Sending the news to my phone number <--- #

#creating the message body template 
message_body =f'University News For {today}:\n'
for i in news_list:
    message_body +=f'- {i["headline"]} : {i["link"]}\n'

# init the client with twilio acount
client = Client(account_sid, auth_token) 

#sending the message with twilio
message = client.messages.create( 
                              from_=f'{from_phone}',  
                              body=f'{news_list}',      
                              to=f'{to_phone}' 
                          ) 
 

# the end of our project
