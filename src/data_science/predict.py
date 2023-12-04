# Charger le modèle à partir du fichier pickle
model_pkl = ''
with open(model_pkl, 'rb') as file:
    loaded_model = pickle.load(file)

dt = X_test_final.head(1)

dt.insert(loc=0, column='const', value=1.0)

srt_conf = loaded_model.get_prediction(dt).conf_int(alpha = .05 )
srt_pre = loaded_model.predict(dt)
srt = {'predict' : np.exp(srt_pre).iloc[0], 'born_inf' : np.exp(srt_conf)[0][0], 'born_sup' : np.exp(srt_conf)[0][1]}