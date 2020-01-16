import const as c
try:
    x=""
    print(x[12])
except Exception as err:
    l=int((len(str(err))-11) /2) + 20 
    endstars = l - 1 if len(str(err))%2 == 0 else l 

    print("\n\n",f"{'*' * l} PARSE ERROR {'*' * endstars}\n",\
                    f"{'*'*20} {err} {'*'*20} ","\n", \
                     f"{'*' * l} PARSE ERROR {'*' * endstars}\n\n")


