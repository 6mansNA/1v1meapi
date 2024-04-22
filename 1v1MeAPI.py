import requests

class Client:
    def __init__(self, authorization_token:str) -> None:
        """
        Initializes the Client with an authorization token.
        
        Parameters:
        - authorization_token (str): The bearer token used for authorization in API requests.
        """
        self.authorization_token = authorization_token
        self.base_url = "https://api.1v1me.com/api"
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": f"Bearer {authorization_token}",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Origin": "https://www.1v1me.com",
            "Referer": "https://www.1v1me.com/",
            "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        }

    def _send_request(self, endpoint, payload) -> dict:
        """
        Sends a POST request to a specified API endpoint with the given payload.

        Parameters:
        - endpoint (str): The API endpoint to send the request to.
        - payload (dict): The payload of the request.

        Returns:
        - dict: A dict containing the JSON response.
        """
        full_url = f"{self.base_url}{endpoint}"
        response = requests.post(full_url, headers=self.headers, json=payload)
        return response.json()
    
    def _get_request(self, endpoint, payload) -> dict:
        """
        Sends a GET request to a specified API endpoint with the given payload.

        Parameters:
        - endpoint (str): The API endpoint to send the request to.
        - payload (dict): The payload of the request.

        Returns:
        - dict: A dict containing the JSON response.
        """
        full_url = f"{self.base_url}{endpoint}"
        response = requests.get(full_url, headers=self.headers, data=payload)
        return response.json()

    def send_message(self, conversation_id: int | str, text=None, giphy_id=None, imgur_id=None) -> dict:
        """
        Sends a message to a specific conversation.

        Parameters:
        - conversation_id (int | str): The ID of the conversation or a URL containing the conversation ID.
        - text (str): The text of the message to send.
        - message_type (str): The type of the message. Default is "Message::TextMessage".

        Returns:
        - dict: A dict containing the JSON response.
        """
        if isinstance(conversation_id, int):
            if text:
                payload = {
                    "conversation_id": int(conversation_id.split('=')[1]),
                    "text": text,
                    "type": "Message::TextMessage"
                }
            elif giphy_id:
                payload = {
                    "conversation_id": int(conversation_id.split('=')[1]),
                    "giphy_id": giphy_id,
                    "type": "Message::GiphyMessage"
                }
            else:
                payload = {
                    "conversation_id": int(conversation_id.split('=')[1]),
                    "imgur_id": imgur_id,
                    "type": "Message::ImgurMessage"
                }
        elif isinstance(conversation_id, str):
            if 'https://www.1v1me.com/inbox?convo=' in conversation_id:
                if text:
                    payload = {
                        "conversation_id": int(conversation_id.split('=')[1]),
                        "text": text,
                        "type": "Message::TextMessage"
                    }
                elif giphy_id:
                    payload = {
                        "conversation_id": int(conversation_id.split('=')[1]),
                        "giphy_id": giphy_id,
                        "type": "Message::GiphyMessage"
                    }
                else:
                    payload = {
                        "conversation_id": int(conversation_id.split('=')[1]),
                        "imgur_id": imgur_id,
                        "type": "Message::ImgurMessage"
                    }
            else:
                return {'error':'Invalid conversation ID'}
        else:
            return {'error':'Invalid conversation ID'}
        return self._send_request("/v1/messages", payload)

    def bet(self, game_id: int, team_id: int, amount: int) -> dict:
        """
        Places a bet on a game.

        Parameters:
        - game_id: The ID of the game to bet on.
        - team_id: The ID of the team to place the bet on.
        - amount: The amount of the bet.

        Returns:
        - dict: A dict containing the JSON response.
        """
        payload = {
            "tournament_team_id": team_id,
            "amount": int(amount * 100)
        }
        return self._send_request(f"/v1/stakes/{game_id}/purchase", payload)
    
    def get_matches(self, amount: int=20) -> dict:
        """
        Retrieves a list of matches.

        Parameters:
        - amount (int): The number of matches to retrieve.

        Returns:
        - dict: A dict containing the JSON response.
        """    
        endpoint = f"/v1/stakes?page=1&page_size={amount}"
        return self._get_request(endpoint, payload=None)
    
    def send_reaction(self, message_id: int, reaction: str) -> dict:
        
        endpoint = f"/v1/messages/{message_id}/reactions"
        payload = {
            "type": "utf8",
            "value": reaction
        }
        return self._send_request(endpoint, payload)
    
    def cheer(self, tv_id: int, team_id: int, amount: int) -> dict:
        """
        Sends a cheer to a specific game.

        Parameters:
        - tv_id (int): The ID of the TV/Game to cheer on.
        - team_id (int): The ID of the team to cheer.
        - amount (int): The amount of the cheer.

        Returns:
        - dict: A dict containing the JSON response.
        """
        endpoint = f"/v1/tv/{tv_id}/cheer"
        payload = {
            "amount": amount,
            "team_id": team_id
        }
        return self._send_request(endpoint, payload)
    
    def get_teams_info(self, game_id: int) -> dict:
        """
        Retrieves information on each team from a game.

        Parameters:
        - game_id (int): The ID of the game in which the teams are playing.

        Returns:
        - dict: A dict containing the JSON response.
        """
        endpoint = f"/v1/stakes/{game_id}/teams"
        return self._get_request(endpoint, payload=None)

    def get_play_by_play(self, game_id: int, amount: int) -> dict:
        """
        Retrieves information on play by play.

        Parameters:
        - game_id (int): The ID of the game in which the teams are playing.
        - amount: The amount of plays to retrieve.

        Returns:
        - dict: A dict containing the JSON response.
        """
        endpoint = f"/v1/matches/{game_id}/play_by_plays?page_size={amount}"
        return self._get_request(endpoint, payload=None)
    
    def get_self_user_info(self):
        """
        Retrieves your information.

        Returns:
        - dict: A dict containing the JSON response.
        """
        endpoint = f"/v1/users/online"
        return self._send_request(endpoint, payload=None)
    
    def get_user_info(self, user_id: int) -> dict:
        """
        Retrieves your information.

        Returns:
        - dict: A dict containing the JSON response.
        """
        #https://api.1v1me.com/api/v1/users/824034
        endpoint = f"/v1/users/{user_id}"
        return self._get_request(endpoint, payload=None)
    
    def get_live_streams(self) -> dict:
        """
        Retrieves current games to watch.

        Returns:
        - dict: A dict containing the JSON response.
        """
        endpoint = f"/v1/stakes/watch"
        return self._get_request(endpoint, payload=None)
    
    
