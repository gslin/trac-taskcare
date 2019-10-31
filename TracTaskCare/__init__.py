# -*- coding: utf-8 -*-

from trac.core import Component, implements
from trac.ticket.api import ITicketChangeListener
import requests

class TracTaskCare(Component):
    implements(ITicketChangeListener)

    def __init__(self):
        self.taskcare = self.config['taskcare']

    def ticket_created(self, ticket):
        pass

    def ticket_changed(self, ticket, comment, author, old_values):
        auth_httpheader_key = self.taskcare.get('auth_httpheader_key')
        auth_httpheader_value = self.taskcare.get('auth_httpheader_value')
        auth_x_httpheader_key = self.taskcare.get('auth_x_httpheader_key')
        auth_x_httpheader_value = self.taskcare.get('auth_x_httpheader_value')
        resource_addtasks = self.taskcare.get('resource_addtasks')
        taskcare_column = self.taskcare.get('taskcare_column')

        if taskcare_column is None or '' == taskcare_column:
            return
        taskcare_ticket_number = ticket[taskcare_column]
        if taskcare_ticket_number is None or '' == taskcare_ticket_number:
            return

        taskcare_comment = '(Made by {} at Trac)\n{}'.format(author, comment)

        data = {
            'subject': ticket['summary'],
            'taskDetails': ticket['description'],
            'taskComments': [
                {
                    'comment': taskcare_comment,
                }
            ],
        }
        headers = {
            auth_x_httpheader_key: auth_x_httpheader_value,
            auth_httpheader_key: auth_httpheader_value,
        }
        url = '{}/{}'.format(resource_addtasks, taskcare_ticket_number)
        requests.put(url, headers=headers, json=data)

    def ticket_deleted(self, ticket):
        pass

    def ticket_comment_modified(self, ticket, cdate, author, comment, old_comment):
        pass

    def ticket_change_deleted(self, ticket, cdate, changes):
        pass
