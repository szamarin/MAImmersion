import argparse
import os
import pandas as pd
import joblib
from fbprophet import Prophet
from glob import glob


def train(data):
    model = Prophet(growth=args.growth,
               changepoints=args.changepoints,
               n_changepoints=args.n_changepoints,
               changepoint_prior_scale=args.changepoint_prior_scale)
    
    model.fit(data)
    
    return model

def evaluate(model, data):
    
    forecast = model.predict(data.loc[:,["ds"]])["yhat"]
    rmse = ((forecast - data["y"])**2).mean()**(1/2)
    
    print(f"train rmse: {rmse}")
    
    return rmse
    


if __name__ =="__main__":

    parser = argparse.ArgumentParser()

    # hyperparameters sent by the client are passed as command-line arguments to the script.
    parser.add_argument("--growth", type=str, default="linear")
    parser.add_argument("--changepoints", nargs="+", default=None)
    parser.add_argument("--n_changepoints", type=int, default=25)
    parser.add_argument("--changepoint_prior_scale", type=float, default=0.05)
    parser.add_argument("--seasonality_prior_scale", type=float, default=0.05)
    parser.add_argument("--seasonality_mode", type=str, default="additive")
    
    # Data, model, and output directories
    parser.add_argument('--output-data-dir', type=str, default=os.environ.get('SM_OUTPUT_DATA_DIR'))
    parser.add_argument('--model-dir', type=str, default=os.environ.get('SM_MODEL_DIR'))
    parser.add_argument('--train', type=str, default=os.environ.get('SM_CHANNEL_TRAIN'))
    parser.add_argument('--test', type=str, default=os.environ.get('SM_CHANNEL_TEST'))

    args, _ = parser.parse_known_args()
    
    data = pd.read_csv(f"{args.train}/train.csv")
    
    model = train(data)
    
    evaluate(model, data)
    
    joblib.dump(model, os.path.join(args.model_dir, "model.joblib"))
    
    