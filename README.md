# Kitchen nightmares

[Diagram](https://github.com/sanjeevsiva17/kitchen-nightmares/Diagram.png?raw=true)

## Getting started

### Recommended Start
    
    git clone
    cd kitchen-nightmares
    virtualenv -p python3 env
    source env/bin/activate
    pip install -r requirements.txt

Install [RabbitMQ](https://www.rabbitmq.com/download.html)

Install [Redis](https://redis.io/download)

    
Finally 

Run RabbitMQ for the messaging queue in the background in a different terminal

`rabbitmq-server`


Run Redis for Django channel layers and declined notifications.

`redis-server` 

Start the server

`python manage.py runserver`


### Libraries

[Django-fsm](https://github.com/viewflow/django-fsm)

[Django-Channels](https://github.com/django/channels)

[pika](https://github.com/pika/pika)

[redis-py](https://github.com/andymccurdy/redis-py/tree/a9347cd0bc3c361cbdf4af6811ee465211eabdb0)

