#----------------------------------------------#
# Students: Guilherme Silva Santos (107961) & João Pedro Pereira Gaspar (107708)
#----------------------------------------------#

import random
import math
import asyncio
import getpass
import json
import os
import websockets
from consts import Direction
from mapa import *

import time

#----------------------------------------------#
#------------------ AI AGENT ------------------#
#----------------------------------------------#

class DigDug:
    def __init__(self, pos):
        self.pos = pos
    
class DigDugAgent:
    @staticmethod
    def find_closest_enemy(digdug, enemies):
        if not enemies:
            return None

        closest_enemy = min(enemies, key=lambda enemy: math.dist(digdug.pos, enemy["pos"]))
        
        return closest_enemy

    @staticmethod
    def decide_movement(digdug, enemies, rocks):
        closest_enemy = DigDugAgent.find_closest_enemy(digdug, enemies)
        #print("ENEMY: ", closest_enemy)
        #ENEMY:  {'name': 'Pooka', 'id': '3337ed4d-5784-4b5a-b9e4-7665da0244e6', 'pos': [25, 10], 'dir': 1}

        if closest_enemy:
            enemy_pos = closest_enemy["pos"]
            rocks_pos = [x["pos"] for x in rocks]
            #print("ROCKS: ", rocks_pos)
            #ROCKS:  [[26, 5]]

            fires_pos = []
            for ene in enemies:
                #print("ENEMIES: ", enemies)
                #ENEMIES:  [{'name': 'Fygar', 'id': 'd4bc864e-483c-4d1d-bc4e-3c37ca026845', 'pos': [39, 8], 'dir': 1}, {'name': 'Pooka', 'id': 'eb4e1aa9-3ddc-4315-a651-b3affe18323e', 'pos': [40, 11], 'dir': 1}, {'name': 'Pooka', 'id': 'd853e6e6-6544-4230-a090-5082b4f79764', 'pos': [10, 3], 'dir': 1, 'traverse': True}]
                if(ene["name"] == "Fygar"):
                    ene_x = ene["pos"][0]
                    ene_y = ene["pos"][1]
                    if(ene["dir"] == 3):
                        fires_pos += [[ene_x, ene_y]]
                        fires_pos += [[ene_x - 1, ene_y]]
                        fires_pos += [[ene_x - 2, ene_y]]
                        fires_pos += [[ene_x - 3, ene_y]]
                        fires_pos += [[ene_x - 4, ene_y]]
                        fires_pos += [[ene_x - 5, ene_y]]
                        fires_pos += [[ene_x, ene_y+1]]
                        fires_pos += [[ene_x - 1, ene_y+1]]
                        fires_pos += [[ene_x - 2, ene_y+1]]
                        fires_pos += [[ene_x - 3, ene_y+1]]
                        fires_pos += [[ene_x - 4, ene_y+1]]
                        fires_pos += [[ene_x - 5, ene_y+1]]
                    elif(ene["dir"] == 1):
                        fires_pos += [[ene_x, ene_y]]
                        fires_pos += [[ene_x + 1, ene_y]]
                        fires_pos += [[ene_x + 2, ene_y]]
                        fires_pos += [[ene_x + 3, ene_y]]
                        fires_pos += [[ene_x + 4, ene_y]]
                        fires_pos += [[ene_x + 5, ene_y]]
                        fires_pos += [[ene_x, ene_y+1]]
                        fires_pos += [[ene_x + 1, ene_y+1]]
                        fires_pos += [[ene_x + 2, ene_y+1]]
                        fires_pos += [[ene_x + 3, ene_y+1]]
                        fires_pos += [[ene_x + 4, ene_y+1]]
                        fires_pos += [[ene_x + 5, ene_y+1]]
        
                            
            if(closest_enemy["dir"] == 0 or closest_enemy["dir"] == 2):
                if(digdug.pos[1] < enemy_pos[1]):
                    enemy_pos[1] -= 1
                elif(digdug.pos[1] > enemy_pos[1]):
                    enemy_pos[1] += 1
            else:
                if(digdug.pos[0] < enemy_pos[0]):
                    enemy_pos[0] -= 1
                elif(digdug.pos[0] > enemy_pos[0]):
                    enemy_pos[0] += 1

            x = digdug.pos[0]
            y = digdug.pos[1]
            
            
            
            new_pos = {}
            if(closest_enemy["dir"] == 0 or closest_enemy["dir"] == 2):
                if digdug.pos[0] != enemy_pos[0]:
                    new_pos[Direction.EAST] = [x+1, y]
                    new_pos[Direction.WEST] = [x-1, y]   
                else:
                    new_pos[Direction.NORTH] = [x, y-1]
                    new_pos[Direction.SOUTH] = [x, y+1]
            else:
                if digdug.pos[1] != enemy_pos[1]:
                    new_pos[Direction.NORTH] = [x, y-1]
                    new_pos[Direction.SOUTH] = [x, y+1]
                else:
                    new_pos[Direction.EAST] = [x+1, y]
                    new_pos[Direction.WEST] = [x-1, y]

            danger = 5
            for pos in new_pos:
                if (new_pos[pos] in rocks_pos) or (new_pos[pos] in fires_pos):
                    danger = pos
                    #print("DANGER: ",danger)
            if danger != 5:
                #print("DANGER!")
                if (danger == 0 or danger == 2):    
                    new_pos[Direction.EAST] = [x+1, y]
                    new_pos[Direction.WEST] = [x-1, y]
                    new_pos[Direction.NORTH] = [9999, 9999]
                    new_pos[Direction.SOUTH] = [9999, 9999] 
                else:
                    new_pos[Direction.NORTH] = [x, y-1]
                    new_pos[Direction.SOUTH] = [x, y+1] 
                    new_pos[Direction.EAST] = [9999, 9999] 
                    new_pos[Direction.WEST] = [9999, 9999] 

            for pos in new_pos:
                if (new_pos[pos][0] < 0 or new_pos[pos][0] > 48) and (new_pos[pos] != [9999, 9999]):
                    #print(new_pos[pos])
                    new_pos[pos] = [9999, 9999]
                    #print("LIMITE X")
                if (new_pos[pos][1] < 0 or new_pos[pos][1] > 24) and (new_pos[pos] != [9999, 9999]):
                    new_pos[pos] = [9999, 9999]
                    #print("LIMITE Y")
                    
            #print(new_pos)
            distance = {}
            for dir in new_pos:
                #print(new_pos)
                #{<Direction.NORTH: 0>: [1, 0], <Direction.SOUTH: 2>: [1, 2]}
                distance[dir] = math.dist(new_pos[dir], enemy_pos)

            enemies_nearby = [ene for ene in enemies if math.dist(digdug.pos, ene["pos"]) <= 3]

            
            if  x != enemy_pos[0] and y != enemy_pos[1] and len(enemies_nearby) < 3:
                attack_distance = 3
            elif x != enemy_pos[0] and y != enemy_pos[1]:
                attack_distance = 2
            else:
                attack_distance = 1

            #print(enemies_nearby)
            #print(closest_enemy)
            #print(attack_distance)
            if (math.dist(digdug.pos, enemy_pos) <= attack_distance) and len(enemies_nearby) < 3: 
                return 4

            if (len(enemies_nearby) >= 3) or ((closest_enemy in enemies_nearby) and (closest_enemy["name"] == "Pooka" and "traverse" in closest_enemy)):
                #print("REVERSED")
                return max(distance, key=distance.get)
            else:
                return min(distance, key=distance.get)

        return random.choice(list(Direction))
    
