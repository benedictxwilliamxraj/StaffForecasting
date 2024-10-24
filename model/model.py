import pickle

# Function to load the model
def load_yearly_model(model_path='model/yearly_model.pkl'):
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

# Example prediction function
def predict(input_data, model):
    return model.predict(input_data)