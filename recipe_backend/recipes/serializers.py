
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

    def create(self, validated_data):
        """
        Overriden to raise a validation error if a user attempts to create more than
        one recipe.
        """
        owner = validated_data.get('owner')
        if hasattr(owner, 'recipe'):
            raise serializers.ValidationError(
                {'non_field_errors': ["User can only create a single recipe."]})
        return super(RecipeSerializer, self).create(validated_data)


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
