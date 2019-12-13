class message(object):
    """description of class"""

    def __init__(self):
        self.raw: str = ""
        self.tags: dict = {}
        self.id: str = ""
        self.prefix: str = None
        self.command: str = None
        self.text: str = ""
        self.channel: channel = None
        self.tags={}
        self.params=[]

class channel(object):

    def __init__(self):
        self.name: str = ""
        self.mods: list = []


