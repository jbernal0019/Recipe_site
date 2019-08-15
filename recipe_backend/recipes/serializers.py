
from rest_framework import serializers

from .models import Recipe
from .models import Step
from .models import Ingredient


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    ingredients = serializers.HyperlinkedIdentityField(view_name='ingredient-list')
    steps = serializers.HyperlinkedIdentityField(view_name='step-list')
    owner = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
    
    class Meta:
        model = Recipe
        fields = ('url', 'id', 'name', 'owner_username', 'ingredients', 'steps', 'owner')


class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    recipe = serializers.HyperlinkedRelatedField(view_name='recipe-detail',
                                                 read_only=True)

    class Meta:
        model = Ingredient
        fields = ('url', 'id', 'text', 'recipe')


class StepSerializer(serializers.HyperlinkedModelSerializer):
    recipe = serializers.HyperlinkedRelatedField(view_name='recipe-detail',
                                                 read_only=True)

    class Meta:
        model = Step
        fields = ('url', 'id', 'step_text', 'recipe')
