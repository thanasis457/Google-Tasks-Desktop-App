from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pprint import pprint
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/tasks']
name='https://www.googleapis.com//tasks/v1/users/@me/lists/'
def func():
    """Shows basic usage of the Tasks API.
    Prints the title and ID of the first 10 task lists.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('tasks', 'v1', credentials=creds)
    return service

def ret_lists(service):

    # Call the Tasks API
    results = service.tasklists().list().execute()
    items = results['items']
    # tmp=items[0]
    # items[0]=items[1]
    # items[1]=tmp
    # pprint(items)
    # items.sort(key=sort_list)
    # more=service.tasks().list(tasklist=items[1]['id']).execute()
    final=[]
    for i in items:
        final.append((i['title'],i['id']))
        # pprint(i)
    return final
    # pprint(final)
    # pprint(items)

def delete(all_tasks,list_id,task_id,service):
    # print(drop_list.currentIndex())
    # print(lists[0])
    # print(tasks[:10])
    # print(tasks[row])
    # print(lists[drop_list.currentIndex()][1])
    # print(tasks[row][1])
    # return
    # service.tasks().delete(tasklist=lists[drop_list.currentIndex()][1],task=tasks[row][1]).execute()
    service.tasks().delete(tasklist=list_id,task=task_id).execute()

def complete(all_tasks,list_id,task_id,task,service):
    # print(task_id)
    task['status']='completed'
    try:
        service.tasks().update(tasklist=list_id,task=task_id,body=task).execute()
    except:
        pass

def sort_func(e):
    # print(type(e['position']))
    try:
        e['parent']
        e['position']=int(e['position'])+1000000000
    except:
        pass
    return int(e['position'])

def ret_tasks(target_list,service):
    # results = service.tasklists().list().execute()
    # items = results['items']
    try:
        more=service.tasks().list(tasklist=target_list,maxResults=40,showCompleted=False,showHidden=True).execute()
        # pprint(more)

        try:
            more=more['items']
            more.sort(key=sort_func)
            dict={}
            for i in more:
                try:
                    dict[i['parent']].append((i['title'],i['id'],i))
                except:
                    dict[i['id']]=[(i['title'],i)]
            # pprint(dict)
            final=[]
            for i,val in dict.items():
                final.append((val[0][0],i,val[0][1]))
                # print(val[0])
                for j in range(1,len(val)):
                    # print(val[j])
                    final.append(('----- '+val[j][0],val[j][1],val[j][2]))
            # print(final)
            return final
        except:
            return [('Empty list - Add something','0','0')]
    except:
        return [('Something went wrong. Try again!','0','0')]
if __name__ == '__main__':
    ret_tasks('MDM4NDkxMDU0Mjk5OTcwMzU2NDM6MDow')
    # ret_lists()
