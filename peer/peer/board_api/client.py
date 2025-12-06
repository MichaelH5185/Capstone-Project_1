import requests

API_URL_BOARDS = 'http://boards_service_url/api/boards'
API_URL_BOARD_MESSAGES = 'http://boards_service_url/api/messages'

def fetch_boards(owner_id):
    response = requests.get(API_URL_BOARDS, params={'owner_id': owner_id})
    response.raise_for_status()
    return response.json

def fetch_messages(owner_id):
    response = requests.get(API_URL_BOARD_MESSAGES, params={'owner_id': owner_id})
    response.raise_for_status()
    return response.json

def create_board(owner_id, moderator_id, name, skill, subskill):
    payload = {
        'creator': owner_id,
        'name': name,
        'moderator': moderator_id,
        'skill': skill,
        'subskill': subskill,
    }
    response = requests.post(API_URL_BOARDS, json=payload)
    response.raise_for_status()  # Raises error if request fails
    return response.json()

def create_board_message(owner_id, reply_to, content, board):
    payload = {
        'poster': owner_id,
        'reply_to': reply_to,
        'content': content,
        'board': board,
    }
    response = requests.post(API_URL_BOARD_MESSAGES, json=payload)
    response.raise_for_status()  # Raises error if request fails
    return response.json()

def delete_board(board_id):
    url = f"http://boards_service_url/api/boards/{board_id}/"
    response = requests.delete(url)
    response.raise_for_status()
    return response.status_code