from django.shortcuts import render
import json
import hashlib
import random
from django.http import HttpResponse

def generate_randomstr(length=64, salt="test"):
    m = hashlib.sha256()
    m.update(salt + str(random.randrange(1, 1000000000000000000)))
    s = m.hexdigest()
    return s[:length]

def post2index(url, doc):
    pass

def search(url=None):
    pass

def generate_randomint(number_count=6):
    return random.randrange(10**(number_count-1), 10**number_count-1)


def http200json(request, dict_var):
    return HttpResponse(json.dumps(dict_var),
                        content_type='application/json')


def http403json(request):
    return render(request, '403.json', {},
                  content_type='application/json',
                  status=403)


def valid_phone_number(phone_number):
    # +380973426645
    if phone_number[0] != '+':
        return False

    if len(phone_number) != 13:
        return False
    for i in range(1,13):
        if not phone_number[i].isalnum():
            return False
    return True