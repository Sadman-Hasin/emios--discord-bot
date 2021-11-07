import json
import requests


class Hadith:
	@staticmethod
	def fetch_random():
		response = requests.get("https://api.sunnah.com/v1/hadiths/random",
						headers={"X-API-Key":"SqD712P3E82xnwOAEOkGd5JZH8s9wRR24TqNFzjk"})

		return [response.status_code,
				response.headers,
				json.loads(response.text)]
