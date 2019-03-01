import pickle

def get_model(path='./model.dat'):
    with open(path, 'rb') as f:
        model = pickle.load(f)

    return model