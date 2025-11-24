#Isso separa a lógica de cálculo das views, deixando o código mais limpo.

def calcular_inss(salario_bruto):
    teto_inss = 7786.02
    if salario_bruto > teto_inss:
        return 908.85
    
    desconto = 0.0
    faixa1 = 1412.00
    faixa2 = 2666.68
    faixa3 = 4000.03
    
    calc_salario = salario_bruto

    # 1ª Faixa
    base = min(calc_salario, faixa1)
    desconto += base * 0.075
    
    # 2ª Faixa
    if calc_salario > faixa1:
        base = min(calc_salario, faixa2) - faixa1
        desconto += base * 0.09
        
    # 3ª Faixa
    if calc_salario > faixa2:
        base = min(calc_salario, faixa3) - faixa2
        desconto += base * 0.12
        
    # 4ª Faixa
    if calc_salario > faixa3:
        base = calc_salario - faixa3
        desconto += base * 0.14
        
    return round(desconto, 2)

def calcular_irrf(salario_bruto, desconto_inss, dependentes=0):
    base_calculo = salario_bruto - desconto_inss - (dependentes * 189.59)
    irrf = 0.0
    
    if base_calculo <= 2259.20:
        return 0.0
    elif base_calculo <= 2826.65:
        irrf = (base_calculo * 0.075) - 169.44
    elif base_calculo <= 3751.05:
        irrf = (base_calculo * 0.15) - 381.44
    elif base_calculo <= 4664.68:
        irrf = (base_calculo * 0.225) - 662.77
    else:
        irrf = (base_calculo * 0.275) - 896.00
        
    return max(round(irrf, 2), 0.0)

def calcular_fgts(salario_bruto):
    """Calcula o FGTS (8%) apenas para referência, não é descontado."""
    return round(salario_bruto * 0.08, 2)