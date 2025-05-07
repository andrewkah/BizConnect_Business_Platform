
from django import urls
from django.urls import path , include
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
  ######### These are the landing pages ##############
  path('', views.indexPage, name ='index'),
  path('about/', views.about, name = 'about'),
  path('service/', views.service, name = 'service'),
  path('service_details/', views.service_detail, name = 'service_details'),
  path('get_started/', views.get_startednow, name = 'get_started'),
  path("membership/", views.after_register, name="after_register"),
  
  ######### These are the entrepreneurs' urls ############
  path('dashboard/', views.homepage1, name = 'homepage1'),
  path('entrepreneur/ideals/', views.business_ideals, name = 'business_ideals'),
  path("entrepreneur/ideal/form/", views.business_ideal_form , name="business_ideal_form"),
  path("entrepreneur/requests/", views.service_requests, name="service_requests"),
  path("entrepreneur/requests/form/", views.service_request_form, name="expert_request_form"),
  path("entrepreneur/schedule/", views.consultation_schedule, name="consultation_schedule"),
  path("entrepreneur/schedule/form/<int:request_id>/", views.consultation_schedule_form, name="consultation_schedule_form"),
  
  path("entrepreneur/investment/deals/", views.investment_deals, name="investment_deals"),
  path("entrepreneur/investment/deals/form/", views.investment_deal_form, name="investment_deal_form"),
  
  ######### These are the Investors' urls ###############
  path("investor/fundings/", views.investment_fundings, name="investment_fundings"),
  path("investor/funding/form/<int:deal_id>/", views.investment_funding_form, name="investment_funding_form"),
  path('submit-investor/', views.submit_investor_form, name='submit_investor_form'),
  path('investors/investor_deals/', views.investor_deals, name='investor_deals'),
  path('business_idea/<int:idea_id>/', views.businessidea_detail, name='businessidea_detail'),
  ######### These are the Experts' urls ##############
  path('expert/library/', views.resources, name = 'resources'),
  path("expert/library/form/", views.resource_form, name="resource_form"),
  path("expert/requests/", views.assistance_request, name="assistance_request"),
  path("expert/consultation/", views.consultation_packages, name="consultation_packages"),
  path("expert/consultation/form/", views.consultation_package_form, name="consultation_package_form"),
  path("expert/feedback/", views.feedback, name="feedback"),
  
  ######### These are the Registration urls ################
  path('membership/entrepreneurs/', views.register_entrepreneur, name = 'register_entrepreneurs'),
  path('membership/investors/', views.register_investor, name='register_investors'),
  path('membership/experts/', views.register_expert, name='register_experts'),
  path('register/',  views.registration_form, name='registration_form'),
  path('register_expert/', views.register_expert, name='register_expert'),
  
  ######### These are the Login urls ################
  path('login/', views.login2, name ='login'),
  path('logout/', views.logout_view, name='logout'),
  path('loginForm/', views.custom_login, name='custom_login'),

 
  path('submit_service_request/', views.submit_service_request, name='submit_service_request'),
  path("submit_investment_deal/", views.create_investment_deal, name="create_investment_deal"),


  ######### These are admin urls ################
  path('tables/', views.allTables, name='allTables'),
  path('loginAdmin/', views.loginAdmin, name='loginAdmin'),
  path('logoutAdmin/', views.logout2, name='logout2'),
  path('admin_dashboard/', views.admin2, name='admin_dashboard'),
  path('charts/', views.charts, name='charts'),
  path("business_proposals/", views.admin_proposals, name="admin_proposals"),
  path("assistance_requests/", views.admin_requests, name="admin_assistance_requests"),
  path("meetings/", views.admin_meetings, name="admin_meetings"),
  path("investment_deals/", views.admin_investment_deals, name="admin_investment_deals"),
  path("investment_funds/", views.admin_investment_funds, name="admin_investment_funds"),
  path("packages/", views.admin_packages, name="admin_packages"),
  path("reply/", views.admin_reply_mail, name="admin_reply_mail"),
  path('tables/data/', views.table_data, name='data_tables'),
  path("users/entrepreneurs/", views.admin_users_entr, name="users_entr"),
  path("users/experts/", views.admin_users_expert, name="users_expert"),
  path("users/investors/", views.admin_users_investor, name="users_investor"),
  path("forms/general/", views.general_forms, name="general_forms"),
  path("forms/advanced/", views.advanced_forms, name="advanced_forms"),
  path("forms/validation/", views.validation_forms, name="validation_forms"),
  path('mailbox/', views.mailbox, name='mailbox'),
  path('mail/compose/', views.compose_mail, name='compose_mail'),
  path('mail/read/', views.read_mail, name='read_mail'),
  path("calendar/", views.admin_calendar, name="calendar"),
  path("gallery/", views.admin_gallery, name="gallery"),
  path('approve_request/<int:request_id>/', views.approve_request, name='approve_request'),
  path('create_package/', views.create_consultation_package, name='create_package'),

  path('schedule_meeting/<int:request_id>/', views.schedule_meeting4theent, name='schedule_meeting'),


  path('update-meeting-status/<int:meeting_id>/<str:status>/', views.update_meeting_status, name='update_meeting_status'),


  path('reply-requests/', views.replay_requests_made, name='replay_requests'),
  path('reply_madenow/', views.replay_requests_madetothemeeting, name='replay_requests_madetothemeeting'),


 path('forward_request/<int:request_id>/', views.forward_request, name='forward_request'),
]
