# -*- coding: utf-8 -*-
import re
import facebook
from client import plugin


class NotificationsPlugin(plugin.SpeechHandlerPlugin):
    def get_phrases(self):
        return ["FACEBOOK", "NOTIFICATION"]

    def handle(self, text, mic):
        """
        Responds to user-input, typically speech text, with a summary of
        the user's Facebook notifications, including a count and details
        related to each individual notification.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        """
        oauth_access_token = self.profile['keys']['FB_TOKEN']

        graph = facebook.GraphAPI(oauth_access_token)

        try:
            results = graph.request("me/notifications")
        except facebook.GraphAPIError:
            mic.say("I have not been authorized to query your Facebook. If " +
                    "you would like to check your notifications in the " +
                    "future, please visit the Jasper dashboard.")
            return
        except:
            mic.say("I apologize, there's a problem with that service at " +
                    "the moment.")

        if not len(results['data']):
            mic.say("You have no Facebook notifications. ")
            return

        updates = []
        for notification in results['data']:
            updates.append(notification['title'])

        count = len(results['data'])
        mic.say("You have " + str(count) +
                " Facebook notifications. " + " ".join(updates) + ". ")

        return

    def is_valid(self, text):
        """
        Returns True if the input is related to Facebook notifications.

        Arguments:
        text -- user-input, typically transcribed speech
        """
        return bool(re.search(r'\bnotification|Facebook\b', text,
                              re.IGNORECASE))
