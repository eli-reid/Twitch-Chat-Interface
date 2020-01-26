import unittest
import MessageHandler
class Test_MessageHandler(unittest.TestCase):
    MH = MessageHandler.MessageHandler()
    def test_1_PRIVMSG(self):
        event, message = self.MH.handleMessage("@badge-info=;badges=broadcaster/1;color=#FF69B4;display-name=EDoG0049a;emotes=;flags=;id=7d97a3e7-7f9f-43da-81ec-e26e055ce904;mod=0;room-id=155181126;subscriber=0;tmi-sent-ts=1579477967323;turbo=0;user-id=155181126;user-type= :edog0049a!edog0049a@edog0049a.tmi.twitch.tv PRIVMSG #edog0049a :xxxx")
        self.assertIsInstance(event, str)
        self.assertIsInstance(message, MessageHandler.Message)
        self.assertEqual(event, self.MH.COMMANDS.MESSAGE)

        for key in message.tags:
            if isinstance(message.tags.get(key), str):
                self.assertIn(f"{key}={message.tags.get(key)};", message.raw)
            elif isinstance(message.tags.get(key), dict):
                value = message.tags.get(key)
                for item in value:
                    self.assertIn(f"{item}/{value.get(item)}", message.raw)
            elif message.tags.get(key) is None:
                self.assertIn(f"{key}=" or f"{key}=;", message.raw)
            elif isinstance(message.tags.get(key), bool):
                self.assertIn(f"{key}={int(message.tags.get(key))};", message.raw)
            else:
                self.fail("error in message tags")
                
    def test_2_CLEARMSG(self):
        pass

if __name__ == '__main__':
    unittest.main()
