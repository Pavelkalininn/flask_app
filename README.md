# User Parameter Storage Server


### Description
API for creating and viewing parameters by user name, parameter name, type

### Technologies
Python 3.7.9
Flask==2.1.2
Flask-RESTful==0.3.9
Flask-SQLAlchemy==2.5.1

### To run in dev mode (Windows) in the work folder:

    python -m venv venv
    source venv/Scripts/activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    
    python app.py

API requests will be available at: http://localhost:8000/

## Request examples:

###To add and update a parameter, you need

POST request at /api/parameters/<user>/<name>/<type>/  with dictionary in request body:

    {
        "value": "Значение параметра"
    }

###To get the parameter:

GET request at /api/parameters/<user>/<name>/<type>/ with dictionary in request body:

Answer:

    {   
        "name": "имя параметра",
        "type": "тип параметра",
        "value": "Значение параметра"
    }

###Get all user parameters:

GET request at  /api/parameters/<user>/

Answer:

    {   
        "name": "имя параметра",
        "type": "тип параметра",
        "value": "Значение параметра"
    }

### Adding parameters via the json API:

POST request at/api/<user>/:

    {
        "Query":
            [
                {
                    "Operation":"SetParam",
                    "Name": "parameter name",
                    "Type": "parameter type",
                    "Value":"parameter value"
                }
            ]
    }

Answer:

    {
        "Result":
            [
                {
                    "Operation":"SetParam",
                    "name": "parameter name",
                    "type": "parameter type",
                    "Status":"OK|ERROR"
                }
            ]
    }


### Author Pavel Kalinin
