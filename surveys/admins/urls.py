from django.urls import path
from surveys.admins import views as admin_views



urlpatterns = [
    path('', admin_views.SurveyListView.as_view(), name='SurveyListView'), # لیست نظرسنجی ها
    path('admin-detail/<str:slug>/', admin_views.DetailSurveyView.as_view(), name='DetailSurveyView'), # جواب های کاربران

    path('admin-create/', admin_views.AdminCrateSurveyView.as_view(), name='admin_create_survey'),
    path('admin-edit/<str:slug>/', admin_views.AdminEditSurveyView.as_view(), name='admin_edit_survey'),
    path('admin-delete/<str:slug>/', admin_views.AdminDeleteSurveyView.as_view(), name='admin_delete_survey'),
    path('admin-forms/<str:slug>/', admin_views.AdminSurveyFormView.as_view(), name='admin_forms_survey'),

    path('admin-question/add/<int:pk>/', admin_views.AdminCreateQuestionView.as_view(), name='admin_create_question'),
    path('admin-question/edit/<int:pk>/', admin_views.AdminUpdateQuestionView.as_view(), name='admin_edit_question'),
    path('admin-question/delete/<int:pk>/', admin_views.AdminDeleteQuestionView.as_view(), name='admin_delete_question'),
    path('admin-question/ordering/', admin_views.AdminChangeOrderQuestionView.as_view(), name='admin_change_order_question'),



    path('admin-download/<str:slug>/', admin_views.DownloadResponseSurveyView.as_view(), name='admin_download_survey'),

    path('admin-summary/<str:slug>/', admin_views.SummaryResponseSurveyView.as_view(), name='admin_summary_survey'),
]
