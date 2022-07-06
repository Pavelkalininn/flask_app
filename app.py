from flask import Flask, request
from flask_restful import Api
from models import db, UsersModel, ParametersModel

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


@app.route('/api/users/', methods=['GET', 'POST'])
def get_user():
    if request.method == 'GET':
        users = UsersModel.query.all()
        return {'Users': list(user.json() for user in users)}
    else:
        data = request.get_json()

        new_user = UsersModel(data['name'], data['username'])
        db.session.add(new_user)
        db.session.commit()
        return new_user.json(), 201


@app.route('/api/parameters/<user>/<name>/<type>/', methods=['GET', 'POST'])
def get_parameters(user, name, type):
    current_user = UsersModel.query.filter_by(username=user).all()
    if not current_user:
        return {'message': 'user not found'}, 404
    if type not in ['int', 'str']:
        return {'message': 'parameter type should be "int" or "str"'}, 400

    if request.method == "GET":
        parameter = ParametersModel.query.filter_by(
            user=user).filter_by(name=name).filter_by(type=type).first()
        if parameter:
            if parameter.type == 'int':
                parameter.value = int(parameter.value)
            return parameter.json()
        return [], 204

    else:
        data = request.get_json()
        parameter = ParametersModel.query.filter_by(
            user=user).filter_by(name=name).filter_by(type=type).first()
        value = data.get("value")
        if type == 'int':
            if not value.isnumeric():
                return {'message': 'wrong type of value'}, 400
            value = int(value)
        if parameter:
            parameter.value = value
        else:
            parameter = ParametersModel(
                user=user, name=name, type=type, value=value)
        db.session.add(parameter)
        db.session.commit()
        return parameter.json()


@app.route('/api/parameters/<user>/<name>/', methods=['GET'])
def get_parameters_without_type(user, name):
    current_user = UsersModel.query.filter_by(username=user).all()
    if not current_user:
        return {'message': 'user not found'}, 404

    if request.method == "GET":
        parameters = ParametersModel.query.filter_by(
            user=user).filter_by(name=name).all()
        list_parameters = []
        if parameters:
            for parameter in parameters:
                if parameter.type == 'int':
                    parameter.value = int(parameter.value)
                list_parameters.append(parameter.json())
            return {'Parameters': list_parameters}
        return {'message': 'parameter not found'}, 404


@app.route('/api/parameters/<user>/', methods=['GET'])
def get_parameters_by_user(user):
    current_user = UsersModel.query.filter_by(username=user).all()
    if not current_user:
        return {'message': 'user not found'}, 404
    parameters = ParametersModel.query.filter_by(
        user=user).all()
    list_parameters = []
    if parameters:
        for parameter in parameters:
            if parameter.type == 'int':
                parameter.value = int(parameter.value)
            list_parameters.append(parameter.json())
        return {'Parameters': list_parameters}
    return {'message': 'parameter not found'}, 404


@app.route('/api/<user>/', methods=['POST'])
def post_parameters_by_user(user):
    data = request.get_json().get('Query')
    if not data:
        return {'message', 'no data'}, 400
    current_user = UsersModel.query.filter_by(username=user).all()
    if not current_user:
        return {'message': 'user not found'}, 404
    parameters = []
    for parameter_data in data:
        status = 'OK'
        name = parameter_data.get('Name')
        type = parameter_data.get('Type')
        value = parameter_data.get('Value')
        if (parameter_data.get('Operation') != 'SetParam'
                or type not in ['int', 'str']):
            status = 'ERROR'

        if type == 'int':
            if not value.isnumeric():
                status = 'ERROR'
            value = int(value)

        parameter = ParametersModel(
            user=user, name=name, type=type, value=value)

        db.session.add(parameter)
        db.session.commit()
        parameter = parameter.json()
        parameter.pop('user')
        parameter.pop('value')
        parameter['Operation'] = 'SetParam'
        parameter['Status'] = status
        parameters.append(parameter)

    return {'Result': parameters}


app.debug = True
if __name__ == '__main__':
    app.run(host='localhost', port=8000)
