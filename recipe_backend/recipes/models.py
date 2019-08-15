
from django.db import models

import django_filters
from django_filters.rest_framework import FilterSet


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    owner = models.OneToOneField('auth.User', on_delete=models.CASCADE,
                                 related_name='recipe')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class RecipeFilter(FilterSet):
    owner_username = django_filters.CharFilter(field_name='owner__username',
                                               lookup_expr='exact')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    name_exact = django_filters.CharFilter(field_name='name', lookup_expr='exact')
    
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'name_exact', 'owner_username']


class Ingredient(models.Model):
    text = models.TextField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='ingredients')

    def __str__(self):
        return self.text


class Step(models.Model):
    step_text = models.TextField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='steps')

    def __str__(self):
        return self.step_text
