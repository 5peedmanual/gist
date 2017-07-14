#!/usr/bin/python
import requests
import time
import json
import my_module as mm

class hfUsers:
	"""A simple bot class for Hackforums"""
	def __init__(self, sitekey, api_key):
		# creates a request session and sets headers
		self.session = requests.session()
		# Sets headers
		self.headers = {
					'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0',
					'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
					'Accept-Language': 'en-US,en;q=0.5',
					'Accept-Encoding': 'gzip, deflate, br',
					'Referer': 'https://hackforums.net/',
					'Connection': 'keep-alive',
					'Upgrade-Insecure-Requests': '1',
						}
		self.aheaders = {
					'Host': 'hackforums.net',
					'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
					'Upgrade-Insecure-Requests' : '1',
					'Content-Type': 'text/html'
					}
		# Updates the headers so we dont have to use headers=headers everytime
		self.session.headers.update(self.headers)
		self.sitekey = sitekey
		self.api_key = api_key

	def go_solve():
		captcha_response = self.complete_captcha(self.sitekey)
		# Extracting id that is required to be sent with form data
		dataID = r.text.split('data-ray="')[-1].split('" async data-sitekey')[0]
		# Setting up a payload
		payload = {'id' : dataID, 'g-recaptcha-response' : captcha_response}
		# Printing stuff for verification
		print(captcha_response)
		print(dataID)
		# Sending parameter and form data for captcha solving
		r = self.session.get('http://hackforums.net/cdn-cgi/l/chk_captcha', data=payload)
		time.sleep(1)
		print('Solved')

	def login(self):
		proxiestor = {
		    'http': 'socks5://127.0.0.1:9050',
		    'https': 'socks5://127.0.0.1:9050',
		    #'http': 'socks4://127.0.0.1:9050',
		    #'https': 'socks4://127.0.0.1:9050'
		}

		proxies = {
            'http':'http://94.181.56.198:16632', # Place http proxy
            'https': 'https://54.187.85.135:80' # Place https proxy
        }
		r = self.session.get("https://hackforums.net/", proxies=proxies)
		mm.write_to_file("get.html", r.text)
		print('Sent get request to hackforums.net ')
		username = 'awdasdqwert' # input("Enter your username: ")
		password = 'zQ6LrRZXpCjb' # input("Enter your password: ")
		postkey = r.text.split('my_post_key = "')[-1].split('";')[0]



		# rtest = self.session.get('https://hackforums.net/showthread.php?tid=5666551')
		# mm.write_to_file("tid.html", rtest.text)
		# print('tid')
		# rPOST = self.session.post("https://hackforums.net/member.php", data=payload, proxies=proxiestor)
		# print('sent post')
		# mm.write_to_file("outputPOST.html", rPOST.text)


		if (r.text.split('<td class="thead"><strong>')[-1].split('</strong></td>')[0]) == "Site Challenge":
			print('captcha spotted')
			print('solving...')
			# Asks the captcha solver function to solve it for me
			captcha_response = self.complete_captcha(self.sitekey)
			# Extracting id that is required to be sent with form data
			dataID = r.text.split('data-ray="')[-1].split('" async data-sitekey')[0]
			# Setting up a payload
			payload = {'id' : dataID, 'g-recaptcha-response' : captcha_response}
			# Printing stuff for verification
			print(captcha_response)
			print(dataID)
			# Sending parameter and form data for captcha solving
			r = self.session.get('http://hackforums.net/cdn-cgi/l/chk_captcha', data=payload)
			time.sleep(1)
			print('Solved')
			# Getting the main page again this time MAYBE without captcah since we solved it
			r = self.session.get('https://hackforums.net/member.php')
			print('get request to member.php inside if')
			mm.write_to_file('getmember.html', r.text)
			payload = {'username': username, 'password':password, 'gauth_code':'','remember':'yes','submit':'Login','action':'do_login','url':'https://hackforums.net/index.php'}
			rPOST = self.session.post("https://hackforums.net/member.php", data=payload, proxies=proxies)
			#print('sent post')
			mm.write_to_file("outputPOSTif.html", rPOST.text)
			print('post')
		print('Done')






	# This asks the api to solve catpcha
	def complete_captcha(self, sitekey):
		payload = {'key': self.api_key, 'method': 'userrecaptcha', 'googlekey': sitekey, 'pageurl': 'https://hackforums.net/', 'json': '1'}
		r = requests.get('http://2captcha.com/in.php', params=payload)
		data = json.loads(r.text)
		get_payload = {'key': self.api_key, 'action': 'get', 'id': data['request'], 'json': '1'}
		while True:
			captcha_response = requests.get('http://2captcha.com/res.php', params=get_payload, timeout=20)
			data = json.loads(captcha_response.text)
			if data['request'] != 'CAPCHA_NOT_READY':
				break
		return data['request']

if __name__ == "__main__":
	bot = hfUsers(sitekey="6LfBixYUAAAAABhdHynFUIMA_sa4s-XsJvnjtgB0", api_key='ef4bb667dbe950a929d7ef40b8871ef5')
bot.login()
