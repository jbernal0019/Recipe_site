
from django.conf.urls import url, include

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from recipes import views as recipe_views
from users import views as user_views

# API v1 endpoints
urlpatterns = format_suffix_patterns([

    url(r'^v1/auth-token/$',
        obtain_auth_token),

    url(r'^v1/users/$',
        user_views.UserCreate.as_view(), name='user-create'),

    url(r'^v1/users/(?P<pk>[0-9]+)/$',
        user_views.UserDetail.as_view(), name='user-detail'),


    url(r'^v1/$',
        recipe_views.RecipeList.as_view(), name='recipe-list'),

    url(r'^v1/search/$',
        recipe_views.RecipeListQuerySearch.as_view(), name='recipe-list-query-search'),

    url(r'^v1/(?P<pk>[0-9]+)/$',
        recipe_views.RecipeDetail.as_view(), name='recipe-detail'),

    url(r'^v1/(?P<pk>[0-9]+)/ingredients/$',
        recipe_views.IngredientList.as_view(), name='ingredient-list'),

    url(r'^v1/ingredients/(?P<pk>[0-9]+)/$',
        recipe_views.IngredientDetail.as_view(), name='ingredient-detail'),

    url(r'^v1/(?P<pk>[0-9]+)/steps/$',
        recipe_views.StepList.as_view(), name='step-list'),

    url(r'^v1/steps/(?P<pk>[0-9]+)/$',
        recipe_views.StepDetail.as_view(), name='step-detail'),

])

# Login and logout views for Djangos' browsable API
urlpatterns += [
    url(r'^v1/auth/', include('rest_framework.urls',  namespace='rest_framework')),
]
