import string
import random
from flask import session
from flask.ext.github import GitHub
from rauth.service import OAuth2Service

def getUser(provider):
	"""Gets user token information from the session"""
	if session.has_key('token'):
		auth = provider.get_session(token = session['token'])
		resp = auth.get('/user')
		if resp.status_code == 200:
			user = resp.json()
			return user
		else:
			return None
	else:
		return None

def getCsrfToken():
	"""Generates a random string for a CSRF token"""
	return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))