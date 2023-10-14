from bs4 import BeautifulSoup
import requests  
import pandas as pd 

class crawler :

    # à commenter et à documenter + mauvaises gestion des erreurs
    @staticmethod
    def extract_html(url):
        try:
            req = requests.get(url)
            status = req.status_code

            if status == 200:
                html_content = BeautifulSoup(req.text, 'html.parser')
                return html_content
            else:
                return {"error": f"error in get method: {status}"}
        except requests.RequestException as e:
            return {"error": str(e)}
            
    @staticmethod
    def find_element(html_content, tag, class_name=None, element_id=None):
        """
        Recherche tous les éléments HTML dans le contenu HTML fourni en utilisant le tag et le nom de la classe ou l'ID.

        :param html_content: Objet BeautifulSoup contenant le contenu HTML à analyser.
        :type html_content: BeautifulSoup

        :param tag: Tag HTML de l'élément à rechercher (par exemple, 'table', 'div', 'a', etc.).
        :type tag: str

        :param class_name: Nom de la classe CSS de l'élément à rechercher. Utilisé pour la sélection d'élément basée sur la classe.
        :type class_name: str, optional

        :param element_id: ID de l'élément à rechercher. Utilisé pour la sélection d'élément basée sur l'ID.
        :type element_id: str, optional

        :return: Renvoie une paire (message, liste des éléments trouvés). Le message fournit le nombre de correspondances trouvées. Si aucun élément n'est trouvé, le message indique une absence de correspondance.
        :rtype: tuple (str, list of BeautifulSoup objects or None)

        :raises ValueError: Si l'objet html_content fourni n'est pas une instance de BeautifulSoup, ou si ni class_name ni element_id ne sont fournis.

        Exemple d'utilisation:
        ---------------------

        from bs4 import BeautifulSoup

        html = "<html><body><table class='myTable'><tr><td>Content</td></tr></table></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        message, elements = find_element(soup, 'table', class_name='myTable')
        """

        # Vérification du type de l'objet html_content
        if not isinstance(html_content, BeautifulSoup): 
            raise ValueError("L'entrée doit être un objet BeautifulSoup.")
        
        # Recherche d'élément en utilisant le nom de la classe ou l'ID
        if class_name is not None: 
            res = html_content.find_all(tag, {'class': class_name})
        elif element_id is not None: 
            res = html_content.find_all(tag, id=element_id)
        else:
            raise ValueError("L'un des deux paramètres class_name ou element_id doit être fourni.")
        
        # Vérification du nombre d'éléments trouvés
        count = len(res)
        if count == 0:
            return f"aucune correspondance avec le tag {tag} et {class_name or element_id}", None
        else:
            return f"{count} correspondance(s) trouvée(s) avec le tag {tag} et {class_name or element_id}", res

        
    @staticmethod
    def find_element(html_content, tag, class_name=None, element_id=None):
        """
        Méthode pour trouver un élément HTML spécifique dans le contenu HTML fourni en utilisant le tag ou le nom de classe
        ou l'ID de l'élément.
        
        :param html_content: Objet BeautifulSoup contenant le contenu HTML à analyser.
        :type html_content: BeautifulSoup
        
        :param tag: Tag HTML de l'élément à rechercher (par exemple, 'table', 'div', 'a', etc.).
        :type tag: str
        
        :param class_name: Nom de la classe CSS de l'élément à rechercher. Utilisé pour la sélection d'élément basée sur la classe.
        :type class_name: str, optional
        
        :param element_id: ID de l'élément à rechercher. Utilisé pour la sélection d'élément basée sur l'ID.
        :type element_id: str, optional
        
        :return: Renvoie l'élément trouvé sous forme d'objet BeautifulSoup si l'élément est trouvé, sinon renvoie un message d'erreur.
        :rtype: BeautifulSoup object or dict
        
        :raises ValueError: Si l'objet html_content fourni n'est pas une instance de BeautifulSoup, ou si ni class_name ni element_id ne sont fournis.
        
        Exemple d'utilisation:
        ---------------------
        
        from bs4 import BeautifulSoup
        
        html = "<html><body><table class='myTable'><tr><td>Content</td></tr></table></body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        
        table_element = MyClass.find_element(soup, 'table', class_name='myTable')
        """
        
        # Vérification du type de l'objet html_content
        if not isinstance(html_content, BeautifulSoup): 
            raise ValueError("L'entrée doit être un objet BeautifulSoup.")
        
        # Recherche d'élément en utilisant le nom de la classe ou l'ID
        # Si class_name est fourni, recherche par classe
        if class_name is not None: 
            res = html_content.find(tag, {'class': class_name})
        # Si element_id est fourni, recherche par ID
        elif element_id is not None: 
            res = html_content.find(tag, id=element_id)
        # Si aucun n'est fourni, lève une exception
        else:
            raise ValueError("L'un des deux paramètres class_name ou element_id doit être fourni.")
        
        # Si aucun élément n'est trouvé, retourne un dictionnaire contenant un message d'erreur
        if len(res) == 0  :
            return {f"aucune correspondance avec le tag {tag} et {class_name or element_id}"}  
        # Si un élément est trouvé, imprime un message et retourne l'élément trouvé
        else:
            return res

    @staticmethod  
    def extract_table(html_content, class_name=None, table_id=None):
        """
        Extrait une table du contenu HTML en utilisant soit class_name soit table_id.

        Paramètres :
        - html_content (BeautifulSoup) : Objet BeautifulSoup contenant le contenu HTML.
        - class_name (str, optionnel) : Nom de classe de la table à extraire. Par défaut à None.
        - table_id (str, optionnel) : ID de la table à extraire. Par défaut à None.

        Renvoie :
        pd.DataFrame : DataFrame contenant les données de la table extraites.

        Lève :
        - ValueError : Si l'entrée n'est pas un objet BeautifulSoup ou si la table n'est pas trouvée.

        Exemple :
        --------
        >>> extract_table(ma_page_html, class_name='ma_classe')
        ... # Renvoie un DataFrame contenant les données de la table
        """

        if not isinstance(html_content, BeautifulSoup): 
            raise ValueError("L'entrée doit être un objet BeautifulSoup.")
        
        # Extrait la table en utilisant le nom de classe ou l'id
        if class_name is not None: 
            table = html_content.find('table', class_=class_name)
        elif table_id is not None: 
            table = html_content.find('table', id=table_id)
        else:
            raise ValueError("L'un des deux paramètres class_name ou table_id doit être fourni.")
        
        # S'assure que la table est trouvée
        if table is None:
            raise ValueError("Table non trouvée.")
        
        # Extrait l'en-tête
        header = [th.text.strip() for th in table.find_all('th')]
            
        # Extrait les données des lignes
        rows_data = []
        for row in table.find_all('tr')[1:]:  # Exclut la ligne d'en-tête
            rows_data.append([td.text.strip() for td in row.find_all('td')])
                
        # Convertit en DataFrame
        df = pd.DataFrame(rows_data, columns=header)
        return df

