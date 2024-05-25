import tweepy
from playwright.sync_api import sync_playwright
import smtplib
from dotenv import load_dotenv
import os
from datetime import datetime, time,date
from accuweather import weather_post
from mlbpredictor.mlbprediction2 import mlbpredict
from stockmarketPredictor.get_daily_stock import get_data
from stockmarketPredictor.predict_stock_tommorrow import predict_prices
from memgenerator.memegen import getRandomMeme


from email.message import EmailMessage

# load the credientials from the local .env file
load_dotenv()
#authenticate usings keys first

bear_token = os.getenv("twitter_bear_token")
consumer_k = os.getenv("twitter_consumer_key")
consumer_s = os.getenv("twitter_consumer_secret")
access_tok = os.getenv("twitter_access_token")
access_sec = os.getenv("twitter_access_secret")

stock_api_secret= os.getenv("stock_api_secret")

client_api = tweepy.Client(bear_token,consumer_k,consumer_s,access_tok,access_sec)

auth = tweepy.OAuthHandler(consumer_key=consumer_k, consumer_secret=consumer_s)
auth.set_access_token(access_tok, access_sec)

media_api = tweepy.API(auth)


def send_email(sender_email, target_email):
    message = "Your Twitter bot has created a new post"
    msg = EmailMessage()
    msg.set_content(message)

    msg['Subject'] = 'Twitter Bot'
    msg['From'] = sender_email
    msg['To'] = target_email

    try:
        # Send the message via Gmail's SMTP server using TLS
        smtp_server = 'smtp.gmail.com'
        smtp_port = 465
        s = smtplib.SMTP_SSL(smtp_server, smtp_port)
      

        # Log in to your Gmail account (use application-specific password for security)
        gmail_username = 'bottybots8219@gmail.com'
        gmail_password = 'ofvingkxjqtckivo'
        s.login(gmail_username, gmail_password)

        # Send the email
        s.send_message(msg)
        s.quit()

        print("Email Notification Has Been Sent")
    except Exception as e:
        print("Error sending email:", e)



url_page = "https://randomwordgenerator.com/motivational-quote.php"
def get_daily_quote(url):

    # start the browser
    playwright_object = sync_playwright().start()
    broswer = playwright_object.chromium.launch()
    

    # create a new page in the browser that we can search through
    quote_page = broswer.new_page()
    quote_page.set_default_timeout(0)

    # go to the website with the provided url
    quote_page.goto(url)
    quote_of_day = ''

   # repeat until a quote under the proper length is found
    while(True):
        
         # find the button that generates a new qoute
        generate_button = quote_page.locator('text=Generate Motivational Quotes')
        generate_button.click()

        # extract the qoute from the webpage and return it
        quote_element = quote_page.query_selector('.support-sentence')
        quote_of_day = quote_element.inner_text()

        if len(quote_of_day) <= 270:
            break
        


    broswer.close()

    return quote_of_day


def actions():

    current_time = datetime.now().time()
    todays_date = date.today()
    todays_date = todays_date.strftime("%B %d")


    tweleve_oclock = time(12,0,0)
    three_oclock = time(15,0,0)
    five_oclock = time(17,0,0)

    sentTweet = False
    print(current_time)
   

    
    if current_time < tweleve_oclock:

        # tweet a weather forecast of a random loaction
        desired_city, Country, Forecast_des, low_t, high_temp = weather_post()
        if desired_city is not None:
            tweet_text = f"Weather forecast for {desired_city}, {Country}: {Forecast_des}.\n "
            tweet_text += f"Low: {low_t}°F,\n High: {high_temp}°F."
            client_api.create_tweet(text=tweet_text)
            sentTweet = True
        

        #tweet stock_predictions
        comp_symbol, comp_name = get_data(stock_api_secret)
        if comp_symbol is not None:

            open_price, high_price,low_price,volume_total,close_price = predict_prices()

            tweet_content = f"Stock Price Predictions For {comp_name}.\n"
            tweet_content += f"Opening Price = {open_price} \n"
            tweet_content += f"Highest Price = {high_price}\n"
            tweet_content += f"Lowest Price = {low_price}\n"
            tweet_content += f"Closing Price = {close_price}\n"
            tweet_content += f"Total Trades = {volume_total}"
            client_api.create_tweet(text=tweet_content)
            sentTweet = True

        else:
            print("Unable to make a prediction due to an error.")

        
        
    elif current_time >= tweleve_oclock and  current_time < three_oclock:
        Team1, Team2, Winner = mlbpredict()

        #check if any games are being played today
        if Team1 is not None:

            tweet_des = f"MLB Game of the Day ({todays_date}) : {Team1} vs {Team2}.\n"
            tweet_des += f" I predict {Winner} will win!!"
            client_api.create_tweet(text=tweet_des)
    

    elif current_time >= three_oclock and  current_time < five_oclock:
        random_title = ""
        memefile = getRandomMeme()
        med_response = media_api.media_upload(filename='dailymeme.jpg', file=memefile)
        med_id_str = med_response.media_id_string
        client_api.create_tweet(text=random_title,media_ids=[med_id_str])
        sentTweet = True


    else:
        print("run motivational quote")
        motivation_tweet = get_daily_quote(url_page)
        client_api.create_tweet(text=motivation_tweet)
        print("quote has been written", motivation_tweet)
        sentTweet = True


    # sent an email only if a tweet has been created.
    if sentTweet is True:
        # Call the function with your email addresses
        from_email = os.getenv("sender_email")
        to_email = os.getenv("reciver_email")
        send_email(from_email, to_email)


# run the logic for the bot
actions()

