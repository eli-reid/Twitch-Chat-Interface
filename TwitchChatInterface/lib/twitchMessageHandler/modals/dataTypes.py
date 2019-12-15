class Message(object):
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

class Channel(object):

    def __init__(self):
        self.name: str = ""
        self.mods: list = []

class RoomeState():

    def __init__(self):
        self.emote_only=0
        self.followers_onlyself.y=0
        self.r9k=0
        self.slow=0
        self.subs_only=0 

class UserNotice():

    def __init__():
        self.badge_info=""
        self.badges=""
        self.color=""
        self.display_name=""
        self.emote_sets=""
        self.turbo=""
        self.user_id=""
        self.user_type=""



