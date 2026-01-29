# read the csv file and show the info
import pandas as pd
import numpy as np
from IPython.display import display


class DataCleaner():
    def __init__(self, fileName):
        path = "./Dataset/" + str(fileName)
        self.dataset = pd.read_csv(path)
        self.dataset_height = self.dataset.shape[0]
        self.dataset_width = self.dataset.shape[1]
        self.dataset_varlist = self.dataset.columns.to_list()

    def show_head(self, num_rows):
        # show the first num_rows rows
        display(self.dataset.head(num_rows))
        
    def show_variable_info(self):
        # show variable (column) information
        display(self.dataset.iloc[:, 0:int(self.dataset_width/2)].info())
        display(self.dataset.iloc[:, int(self.dataset_width/2): self.dataset_width].info())

    def show_description(self):
        # show summaries of the columns
        display(self.dataset.iloc[:,0: int(self.dataset_width/2)].describe())
        display(self.dataset.iloc[:,int(self.dataset_width/2):self.dataset_width].describe())

    # ---------------------------data manipulation-------------------------

    def delete_column(self, col_name):
        # delete the particular column
        # You should work on the dataset_output (deep copy of original one), not the original one
        if col_name in self.dataset_varlist:
            self.dataset = self.dataset.drop(columns=str(col_name), axis=1)
            self.dataset_varlist = self.dataset.columns.to_list()

        else:
            print("Already deleted!")

    def change_var_type(self, col_name, new_type):
        # change the column type to int, float, string, boolean
        if new_type not in [int, float, str, bool]:
            print("Only int, float, str, bool are acceptable!")
            return
        
        self.dataset[col_name] = self.dataset[col_name].astype(new_type)

    def replace_values(self, col_name, mapping_dict):
        # repalce the values in the column, from old to new
        # mapping_dict should be a dictionary
        self.dataset[col_name] = self.dataset[col_name].replace(mapping_dict)

    def check_missingValues(self):
        # show number of missing values in each column
        missing_values = self.dataset.iloc[:, 0: int(self.dataset_width/2)].isnull().sum()
        display(missing_values)
        missing_values = self.dataset.iloc[:, int(self.dataset_width/2): self.dataset_width].isnull().sum()
        display(missing_values)

    def save_dataset(self):
        # save current dataset as cleaned data
        output_path = "./Dataset/cleaned_Employee_Attrition.xlsx"
        self.dataset.to_excel(output_path, index=False)

        output_path = "./Dataset/cleaned_Employee_Attrition.csv"
        self.dataset.to_csv(output_path, index=False)
        print("Dataset saved as both csv and excel!")

    # ---------------------------Interactive Pipeline Process-------------------------
    def run_pipeline(self):
        # Read the data, and show basic info
        print("Data loaded! Run the cleaning pipeline now ...")

        # Remove redundant/meaningful variables (EmployeeCount, StandardHours)
        rm_varlist = ["EmployeeCount", "StandardHours", "Over18"]
        for var in rm_varlist:
            self.delete_column(var)
            print("{0} is deleted!".format(var))

        # Replace values in certain varibales
        map_list = {"Attrition":{"Yes": 1, "No": 0}}
        for key, value in map_list.items():
            self.replace_values(key, value)
            print("Changed the value in variable {0}, mapping rules are {1}!".format(key, value))
   
        # data_loader.replace_values("Attrition", {"Yes": 1, "No": 0})

        # Change variable type
        var_type = {"Attrition": int}
        for var, data_type in var_type.items():
            self.change_var_type(var, data_type)
            print("Transformed the variable {0} to data type {1}".format(var, str(data_type)))
        
        # Export the cleaned data
        self.save_dataset()