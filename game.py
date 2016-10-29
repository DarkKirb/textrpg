#!/usr/bin/env python3
import json
with open("data/maps.json") as f:
    maps=json.loads(f.read())
print(repr(maps))
room=0
text=""
inventory={}
while text != "suicide":
    print("You are here: {name}".format(name=maps["rooms"][room]["name"]))
    text = input("> ")
    ex=text.split(' ')
    if len(ex)==0:
        continue
    if ex[0] == "look":     
        if "npcs" in maps["rooms"][room]:
            print("Here are {count} NPC(s):".format(count=len(maps["rooms"][room]["npcs"])))
            x=0
            for npc in maps["rooms"][room]["npcs"]:
                print("{name} ({id}), ".format(name=npc["name"], id=x), end="")
                x=x+1
            print("")
        if "objs" in maps["rooms"][room]:
            print("There are also {count} thing(s) lying on the floor:".format(count=len(maps["rooms"][room]["objs"])))
            x=0
            for obj in maps["rooms"][room]["objs"]:
                print("{name} ({id}), ".format(name=maps["items"][obj]["name"], id=x), end="")
                x=x+1
            print("")
        if "entrances" in maps["rooms"][room]:
            print("There are {count} door(s) waiting to be opened:".format(count=len(maps["rooms"][room]["entrances"])))
            x=0
            for entr in maps["rooms"][room]["entrances"]:
                print("{name} ({id}), ".format(name=maps["rooms"][entr["dest"]]["name"], id=x), end="")
                x=x+1
            print("")
    elif ex[0]=="map":
        print(maps["rooms"][room]["desc"])
        if "north" in maps["rooms"][room]:
            print("To the north is {name}.".format(name=maps["rooms"][maps["rooms"][room]["north"]]["name"]))
        if "south" in maps["rooms"][room]:
            print("To the south is {name}.".format(name=maps["rooms"][maps["rooms"][room]["south"]]["name"]))
        if "west" in maps["rooms"][room]:
            print("To the west is {name}.".format(name=maps["rooms"][maps["rooms"][room]["west"]]["name"]))
        if "east" in maps["rooms"][room]:
            print("To the east is {name}.".format(name=maps["rooms"][maps["rooms"][room]["east"]]["name"]))
    elif ex[0]=="speak" or ex[0]=="talk":
        if len(ex)==1:
            print("Whom do you want to talk to?")
        else:
            pid=0
            try:
                pid=int(ex[1])
            except:
                print("Sorry, I can only accept numbers.")
                continue
            if pid >= len(maps["rooms"][room]["npcs"]):
                print("I can't see this person here.")
                continue
            if not "msg" in maps["rooms"][room]["npcs"][pid]:
                print("{name}: {quest}".format(name=maps["rooms"][room]["npcs"][pid]["name"], quest=maps["rooms"][room]["npcs"][pid]["textn"]))
                req=True
                tmp=dict(inventory)
                for iid in maps["rooms"][room]["npcs"][pid]["wants"]:
                    if not iid in tmp:
                        req=False
                        break
                    tmp[iid]=tmp[iid]-1
                    if tmp[iid]==0:
                        del tmp[iid]
                if req:
                    inventory=tmp
                    for iid in maps["rooms"][room]["npcs"][pid]["gives"]:
                        if not iid in inventory:
                            inventory[iid]=1
                        else:
                            inventory[iid]=inventory[iid]+1
                    maps["rooms"][room]["npcs"][pid]["msg"]=maps["rooms"][room]["npcs"][pid]["texts"]
                    print("{name}: {text}".format(name=maps["rooms"][room]["npcs"][pid]["name"], text=maps["rooms"][room]["npcs"][pid]["msg"]))
            else:
                print("{name}: {text}".format(name=maps["rooms"][room]["npcs"][pid]["name"], text=maps["rooms"][room]["npcs"][pid]["msg"]))
    elif ex[0]=="take":
        if len(ex)==1:
            print("What do you want to take?")
        oid=0
        try:
            oid=int(ex[1])
        except:
            print("Sorry, I can only accept numbers.")
            continue
        if oid >= len(maps["rooms"][room]["objs"]):
            print("I don't see this object here")
            continue
        iid=maps["rooms"][room]["objs"][oid]
        del maps["rooms"][room]["objs"][oid]
        if not iid in inventory:
            inventory[iid]=1
        else:
            inventory[iid]=inventory[iid]+1
        print("You received {name}!".format(name=maps["items"][iid]["name"]))
    elif ex[0]=="inventory":
        print("You have in your pockets: ")
        for items, count in inventory.items():
            if not count:
                continue
            if count==1:
                print("one {name} ({id})".format(name=maps["items"][items]["name"], id=items))
            else:
                print("{count}x{name} ({id})".format(name=maps["items"][items]["name"], count=count, id=items))
    elif ex[0]=="north":
        if "north" in maps["rooms"][room]:
            room=maps["rooms"][room]["north"]
    elif ex[0]=="south":
        if "south" in maps["rooms"][room]:
            room=maps["rooms"][room]["south"]
    elif ex[0]=="east":
        if "east" in maps["rooms"][room]:
            room=maps["rooms"][room]["east"]
    elif ex[0]=="west":
        if "west" in maps["rooms"][room]:
            room=maps["rooms"][room]["west"]
    elif ex[0]=="enter":
        if len(ex)==1:
            print("Which door do you want to open?")
        did=0
        try:
            did=int(ex[1])
        except:
            print("Sorry, I can only accept numbers.")
            continue
        if did >= len(maps["rooms"][room]["entrances"]):
            print("I don't see this door here")
            continue
        iid=-1
        if "key" in maps["rooms"][room]["entrances"][did]:
            iid=maps["rooms"][room]["entrances"][did]["key"]
        if iid != -1:
            if not iid in inventory:
                print("It seems the door won't open unless you get {item}".format(maps["items"][iid]["name"]))
                continue
            else:
                if iid==0:
                    #Special code for small keys
                    inventory[iid]=inventory[iid]-1
                    if not inventory[iid]:
                        del inventory[iid]
                maps["rooms"][room]["entrances"][did]["key"]=-1
        room=maps["rooms"][room]["entrances"][did]["dest"]
    elif ex[0]=="info":
        if len(ex)==1:
            print("Available commands: look, map, talk {person id}, take {object id}, inventory, enter {door id}, north, south, west, east, info, info {item id}, suicide")
            continue
        iid=0
        try:
            iid=int(ex[1])
        except:
            print("Sorry, I can only accept numbers.")
            continue
        if iid >= len(maps["items"]):
            print("Sorry, I don't know this item.")
        print("Item name: {name}\nType: {type}\nDescription: {desc}".format(name=maps["items"][iid]["name"],type=maps["items"][iid]["type"],desc=maps["items"][iid]["desc"]))
