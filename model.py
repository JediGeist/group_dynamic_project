import pickle

def get_model(path='./model.dat'):
    with open(path, 'rb') as f:
        model = pickle.load(f)
#    print(type(model))
    return model

#def main(): 
#    get_model()
#
#if __name__ == '__main__':  #
#    main()  #
