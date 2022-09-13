import json, time, redis
from datetime import datetime
from django.conf import settings
from django.http import (HttpResponseRedirect, HttpResponseBadRequest)
from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from urllib.parse import urlparse

# Connect to our Redis instance
r = redis.StrictRedis(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT, db=0)


@api_view(['GET'])
def visited_domains(request, *args, **kwargs):
    if request.method == 'GET':
        try:
            print("делаю")
            time1 = int(request.GET.get('from'))
            time2 = int(request.GET.get('to'))
            domains = set()
            for target_time in range(time1, time2):
                try: # Этот обработчик ошибок нужен если в redis вдруг попадутся данные, отличные от множества, тогда просто пропускаем их
                    if r.smembers(str(target_time)):
                        print(target_time, datetime.fromtimestamp(target_time), r.smembers(str(target_time)))
                        domains.update(r.smembers(str(target_time)))
                except: pass
            return Response(data={'domains': domains, 'status': 'ok'}, status=200)
        except Exception as e: HttpResponseBadRequest(content=e)
    return Response(f"запрос некорректный, пример (последние 24 часа): http://127.0.0.1:8000/visited_domains?from={round(time.time())-86400}&to={round(time.time())}", status=400)


@api_view(['POST'])
def visited_links(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            items = json.loads(request.body)
            links=[]
            for item in items['links']:
                # парсим каждую запись, чтобы отделить домены
                item_parsed = urlparse(item)
                # собираю список из доменов
                links.append(item_parsed.netloc or item_parsed.path)
            # раз все эти домены приехали с одним временем, сразу убираем одинаковые чтобы не раздувать базу redis
            links = set(links)
            print("links = ", links)
            # пишем в redis: дата - ключ, домены - множество
            r.sadd(round(time.time()), *links)
            print(round(time.time()))
            return Response(data={'status': 'ok'}, status=201)
        except Exception as e: HttpResponseBadRequest(content=e)
    return HttpResponseRedirect(reverse('links'))


