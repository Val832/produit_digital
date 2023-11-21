# Price Estimation of an Accommodation in Paris on Airbnb

## Project Goal

Create an application which aims to estimate the price of your real estate located in Paris on the Airbnb application. It will allow you to offer your accommodation at the right price based on the characteristics and the location of your property.

## Details of folders and files

* `VBA` : Folder which contains the Excel file FormulaireAIRBNB.xlsm.
* `data` : Folder which contains database cleanup files.
* `src` : Source folder. It contains two subfolders:  
        - `data_science` : Subfolder which contains the scripts to create the model.  
        - `df_manipulation` : Subfolder which contains the scripts for the transformation of the database.  
* `tests` : Folder which contains unit tests.
* `utils` : Folder which contains a txt file which gives the list of dummy variables created in the database.
* `venv` : Folder which contains the virtual environment.
* `README.txt` : File which presents the organization of the project and helps for files manipulation.
* `requirements.txt` : File which lists the Python packages required to use the application.  

Additionally, a dictionary of database variables is available in the wiki.

## Execution of the project

* To clone this repository  
  `https://github.com/Val832/produit_digital.git`  
  `cd produit_digital`  

* Be sure to activate your virtual environment if you have one  
  `# Sur Mac / Linux`  
  `source venv/bin/activate`  
  `# Sur Windows`  
  `.\venv\Scripts\activate`  

* Make sure all required dependencies are installed  
  `pip install -r requirements.txt`

* Run the script of the model in the `src` folder.
