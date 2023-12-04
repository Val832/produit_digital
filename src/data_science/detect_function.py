# detect_columns permet de standariser les noms des variables (mininuscule et snake_case)
# elle permet aussi de selection un ensemble de variable qui pourrait être intéressante pour notre analyse
<<<<<<< HEAD
=======

>>>>>>> c9f4d6c5ac62d90d89a42d2cde63b8e293cdc839
def detect_columns(data, select = True, nodollar = True):#add_var
    
    """
        detect_columns permet de standariser les noms des variables. Elle detecte le présence de majuscule et 
        des espaces dans le nom des variables pour remplacer les majuscules par des miniscules et les espaces 
        par des undersocre (mininuscule et snake_case).
        Cette fonction permet aussi de selection les variables qui pourraient être intéressantes pour notre analyse
        ou de gérer le $ de la variable price.
        
        Paramètres
        ----------
        data (pd.DataFrame): la base de données des annonces Airbnb
        
        select (Boolean, default: True): permet la sélection de variables. les variables sélectionner sont:
            [
            'id','listing_url','scrape_id','last_scraped','name','space','description','neighborhood_overview',
            'street','neighbourhood', 'neighbourhood_cleansed','neighbourhood_group_cleansed', 'city', 'state', 
            'zipcode', 'market', 'smart_location', 'country_code', 'country', 'latitude', 'longitude',
            'property_type', 'room_type', 'accommodates', 'bathrooms', "bathrooms_text", 'bedrooms','beds', 
            'bed_type', 'amenities', 'square_feet', 'price',
            ]
            
        nodallar (Boolean, default: True): permet de gérer le $ de la variable price.
        
        Retourne
        --------
        data (pd.DataFrame): la base de données ayant sublie les traitements
    """
    
    
    data.columns =[column.strip().replace(" ", "_").lower() for column in data.columns]
    var = [
        'id','listing_url','scrape_id','last_scraped','name','space','description','neighborhood_overview',
        'street','neighbourhood', 'neighbourhood_cleansed','neighbourhood_group_cleansed', 'city', 'state', 'zipcode', 'market',
        'smart_location', 'country_code', 'country', 'latitude', 'longitude','property_type', 'room_type', 'accommodates', 
        'bathrooms', "bathrooms_text", 'bedrooms','beds', 'bed_type', 'amenities', 'square_feet', 'price',
        ]
    if select:
        va = []
        for i in var:
            if i in data.columns:
                va.append(i)
        data=data[va].copy()
    if nodollar:
        data['price'] = data.price.replace('[\$,]', '', regex=True).astype(float)
    return data