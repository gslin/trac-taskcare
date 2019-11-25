# -*- coding: utf-8 -*-

from threading import Timer
from trac.core import Component, implements
from trac.env import IEnvironmentSetupParticipant
from trac.ticket.api import ITicketChangeListener
import requests

class TracTaskCare(Component):
    implements(IEnvironmentSetupParticipant)
    implements(ITicketChangeListener)

    def __init__(self):
        self.env.log.info('TracTaskCare __init__()')
        taskcare = self.config['taskcare']

        self.auth_httpheader_key = taskcare.get('auth_httpheader_key')
        self.auth_httpheader_value = taskcare.get('auth_httpheader_value')
        self.auth_x_httpheader_key = taskcare.get('auth_x_httpheader_key')
        self.auth_x_httpheader_value = taskcare.get('auth_x_httpheader_value')
        self.cron_period = int(taskcare.get('cron_period'))
        self.filter_column_key = taskcare.get('filter_column_key')
        self.filter_column_value = taskcare.get('filter_column_value')
        self.resource_addtasks = taskcare.get('resource_addtasks')
        self.resource_getalltickets = taskcare.get('resource_gettickets')
        self.resource_getticket = taskcare.get('resource_getticket')
        self.taskcare_column = taskcare.get('taskcare_column')

    def background_cron(self):
        self.env.log.info('TracTaskCare _cron()')

        t = Timer(self.cron_period, self._cron)
        t.start()

        headers = {
            self.auth_x_httpheader_key: self.auth_x_httpheader_value,
            self.auth_httpheader_key: self.auth_httpheader_value,
        }

        # Scan existing tickets on Trac
        with self.env.db_query as db:
            rows = db('SELECT id, summary, description, status FROM ticket LEFT JOIN ticket_custom ON ticket.id = ticket_custom.ticket WHERE status != "closed" AND name = %s AND value != "";', (self.taskcare_column, ))
            for t in rows:
                url = '{}/{}'.format(self.resource_getticket, t[0])

    def environment_created(self):
        pass

    def environment_needs_upgrade(self):
        self.background_cron()
        return False

    def ticket_created(self, ticket):
        pass

    def ticket_changed(self, ticket, comment, author, old_values):
        if self.taskcare_column is None or '' == self.taskcare_column:
            return
        taskcare_ticket_number = ticket[self.taskcare_column]
        if taskcare_ticket_number is None or '' == taskcare_ticket_number:
            return

        taskcare_comment = '(made by {} at Trac)\n{}'.format(author, comment)

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

    def upgrade_environment(self):
        pass
