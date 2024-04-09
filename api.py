from fastapi import FastAPI
from pydantic import BaseModel
import pickle

class InputData(BaseModel):

    code_post:float
    surface: float
    nb_piece: float
    code_reg: float


with open('xgb.pkl', 'rb') as file:
    model = pickle.load(file)

app = FastAPI()

@app.post("/predict")
def predict(data: InputData):

    input_data = [data.code_post, data.surface, data.nb_piece, data.code_reg]
    prediction = model.predict([input_data])
    return {"prediction": prediction[0]}
