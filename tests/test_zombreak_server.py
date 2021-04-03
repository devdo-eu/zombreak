from fastapi.testclient import TestClient
from time import sleep
from zombreak_server import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_start_game():
    game_json = {'initial_survivors': 2, 'players_names': ["John", "CPU1"]}
    response = client.post("/", json=game_json)
    assert response.status_code == 200
    assert response.json()['game_id'] == 0
    assert response.json()['status'] == 'OK'

    game_json = {'initial_survivors': 2, 'players_names': ["John", 462462]}
    response = client.post("/", json=game_json)
    assert response.status_code == 400
    assert response.json()['game_id'] is None
    assert response.json()['status'] == 'Wrong names'


def test_next_start_game():
    game_json = {'initial_survivors': 2, 'players_names': ["John", "CPU1"]}
    response = client.post("/", json=game_json)
    assert response.status_code == 200
    assert response.json()['game_id'] == 1
    assert response.json()['status'] == 'OK'

    with TestClient(app) as tc:
        response = tc.post("/", json=game_json)
        assert response.status_code == 200
        assert response.json()['game_id'] == 0
        assert response.json()['status'] == 'OK'


def test_get_game_output():
    game_json = {'initial_survivors': 2, 'players_names': ["John", "Tony"]}
    with TestClient(app) as tc:
        response = tc.post("/", json=game_json)
        assert response.status_code == 200
        assert response.json()['game_id'] == 0
        assert response.json()['status'] == 'OK'

        response = tc.get("/250")
        assert response.status_code == 404
        assert response.json()['status'] == 'No game'
        assert response.json()['output'] is None

        response = tc.get("/0")
        output = response.json()['output']
        assert response.status_code == 200
        assert response.json()['status'] == "OK"
        assert len(output) >= 1
        assert output[0] == 'John will play round now...'


def test_get_player_ui():
    game_json = {'initial_survivors': 2, 'players_names': ["John", "CPU1"]}
    with TestClient(app) as tc:
        response = tc.post("/", json=game_json)
        assert response.status_code == 200
        assert response.json()['game_id'] == 0
        assert response.json()['status'] == 'OK'

        response = tc.get("/250/Tony?access_token=0")
        assert response.status_code == 404
        assert response.json()['status'] == 'No game'
        assert response.json()['output'] is None

        response = tc.get("/0/Tony?access_token=0")
        assert response.status_code == 404
        assert response.json()['status'] == 'No player'
        assert response.json()['output'] is None

        response = tc.get("/250/Tony/key")
        assert response.status_code == 404
        assert response.json()['status'] == 'No game'
        assert response.json()['output'] is None

        response = tc.get("/0/Tony/key")
        assert response.status_code == 404
        assert response.json()['status'] == 'No player'
        assert response.json()['output'] is None

        response = tc.get("/0/John?access_token=0")
        assert response.status_code == 401
        assert response.json()['status'] == 'Bad token'
        assert response.json()['output'] is None

        response = tc.get("/0/John/key")
        assert response.status_code == 200
        assert response.json()['status'] == 'OK'
        assert response.json()['access_token'] != ''
        token = response.json()['access_token']

        response = tc.get("/0/John/key")
        assert response.status_code == 403
        assert response.json()['status'] == 'Token already exists'

        response = tc.get(f"/0/John?access_token={token}")
        assert response.status_code == 200
        assert response.json()['status'] == 'OK'
        assert "John" in response.json()['output'][0]
        assert 'John will play round now...' == response.json()['output'][0]
        assert 'Your Shelter: "John"' in response.json()['output'][1]


def test_post_player_move():
    game_json = {'initial_survivors': 2, 'players_names': ["John", "CPU1"]}
    with TestClient(app) as tc:
        response = tc.post("/", json=game_json)
        assert response.status_code == 200
        assert response.json()['game_id'] == 0
        assert response.json()['status'] == 'OK'
        move = "0"

        response = tc.post(f"/0/John?player_move={move}&access_token=0")
        assert response.status_code == 401
        assert response.json()['status'] == 'Bad token'
        assert response.json()['input'] is None

        response = tc.get("/0/John/key")
        assert response.status_code == 200
        assert response.json()['status'] == 'OK'
        assert response.json()['access_token'] != ''
        token = response.json()['access_token']

        response = tc.get(f"/0/John?access_token={token}")
        assert response.status_code == 200
        assert response.json()['status'] == 'OK'
        response = tc.post(f"/0/John?player_move={move}&access_token={token}")
        sleep(0.05)
        assert response.status_code == 200
        assert response.json()['status'] == 'OK'
        assert response.json()['input'] == move

        response = tc.post(f"/0/John?player_move={move}&access_token={token}")
        sleep(0.05)
        assert response.status_code == 200
        assert response.json()['status'] == 'OK'
        assert response.json()['input'] == move

        sleep(0.05)
        response = tc.get(f"/0/John?access_token={token}")
        assert response.status_code == 200
        assert response.json()['status'] == 'OK'
        output = response.json()['output']
        assert len(output) > 4


def test_post_player_move_negatives():
    game_json = {'initial_survivors': 2, 'players_names': ["John", "CPU1"]}
    with TestClient(app) as tc:
        response = tc.post("/", json=game_json)
        assert response.status_code == 200
        assert response.json()['game_id'] == 0
        assert response.json()['status'] == 'OK'
        move = 'hearts Q'

        response = tc.post(f"/250/John?player_move={move}&access_token=0")
        sleep(0.05)
        assert response.status_code == 404
        assert response.json()['status'] == 'No game'

        response = tc.post(f"/0/Tony?player_move={move}&access_token=0")
        sleep(0.05)
        assert response.status_code == 404
        assert response.json()['status'] == 'No player'


def test_get_game_log():
    game_json = {'initial_survivors': 2, 'players_names': ["John", "CPU1"]}
    with TestClient(app) as tc:
        response = tc.post("/", json=game_json)
        assert response.status_code == 200
        assert response.json()['game_id'] == 0
        assert response.json()['status'] == 'OK'

        response = tc.get("/0/John/key")
        assert response.status_code == 200
        assert response.json()['access_token'] != ''
        token = response.json()['access_token']

        response = tc.get(f"/0/John?access_token={token}")
        assert response.status_code == 200
        assert response.json()['status'] == 'OK'
        move = '3'
        response = tc.post(f"/0/John?player_move={move}&access_token={token}")
        sleep(0.05)
        assert response.status_code == 200
        assert response.json()['status'] == 'OK'
        assert response.json()['input'] == move
        sleep(0.05)

        response = tc.post(f"/0/John?player_move={move}&access_token={token}")
        sleep(0.05)
        assert response.status_code == 200
        assert response.json()['status'] == 'OK'
        assert response.json()['input'] == move
        sleep(0.05)

        response = tc.get("/0")
        assert response.status_code == 200
        assert response.json()['status'] == 'OK'
        data = response.json()['output']
        assert len(data) > 0
        assert 'John will play round now...' == data[0]
        assert 'John discards all supplies.' == data[1]
        assert 'John turn has ended.' == data[2]

        response = tc.get("/250")
        assert response.status_code == 404
        assert response.json()['status'] == 'No game'


def test_get_javascript():
    with TestClient(app) as tc:
        response = tc.get("/js/index.js")
        assert response.status_code == 200

        response = tc.get("/js/nonsense.js")
        assert response.status_code == 400
