import json
from django.conf import settings
import redis
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

# Connect to our Redis instance
r = redis.StrictRedis(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT, db=0)


@api_view(['GET'])
def visited_domains(request, *args, **kwargs):
    if request.method == 'GET':
        items = {}
        count = 0
        for key in r.keys("*"):
            items[key.decode("utf-8")] = r.get(key)
            count += 1
        response = {
            'count': count,
            'msg': f"Found {count} items.",
            'items': items
        }
        return Response(response, status=200)

@api_view(['POST'])
def visited_links(request, *args, **kwargs):
    if request.method == 'POST':
        item = json.loads(request.body)
        key = list(item.keys())[0]
        value = item[key]
        r.set(key, value)
        response = {
            'msg': f"{key} successfully set to {value}"
        }
        return Response(response, 201)