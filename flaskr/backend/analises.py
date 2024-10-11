import pandas as pd
from scipy import integrate
from scipy.optimize import curve_fit


class motor_analisys:
    def __init__(self, archive):
        self.df = pd.read_csv(archive, sep=';')
        self.df['Empuxo'] = self.df['Empuxo'].astype(float) * 9.81
        self.df['Tempo'] = self.df['Tempo'].astype(float) / 1000

    def get_data(self):
        return self.df

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

        impulso = integrate.simpson(y=self.df['Empuxo'], x=self.df['Tempo'])
        empuxo_max = max(self.df['Empuxo'])
        empuxo_medio = (
            1 / (self.df['Tempo'].iloc[-1] - self.df['Tempo'].iloc[0])) * impulso
        pontos_amostrais = len(self.df)
        duracao = self.df['Tempo'].iloc[-1] - self.df['Tempo'].iloc[0]
        classe_motor = classe(impulso, empuxo_medio, duracao)
        curva = self.get_curve()

        dados_result = {
            'Impulso': [impulso],
            'Empuxo max (N)': [empuxo_max],
            'Empuxo medio (N)': [empuxo_medio],
            'Pontos amostrais': [pontos_amostrais],
            'Duração (s)': [duracao],
            'Classe': [classe_motor],
            'Curva': [curva]
        }
        self.df_result = pd.DataFrame(dados_result)

        return self.df_result

    def get_curve(self):
        def objective(x, a, b, c, d, e, f):
            return (a * x) + (b * x**2) + (c * x**3) + (d * x**4) + (e * x**5) + f

        popt, _ = curve_fit(objective, self.df['Tempo'], self.df['Empuxo'])
        a, b, c, d, e, f = popt
        return f'({a} * t) + ({b} * t**2) + ({c} * t**3) + ({d} * t**4) + ({e} * t**5) + {f}'

    def plot_analisys(self, name: str):
        import matplotlib.pyplot as plt
        # import mplcyberpunk
        # plt.style.use("cyberpunk")
        plt.scatter(self.df['Tempo'], self.df['Empuxo'],
                    label='Pontos de Amostragem', color='#00ff41')
        curve = self.get_curve()
        xi = self.df['Tempo'].tolist()
        y = [eval(curve) for t in xi]
        plt.plot(xi, y, label='Curva de Empuxo', color='#08F7FE')
        plt.xlabel('Tempo (s)')
        plt.ylabel('Empuxo (N)')
        plt.title('Empuxo do Motor')
        plt.legend()
        plt.savefig('CenterFlask/flaskr/archives/motor/' +
                    name + '_grafico.png')

    def save_analisys(self, name: str):
        result = self.get_result()
        result.to_csv('CenterFlask/flaskr/archives/motor/' + name + '_resultados.csv',
                      sep=';', index=False)
        self.df.to_csv('CenterFlask/flaskr/archives/motor/' +
                       name + '_dados.csv', sep=';', index=False)
        self.plot_analisys(name)


class flight_analysis:
    def __init__(self, archive):
        self.df = pd.read_csv(archive, sep=';', names=[], header=None)


if __name__ == '__main__':
    import easygui
    motor = motor_analisys(easygui.fileopenbox())
    motor.save_analisys('teste1')
    # voo = flight_analysis(easygui.fileopenbox())
