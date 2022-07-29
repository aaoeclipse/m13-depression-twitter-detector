import pickle
import pandas as pd

def load_model():
    with open('model/model_pkl' , 'rb') as f:
        lr = pickle.load(f)
    
        return lr

def predict(df: pd.DataFrame) -> float:
    model = load_model()
    if model == None:
        raise Exception("Error on Model")

    X = df[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]]
    return model.predict_proba(X)