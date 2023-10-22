#pip install scikit-fuzzy

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


# Peso com gaussiana
peso = ctrl.Antecedent(np.arange(30, 151, 1), 'peso')
peso['Muito Magro'] = fuzz.gaussmf(peso.universe, 40, 5)
peso['Magro'] = fuzz.gaussmf(peso.universe, 55, 5)
peso['Aesthetic'] = fuzz.gaussmf(peso.universe, 75, 5)
peso['Gordo'] = fuzz.gaussmf(peso.universe, 95, 5)
peso['Muito Gordo'] = fuzz.gaussmf(peso.universe, 125, 15)

# Altura com gaussiana
altura = ctrl.Antecedent(np.arange(1.0, 2.51, 0.01), 'altura')
altura['Baixo'] = fuzz.gaussmf(altura.universe, 1.32, 0.1)
altura['Mediano'] = fuzz.gaussmf(altura.universe, 1.75, 0.05)
altura['Alto'] = fuzz.gaussmf(altura.universe, 2.15, 0.15)

# Peso de massa magra com gaussiana
pesoM = ctrl.Antecedent(np.arange(30, 151, 1), 'pesoM')
pesoM['Pouca Massa'] = fuzz.gaussmf(pesoM.universe, 45, 7)
pesoM['Massa Normal'] = fuzz.gaussmf(pesoM.universe, 75, 10)
pesoM['Muito Massa'] = fuzz.gaussmf(pesoM.universe, 115, 15)

# Tempo de academia e atv física com gaussiana
tempoAF = ctrl.Antecedent(np.arange(0, 25, 0.5), 'tempoAF')
tempoAF['Pouco tempo'] = fuzz.gaussmf(tempoAF.universe, 2, 1.5)
tempoAF['Tempo Normal'] = fuzz.gaussmf(tempoAF.universe, 9, 3)
tempoAF['Rato de Academia'] = fuzz.gaussmf(tempoAF.universe, 20, 3)

# Obesidade com gaussiana
obesidade = ctrl.Consequent(np.arange(0, 101, 1), 'obesidade')
obesidade['Abaixo do peso'] = fuzz.gaussmf(obesidade.universe, 15, 5)
obesidade['Normal'] = fuzz.gaussmf(obesidade.universe, 35, 10)
obesidade['Sobrepeso'] = fuzz.gaussmf(obesidade.universe, 65, 7)
obesidade['Obesidade Grau I'] = fuzz.gaussmf(obesidade.universe, 82.5, 5)
obesidade['Obesidade Grau II'] = fuzz.gaussmf(obesidade.universe, 92.5, 3)
obesidade['Obesidade Grau III'] = fuzz.gaussmf(obesidade.universe, 97.5, 1.5)

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
