# Price Estimate of an Accommodation in Paris on Airbnb

## Project Goal

Create an application which aims to estimate the price of your real estate located in Paris on the Airbnb application. It will allow you to offer your accommodation at the right price based on the characteristics and the location of your property.

## Details of folders and files

* `VBA` : Folder which contains the Excel file FormulaireAIRBNB.xlsm.  
* `config` : Folder which contains URL and paths to download databases.  
* `src` : Source folder. It contains two subfolders:  
        - `data_science` : Subfolder which contains the scripts to create the model.  
        - `df_manipulation` : Subfolder which contains the scripts to download the database and create dummy variables. There are one Airbnb database dated back to 2017 and           another of 2023.  
* `tests` : Folder which contains unit tests.
* `venv` : Folder which contains the virtual environment.
* `README.txt` : File which presents the organization of the project and helps for files manipulation.
* `requirements.txt` : File which lists the Python packages required to use the application.  

Additionally, a dictionary of database variables is available in the wiki.

## Execution of the project

* To clone this repository  
  `git clone https://github.com/Val832/produit_digital.git`  
  `cd produit_digital`  

* Download the Airbnb 2017 database  
  `python -m src.df_manipulation.2017.download_db2017`   
* Create dummy variables from the Airbnb 2017 database  
  `python -m src.df_manipulation.2017.create_dummies2017`  
* Download the Airbnb 2023 database  
  `python -m src.df_manipulation.2023.download_db2023`  
* Create dummy variables from the Airbnb 2023 database  
  `python -m src.df_manipulation.2023.create_dummies2023`  

* Make sure all required dependencies are installed  
  `pip install -r requirements.txt`

* Run the script of the model in the `src` folder.
