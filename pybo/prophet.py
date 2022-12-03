import pickle

def predict_chicken():
    with open('./static/forecast_model.pkl', 'rb') as pickle_file:
        model = pickle.load(pickle_file)

    future = model.make_future_dataframe(periods=4,freq='W')
    forecast = model.predict(future)

    fore_num = forecast[['ds','yhat']][-4:]
    fore = format(int(fore_num), ',')

    return fore

predict_chicken()