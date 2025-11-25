from django.contrib import admin
from .models import HistoricoCalculo

# Configuração para melhorar a visualização na lista do Admin
class HistoricoCalculoAdmin(admin.ModelAdmin):
    # Colunas que serão exibidas na tabela
    list_display = ('usuario', 'tipo', 'salario_base', 'resultado_liquido', 'data_calculo')
    
    # Filtros laterais para ajudar na busca
    list_filter = ('tipo', 'data_calculo')
    
    # Barra de pesquisa (busca pelo nome do usuário ou e-mail)
    search_fields = ('usuario__username', 'usuario__email')
    
    # Ordenação padrão (do mais recente para o mais antigo)
    ordering = ('-data_calculo',)

# Registra o modelo com a configuração acima
admin.site.register(HistoricoCalculo, HistoricoCalculoAdmin)