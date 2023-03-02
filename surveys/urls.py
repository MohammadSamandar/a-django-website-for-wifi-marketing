from django.urls import path, include
from surveys import views
from surveys.app_settings import SURVEYS_ADMIN_BASE_PATH

app_name = 'surveys'
urlpatterns = [
    # path('list/', views.SurveyListView.as_view(), name='index'),
    # path('detail/<str:slug>/', views.DetailSurveyView.as_view(), name='detail'),
    path('detail/result/<int:pk>/', views.DetailResultSurveyView.as_view(), name='detail_result'),# نمایش نتیجه جوابی که کاربر به سوال نظر سنجی داده
    path('create/<str:slug>', views.CreateSurveyFormView.as_view(), name='create'),# صفحه سوال نظر سنجی
    path('', include('surveys.admins.urls')),

    path('edit/<int:pk>/', views.EditSurveyFormView.as_view(), name='edit'),# ویرایش یا اصلاح امتیازی که کاربر وارد کرده توسط خودش
    path('delete/<int:pk>/', views.DeleteSurveyAnswerView.as_view(), name='delete'),# حذف جواب های سوالات نظر سنجی
    path('share/<str:slug>/', views.share_link, name='share_link'),

]
