from fastapi import FastAPI
import uvicorn

import jsonpickle

from pydantic import BaseModel

app = FastAPI()

jsonpickle.set_encoder_options('json', indent=4, separators=(',', ': '))

class desks():
    def __init__(self, id, name, manufacturer, position, speed, status):
        self.id = id
        self.name = name
        self.manufacturer = manufacturer
        self.position : str = position
        self.speed = speed
        self.status = status



list = []

list.append(desks('1', 'desk_1', 'linak', 500, 3.0,'available'))
list.append(desks('2', 'desk_2', 'linak', 300, 2.0,'available'))
list.append(desks('3', 'desk_3', 'linak', 600, 5.0,'occupied'))
list.append(desks('4', 'desk_4', 'linak', 800, 3.0,'available'))
list.append(desks('5', 'desk_5', 'linak', '300', 1.0,'occupied'))

@app.get("/api/v1/dev/desks")
async def root():
    JSON = jsonpickle.encode(list, unpicklable=False, indent=4,
                                 separators=(', ', ': '),max_depth=4)
    return JSON


@app.get("/api/v1/dev/desks/{id}")
async def show_desk(id: str):
    #print('showing user:' + id)
    JSON = await get_desk_by_id(id, list)
    print('return json')
    return JSON

@app.put("/api/v1/dev/desks/{id}/{position}")
async def update_item(id: str, position : str):
    await update_desk_by_id(id, position, list)
    return jsonpickle.encode(list, unpicklable=False, indent=4,
                                 separators=(', ', ': '),max_depth=4)

#@app.put("/api/v1/dev/desks/{id}")
#async def update_item(id: int, desk: desks, q: str | None = None):
#   await update_desk_by_id(id, q, list)
#   return jsonpickle.encode(list, unpicklable=False, indent=4,
#                                 separators=(', ', ': '),max_depth=4)

#@app.put("/api/v1/dev/desks/{id}")
#async def update_item(id: int, desk: desks, q: str | None = None):
##    result = {"id": id, **desks.dict()}
 #   if q:
 #       result.update({"q": q})
 #   return result

async def get_desk_by_id(x : str, list: desks):
    JSON = jsonpickle.encode('id not found', unpicklable=False, indent=4,
                                 separators=(', ', ': '), max_depth=4)
    for obj in list:
        if obj.id == x:
            print('found user')
            JSON = jsonpickle.encode(obj, unpicklable=False, indent=4,
                                 separators=(', ', ': '), max_depth=4)
    
    print('finished user query')
    return JSON

async def update_desk_by_id(x : str, new_pos : str, list: desks):
    for obj in list:
        if obj.id == x:
            print('found user')
            obj.position = new_pos;    
    print('finished user query')
    

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3001)
