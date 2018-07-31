import tweepy
from tweepy import OAuthHandler
import json
import gzip
import boto3
import os
import logging
import time
from StringIO import StringIO

auth = OAuthHandler('yWzQy0QRtXh8g7J3eLaDBsd2Q', 'Ltv2bW1BnMOJsrpBcZQJ3BtZp6T6l20nDbpIahPU8c3PBOQXyL')
auth.set_access_token('1005244560119947264-HAIffBBHoNsIur4rTMoiuhzy3DJ1xh', 'qzPJLyFHhKiBOObMMvr3PnEJAKeapDJmmOfiiTz5fVcpq')
 
api = tweepy.API(auth, wait_on_rate_limit=True)
#queryHashtag = 'DonaldTrump'
firehose_client = boto3.client('firehose', region_name='us-east-1')
LOG_FILENAME = '/tmp/Twitter-sentiment-analytics.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
search = tweepy.Cursor(api.search, geocode= ['-127.33,23.34,-55.52,49.56']).items(100)
def lambda_handler(event, context):
	for tweet in search:
		try:
			firehose_client.put_record(
				DeliveryStreamName = 'tweets',
				Record =  {
					'Data': json.dumps(tweet._json, ensure_ascii=False, encoding="utf-8")+'\n' 
				} ) 
		except Exception:
			logging.exception("Problem pushing to firehose")

