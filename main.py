import pandas as pd
import numpy as np
import re
import seaborn as sns
import openpyxl
from scipy.stats import gamma
import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None

class Data:
    def __init__(self, filepath):
        self._path = filepath
        self._data = None

class CheckData(Data):
    def __init__(self, filepath):
        super().__init__(filepath)

    @property
    def OpenData(self):
        with open(self._path, 'r', encoding='utf8') as file:
            for index, value in enumerate(file):
                if index < 10:
                    print(index, value)

    @property
    def LoadData(self):
        self._data = pd.read_csv(self._path, delimiter = ',', engine = 'python')
        return self._data

    @property
    def InfoData(self):
        return self._data.info()

class PreprocessingData(Data):
    def __init__(self, filepath):
        super().__init__(filepath)

    def DeleteCols(self, cols_name):
        self._data = self.LoadData
        self._data = self._data.drop(columns = cols_name)

    def RenameCols(self, cols_name):
        self._data.rename(columns = cols_name, inplace = True)

    def FillNa(self, cols_name):
        self._data.fillna(cols_name, inplace = True)

    @property
    def CheckDuplicatedData(self):
        return self._data[self._data.loc[:,:].duplicated()]

    @property
    def DropDuplicatedData(self):
        self._data = self._data.drop_duplicates(subset = self._data.loc[:,:], keep = 'first', ignore_index = True)

    def FindUniqueCols(self, char):
        result = []
        columns = self._data.columns
        for column in columns:
            strings = self._data[column]
            for string in strings:
                match = re.search(char, string)
                if match:
                    if column not in result:
                        result.append(column)
        return result

    def ReplaceUniqueChar(self, cols_name, dictionary):
        for old_char, new_char in dictionary.items():
            for cols in cols_name:
                index = self._data[self._data[cols].str.contains(old_char, case = False, na = False, regex = True)].index
                self._data.loc[index, cols] = self._data[cols].str.replace(old_char, new_char, regex = True)

    def ReplaceChar(self, cols_name, string, transform):
        self._data[cols_name] = self._data[cols_name].str.replace(string, transform, case = False, regex = True)

    def SpecialCaseChar(self, char, cols_name, transform, mode, old_char = None, custom_cols = None):
        if mode == 'assignment':
            index = self._data[cols_name][self._data[cols_name].str.contains(char, case = False, na = False, regex = True)].index
            self._data.loc[index, cols_name] = transform
        elif mode == 'replace':
            if old_char is None:
                raise ValueError("Parameter 'old_char' is required when mode is 'replace'")
            index = self._data[cols_name][self._data[cols_name].str.contains(char, case = False, na = False, regex = True)].index
            self._data.loc[index, cols_name] = self._data[cols_name].str.replace(old_char, transform, regex = True)
        elif mode == 'custom':
            if custom_cols is None:
                raise ValueError("Parameter 'custom_cols' is required when mode is 'custom'")
            index = self._data[cols_name][self._data[cols_name].str.contains(char, case = True, na = False, regex = True)].index
            self._data.loc[index, custom_cols] = transform

    def StrTitle(self, cols_name):
        self._data[cols_name] = self._data[cols_name].str.title()

    def AddFillCols(self, num_key_cols, key_cols1, new_cols, keyword_map, position_cols, default_value, key_cols2 = None):
        self._data.insert(position_cols, column = new_cols, value = np.nan)
        
        #Single Key Column
        if num_key_cols == 1:
            conditions = [self._data[key_cols1].str.contains(keyword, case = False, na = False, regex = True) for keyword in keyword_map.keys()]
            choice = list(keyword_map.values())
            self._data[new_cols] = np.select(conditions, choice, default = default_value)
            
        #Multiple Key Column
        elif num_key_cols == 2:
            if key_cols2 == None:
                raise ValueError("'key_cols2' is not defined.")
            conditions = [(self._data[key_cols1].str.contains(keyword, case = False, na = False, regex = True) | self._data[key_cols2].str.contains(keyword, case = False, na = False, regex = True)) for keyword in keyword_map.keys()]
            choice = list(keyword_map.values())
            self._data[new_cols] = np.select(conditions, choice, default = default_value)

        else:
            raise ValueError("Wrong input for 'num_key_cols'")

    
    ## Cleaned Salary Column
    def CleanedSalary(self, text):
        if pd.notnull(text):
            replace_kilo = re.sub(r'(\d+)\s*K\b', lambda newstr: str(int(newstr.group(1)) * 1000), text, flags = re.I)
            remove_parentheses = re.sub(r'\([^()]*\)', '', replace_kilo)
            cleaned_salary = re.sub(r'[^\d+,\.\-\s*a-zA-Z]', '', remove_parentheses)
            return cleaned_salary
        return ''

    def FinalFixedSalary(self, text):
        if text != 'Undef':
            remove_comma = re.sub(r'\,', '', text)
            remove_char = re.sub(r'[a-zA-Z]\s*', '', remove_comma)
            final_salary = re.sub(r'\d{7,}\s*', '', remove_char)
            result = re.sub(r'\b(?!\d{5,6}\b)\d+(?:\.\d+)?|\D+', ' ', final_salary)
            result = result.strip()
            return result
        return text

    def MinSalary(self, text):
        if text != 'Undef':
            pattern = r'\d+'
            match = re.findall(pattern, text)
            return match[0]
        else:
            return text

    def MaxSalary(self, text):
        if text != 'Undef':
            match = re.findall(r'\d+', text)
            if len(match) >= 2:
                items = [int(x) for x in match]
                if match[0] == str(max(items)):
                    return 'Undef'
                else:
                    return str(max(items))
            else:
                return 'Undef'
        else:
            return 'Undef'

    def ApplyFunction(self, def_name, cols_name, new_cols = None):
        if def_name == 'CleanedSalary':
            self._data[cols_name] = self._data[cols_name].apply(self.CleanedSalary)
            return self._data[cols_name]
        elif def_name == 'FinalFixedSalary':
            self._data[cols_name] = self._data[cols_name].apply(self.FinalFixedSalary)
            return self._data[cols_name]
        else:
            if new_cols == None:
                raise ValueError('Error Add Name of New Columns!')
            else:
                if def_name == 'MinSalary':
                    self._data[new_cols] = self._data[cols_name].apply(self.MinSalary)
                    return self._data[new_cols]
                elif def_name == 'MaxSalary':
                    self._data[new_cols] = self._data[cols_name].apply(self.MaxSalary)
                    return self._data[new_cols]

    def FixedSalary(self, char, convert_time = None):
        if char == 'day':
            index = self._data['Salary'][self._data['Salary'].str.contains(char, case = False, na = False, regex = True)].index
            txt = self._data.loc[index, 'Salary']
            for string in txt:
                fixed_comma = re.sub(r'\,', '.', string)
                self._data.loc[index, 'Salary'] = re.sub(r'er day', ' a year', fixed_comma)
        else:
            if convert_time == None:
                raise ValueError("Need Convert Time Parameter!")
            index = self._data['Salary'][self._data['Salary'].str.contains(char, case = False, na = False, regex = True)].index
            if char == 'hour':
                strings = self._data.loc[index, 'Salary']
            else:
                strings = self._data.loc[index, 'Salary'].str.replace(',','')
            result = []
            for string in strings:
                numeric_fixed = re.sub(r'([+-]?[0-9]*[.]?[0-9]+)', lambda newstr: str(int((float(newstr.group(1)) * convert_time))), string)
                fixed_salary = re.sub(char, 'year', numeric_fixed, flags = re.I)
                result.append(fixed_salary)
            self._data.loc[index, 'Salary'] = result
            
    ## SpecialCase
    @property
    def SpecialCaseSalary(self):
        for index, value in enumerate(self._data['Salary']):
            if value == '':
                self._data.loc[index, 'Salary'] = 'Undef'

    @property
    def SalaryToNumeric(self):
        self._data['Min Salary'] = pd.to_numeric(self._data['Min Salary'], errors = 'coerce')
        self._data['Max Salary'] = pd.to_numeric(self._data['Max Salary'], errors = 'coerce')

    @property
    def FinalData(self):
        return self._data

class MergeFunction(CheckData, PreprocessingData):
    def __init__(self, filepath):
        super().__init__(filepath)
    