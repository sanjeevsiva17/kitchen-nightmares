# Kitchen nightmares
## Getting started

Install [RabbitMQ](https://www.rabbitmq.com/download.html)

Create a virtual environment

    virtualenv -p python3 env
    cd env
    source bin/activate
    git clone
    cd kitchen-nightmares
    pip install -r requirements.txt
    
Finally 

Run RabbitMQ for the messaging queue in the background in a different terminal

`rabbitmq-server`

Start the server

`python manage.py runserver`


