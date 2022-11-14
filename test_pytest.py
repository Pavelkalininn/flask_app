

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_edit_user(client):

    response = client.post(
        '/api/users/',
        data=dict(username="username", name="name")
    )
    assert response.status_code == 200

    request = self.app.get('/api/users/')
    assert request.data, {"Users":
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


if __name__ == '__main__':
    pytest.test_edit_user()
