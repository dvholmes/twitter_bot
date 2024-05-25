import requests
import os 
from dotenv import load_dotenv
from io import BytesIO
import json
import random

#load in the env file variables
load_dotenv()
# Define the URL endpoint
url = "https://api.humorapi.com/memes/random"


# generate a random top for a meme.

def generateTopic():
	current_dir = os.path.dirname(__file__)

	jsonFilePath = os.path.join(current_dir, "topics.json")

	with open(jsonFilePath) as Topicsfile:

		# read in the data from the file
		data = json.load(Topicsfile)

		

		# get list of topics:
	
		listOfTopics = data['topics']
		print(len(listOfTopics),listOfTopics[0])

		return random.choice(listOfTopics)





# # Make the GET request for the random meme of the day.
def getRandomMeme():
	# repeat until we get a valid meme.
 
	# Define the parameters including the API key
 
 
 
	memeTopic = generateTopic()

	params = {
		"keywords": memeTopic,
		"api-key": os.getenv("humorapikey")
	}
	
	counter = 0
	# we only get 10 request a day.
	while(counter < 10):
		response = requests.get(url, params=params)


		# now check if the meme is reachable
		if response.status_code != 200:

			return None
		
		memeImageUrl = response.json()['url']
		
		print(response.json())

		# now check if this image is reachable.
		memeImageResponse = requests.get(memeImageUrl)


		if memeImageResponse.status_code == 200:
			image_file = BytesIO(memeImageResponse.content)
			return image_file
		counter += 1
	
	return None
		



# print(response.json())

