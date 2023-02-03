import keyboard
import time
import json
time.sleep(1)
event = keyboard.KeyboardEvent(keyboard.KEY_DOWN, None, name="h")
print(event)
key = event.scan_code or event.name
print(key)

# with open("logs.json", "w") as log_file:
#     logs = [
#         {"name": "trail_one", "inputs":
#          [
#              {"name": "p", "event_type": "down", "time": 2},
#              {"name": "d", "event_type": "down", "time": 4},
#              {"name": "p", "event_type": "up", "time": 5},
#              {"name": "d", "event_type": "up", "time": 7}
#          ]
#          },
#         {"name": "trail_two", "inputs":
#          [
#              {"name": "a", "event_type": "down", "time": 2},
#              {"name": "b", "event_type": "down", "time": 4},
#              {"name": "b", "event_type": "up", "time": 5},
#              {"name": "a", "event_type": "up", "time": 7}
#          ]
#          }
#     ]
#     log_str = json.dumps(logs)
#     log_file.write(log_str)


def dic2Event(log):
    return keyboard.KeyboardEvent(log["event_type"], None, name=log["name"], time=log["time"])


def getIndexFromName(logs, name):
    return [i for i in range(len(logs)) if logs[i]["name"] == name][0]


def listdict2Event(logs, byId=True, Id=0, name=""):
    if byId:
        return [dic2Event(log)for log in logs[Id]["inputs"]]
    else:
        return [dic2Event(log)for log in logs[getIndexFromName(logs, name)]["inputs"]]


with open("logs.json", "r") as log_file:
    logs_str = "".join(log_file.readlines())
logs = json.loads(logs_str)
events = listdict2Event(logs=logs, byId=False, Id=1, name="trail_one")

# # Record events until 'esc' is pressed.
# recorded = keyboard.record(until='esc')
# # Then replay back at three times the speed.
print("ready")
time.sleep(1)
keyboard.play(events=events, speed_factor=1)
# with open("keypress_log.txt", "w") as log_file:
#     [log_file.write(r.to_json()+"\n") for r in recorded]
