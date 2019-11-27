# -*- coding: utf-8 -*-

from threading import Timer
from trac.core import Component, implements
from trac.env import IEnvironmentSetupParticipant
from trac.ticket.api import ITicketChangeListener
from trac.ticket.model import Ticket
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

        t = Timer(self.cron_period, self.background_cron)
        t.start()

        headers = {
            'Content-Type': 'application/json',
            self.auth_x_httpheader_key: self.auth_x_httpheader_value,
            self.auth_httpheader_key: self.auth_httpheader_value,
        }
        url = self.resource_getalltickets
        res = requests.get(url, headers=headers)
        payload = res.json()['payload']
        for taskcare_ticket in payload:
            if taskcare_ticket['status'] == 'Solved':
                continue
            if taskcare_ticket[self.filter_column_key] != self.filter_column_value:
                continue

            # taskTitle = 'TKT-xxxxx'
            with self.env.db_query as db:
                sql = 'SELECT ticket FROM ticket_custom WHERE name = %s AND value = %s;'
                rows = db(sql, (self.taskcare_column, taskcare_ticket['taskTitle']))

                if 0 == len(rows):
                    # Create a new ticket and sync
                    ticket = Ticket(self.env)
                    ticket['description'] = taskcare_ticket['Description']
                    ticket['summary'] = taskcare_ticket['subject']
                    ticket[self.taskcare_column] = taskcare_ticket['taskTitle']
                    ticket.insert()
                else:
                    ticket = Ticket(self.env, tkt_id=int(rows[0]))

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

        taskcare_comment = '(From {})\n\n{}'.format(author, comment)

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
