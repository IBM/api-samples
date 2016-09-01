'''
This is a utility class to be used in samples for handling asynchronous task.
'''


import json

from timer import Timer


class TaskManager():
    '''class used to manage tasks'''

    # pass in the client and the url
    def __init__(self, api_client, task_status_url):
        self.api_client = api_client
        self.task_status_url = task_status_url

    def wait_for_task_to_complete(self, timeout=600):

        timer = Timer()

        timer.start()

        while True:
            timer.print_time_elapsed()
            print("Checking status of task.")

            if timer.has_timeout(timeout):
                raise TimeOutError("Task timed out after " + str(timeout) +
                                   " seconds.")

            if self.is_task_completed():
                print("Task Completed!")
                return

            timer.sleep(3)

    def is_task_completed(self):
        response = self.get_task_status()

        if response.code == 200:
            task_status = json.loads(response.read().decode('utf-8'))
            return task_status['status'] == 'COMPLETED'
        else:
            return False

    def get_task_status(self):

        return self.api_client.call_api(self.task_status_url, 'GET')


class Error(Exception):
    pass


class TimeOutError(Error):

    def __init__(self, msg):
        self.msg = msg
