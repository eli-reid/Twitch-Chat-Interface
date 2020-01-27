import unittest
import MessageHandler
class Test_MessageHandler(unittest.TestCase):
    MH = MessageHandler.MessageHandler()
    def test_1_PRIVMSG(self):
        event, message = self.MH.handleMessage("@badge-info=;badges=global_mod/1,turbo/1;color=#0D4200;display-name=ronni;emotes=25:0-4,12-16/1902:6-10;id=b34ccfc7-4977-403a-8a94-33c6bac34fb8;mod=0;room-id=1337;subscriber=0;tmi-sent-ts=1507246572675;turbo=1;user-id=1337;user-type=global_mod :ronni!ronni@ronni.tmi.twitch.tv PRIVMSG #ronni :Kappa Keepo Kappa")
        self.assertIsInstance(event, str)
        self.assertIsInstance(message, MessageHandler.Message)
        self.assertEqual(event, self.MH.COMMANDS.MESSAGE)
        self.assertEqual(len(message.tags),13)
        self.assertEqual(len(message.tags.get("emotes")),2)
        self.assertEqual(message.text,"Kappa Keepo Kappa")
        self.assertEqual(message.username,"ronni")
        self.assertEqual(message.channel,"#ronni")

    def test_2_CLEARCHAT(self):
        event, message = self.MH.handleMessage(":tmi.twitch.tv CLEARCHAT #dallas :ronni")
        self.assertIsInstance(event, str)
        self.assertIsInstance(message, MessageHandler.Message)
        self.assertEqual(event, self.MH.COMMANDS.CLEARCHAT)    
        
    def test_3_CLEARMSG(self):
        event, message = self.MH.handleMessage("@login=ronni;target-msg-id=abc-123-def :tmi.twitch.tv CLEARMSG #dallas :HeyGuys")
        self.assertIsInstance(event, str)
        self.assertIsInstance(message, MessageHandler.Message)
        self.assertEqual(event, self.MH.COMMANDS.CLEARMSG)  
    def test_4_GLOBALUSERSTATE(self):
        event, message = self.MH.handleMessage("@badge-info=subscriber/8;badges=subscriber/6;color=#0D4200;display-name=dallas;emote-sets=0,33,50,237,793,2126,3517,4578,5569,9400,10337,12239;turbo=0;user-id=1337;user-type=admin :tmi.twitch.tv GLOBALUSERSTATE")
        self.assertIsInstance(event, str)
        self.assertIsInstance(message, MessageHandler.Message)
        self.assertEqual(event, self.MH.COMMANDS.GLOBALUSERSTATE)  

    def test_5_ROOMSTATE(self):
        event, message = self.MH.handleMessage("@emote-only=0;followers-only=0;r9k=0;slow=0;subs-only=0 :tmi.twitch.tv ROOMSTATE #dallas")
        self.assertIsInstance(event, str)
        self.assertIsInstance(message, MessageHandler.Message)
        self.assertEqual(event, self.MH.COMMANDS.ROOMSTATE)  
    def test_6_USERNOTICE(self):
        event, message = self.MH.handleMessage("@badge-info=;badges=staff/1,broadcaster/1,turbo/1;color=#008000;display-name=ronni;emotes=;id=db25007f-7a18-43eb-9379-80131e44d633;login=ronni;mod=0;msg-id=resub;msg-param-cumulative-months=6;msg-param-streak-months=2;msg-param-should-share-streak=1;msg-param-sub-plan=Prime;msg-param-sub-plan-name=Prime;room-id=1337;subscriber=1;system-msg=ronni\shas\ssubscribed\sfor\s6\smonths!;tmi-sent-ts=1507246572675;turbo=1;user-id=1337;user-type=staff :tmi.twitch.tv USERNOTICE #dallas :Great stream -- keep it up!")
        self.assertIsInstance(event, str)
        self.assertIsInstance(message, MessageHandler.Message)
        #self.assertEqual(event, self.MH.COMMANDS.USERNOTICE)  
    def test_7_USERSTATE(self):
        event, message = self.MH.handleMessage("@badge-info=;badges=staff/1;color=#0D4200;display-name=ronni;emote-sets=0,33,50,237,793,2126,3517,4578,5569,9400,10337,12239;mod=1;subscriber=1;turbo=1;user-type=staff :tmi.twitch.tv USERSTATE #dallas")
        self.assertIsInstance(event, str)
        self.assertIsInstance(message, MessageHandler.Message)
        self.assertEqual(event, self.MH.COMMANDS.USERSTATE)  
        
if __name__ == '__main__':
    unittest.main()
