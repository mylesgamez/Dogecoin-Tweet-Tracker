import tweepy
import requests
from datetime import datetime, timedelta

# Set up your Twitter API keys and access tokens
consumer_key = 'your_consumer_key'
consumer_secret = 'your_consumer_secret'
access_token = 'your_access_token'
access_token_secret = 'your_access_token_secret'

# Set up your Twitter API connection
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Define the keywords to search for in tweets
keywords = ['dog', 'dogs', 'doge']

# Define the time period to analyze (2 years)
time_period = timedelta(days=365 * 2)

# Fetch Elon Musk's tweets
tweets = []
for tweet in tweepy.Cursor(api.user_timeline, screen_name='elonmusk', tweet_mode='extended').items():
    if any(keyword in tweet.full_text.lower() for keyword in keywords):
        tweets.append(tweet)

# Fetch historical Dogecoin price data
end_date = datetime.now()
start_date = end_date - time_period
coin_gecko_url = f'https://api.coingecko.com/api/v3/coins/dogecoin/market_chart/range?vs_currency=usd&from={int(start_date.timestamp())}&to={int(end_date.timestamp())}'
response = requests.get(coin_gecko_url)
price_data = response.json()

# Initialize a list to store price changes
price_changes = []

# Calculate price changes for each tweet
for tweet in tweets:
    tweet_time = tweet.created_at
    tweet_price = None
    
    # Find the corresponding price data in the historical data
    for data_point in price_data['prices']:
        data_time = datetime.utcfromtimestamp(data_point[0] / 1000)  # Convert milliseconds to seconds
        if data_time > tweet_time:
            break
        tweet_price = data_point[1]
    
    # Calculate the price change for the specified time period (2 hours) after the tweet
    if tweet_price is not None:
        end_time = tweet_time + timedelta(hours=2)
        end_price = None
        for data_point in price_data['prices']:
            data_time = datetime.utcfromtimestamp(data_point[0] / 1000)  # Convert milliseconds to seconds
            if data_time > end_time:
                break
            end_price = data_point[1]
        
        if end_price is not None:
            price_change = (end_price - tweet_price) / tweet_price
            price_changes.append(price_change)

# Calculate the average price change
if price_changes:
    average_price_change = sum(price_changes) / len(price_changes)
    print(f'Average Price Change after Elon Musk tweets: {average_price_change:.2%}')
else:
    print('No relevant tweets found in the specified time period.')

# You may want to use pandas or other data manipulation libraries for more complex analysis
