#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
import datetime


def send_message(subject, text, recipients, apiKey, from_address='pbk236@nyu.com'):
		assert apiKey is not None

		return requests.post(
				"https://api.mailgun.net/v3/mg.foobar.com/messages",
				auth=("api", apiKey),
				data={"from": from_address,
							"to": recipients,
							"subject": subject,
							"text": text})