#----------------------------------------------#
#- DO NOT CHANGE THE CODE BELLOW THIS COMMENT -#
#----------------------------------------------#

async def agent_loop(server_address="localhost:8000", agent_name="student"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
        
        agent = DigDugAgent()
        
        flag = 0
        old_pos = [0, 0]

        map_state = None
        while True:
            try:
                if(map_state is None):
                    map_state = json.loads(await websocket.recv())

                game_state = json.loads(await websocket.recv())

                if game_state["level"] != map_state["level"]:
                    map_state = json.loads(await websocket.recv())

                if("digdug" in game_state):
                    digdug = DigDug(game_state["digdug"])
                else:
                    continue
                                
                agent.current_position = digdug
                agent.game_state = game_state

                action = agent.decide_movement(digdug, game_state["enemies"], game_state["rocks"])

                if(digdug.pos == old_pos):
                    flag += 1
                
                if flag < 60:
                    if action == 0:
                        key = "w"
                        flag = 0
                    elif action == 1:
                        key = "d"
                        flag = 0
                    elif action == 2:
                        key = "s"
                        flag = 0
                    elif action == 3:
                        key = "a"
                        flag = 0
                    elif action == 4:
                        key = "A"
                else:
                    key = random.choice(["w", "d", "s", "a"]) 
                    flag = 0   

                old_pos = digdug.pos
                #print(digdug.pos, old_pos, flag)
                
                await websocket.send(json.dumps({"cmd": "key", "key": key}))
            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return


# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
