from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Formulário para entrada de dados do Contracheque
class ContrachequeForm(forms.Form):
    # ADICIONADO: Campo Nome Completo
    nome_completo = forms.CharField(label='Nome do Funcionário', max_length=150, required=True)
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
    email = forms.EmailField(label='E-mail')    # EmailField valida se o texto tem formato de e-mail.
    mensagem = forms.CharField(label='mensagem', max_length=300)

class CadastroForm(UserCreationForm):
    # Define o campo de email como obrigatório e com o rótulo correto
    email = forms.EmailField(label='E-mail', required=True) 

    
    class Meta:
        model = User
        # Mostra apenas E-mail e Primeiro Nome (além das senhas que já vêm no UserCreationForm)
        fields = ('email', 'first_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado. Tente fazer login.")
        return email

    def save(self, commit=True):
        # Pega os dados do formulário sem salvar ainda
        user = super().save(commit=False)
        # AQUI ESTÁ O TRUQUE: Copia o e-mail para o campo 'username'
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user