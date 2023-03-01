import pickle

Load_RF_Model = None
Load_DT_Model = None
Load_SVM_Model = None
Load_LR_Model = None

def load_models():
    global Load_RF_Model
    global Load_DT_Model
    global Load_SVM_Model
    global Load_LR_Model
    Load_RF_Model = pickle.load(open('./models/RF.sav', 'rb'))
    Load_DT_Model = pickle.load(open('./models/DT.sav', 'rb'))
    Load_SVM_Model = pickle.load(open('./models/SVM.sav', 'rb'))
    Load_LR_Model = pickle.load(open('./models/LR.sav', 'rb'))

def predict_RF_model(data):
    return Load_RF_Model.predict([data])

def predict_DT_model(data):
    return Load_DT_Model.predict([data])

def predict_SVM_model(data):
    return Load_SVM_Model.predict([data])

def predict_LR_model(data):
    return Load_LR_Model.predict([data])

def predict_model(data, model):
    if model == 'RF':
        return predict_RF_model(data)
    elif model == 'DT':
        return predict_DT_model(data)
    elif model == 'SVM':
        return predict_SVM_model(data)
    elif model == 'LR':
        return predict_LR_model(data)
    else:
        return None
    
def prob_score_combination(data,weights):
    predict_prob_RF = Load_RF_Model.predict_proba([data])
    predict_prob_DT = Load_DT_Model.predict_proba([data])
    predict_prob_SVM = Load_SVM_Model.predict_proba([data])
    predict_prob_LR = Load_LR_Model.predict_proba([data])
    print(predict_prob_RF)
    predict_prob = [predict_prob_RF[0][0]*weights[0]+predict_prob_DT[0][0]*weights[1]+predict_prob_SVM[0][0]*weights[2]+predict_prob_LR[0][0]*weights[3],predict_prob_RF[0][1]*weights[0]+predict_prob_DT[0][1]*weights[1]+predict_prob_SVM[0][1]*weights[2]+predict_prob_LR[0][1]*weights[3]]
    return predict_prob
    
# print("Loading models...")
# load_models()
# print("Models loaded!")

# print(prob_score_combination([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],[0.25,0.25,0.25,0.25]))

# print("Predicting...")
# print(predict_model([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'RF'))
# print(predict_model([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'DT'))
# print(predict_model([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'SVM'))
# print(predict_model([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'LR'))

