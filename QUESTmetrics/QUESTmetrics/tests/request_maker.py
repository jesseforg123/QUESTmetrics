import requests

ROOT = 'http://127.0.0.1:5000'

def GET(resource_call):
    response = requests.get(ROOT + resource_call)
    return response

def PUT(resource_call, file=None, attachment_name=None):
    if file is None:
        response = requests.put(ROOT + resource_call)
    else:
        files = {attachment_name: ("test.csv", open(file, 'rb'))}
        response = requests.put(ROOT + resource_call, files=files)
    return response

def POST(resource_call):
    response = requests.post(ROOT + resource_call)
    return response

def DELETE(resource_call):
    response = requests.delete(ROOT + resource_call)
    return response


