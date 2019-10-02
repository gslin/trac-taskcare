# -*- coding: utf-8 -*-

from trac.core import Component, implements
import requests

class TracTaskCare(Component):
    implements(ITicketChangeListener)

    def __init__(self):
        self.taskcare = self.config['taskcare']

    def ticket_created(self, ticket):
        pass

    def ticket_changed(self, ticket, comment, author, old_values):
        pass

    def ticket_deleted(self, ticket):
        pass

    def ticket_comment_modified(self, ticket, cdate, author, comment, old_comment):
        pass

    def ticket_change_deleted(self, ticket, cdate, changes):
        pass
