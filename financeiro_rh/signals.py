from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

@receiver(post_save, sender=User)
def atribuir_grupo_padrao(sender, instance, created, **kwargs):
    if created:
        # Tenta pegar o grupo, se não existir (caso não tenha rodado o setup), não faz nada para não quebrar
        try:
            grupo = Group.objects.get(name='Colaboradores')
            instance.groups.add(grupo)
        except Group.DoesNotExist:
            pass