from django.contrib import admin
from .models import HistoricoCalculo

class HistoricoCalculoAdmin(admin.ModelAdmin):
    list_display = ('nome_funcionario', 'usuario', 'tipo', 'salario_base', 'resultado_liquido', 'data_calculo')
    list_filter = ('tipo', 'data_calculo')
    search_fields = ('nome_funcionario', 'usuario__username', 'usuario__email') # Adicionado busca por nome
    ordering = ('-data_calculo',)

    # --- Lógica de Segurança de Roles ---
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Se for superusuário ou Gestor, vê tudo
        if request.user.is_superuser or request.user.groups.filter(name='Gestores_RH').exists():
            return qs
        # Se for colaborador comum, só vê os seus próprios registros
        return qs.filter(usuario=request.user)

    def has_change_permission(self, request, obj=None):
        # Impede que colaboradores editem registros (histórico deve ser imutável para eles)
        if not request.user.is_superuser and not request.user.groups.filter(name='Gestores_RH').exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        # Impede que colaboradores deletem registros
        if not request.user.is_superuser and not request.user.groups.filter(name='Gestores_RH').exists():
            return False
        return True

admin.site.register(HistoricoCalculo, HistoricoCalculoAdmin)