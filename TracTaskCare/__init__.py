# -*- coding: utf-8 -*-

from threading import Timer
from trac.core import Component, implements
from trac.ticket.api import ITicketChangeListener
import requests

class TracTaskCare(Component):
    implements(ITicketChangeListener)

    def __init__(self):
        taskcare = self.config['taskcare']

        self.auth_httpheader_key = taskcare.get('auth_httpheader_key')
        self.auth_httpheader_value = taskcare.get('auth_httpheader_value')
        self.auth_x_httpheader_key = taskcare.get('auth_x_httpheader_key')
        self.auth_x_httpheader_value = taskcare.get('auth_x_httpheader_value')
        self.cron_period = taskcare.get('cron_period')
        self.resource_addtasks = taskcare.get('resource_addtasks')
        self.taskcare_column = taskcare.get('taskcare_column')

        self.t = Timer(self.cron_period, self._cron)
        self.t.start()

    def ticket_created(self, ticket):
        pass

    def ticket_changed(self, ticket, comment, author, old_values):
        if self.taskcare_column is None or '' == self.taskcare_column:
            return
        taskcare_ticket_number = ticket[self.taskcare_column]
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
            self.auth_x_httpheader_key: self.auth_x_httpheader_value,
            self.auth_httpheader_key: self.auth_httpheader_value,
        }
        url = '{}/{}'.format(self.resource_addtasks, taskcare_ticket_number)
        requests.put(url, headers=headers, json=data)

    def ticket_deleted(self, ticket):
        pass

    def ticket_comment_modified(self, ticket, cdate, author, comment, old_comment):
        pass

    def ticket_change_deleted(self, ticket, cdate, changes):
        pass

    def _cron(self):
        self.t(self.cron_period, self._cron)

        with self.env.db_query as db:
            rows = db('SELECT * FROM ticket WHERE status != "closed";')
