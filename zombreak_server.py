from typing import Optional
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from collections.abc import Callable, Awaitable
import asyncio
from player.player_shelter import PlayerShelter
import logic.game_state as game
import uuid
import os.path as path

app = FastAPI()
games_container = []


class GameParams(BaseModel):
    initial_survivors: int
    players_names: list


def create_print(game_id: int) -> Callable[[str], None]:
    """
    Function used to inject print function - proper for client-server solution
    :param game_id: integer value of game id
    :return: functor of created print function
    """
    global games_container
    gc = games_container[game_id]

    def print_foo(message: str) -> None:
        private_message = False
        if 'Your Shelter:' in message:
            private_message = True

        if not private_message:
            for gamer in gc['outputs']:
                gc['outputs'][gamer].append(message)
        else:
            active = gc['state'].active_player
            gc['outputs'][active.name].append(message)
    return print_foo


def create_input(name: str, game_id: int) -> Callable[[str], Awaitable[str]]:
    """
    Function used to inject input function - proper for client-server solution
    :param name: string with name of player
    :param game_id: integer value of game id
    :return: functor of created input function
    """
    global games_container
    gc = games_container[game_id]

    async def waiter():
        while len(gc['inputs'][name]) <= 0:
            await asyncio.sleep(0.05)

    async def input_foo(message: str) -> str:
        gc['outputs'][name].append(message)
        await waiter()
        move = gc['inputs'][name].pop()
        return move

    return input_foo


async def create_io(game_id: int, game_state: game) -> None:
    """
    Function used to inject proper print and input functions to human players.
    :param game_id: integer value of game id
    :param game_state: GameState object with all game data inside
    """
    for player in game_state.players:
        player.print = create_print(game_id)
        if type(player) is PlayerShelter:
            player.input_async = create_input(player.name, game_id)


def validate_game_and_player_data(game_id: int, player_name: str) -> tuple[dict, int]:
    """
    Function used to ease validation of data given to post_player_move and get_player_ui.
    :param game_id: integer value of existing game
    :param player_name: string with name of player
    :return: dict with content to send out with status code, integer with status code
    """
    if game_id >= len(games_container):
        return {'status': 'No game', 'output': None}, 404
    gs = games_container[game_id]['state']
    names = [player.name for player in gs.players]
    if player_name not in names:
        return {'status': 'No player', 'output': None}, 404
    return {}, 200


@app.on_event("startup")
async def startup_event() -> None:
    """
    Method used to setup starting game server.
    """
    global games_container
    games_container = []


@app.get("/js/{file}", include_in_schema=False)
def get_javascript(file: str):
    content = ''
    if path.isfile(f'./html/js/{file}'):
        with open(f'./html/js/{file}') as file:
            content = file.read()
            return HTMLResponse(content=content, status_code=200)
    return HTMLResponse(content=content, status_code=400)


@app.get("/", include_in_schema=False)
async def read_root() -> HTMLResponse:
    """
    Method used to show welcome page of Macau game server.
    :return: HTML content
    """
    with open('./html/index.html') as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)


@app.post("/")
async def start_game(game_params: GameParams) -> JSONResponse:
    """
    Method used to create game instance with given parameters
    :param game_params: GameParams object with integer initial survivors and list of strings with players_names
    :return: Response with integer value of game_id
    """
    state = game.GameState()
    gp = game_params
    names = gp.players_names
    initial_survivors = gp.initial_survivors
    zombreak = {"state": state, "inputs": {}, 'outputs': {}, 'tokens': {}}
    for name in names:
        if type(name) is not str:
            return JSONResponse(content={'status': 'Wrong names', 'game_id': None}, status_code=400)
        zombreak['inputs'][name] = []
        zombreak['outputs'][name] = []
        zombreak['tokens'][name] = ''
    zombreak['outputs']['game'] = []
    state.setup_game(names, initial_survivors)
    games_container.append(zombreak)
    game_id = len(games_container) - 1
    await create_io(game_id, state)
    asyncio.create_task(state.play_game())
    content = {'status': 'OK', 'game_id': game_id}
    return JSONResponse(content=content, status_code=200)


@app.get("/{game_id}")
def get_game_log(game_id: int) -> JSONResponse:
    """
    Method used to get list of important events of game with given game id.
    :param game_id: integer value of existing game
    :return: Response with list with string with all important events in game
    """
    if game_id >= len(games_container):
        return JSONResponse(content={'status': 'No game', 'output': None}, status_code=404)
    outputs = games_container[game_id]['outputs']['game']
    return JSONResponse(content={"status": "OK", "output": outputs}, status_code=200)


@app.get("/{game_id}/{player_name}/key")
def get_key_for_player_ui(game_id: int, player_name: str) -> JSONResponse:
    """
    Method used to generate user private access token for view ui and send moves
    :param game_id: integer value of existing game
    :param player_name: string with name of player
    :return: Response with access token as string
    """
    content, status_code = validate_game_and_player_data(game_id, player_name)
    if status_code != 200:
        return JSONResponse(content=content, status_code=status_code)

    token = games_container[game_id]['tokens'][player_name]
    if token == '':
        token = uuid.uuid4().hex
        response = JSONResponse(status_code=200, content={'status': 'OK', 'access_token': token})
        games_container[game_id]['tokens'][player_name] = token
        return response
    return JSONResponse(status_code=403, content={'status': 'Token already exists'})


@app.get("/{game_id}/{player_name}")
def get_player_ui(game_id: int, player_name: str, access_token: Optional[str]) -> JSONResponse:
    """
    Method used to get messages prepared for a player with the given name
    :param game_id: integer value of existing game
    :param player_name: string with name of player
    :param access_token: User private access token
    :return: Response list of strings with all messages to player with given name
    """
    content, status_code = validate_game_and_player_data(game_id, player_name)
    if status_code != 200:
        return JSONResponse(content=content, status_code=status_code)

    token = games_container[game_id]['tokens'][player_name]
    if access_token != token or token is None:
        return JSONResponse(content={"status": "Bad token", "output": None}, status_code=401)

    outputs = games_container[game_id]['outputs'][player_name]
    return JSONResponse(content={"status": "OK", "output": outputs}, status_code=200)


@app.post("/{game_id}/{player_name}")
def post_player_move(game_id: int, player_name: str, player_move: str, access_token: Optional[str]) -> JSONResponse:
    """
    Method used to send next move by player with given name to game with given game id
    :param game_id: integer value of existing game
    :param player_name: string with name of player
    :param player_move: string with player's next move
    :param access_token: User private access token
    :return: Response with saved next player's move
    """
    content, status_code = validate_game_and_player_data(game_id, player_name)
    if status_code != 200:
        return JSONResponse(content=content, status_code=status_code)

    token = games_container[game_id]['tokens'][player_name]
    if access_token != token or token is None:
        return JSONResponse(content={"status": "Bad token", "input": None}, status_code=401)

    games_container[game_id]['inputs'][player_name].append(player_move)
    return JSONResponse(content={'status': 'OK', "input": player_move}, status_code=200)
