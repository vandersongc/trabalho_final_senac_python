# modelo para salvar o histórico de cálculos. Isso permitiria que o usuário visse cálculos passados.
#Atenção: Após salvar este arquivo, você precisará rodar os comandos no terminal para criar as tabelas no banco:

from django.db import models
from django.contrib.auth.models import User

class HistoricoCalculo(models.Model):
    TIPO_CHOICES = [
        ('contracheque', 'Contracheque'),
        ('rescisao', 'Rescisão'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    data_calculo = models.DateTimeField(auto_now_add=True)
    salario_base = models.DecimalField(max_digits=10, decimal_places=2)
    resultado_liquido = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.usuario.username} - {self.tipo} - {self.data_calculo.strftime('%d/%m/%Y')}"