
from rest_framework import generics, permissions
from rest_framework.reverse import reverse

from collectionjson import services

from .models import Recipe, RecipeFilter
from .models import Step
from .models import Ingredient
from .serializers import RecipeSerializer
from .serializers import StepSerializer
from .serializers import IngredientSerializer
from .permissions import IsOwnerOrReadOnly, IsRecipeOwnerOrReadOnly


class RecipeList(generics.ListCreateAPIView):
    """
    A view for the collection of recipes.
    """
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        """
        Overriden to associate an owner with the recipe.
        """
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        """
        Overriden to append a document-level link relation, a query list and a
        collection+json template to the response.
        """
        response = super(RecipeList, self).list(request, *args, **kwargs)
        # append document-level link relations
        user = self.request.user
        if user.is_authenticated:
            links = {'user': reverse('user-detail', request=request,
                                     kwargs={"pk": user.id})}
            response = services.append_collection_links(response, links)
        # append query list
        query_list = [reverse('recipe-list-query-search', request=request)]
        response = services.append_collection_querylist(response, query_list)
        # append write template
        template_data = {'name': ''}
        return services.append_collection_template(response, template_data)


class RecipeListQuerySearch(generics.ListAPIView):
    """
    A view for the collection of recipes resulting from a query search.
    """
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    filterset_class = RecipeFilter
        

class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    A recipe view.
    """
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        """
        Overriden to append a collection+json template.
        """
        response = super(RecipeDetail, self).retrieve(request, *args, **kwargs)
        template_data = {'name': ''}
        return services.append_collection_template(response, template_data)


class IngredientList(generics.ListCreateAPIView):
    """
    A view for the collection of recipe-specific ingredients.
    """
    serializer_class = IngredientSerializer
    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        """
        Overriden to associate a recipe with the newly created ingredient.
        """
        recipe = self.get_object()
        serializer.save(recipe=recipe)

    def list(self, request, *args, **kwargs):
        """
        Overriden to return the list of ingredients for the queried recipe.
        A document-level link relation and a collection+json template are also added
        to the response.
        """
        queryset = self.get_ingredients_queryset()
        response = services.get_list_response(self, queryset)
        recipe = self.get_object()
        # append document-level link relations
        links = {'recipe': reverse('recipe-detail', request=request,
                                   kwargs={"pk": recipe.id})}
        response = services.append_collection_links(response, links)
        # append write template
        template_data = {'text': ""}
        return services.append_collection_template(response, template_data)

    def get_ingredients_queryset(self):
        """
        Custom method to get the actual ingredients' queryset.
        """
        recipe = self.get_object()
        return self.filter_queryset(recipe.ingredients.all())

    
class IngredientDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    An ingredient view.
    """
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = (IsRecipeOwnerOrReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        """
        Overriden to append a collection+json template.
        """
        response = super(IngredientDetail, self).retrieve(request, *args, **kwargs)
        template_data = {'text': ''}
        return services.append_collection_template(response, template_data)


class StepList(generics.ListCreateAPIView):
    """
    A view for the collection of recipe-specific steps.
    """
    serializer_class = StepSerializer
    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        """
        Overriden to associate a recipe with the newly created step.
        """
        recipe = self.get_object()
        serializer.save(recipe=recipe)

    def list(self, request, *args, **kwargs):
        """
        Overriden to return the list of steps for the queried recipe.
        A document-level link relation and a collection+json template are also added
        to the response.
        """
        queryset = self.get_steps_queryset()
        response = services.get_list_response(self, queryset)
        recipe = self.get_object()
        # append document-level link relations
        links = {'recipe': reverse('recipe-detail', request=request,
                                   kwargs={"pk": recipe.id})}
        response = services.append_collection_links(response, links)
        # append write template
        template_data = {'step_text': ""}
        return services.append_collection_template(response, template_data)

    def get_steps_queryset(self):
        """
        Custom method to get the actual steps' queryset.
        """
        recipe = self.get_object()
        return self.filter_queryset(recipe.steps.all())


class StepDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    An step view.
    """
    serializer_class = StepSerializer
    queryset = Step.objects.all()
    permission_classes = (IsRecipeOwnerOrReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        """
        Overriden to append a collection+json template.
        """
        response = super(StepDetail, self).retrieve(request, *args, **kwargs)
        template_data = {'step_text': ''}
        return services.append_collection_template(response, template_data)
