import pandas as pd 
import re 

def create_column_from_match(df, reference_column,  word = None, words_list = None) : 

    """
    Cette fonction crée une ou plusieurs colonnes indicatrices dans un DataFrame pandas 
    basées sur une correspondance regex de mots dans une colonne de référence.

    Paramètres:
    ----------
    df : pd.DataFrame
        Le DataFrame sur lequel effectuer l'opération.
    
    reference_column : str
        Le nom de la colonne sur laquelle effectuer la recherche de mots.
    
    word : str, optionnel
        Le mot à rechercher dans la colonne de référence. Si renseigné, une colonne indicatrice 
        portant ce nom sera ajoutée au DataFrame.
    
    words_list : list de str, optionnel
        Liste de mots à rechercher dans la colonne de référence. Pour chaque mot, une colonne 
        indicatrice sera ajoutée au DataFrame.

    Retours:
    --------
    df : pd.DataFrame
        DataFrame avec les nouvelles colonnes indicatrices ajoutées.

    Remarques:
    ----------
    - Au moins un des arguments 'word' ou 'words_list' doit être renseigné.
    - Seul l'un des arguments 'word' ou 'words_list' doit être renseigné, mais pas les deux simultanément.
    - La recherche de mots est insensible à la casse grâce à (?i) dans l'expression regex.
    """
    
    # L'argument df doit être un pandas.dataframe 
    if not isinstance (df, pd.DataFrame) : 
        raise TypeError("L'argument df doit prendre en entrée un objet de type pandas.DataFrame")
    
    if reference_column not in df.columns :
        raise ValueError(f"La colonne de référence '{reference_column}' n'est pas présente dans le DataFrame.")

    # Au moins un paramètre doit être renseigné 
    if word is None and words_list is None :
        raise ValueError("Vous devez renseigner un mot ou une liste de mot")
    
    # Les deux paramètre ne peuvent pas être renseigné en même temps 
    if word and words_list : 
        raise ValueError("Si vous avez plusieurs colonnes à créer, veuillez les inclures dans une liste et utiliser uniquement l'argument 'words_list'")
    
    
    if word :
        # Gestion des erreurs de type 
        if not isinstance(word, str) : 
            raise TypeError("L'argument word doit être de type 'str'")
        #Créer une colonne dummies à partir du mot renseigné si un match est trouvé avec dummies
        # (?i) permet de matcher qu'importe la capitalisation 
        df[word] = df[reference_column].str.contains(rf'(?i){word}').astype(int)

    else : 
        # Gestion des erreurs de type 
        if not isinstance (words_list, list) : 
                raise TypeError("L'argument words prend en entrée une liste")
        
        for i in words_list : 
            if not isinstance(i, str) : 
                raise TypeError(f"L'argument words_list prend uniquement en entrée une liste contenant des objets de type 'str'")
        #Créer des colonnes dummies à partir de la liste de mots renseignée si un match est trouvé
        for new_column in words_list : 
            df[new_column] = df[reference_column].str.contains(rf'(?i){new_column}').astype(int)  

    return df    