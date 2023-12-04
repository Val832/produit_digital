# loading packages
import pandas as pd
import matplotlib.pyplot as plt

# loading database
df = pd.read_csv('airbnb-listings.csv',sep=';')

# data preparation
data = df["Neighbourhood Cleansed"]
datalist = data.tolist()

# names of neighbourhood
values = []
values.append(int(datalist.count('Louvre')))
values.append(int(datalist.count('Bourse')))
values.append(int(datalist.count('Temple')))
values.append(int(datalist.count('Hôtel-de-Ville')))
values.append(int(datalist.count('Panthéon')))
values.append(int(datalist.count('Luxembourg')))
values.append(int(datalist.count('Palais-Bourbon')))
values.append(int(datalist.count('Élysée')))
values.append(int(datalist.count('Opéra')))
values.append(int(datalist.count('Entrepôt')))
values.append(int(datalist.count('Popincourt')))
values.append(int(datalist.count('Reuilly')))
values.append(int(datalist.count('Gobelins')))
values.append(int(datalist.count('Observatoire')))
values.append(int(datalist.count('Vaugirard')))
values.append(int(datalist.count('Passy')))
values.append(int(datalist.count('Batignolles-Monceau')))
values.append(int(datalist.count('Buttes-Montmartre')))
values.append(int(datalist.count('Buttes-Chaumont')))
values.append(int(datalist.count('Ménilmontant')))

arrondlist = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']

# graph
plt.bar(arrondlist, values)
plt.title("Répartition des logements Airbnb à Paris")
plt.xlabel("Numéro d'arrondissement")
plt.ylabel("Nombre de logements disponibles sur Airbnb")
plt.show()