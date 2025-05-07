from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
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
    if os.path.exists('token.json'):
        try:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        except:
            creds = None
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('tasks', 'v1', credentials=creds)
    return service

def ret_lists(service):

    # Call the Tasks API
    results = service.tasklists().list().execute()
    items = results['items']
    tmp=items[0]
    items[0]=items[1]
    items[1]=tmp
    final=[]
    for i in items:
        final.append((i['title'],i['id']))
        # pprint(i)
    return final
    # pprint(final)
    # pprint(items)

def delete(list_id,task_id,service):
    try:
        service.tasks().delete(tasklist=list_id,task=task_id).execute()
    except:
        pass

def complete(list_id,task_id,task,service):
    # print(task_id)
    try:
        task['status']='completed'
        service.tasks().update(tasklist=list_id,task=task_id,body=task).execute()
    except Exception as e:
        print('Something failed')
        pprint(e)

def restore(list_id,task_id,task,service):
    try:
        if(task['deleted']==True):
            task['deleted']=False
        elif(task['status']=='completed'):
            task['status']='needsAction'
            del task['completed']
    except:
        try:
            # print('Checking if completed')
            if(task['status']=='completed'):
                task['status']='needsAction'
                del task['completed']
                # print('Changed to completed')
        except:
            # print("Caught")
            pass
    # print("Calling api")
    pprint(task_id)
    service.tasks().update(tasklist=list_id,task=task_id,body=task).execute()
        
def sort_func(e):
    # print(type(e['position']))
    try:
        e['parent']
        return int(e['position'])+1000000000
    except:
        return int(e['position'])

def add(list_id,task,service):
    # print(list_id)
    try:
        service.tasks().insert(tasklist=list_id,body=task).execute()
    except:
        print("Something went wrong with adding the new task")

def ret_tasks(target_list,service,show_completed=False,show_deleted=False):
    # results = service.tasklists().list().execute()
    # items = results['items']
    try:
        more=service.tasks().list(tasklist=target_list,maxResults=80,showCompleted=show_completed,showDeleted=show_deleted,showHidden=True).execute()
        # pprint(more)

        try:
            more=more['items']
            more.sort(key=sort_func)
            dict={}
            for i in more:
                if(show_completed and i['status']=='needsAction'): continue
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
            cnt=0
            # pprint(final)
            if(not show_completed and not show_deleted): return final
            final_edited=[]
            for i in final:
                if(show_completed):
                    if(i[2]['status']=='needsAction'): continue
                    final_edited.append(i)
                elif(show_deleted):
                    try:
                        if(i[2]['deleted']=='False'): continue
                        final_edited.append(i)
                    except:
                        continue
            return final_edited
        except:
            return [('Empty list - Add something','0','0')]
    except:
        return [('Something went wrong. Try again!','0','0')]
if __name__ == '__main__':
    ret_tasks('MDM4NDkxMDU0Mjk5OTcwMzU2NDM6MDow')
    # ret_lists()
