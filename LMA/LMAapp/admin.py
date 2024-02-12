from django.contrib import admin
from .models import User_details, Book_details, Res_fin_details,purchase

class UserAdmin(admin.ModelAdmin):
    list_display = ['User_Id', 'UserType', 'UserName', 'Gender', 'DateofBirth', 'Address', 'PhoneNumber', 'EmailId']
    ordering = ('UserName',)  # Specify the field(s) you want to use for ordering
    search_fields = ('UserName', 'EmailId')

class BookAdmin(admin.ModelAdmin):
    Booklist_display=['Book_Id','Book_Title','Auther','Image','Publication','Edition','Price','Date','Quantity','Status']
   # ordering=('UserName')
    search_fields=('Book_Id','Book_Title')
admin.site.register(Book_details,BookAdmin)

class fine(admin.ModelAdmin):
    listreturn=['User_Id','Book_Id','Date_issue','Date_return','fine','status']
   # ordering=('UserName')
    search_fields=('User_Id',)
admin.site.register(Res_fin_details,fine)

class purchas(admin.ModelAdmin):
    list=['User_Id','Book_Id','Date_issue','Date_return','fine','status']
   # ordering=('UserName')
    search_fields=('User_Id',)
admin.site.register(purchase,purchas)

