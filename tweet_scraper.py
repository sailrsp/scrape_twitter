import tweepy  
import csv
import sys

 

#Twitter API credentials
consumer_key = "xxxxxxxxxxxxxxxxxx" #api key
consumer_secret = "xxxxxxxxxxxxxxxxxxxxxxx"  # api secret key
access_key = "xxxxxxxxxxxxxxxxxxxxxxxx" # access token
access_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxx" # access token secret


def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []  
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    # check if user is there
    try:
        new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    except:
        print('Sorry, Twitter Handle does not exist for user:' , screen_name)
        exit()


    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    # ok, you may have the  user, but he has not made any tweets
    # so , we need to handle that exception also
    if (len(alltweets))==0:
        print ('No tweets made by the user' ,screen_name,'till now')
        exit()


    
    # for debugging, you may uncomment the line below    
    #print(len(alltweets))
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print(f"getting tweets before {oldest}")
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
        print(f"...{len(alltweets)} tweets downloaded so far")
    

     
    #transform the tweepy tweets into a 2D array that will populate the csv 
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]
    
    #write the csv  
    with open(f'new_{screen_name}_tweets.csv','w',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)
    
    pass


if __name__ == '__main__':
	#pass in the username of the account you want to download
	
    #print('Number of arguments:', len(sys.argv), 'arguments.')
    if len(sys.argv)>2:
        print('please enter in correct format. only one twitter handle at a time')
        print('Anyway , i will be searching for',str(sys.argv[1]))
    
tweet_search=str(sys.argv[1])

get_all_tweets(tweet_search)

