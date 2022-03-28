from django.urls import path
from.import views as v 
urlpatterns=[
    path('',v.Index.as_view(),name="homepage"),
    path('login/',v.LoginView.as_view(),name="registration/loginpage"),
    path('register/',v.RegisterView.as_view(),name="registration/registerpage"),
    path('librarianindex/',v.LibrarianIndexView.as_view(),name="librarian/librarianindex"),
    path('addbook/',v.AddBook.as_view(),name="librarian/addbook"),
    path('edit/<str:pk>',v.editbook,name="librarian/editbookpage"),
    path('userindex/',v.UserIndexView.as_view(),name="user/userindexpage"),
    #path('update/<str:pk>',v.updatedata,name="librarian/updatepage"),
    path('delete/<int:id>',v.deletedata,name="librarian/deletepage"),
]