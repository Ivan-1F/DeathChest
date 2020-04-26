def convert_item(item):
    ret = ""
    id = item["id"]
    Count = item["Count"]
    ret += id
    del item["id"]
    del item["Count"]
    del item["Slot"]
    if "tag" in item:
        tags = item["tag"]
        ret += str(tags)
    ret += " " + str(Count)
    return ret


def place_item(x, y, z, slot, item, server):
    server.execute("replaceitem block {} {} {} container.{} {}".format(x, y, z, slot, item))

def transfer_item_to_chest(x, y, z, server, player):
    PlayerInfoAPI = server.get_plugin_instance("PlayerInfoAPI")
    Inventory = PlayerInfoAPI.getPlayerInfo(server, player, "Inventory")
    if len(Inventory) > 27:
        server.execute("setblock {} {} {} chest[type=right]".format(x, y, z))
        server.execute("setblock {} {} {} chest[type=left]".format(x - 1, y, z))
    else:
        server.execute("setblock {} {} {} chest".format(x, y, z))

    pos = 0
    # server.say(Inventory)
    for i in range(0, len(Inventory)):
        if i == 27:
            x -= 1
            pos = 0
        place_item(x, y, z, pos, convert_item(Inventory[i]), server)
        pos += 1

def on_death_message(server, death_message):
    player = death_message.split()[0]
    PlayerInfoAPI = server.get_plugin_instance("PlayerInfoAPI")
    pos_x = int(PlayerInfoAPI.getPlayerInfo(server, player, "Pos")[0])
    pos_y = int(PlayerInfoAPI.getPlayerInfo(server, player, "Pos")[1])
    pos_z = int(PlayerInfoAPI.getPlayerInfo(server, player, "Pos")[2])

    # server.execute("setblock {} {} {} chest".format(pos_x, pos_y, pos_z))
    transfer_item_to_chest(pos_x, pos_y, pos_z, server, player)
    server.execute("clear " + player)
    server.execute("/xp set " + player + " 0 levels")
    server.execute("/xp set " + player + " 0 points")
    server.tell(player, "§a成功在[x:{}, y:{}, z:{}]§a生成了死亡箱§r".format(pos_x, pos_y, pos_z))

def on_info(server, info):
    if info.content == "!!debug":
        PlayerInfoAPI = server.get_plugin_instance("PlayerInfoAPI")
        Inventory = PlayerInfoAPI.getPlayerInfo(server, info.player, "Inventory")[0]
        server.say(convert_item(Inventory))