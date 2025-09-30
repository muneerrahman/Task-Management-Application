from.import views
from django.urls import path
from .views import TaskListView, TaskUpdateView, TaskReportView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [
    # API views
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:pk>/report/', TaskReportView.as_view(), name='task-report'),   

    # Template views
    path('tasks/task_list_web/', views.task_list_view, name='task-list-web'),
    path('tasks/task_detail_web/<int:pk>/', views.task_detail_view, name='task-detail-web'),
    path('tasks/task_report_web/<int:pk>/report/', views.task_report_view, name='task-report-web'),

    # SuperAdmin URLs for admin
    path('superadmin/create-user/', views.superadmin_create_user, name='superadmin_create_user'),
    path('superadmin/admins/', views.superadmin_admin_list, name='superadmin_admin_list'),
    path('superadmin/edit-admin/<int:admin_id>/', views.superadmin_edit_admin, name='superadmin_edit_admin'),
    path('superadmin/delete-admin/<int:admin_id>/', views.superadmin_delete_admin, name='superadmin_delete_admin'),
    # SuperAdmin URLs for users
    path('superadmin/users/', views.superadmin_user_list, name='superadmin_user_list'),
    path('superadmin/assign-user/', views.superadmin_assign_user_to_admin, name='superadmin_assign_user'),
    path('superadmin/edit-user/<int:user_id>/', views.superadmin_edit_user, name='superadmin_edit_user'),
    path('superadmin/delete-user/<int:user_id>/', views.superadmin_delete_user, name='superadmin_delete_user'),


    # Admin URLs
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/task-delete/<int:task_id>/', views.admin_task_delete, name='admin_task_delete'),
    
    # JWT Authentication Routes
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
]