from django.urls import path
from.import views as v 
urlpatterns=[
    path('',v.index,name="homepage"),
    path('login/',v.login,name="registration/loginpage"),
    path('register/',v.registerr,name="registration/registerpage"),
    path('librarianindex/',v.librarianindex,name="librarian/librarianindex"),
    path('addbook/',v.addbook,name="librarian/addbook"),
    path('edit/<str:pk>',v.editbook,name="librarian/editbookpage"),
    path('userindex/',v.userindex,name="user/userindexpage"),
    #path('update/<str:pk>',v.updatedata,name="librarian/updatepage"),
    path('delete/<int:id>',v.deletedata,name="librarian/deletepage"),
]