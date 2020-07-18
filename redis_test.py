from redis import Redis
from rq import Queue

q = Queue(connection=Redis())

from my_module import count_words_at_url
result = q.enqueue(
             count_words_at_url, 'http://nvie.com')

print(result)