import pandas as pd
from scipy import integrate
from scipy.optimize import curve_fit


class motor_analisys:
    def __init__(self, archive):
        self.df = pd.read_csv(
            archive, sep='\t', header=None).iloc[:, 0].str.split(';', expand=True)
        self.df[2] = self.df[2].astype(float) * 9.81
        self.df[3] = self.df[3].astype(float) / 100
        temp = self.df[3].iloc[0]
        self.df[3] -= temp

    def get_data(self):
        dados_result = {'Data':self.df[0],'Hora':self.df[1],'Empuxo (N)': self.df[2], 'Tempo (s)': self.df[3]}
        df_result = pd.DataFrame(dados_result)
        return df_result
    

    def get_result(self):
        def classe(total, medio, tempo):
            classes = [
                (0.625, '1/4A'), (1.25, '1/2A'), (2.5, 'A'), (5, 'B'), (10, 'C'),
                (20, 'D'), (40, 'E'), (80, 'F'), (160, 'G'), (320, 'H'),
                (640, 'I'), (1280, 'J'), (2560, 'K'), (5120, 'L'), (10240, 'M')
            ]

            for limit, designation in classes:
                if total <= limit:
                    return f"{designation}{medio:.1f} - {tempo:.1f}"

            return 'ERRO'

        dados_result = {'Info': ['Impulso', 'Empuxo max (N)', 'Empuxo medio (N)', 'Pontos amostrais', 'Duração (s)', 'Classe'],
                        'Valor': [0.0, 0.0, 0.0, 0, 0.0, '']}
        df_result = pd.DataFrame(dados_result)

        df_result.at[0, 'Valor'] = integrate.simpson(
            y=self.df[2], x=self.df[3])
        df_result.at[1, 'Valor'] = max(self.df[2])
        df_result.at[2, 'Valor'] = (
            1/(self.df[3].iloc[-1]-self.df[3].iloc[0]))*df_result.at[0, 'Valor']
        df_result.at[3, 'Valor'] = len(self.df)
        df_result.at[4, 'Valor'] = self.df[3].iloc[-1]-self.df[3].iloc[0]
        df_result.at[5, 'Valor'] = classe(
            df_result.at[0, 'Valor'], df_result.at[2, 'Valor'], df_result.at[4, 'Valor'])

        return df_result

    def get_curve(self):
        def objective(x, a, b, c, d, e, f, g, h):
            return (a * x) + (b * x**2) + (c * x**3) + (d * x**4) + (e * x**5) + (f * x*6) + (g * x*7) + (h)

        popt, _ = curve_fit(objective, self.df[3], self.df[2])
        a, b, c, d, e, f, g, h = popt

        return f'{a:.2f}*x + {b:.2f}*x**2 + {c:.2f}*x**3 + {d:.2f}*x**4 + {e:.2f}*x**5 + {f:.2f}*x**6 + {g:.2f}*x**7 + {h:.2f}'


class flight_analysis:
    def __init__(self, archive):
        self.df = pd.read_csv(
            archive, sep='\t', header=None).iloc[:, 0].str.split(';', expand=True)
    
    def get_data(self):
        return self.df

    # def get_trajectory(self):
        # dados_result = {'Pressão':[], 'Altura':[], 'Altura GPS':[], 'Velocidade Intantânea':[], 'Aceleração Instantânea':[], 'Tempo de Voo':self.df[0]}                       }
        # df_result = pd.DataFrame(dados_result)

        # return df_result

    def get_sensor_data(self):
        dados_result = {'Pressão': self.df[1], 'Temperatura': self.df[4],
                        'Altura': self.df[2], 'Tempo de Voo': self.df[0]}
        df_result = pd.DataFrame(dados_result)

        return df_result

    def get_GPS(self):
        dados_result = {'Latitude': self.df[1], 'Longitude': self.df[4],
                        'Altura GPS': self.df[4], 'Tempo de Voo': self.df[0]}
        df_result = pd.DataFrame(dados_result)

        return df_result


if __name__ == '__main__':
    import easygui
    motor = motor_analisys(easygui.fileopenbox())
    print(motor.get_result())
    # voo = flight_analysis(easygui.fileopenbox())
    # print(voo.get_GPS())
