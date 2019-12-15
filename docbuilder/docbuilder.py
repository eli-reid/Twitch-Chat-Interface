import const as c

for cl in c.__dict__:
    if not cl.startswith("_"):
        title=f"TwichChatInterface.{cl}"
        print(title, "\n", \
                "-" * len(title),"\n\n", \
                f".. autoclass:: lib.twitchMessageHandler.modals.const.{cl}\n")
        for key in c.__dict__[cl].__class__.__dict__:
            if not key.startswith("_"):
                att=f"{key}" 
                print (att,"\n","^" * len(att),"\n\n",f".. autoattribute:: lib.twitchMessageHandler.modals.const.{cl}.{key}\n")

