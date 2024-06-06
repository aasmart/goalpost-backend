from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from goalpost_app import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'users', viewset=views.GoalpostUserViewSet, basename='users')

user_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
user_router.register(r'goals', views.GoalViewSet, basename="goals")

goal_router = routers.NestedSimpleRouter(user_router, r'goals', lookup="goal")
goal_router.register(r'reflections', views.GoalReflectionViewSet, basename="reflections")

urlpatterns = [
    path('', include(router.urls)),
    path('', include(user_router.urls)),
    path('', include(goal_router.urls))
]