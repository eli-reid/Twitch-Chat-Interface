import unittest
from EventHandler import EventHandler
class EventHandler_test(unittest.TestCase):

    def test_1_getEvents_empty(self):
        self.assertListEqual(EventHandler.getEvents() , [])
        
    def test_2_emit_eventNoCallbacksOrEvent(self):
        self.assertIsNone(EventHandler.emit("eventNoCallbacksOrEvent", "test_emit_1"))
        self.assertEqual(len(EventHandler.getEvents()), 1)
        self.assertListEqual(["test_emit_1"], EventHandler.getEvents() )
        self.assertListEqual(EventHandler.getCallbackFuncs(EventHandler.getEvents()[0]), [])
    
    def test_3_on_noEventAddCallback(self):
        def test_callback_1(sender, obj):
            print("test_callback_1")
            
        self.assertIsNone(EventHandler.on("test_emit_2", test_callback_1))
        self.assertEqual(len(EventHandler.getEvents()), 2)
        self.assertListEqual(["test_emit_1", "test_emit_2"], EventHandler.getEvents() )
        self.assertEqual(EventHandler.getCallbackFuncs(EventHandler.getEvents()[1])[0].__name__  , "test_callback_1")

    def test_4_emit_eventNoCallback(self):
        self.assertIsNone(EventHandler.emit(self, "test_emit_1"))
    
    def test_4_emit_eventWithCallback(self):
        self.assertIsNone(EventHandler.emit(self.test_4_emit_eventWithCallback," test_emit_2"))

    def test_5_emit_eventNameNotString(self):
        try:
            EventHandler.emit(self, ["test_emit_2"])
        except:   
            self.assertRaises(TypeError)
    def test_5_on_eventNameNotString(self):
        try:
            EventHandler.on( ["test_emit_2"], test_callback_1)
        except:   
            self.assertRaises(TypeError)

    def test_5_on_funcNotFunction(self):
        try:
            EventHandler.on( ["test_emit_2"], "test_callback_1")
        except:   
            self.assertRaises(TypeError)

if __name__ == '__main__':
    unittest.main()
