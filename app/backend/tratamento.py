import pandas as pd

class data_treatment:
    def __init__(self, archive, team, objective):
        self.data = None
        if objective == 'static':
            self._load_static_data(archive, team)
        elif objective == 'flight':
            self._load_flight_data(archive, team)
        else:
            raise ValueError('Objetivo de teste não suportado!')

    def _load_static_data(self, archive, team):
        if team == 'Serra Rocketry':
            self.data = pd.read_csv(archive, header=None, names=['Data', 'Hora', 'Empuxo', 'Tempo'], sep=';')
        elif team == 'GFRJ':
            self.data = pd.read_csv(archive, header=None, names=['Tempo', 'Empuxo', 'Temperatura', 'Pressao'], sep='\t')
            self._clean_gfrj_data()
        else:
            raise ValueError('Dados de equipe não suportada!')

    def _clean_gfrj_data(self):
        self.data = self.data[~self.data['Empuxo'].str.contains('not found')]
        self.data = self.data[~self.data['Temperatura'].str.contains('not found')]
        self.data = self.data[~self.data['Pressao'].str.contains('not found')]

        self.data['Empuxo'] = self.data['Empuxo'].str.replace('HX711 reading:', '').str.replace(' Kg', '')
        self.data['Temperatura'] = self.data['Temperatura'].str.replace('Temperatura:', '').str.replace(' °C', '')
        self.data['Pressao'] = self.data['Pressao'].str.replace('Pressão:', '').str.replace(' psi', '')

        self.data = self.data.astype({'Tempo': float, 'Empuxo': float, 'Temperatura': float, 'Pressao': float})

    def _load_flight_data(self, archive, team):
        if team == 'Serra Rocketry':
            pass  # Implement flight data loading for Serra Rocketry
        elif team == 'GFRJ':
            pass  # Implement flight data loading for GFRJ
        else:
            raise ValueError('Dados de equipe não suportada!')

    def static_data_info(self):
        return self.data['Empuxo'].describe()
    
    def static_histogram(self):
        return self.data['Empuxo'].hist()
    
    def static_filter(self, threshold):
        self.data_cleaned = self.data[self.data['Empuxo'] > threshold]
        return self.data_cleaned
    
    def static_save(self, name):
        self.data_cleaned.to_csv(name, sep=';', index=False)
        return 'Dados salvos com sucesso!'
