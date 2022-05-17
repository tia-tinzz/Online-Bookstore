from django.urls import path
from.import views as v 
urlpatterns=[
    path('',v.Index.as_view(),name="homepage"),
    path('login/',v.LoginView.as_view(),name="registration/loginpage"),
    path('logout/',v.LogoutView.as_view(),name="registration/logout"),
    path('register/',v.RegisterView.as_view(),name="registration/registerpage"),
    path('librarianindex/',v.LibrarianIndexView.as_view(),name="librarian/librarianindex"),
    path('addbook/',v.AddBook.as_view(),name="librarian/addbook"),
    path('edit/<str:pk>',v.EditBook.as_view(),name="librarian/editbookpage"),
    path('userindex/',v.UserIndexView.as_view(),name="user/userindexpage"),
    #path('update/<str:pk>',v.updatedata,name="librarian/updatepage"),
    #path('delete/<int:pk>',v.deletedata,name="librarian/deletepage"),
    path('delete/<str:pk>',v.DeleteDataView.as_view(),name="librarian/deletepage"),
    path('checkout', v.checkout, name="user/checkout"),
    path('success', v.success, name='success'),
    path('cancel', v.cancel, name='cancel'),
    path('checkoutsub', v.checkoutsubscription, name="user/checkoutsubscription"),
    path('seeplan', v.joinplan, name="user/subscriptionplan"),
    path('cancelsubscription', v.cancelsubscription, name='user/cancelsubscription'),
    path('successsub', v.successsubscription, name='user/subscriptionsuccess'),
    path('pausesubscription', v.pausesubscription, name='user/pausesubscription'),
    path('resumesubscription', v.resumesubscription, name='user/resumesubscription'),
    path('updatesubscription',v.updatesubscription,name='user/updatesubscription'),
    
]
