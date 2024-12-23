import pandas as pd
from scipy import integrate
from scipy.interpolate import CubicSpline
from scipy.optimize import curve_fit


class motor_analisys:
    def __init__(self, archive, saved):
        if saved:
            self.df = pd.read_csv(archive, sep=';')
        else:
            self.df = pd.read_csv(archive, sep=';')
            self.df['Empuxo'] = pd.to_numeric(self.df['Empuxo'], errors='coerce')
            self.df['Tempo'] = pd.to_numeric(self.df['Tempo'], errors='coerce')
            self.df['Tempo'] -= self.df['Tempo'].iloc[0]
            self.df['Empuxo'] = round(self.df['Empuxo'] * 9.81, 4)
            self.df['Tempo'] = round(self.df['Tempo'] / 1000, 4)

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
                    return f"{designation}{medio:.1f}-{tempo:.1f}"

            return 'ERRO'

        impulso = round(integrate.simpson(
            y=self.df['Empuxo'], x=self.df['Tempo']), 4)
        empuxo_max = round(max(self.df['Empuxo']), 4)
        empuxo_medio = round(
            (1 / (self.df['Tempo'].iloc[-1] - self.df['Tempo'].iloc[0])) * impulso, 4)
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

    def spline(self):
        x = self.df['Tempo'].tolist()
        y = self.df['Empuxo'].tolist()
        curve = CubicSpline(x, y)
        return curve
    
    def plot_analisys(self, name: str):
        import matplotlib.pyplot as plt
        plt.scatter(self.df['Tempo'], self.df['Empuxo'],
                    label='Pontos de Amostragem', color='red')
        curve = self.spline()
        xi = self.df['Tempo'].tolist()
        plt.plot(xi, curve(xi), label='Curva de Empuxo', color='black')
        plt.xlabel('Tempo (s)')
        plt.ylabel('Empuxo (N)')
        plt.title('Empuxo do Motor - ' + name)
        plt.grid()
        plt.legend()
        plt.savefig('Analise_Flask/app/archives/motor/' +
                    name + '_grafico.png')

    def pdf(self, name: str):
        from fpdf import FPDF

        class PDF(FPDF):
            def header(self):
                # Logos
                self.image(
                    'CenterFlask/flaskr/static/assets/LOGO - ALTERNATIVA.png', 210-47, -5, 50)
                self.image(
                    'CenterFlask/flaskr/static/assets/logomarca-uerj-300x300.png', 2, 2, 35)

                self.set_font('Arial', 'B', 25)
                # Move to the right
                self.cell(80)
                # Title
                self.cell(30, 25, 'Relatório de Teste Estático', 0, 0, 'C')
                # Line break
                self.ln(20)
                self.set_fill_color(r=43, g=18, b=76)
                self.set_y(45)
                self.cell(0, 1, ' ', 0, 1, 'C', 1)

            # Page footer
            def footer(self):
                # Position at 1.5 cm from bottom
                self.set_y(-15)
                # Arial italic 8
                self.set_font('Arial', 'I', 8)
                # Page number
                self.cell(0, 10, 'Página ' + str(self.page_no()) +
                          '/{nb}' + ' - Equipe Serra Rocketry', 0, 0, 'C')

        # Instantiation of inherited class
        pdf = PDF()
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_xy(15, 50)
        pdf.set_font('Courier', 'B', 20)
        pdf.cell(0, 10, '{}'.format(name), 0, 0, 'C', 0)
        pdf.set_xy(15, 60)
        pdf.set_font('Courier', '', 16)
        pdf.multi_cell(0, 10, 'Data do teste: {}'.format(self.df.at[0, 'Data']) +
                       '\nHorário do teste: {}'.format(self.df.at[0, 'Hora']))

        pdf.set_xy(15, 75)
        pdf.set_font('Courier', '', 14)
        pdf.multi_cell(0, 8, '\nImpulso Total (N*s) = {:.3f}'.format(self.df_result.at[0, 'Impulso']) +
                       '\nEmpuxo Médio (N) = {:.3f}'.format(self.df_result.at[0, 'Empuxo medio (N)']) +
                       '\nEmpuxo Máximo (N) = {:.3f}'.format(self.df_result.at[0, 'Empuxo max (N)']) +
                       '\nTempo aproximado de queima (s)= {:.1f}'.format(self.df_result.at[0, 'Duração (s)']), 0, 1)

        pdf.set_xy(105, 83)
        pdf.set_font('Courier', '', 40)
        pdf.cell(0, 10, '{}'.format(self.df_result.at[0, 'Classe']))

        pdf.set_fill_color(r=43, g=18, b=76)
        pdf.set_y(120)
        pdf.cell(0, 1, ' ', 0, 1, 'C', 1)
        pdf.image('Analise_Flask/app/archives/motor/' + name +
                  '_grafico.png', (210/2)-90, 130, 180, 140)
        pdf.output('Analise_Flask/app/archives/motor/' + name + '.pdf', 'F')

    def save_analisys(self, name: str):
        result = self.get_result()
        result.to_csv('Analise_Flask/app/archives/motor/' + name + '_resultados.csv',
                      sep=';', index=False)
        self.df.to_csv('Analise_Flask/app/archives/motor/' +
                       name + '_dados.csv', sep=';', index=False)
        self.plot_analisys(name)
        # self.pdf(name)
