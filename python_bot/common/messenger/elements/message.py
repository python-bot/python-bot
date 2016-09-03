class MessageType:
    text = "text"
    contact = "contact"
    location = "location"
    audio = "audio"
    voice = "voice"
    document = "document"
    sticker = "sticker"
    video = "video"
    venue = "venue"
    new_chat_member = "new_chat_member"
    left_chat_member = "left_chat_member"


ALLOWED_TYPES = [MessageType.text]


def create_message(content_type, **kwargs):
    if content_type not in ALLOWED_TYPES:
        return

    for sub_class in BotBaseMessage.__subclasses__():
        if content_type == sub_class.content_type:
            return sub_class(**kwargs)


class BotBaseMessage:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if hasattr(self, "content_type"):
            self.kwargs["content_type"] = self.content_type
        self.message_id = self.kwargs.get("message_id")
        self.user = self.kwargs.get("user")
        self.date = self.kwargs.get("date")

        # self.chat = chat
        # self.forward_from_chat = None
        # self.forward_from = None
        # self.forward_date = None
        # self.reply_to_message = None
        # self.edit_date = None

        # self.text = None
        # self.entities = None
        # self.audio = None
        # self.document = None
        # self.photo = None
        # self.sticker = None
        # self.video = None
        # self.voice = None
        # self.caption = None
        # self.contact = None
        # self.location = None
        # self.venue = None
        # self.new_chat_member = None
        # self.left_chat_member = None
        # self.new_chat_title = None
        # self.new_chat_photo = None
        # self.delete_chat_photo = None
        # self.group_chat_created = None
        # self.supergroup_chat_created = None
        # self.channel_chat_created = None
        # self.migrate_to_chat_id = None
        # self.migrate_from_chat_id = None
        # self.pinned_message = None


class BotTextMessage(BotBaseMessage):
    content_type = "text"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = self.kwargs.get("text")


class BotContactMessage(BotBaseMessage):
    content_type = "contact"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.contact = self.kwargs.get("contact")


class BotLocationMessage(BotBaseMessage):
    content_type = "location"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.location = self.kwargs.get("location")
