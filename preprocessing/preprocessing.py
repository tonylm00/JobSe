import pandas as pd
import numpy as np

pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', None)

# caricamento del dataset
dataset = pd.read_csv("../data/original_data.csv", delimiter=';')

# sostituzione di 'Not Avilable' con NaN
dataset.replace('Not Avilable', np.nan, inplace=True)

# drop IDs non necessari
dataset = dataset.drop(['job_ID', 'company_id', 'details_id', 'linkedin_followers'], axis=1)

# drop delle colonne senza intestazione e informazioni rilevanti
unNamedColumns = [colonna for colonna in dataset.columns if colonna.startswith('Unnamed')]
dataset = dataset.drop(unNamedColumns, axis=1)

# imputazione dei valori mancanti in base al tipo di lavoro
dataset.loc[dataset['work_type'] == 'Remote', ['City', 'State']] = ['Presence on site not required', 'Work in remote']

# imputazione dei valori mancanti in base al tipo di lavoro

# Sostituisci i valori NaN e Not Available con "To be determined based on experience"
dataset['level'].fillna('To be determined based on experience', inplace=True)
dataset['level'].replace('Not Avilable', 'To be determined based on experience', inplace=True)

# inputazione di industry sulla base di designation'
grouped_data = dataset.groupby('designation')

def replace_nan_with_mode(x):
    mode_value = x.mode()
    fill_value = mode_value.iloc[0] if not mode_value.empty else "Unknown"
    return x.fillna(fill_value)

dataset['industry'] = grouped_data['industry'].transform(replace_nan_with_mode)

# Elimina le righe con "City" mancante (NaN)
dataset = dataset.dropna(subset=['City'])

# Sostituisci i valori nulli di 'monthly_salary' con la media dei valori di 'monthly_salary' delle righe con lo stesso valore di 'designation'
dataset['monthly_salary'] = dataset.groupby('designation')['monthly_salary'].transform(lambda x: x.fillna(x.mean()))

#save csv
dataset.to_csv('cleaned_data.csv')
print(dataset)
