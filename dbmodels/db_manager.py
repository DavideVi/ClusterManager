
class DBManager():

    class __DBManager:
        def __init__(self, endpoint):
            self.endpoint = endpoint
        def __str__(self):
            return repr(self) + self.val

    instance = None

    def __init__(self, endpoint):
        if not DBManager.instance:
            DBManager.instance = DBManager.__DBManager(endpoint)
        else:
            DBManager.instance.endpoint = endpoint

    def __getattr__(self, name):
        return getattr(self.instance, name)
