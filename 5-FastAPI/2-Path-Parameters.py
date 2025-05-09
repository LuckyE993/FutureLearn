from enum import Enum
from fastapi import FastAPI

app = FastAPI()


# @app.get("/items/{item_id}")
# async def read_item(item_id):
#     return {"item_id": item_id}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# 路径中的顺序
# 由于路径操作是按顺序依次运行的，因此，一定要在 /users/{user_id} 之前声明 /users/me


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):  # 使用 Enum 类（ModelName）创建使用类型注解的路径参数
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "resnet":
        return {"model_name": model_name, "message": "Residual Networks FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeNet FTW!"}
    # raise HTTPException(status_code=400, detail="Model not found")
    return {"model_name": model_name, "message": "Model not found"}
