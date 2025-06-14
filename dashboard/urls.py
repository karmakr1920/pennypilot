from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('all-expenses/', views.expense_list, name='expense_list'),
    path('expense-report/', views.report_view, name='expense_report'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('<int:exp_id>/update-expense/', views.update_expense, name='update_expense'),
    path('<int:exp_id>/delete-expense/', views.delete_expense, name='delete_expense'),
    path('report/', views.report_view, name='report'),
    path('set-budget/', views.set_monthly_budget, name='set_monthly_budget'),

    # Auth-related
    path('register/', views.register_view, name='register'),
    path('update-user/', views.update_user_view, name='update_user'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
