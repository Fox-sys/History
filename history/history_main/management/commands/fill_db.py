from django.core.management.base import BaseCommand
from ...models import MainUser
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = "Preparing database"

    def handle(self, *args, **kwargs):
        self.create_moder()
        self.create_admin()
        MainUser.objects.create_superuser(username="Fox", password="135790asz")
        # queryset = Permission.objects.all()
        # result = [i for i in queryset]
        # for i in result:
        #     print(f"{i.name} - {i.id}")

    def create_moder(self):
        try:
            Group.objects.get(name="Moder").delete()
        except:
            pass
        moder = Group(name="Moder")
        moder.save()
        for i in self.moder_permission_ids:
            moder.permissions.add(Permission.objects.get(id=i))
        moder.save()


    def create_admin(self):
        try:
            Group.objects.get(name="Admin").delete()
        except:
            pass
        admin = Group(name="Admin")
        admin.save()
        for i in self.admin_permission_ids:
            admin.permissions.add(Permission.objects.get(id=i))
        admin.save()        

    @property
    def moder_permission_ids(self):
        white_list = [4, 12, 8, 16, 28, 24, 32, 31, 30]        
        return white_list
        
    @property
    def admin_permission_ids(self):
        white_list = self.moder_permission_ids + [25, 26, 27, 23]
        return white_list