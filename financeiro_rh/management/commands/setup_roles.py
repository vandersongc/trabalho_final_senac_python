from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from financeiro_rh.models import HistoricoCalculo

class Command(BaseCommand):
    help = 'Configura os grupos de usuários e permissões iniciais'

    def handle(self, *args, **kwargs):
        # 1. Criar Grupo de Colaboradores (Usuários Comuns)
        grupo_colab, created = Group.objects.get_or_create(name='Colaboradores')
        
        # Obter o tipo de conteúdo do nosso modelo
        content_type = ContentType.objects.get_for_model(HistoricoCalculo)
        
        # Definir permissões: Pode adicionar e ver cálculos, mas não deletar ou alterar
        permissoes_colab = Permission.objects.filter(
            content_type=content_type,
            codename__in=['add_historicocalculo', 'view_historicocalculo']
        )
        
        grupo_colab.permissions.set(permissoes_colab)
        self.stdout.write(self.style.SUCCESS('Grupo "Colaboradores" configurado com sucesso!'))

        # 2. Criar Grupo de Gestores (RH)
        grupo_rh, created = Group.objects.get_or_create(name='Gestores_RH')
        
        # Gestores podem fazer tudo no histórico
        permissoes_rh = Permission.objects.filter(content_type=content_type)
        
        grupo_rh.permissions.set(permissoes_rh)
        self.stdout.write(self.style.SUCCESS('Grupo "Gestores_RH" configurado com sucesso!'))