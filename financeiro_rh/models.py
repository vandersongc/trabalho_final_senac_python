from django.db import models
from django.contrib.auth.models import User

# O modelo HistoricoCalculo serve para persistir os cálculos realizados pelos usuários.
# Cada vez que um cálculo é feito, ele é salvo aqui.
class HistoricoCalculo(models.Model):
    # Opções para o campo 'tipo', limitando o que pode ser salvo no banco.
    TIPO_CHOICES = [
        ('contracheque', 'Contracheque'),
        ('rescisao', 'Rescisão'),
    ]

    # Vínculo com o usuário do sistema (chave estrangeira). Se o usuário for deletado, o histórico também é (CASCADE).
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Define qual foi o cálculo realizado.
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    
    # Data e hora exata em que o cálculo foi feito (auto_now_add preenche automaticamente).
    data_calculo = models.DateTimeField(auto_now_add=True)

    # ADICIONADO: Campo para salvar o nome de quem foi calculado
    nome_funcionario = models.CharField(max_length=150, default="Não Informado")
    
    # Armazena os valores monetários. DecimalField é mais preciso que FloatField para dinheiro.
    salario_base = models.DecimalField(max_digits=15, decimal_places=2)
    resultado_liquido = models.DecimalField(max_digits=15, decimal_places=2)

    # Representação em string do objeto (aparece assim no painel administrativo do Django).
    def __str__(self):
        return f"{self.usuario.username} - {self.tipo} - {self.data_calculo.strftime('%d/%m/%Y')}"