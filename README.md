# trac-taskcare

## Configuration

    [taskcare]
    auth_httpheader_key = exampletaskcare-serviceid
    auth_httpheader_value = xxx
    auth_x_httpheader_key = X-exampletaskcare-authorization
    auth_x_httpheader_value = yyy
    cron_period = 300
    filter_column_key = assignedTo
    filter_column_value = "John Doe"
    resource_addtasks = https://zzz.cloudfunctions.net/example/addTasks
    resource_getalltickets = https://zzz.cloudfunctions.net/example/getAllTickets
    resource_getticket = https://zzz.cloudfunctions.net/example/getTicket
    taskcare_column = taskcare_ticket

## License

See [LICENSE](LICENSE).
