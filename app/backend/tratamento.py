import pandas as pd

class data_treatment:
    def __init__(self, archive):
        self.data = pd.read_csv(archive, header=None, names=['Data', 'Hora', 'Empuxo', 'Tempo'], sep=';')

    def get_data(self):
        return self.data
    
    def data_filter(self, threshold, interval=None):
        if interval:
            min_interval, max_interval = interval
            self.data_cleaned = self.data[(self.data['Empuxo'] > threshold) & (self.data['Tempo'].between(min_interval, max_interval))]
        else:
            self.data_cleaned = self.data[self.data['Empuxo'] > threshold]
        return self.data_cleaned
    
    def save_treatment(self, name):
        self.data_cleaned.to_csv('Analise_Flask/app/data/data_treatment/' + name + '_processed.csv', sep=';', index=False)