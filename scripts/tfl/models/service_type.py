from msrest.serialization import Model

class ServiceType(Model):
    """ServiceType.

    :param name:
    :type name: str
    :param uri:
    :type uri: str
    """

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'uri': {'key': 'uri', 'type': 'str'}
	}
    
    def __init__(self, name=None, uri=None):
        super(ServiceType, self).__init__()
        self.name = name
        self.uri = uri