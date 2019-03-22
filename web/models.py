import requests

class ApiRestaurantException(Exception):
    pass

class ApiRestaurantTokenInvalidException(Exception):
    pass

"""
This is an extension for requests class.

As in the client, the token has to be handled in a different way,
we need to send a different exception to be catched.

"""
class RestaurantApiClient():
    accepted_methods = ["get", "post", "delete"]

    """
    Parse response from API and check if token is invalid.

    Args:
        response: Response from API, request.response object.

    Returns:
        JSON object if response has status 200.

    Raises:
        ApiRestaurantTokenInvalidException: token has expired or is missing.
        ApiRestaurantException: Other not token issues (permissions, etc).
    """
    def parseResponse(self, response):
        json_response = response.json()
        if response.status_code != 200:
            if json_response["message"] == "Token is invalid!":
                raise ApiRestaurantTokenInvalidException("Token is invalid!")
            else:
                raise ApiRestaurantException(json_response["message"])
        else:
            return json_response

    """
    Send a request using requests package.

    Args:
        http_method: must be post, delete or get.
        others: the other parameters are passed to requests class.

    Returns:
        JSON object if response has status 200.

    Raises:
        ApiRestaurantException: if status is not 200, return message from API.
    """
    def sendRequest(self, *args, **kwargs):
        if not "http_method" in kwargs:
            raise ApiRestaurantException("Parameter http_method not found.")
        if kwargs["http_method"] not in self.accepted_methods:
            raise ApiRestaurantException("Invalid http_method.")

        http_method = kwargs.pop("http_method")
        http_request = getattr(requests, http_method)
        try:
            r = http_request(*args, **kwargs)
        except requests.exceptions.ConnectionError:
            raise ApiRestaurantException("API restaurant down!")

        return self.parseResponse(r)