class clean_df : 

    @staticmethod
    def drop_na(df, col=None, cols=None):
        """
        Supprime les lignes du DataFrame qui contiennent des valeurs NA/NaN.

        Paramètres:
        - df (pd.DataFrame): Le DataFrame en entrée.
        - col (str, optionnel): La colonne spécifique dans laquelle vérifier la présence de valeurs NA. 
                                Si None, toutes les colonnes sont vérifiées.
        - cols (list of str, optionnel): Une liste de colonnes dans lesquelles vérifier la présence de valeurs NA.
                                        Si None, toutes les colonnes sont vérifiées. `col` et `cols` ne doivent pas être utilisés ensemble.

        Retourne:
        pd.DataFrame: DataFrame avec les lignes contenant des valeurs NA supprimées.

        Exemples d'utilisation:
        - Pour supprimer les lignes avec des NA dans toutes les colonnes : drop_na(df)
        - Pour supprimer les lignes avec des NA dans une colonne spécifique : drop_na(df, col='nom_colonne')
        - Pour supprimer les lignes avec des NA dans plusieurs colonnes spécifiques : drop_na(df, cols=['col1', 'col2'])

        """

        if not isinstance(df, pd.DataFrame):
            raise ValueError("L'entrée doit être un DataFrame Pandas.")

        # Vérifie si le paramètre `col` est utilisé.
        if col is not None:
            if col not in df.columns:
                raise ValueError(f"Colonne {col} non trouvée dans le DataFrame.")
            return df.dropna(subset=[col])

        # Vérifie si le paramètre `cols` est utilisé.
        elif cols is not None:
            # Vérifie que cols est une liste
            if not isinstance(cols, list):
                raise ValueError("L'argument `cols` doit être une liste de noms de colonnes.")

            # Vérifie que chaque élément de cols est une chaîne et qu'il existe dans le DataFrame
            for col_name in cols:
                if not isinstance(col_name, str):
                    raise ValueError("Tous les éléments de `cols` doivent être des chaînes représentant les noms de colonnes.")
                if col_name not in df.columns:
                    raise ValueError(f"Colonne {col_name} non trouvée dans le DataFrame.")
            
            return df.dropna(subset=cols)
        
        # Si ni `col` ni `cols` n'est spécifié, supprime les lignes avec NA dans toutes les colonnes.
        else:
            return df.dropna()
        