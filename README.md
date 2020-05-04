# Kitchen nightmares
## Getting started

###Recommended Start
    
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


