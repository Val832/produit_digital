import pickle
import statsmodels.api as sm

# Charger le modèle à partir du fichier pickle
model_pkl = 'mettre le modèle'
with open(model_pkl, 'rb') as file:
    loaded_model = pickle.load(file)

dt = 'mettre la base de données pd.DatFrame '


srt_conf = loaded_model.get_prediction(dt).conf_int(alpha = .05 )
srt_pre = loaded_model.predict(dt)
srt = {'predict' : np.exp(srt_pre).iloc[0], 'born_inf' : np.exp(srt_conf)[0][0], 'born_sup' : np.exp(srt_conf)[0][1]}

print(str)