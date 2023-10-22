#pip install scikit-fuzzy

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt



# Peso com triangular
peso = ctrl.Antecedent(np.arange(30, 151, 1), 'peso')
peso['Muito Magro'] = fuzz.trimf(peso.universe, [30, 40, 50])
peso['Magro'] = fuzz.trimf(peso.universe, [40, 55, 70])
peso['Aesthetic'] = fuzz.trimf(peso.universe, [60, 75, 90])
peso['Gordo'] = fuzz.trimf(peso.universe, [80, 95, 110])
peso['Muito Gordo'] = fuzz.trimf(peso.universe, [100, 125, 150])

# Altura com triangular
altura = ctrl.Antecedent(np.arange(1.0, 2.51, 0.01), 'altura')
altura['Baixo'] = fuzz.trimf(altura.universe, [1.0, 1.32, 1.65])
altura['Mediano'] = fuzz.trimf(altura.universe, [1.6, 1.75, 1.9])
altura['Alto'] = fuzz.trimf(altura.universe, [1.8, 2.15, 2.5])

# Peso de massa magra com triangular
pesoM = ctrl.Antecedent(np.arange(30, 151, 1), 'pesoM')
pesoM['Pouca Massa'] = fuzz.trimf(pesoM.universe, [30, 45, 60])
pesoM['Massa Normal'] = fuzz.trimf(pesoM.universe, [55, 75, 95])
pesoM['Muito Massa'] = fuzz.trimf(pesoM.universe, [80, 115, 150])

# Tempo de academia e atv física com triangular
tempoAF = ctrl.Antecedent(np.arange(0, 25, 0.5), 'tempoAF')
tempoAF['Pouco tempo'] = fuzz.trimf(tempoAF.universe, [0, 2, 5])
tempoAF['Tempo Normal'] = fuzz.trimf(tempoAF.universe, [4, 9, 15])
tempoAF['Rato de Academia'] = fuzz.trimf(tempoAF.universe, [12, 20, 25])

# Obesidade com triangular
obesidade = ctrl.Consequent(np.arange(0, 101, 1), 'obesidade')
obesidade['Abaixo do peso'] = fuzz.trimf(obesidade.universe, [0, 15, 30])
obesidade['Normal'] = fuzz.trimf(obesidade.universe, [20, 35, 50])
obesidade['Sobrepeso'] = fuzz.trimf(obesidade.universe, [45, 65, 75])
obesidade['Obesidade Grau I'] = fuzz.trimf(obesidade.universe, [70, 82.5, 90])
obesidade['Obesidade Grau II'] = fuzz.trimf(obesidade.universe, [85, 92.5, 97])
obesidade['Obesidade Grau III'] = fuzz.trimf(obesidade.universe, [95, 100, 100])

# Visualização das variáveis
peso.view()
altura.view()
pesoM.view()
tempoAF.view()
obesidade.view()
plt.show()




#1 Abaixo do peso
#2 Normal
#3 Sobrepeso
#4 Obesidade Grau I
#5 Obesidade Grau II
#6 Obesidade Grau III


# Criando as regras
regra_1 = ctrl.Rule((peso['Muito Magro'] | peso['Magro']) & altura['Alto'], obesidade['Abaixo do peso'])
regra_2 = ctrl.Rule((peso['Magro'] | peso['Aesthetic']) & (altura['Alto'] | altura['Mediano']), obesidade['Normal'])
regra_3 = ctrl.Rule(peso['Gordo'] & (altura['Mediano'] | altura['Baixo']), obesidade['Sobrepeso'])
regra_4 = ctrl.Rule(peso['Gordo'], obesidade['Sobrepeso'])
regra_5 = ctrl.Rule(peso['Gordo'] & (altura['Mediano'] | altura['Baixo']), obesidade['Obesidade Grau I'])
regra_6 = ctrl.Rule(peso['Gordo'] & altura['Baixo'], obesidade['Obesidade Grau II'])
regra_7 = ctrl.Rule(peso['Muito Gordo'] & altura['Baixo'], obesidade['Obesidade Grau III'])
regra_8 = ctrl.Rule(pesoM['Pouca Massa'] & tempoAF['Pouco tempo'], obesidade['Abaixo do peso'])
regra_9 = ctrl.Rule(pesoM['Muito Massa'] & tempoAF['Rato de Academia'], obesidade['Normal'])
regra_10 = ctrl.Rule(pesoM['Pouca Massa'] & tempoAF['Rato de Academia'], obesidade['Normal'])

controlador = ctrl.ControlSystem([regra_1, regra_2, regra_3, regra_4, regra_5, regra_6, regra_7, regra_8, regra_9, regra_10])


# Simulando
CalculoObesidade = ctrl.ControlSystemSimulation(controlador)

peso_input = float(input('Peso em kg (uma casa decimal): '))
altura_input = float(input('Altura em metros (duas casas decimais): '))
pesoM_input = float(input('Peso muscular em kg (uma casa decimal): '))
tempoAF_input = float(input('Tempo de atividade física por semana em horas (inteiro): '))

CalculoObesidade.input['peso'] = peso_input
CalculoObesidade.input['altura'] = altura_input
CalculoObesidade.input['pesoM'] = pesoM_input
CalculoObesidade.input['tempoAF'] = tempoAF_input
CalculoObesidade.compute()

obesidade_result = CalculoObesidade.output['obesidade']

print("\nPeso %f \nAltura %f \nObesidade %f" % (
    peso_input,
    altura_input,
    obesidade_result
))

peso.view(sim=CalculoObesidade)
altura.view(sim=CalculoObesidade)
pesoM.view(sim=CalculoObesidade)
tempoAF.view(sim=CalculoObesidade)
obesidade.view(sim=CalculoObesidade)
#1 Abaixo do peso
#2 Normal
#3 Sobrepeso
#4 Obesidade Grau I
#5 Obesidade Grau II
#6 Obesidade Grau III
plt.show()
