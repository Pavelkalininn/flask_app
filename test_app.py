import os
from app import create_table
import unittest
import tempfile

app = flask.Flask(__name__)


class FlaskTestCase(unittest.TestCase):

    def __init__(self):
        self.app = app.test_client()
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()

    def setUp(self):
        app.config['TESTING'] = True
        with app.app_context():
            create_table()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_client_create(self):
        print(
            (
                self.app.post(
                    '/api/users/',
                    data=dict(
                        username="username",
                        name="name"
                    )
                )
            ).data
        )
        self.app.post(
            '/api/users/',
            data={"username": "username", "name": "name"}
        )
        request = self.app.get('/api/users/')
        self.assertEqual(
            request.data,
            {
                "Users":
                [
                    {
                        "name": "name",
                        "username": "username"
                    },
                    {
                        "name": "name1",
                        "username": "username1"
                    }
                ]
            }
        )

    def test_parameter_create(self):
        self.app.post(
            '/api/parameters/username/parameter_name/int/',
            data={"value": "244"}
        )
        request = self.app.get('/api/parameters/username/parameter_name/int/')
        self.assertEqual(
            request.data,
            {
                "name": "parameter_name",
                "type": "int",
                "user": "username",
                "value": 244
            }
        )


if __name__ == '__main__':
    unittest.main()
