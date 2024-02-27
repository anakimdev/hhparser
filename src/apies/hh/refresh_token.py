import requests
import configs

def get_token():
    post_data = {'grant_type': 'client_credentials',
        'client_secret': configs.CLIENT_SECRET,
        'client_id': configs.CLIENT_ID}
    response = requests.post(url = configs.TOKEN_URL, data = post_data)
    print(response.json())

get_token()
