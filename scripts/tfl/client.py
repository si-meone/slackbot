from msrest import Deserializer
from .config import endpoints
from .api_token import ApiToken
from .rest_client import RestClient
from . import models

class Client:
    """Client

    :param ApiToken api_token: API token to access TfL unified API
    """

    def __init__(self, api_token):
        self.client = RestClient(api_token)
        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
        #print (client_models)
        self._deserialize = Deserializer(client_models)

    def get_stop_points_by_line_id(self, line_id):
        response = self.client.send_request(endpoints['stopPointsByLineId'].format(line_id))
        if response.status_code is not 200:
            return self._deserialize('ApiError', response)
        return self._deserialize('[StopPoint]', response)

    def get_line_meta_modes(self):
        response = self.client.send_request(endpoints['lineMetaModes'])
        if response.status_code is not 200:
            return self._deserialize('ApiError', response)
        return self._deserialize('[Mode]', response)

    def get_lines(self, line_id=None, mode=None):
        if line_id is None and mode is None:
            raise Exception('Either the --line_id argument or the --mode argument needs to be specified.')
        if line_id is not None:
            endpoint = endpoints['linesByLineId'].format(line_id)
        else:
            endpoint = endpoints['linesByMode'].format(mode)
        response = self.client.send_request(endpoint)
        if response.status_code is not 200:
            return self._deserialize('ApiError', response)
        return self._deserialize('[Line]', response)

    def get_line_status(self, line, include_details=None):
        response = self.client.send_request(endpoints['lineStatus'].format(line), {'detail': include_details is True})
        if response.status_code is not 200:
            return self._deserialize('ApiError', response)
        return self._deserialize('[Line]', response)

    def get_line_status_severity(self, severity):
        response = self.client.send_request(endpoints['lineStatusBySeverity'].format(severity))
        if response.status_code is not 200:
            return self._deserialize('ApiError', response)
        return self._deserialize('[Line]', response)

    def get_route_by_line_id(self, line_id):
        response = self.client.send_request(endpoints['routeByLineId'].format(line_id))
        if response.status_code is not 200:
            return self._deserialize('ApiError', response)
        return self._deserialize('[Line]', response)

    def get_route_by_mode(self, mode):
        response = self.client.send_request(endpoints['routeByMode'].format(mode))
        if response.status_code is not 200:
            return self._deserialize('ApiError', response)
        return self._deserialize('[Line]', response)

    def get_line_disruptions_by_line_id(self, line_id):
        response = self.client.send_request(endpoints['lineDisruptionsByLineId'].format(line_id))
        if response.status_code is not 200:
            return self._deserialize('ApiError', response)
        return self._deserialize('[Disruption]', response)

    def get_line_disruptions_by_mode(self, mode):
        response = self.client.send_request(endpoints['lineDisruptionsByMode'].format(mode))
        if response.status_code is not 200:
            return self._deserialize('ApiError', response)
        return self._deserialize('[Disruption]', response)

    def get_stop_points_by_id(self, id):
        response = self.client.send_request(endpoints['stopPointById'].format(id))
        if response.status_code is not 200:
            return self._deserialize('ApiError', response)
        return self._deserialize('StopPoint', response)
    
    def get_stop_points_by_mode(self, mode):
        response = self.client.send_request(endpoints['stopPointByMode'].format(mode))
        if response.status_code is not 200:
            return self._deserialize('ApiError', response)
        return self._deserialize('StopPointsResponse', response)

    def get_stop_point_meta_modes(self):
        response = self.client.send_request(endpoints['stopPointMetaModes'])
        if response.status_code is not 200:
            return self._deserialize('ApiError', response)
        return self._deserialize('[Mode]', response)

    def get_arrivals_by_line_id(self, line_id):
        response = self.client.send_request(endpoints['arrivalsByLineId'].format(line_id))
        if response.status_code is not 200:
            return self._deserialize('ApiError', response)
        return self._deserialize('[Prediction]', response)

    def get_arrivals_by_stop_id(self, stop_id):
        # GET	/StopPoint/{id}/Arrivals
        # https://api.tfl.gov.uk/StopPoint/490005183E/arrivals
        response = self.client.send_request(endpoints['arrivalsByStopId'].format(stop_id))
        if response.status_code is not 200:
            return self._deserialize('ApiError', response)
        return self._deserialize('[Prediction]', response)