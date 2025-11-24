from django import forms

# Formulário para entrada de dados do Contracheque
class ContrachequeForm(forms.Form):
    # DecimalField garante que o usuário digite um número válido.
    venc_salario = forms.DecimalField(label='Salário Base', min_value=0, decimal_places=2)

# Formulário para cálculo de Rescisão
class RescisaoForm(forms.Form):
    # DateField gera a validação de datas. No HTML, usaremos type="date".
    data_admissao = forms.DateField(label='Data Admissão')
    data_demissao = forms.DateField(label='Data Demissão')
    
    # ChoiceField cria um menu de seleção (dropdown) com as opções de desligamento.
    motivo = forms.ChoiceField(choices=[
        ('sem_justa_causa', 'Dispensa sem Justa Causa'),
        ('pedido_demissao', 'Pedido de Demissão'),
        ('justa_causa', 'Por Justa Causa')
    ])
    ultimo_salario = forms.DecimalField(label='Último Salário', min_value=0, decimal_places=2)

# Formulário simples de Contato
class ContatoForm(forms.Form):
    name = forms.CharField(label='Nome', max_length=100)
    email = forms.EmailField(label='E-mail') # EmailField valida se o texto tem formato de e-mail.