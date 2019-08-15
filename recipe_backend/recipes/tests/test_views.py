
import json
from unittest import mock

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status

from recipes.models import Recipe
from recipes.models import Ingredient
from recipes.models import Step


class ViewTests(TestCase):
    
    def setUp(self):
        self.username = 'foo'
        self.password = 'foopassword'
        self.email = 'dev@server.org'
        self.recipe_name = 'recipe1'
        self.content_type = 'application/vnd.collection+json'

        # create basic models

        # create a user
        user = User.objects.create_user(username=self.username,
                                        email=self.email,
                                        password=self.password)

        # create another  user
        User.objects.create_user(username='another', email='another@server.org',
                                 password='another-pass')

        # create a recipe
        Recipe.objects.get_or_create(name=self.recipe_name, owner=user)


class RecipeListViewTests(ViewTests):
    """
    Test the recipe-list view.
    """

    def setUp(self):
        super(RecipeListViewTests, self).setUp()
        self.create_read_url = reverse("recipe-list")
        self.post = json.dumps({
            "template": {"data": [{"name": "name", "value": "another_recipe"}]}})

    def test_recipe_create_success(self):
        self.client.login(username='another', password='another-pass')
        response = self.client.post(self.create_read_url, data=self.post,
                                    content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_recipe_create_failure_unauthenticated(self):
        response = self.client.post(self.create_read_url, data=self.post,
                                    content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_recipe_list_success_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.create_read_url)
        self.assertContains(response, self.recipe_name)

    def test_plugin_list_success_unauthenticated(self):
        response = self.client.get(self.create_read_url)
        self.assertContains(response, self.recipe_name)


class RecipeDetailViewTests(ViewTests):
    """
    Test the recipe-detail view.
    """

    def setUp(self):
        super(RecipeDetailViewTests, self).setUp()

        recipe = Recipe.objects.get(name=self.recipe_name)
        self.read_update_delete_url = reverse("recipe-detail", kwargs={"pk": recipe.id})
        self.put = json.dumps({
            "template": {"data": [{"name": "name", "value": "another_recipe"}]}})

    def test_recipe_detail_success_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.read_update_delete_url)
        self.assertContains(response, self.recipe_name)

    def test_recipe_detail_success_unauthenticated(self):
        response = self.client.get(self.read_update_delete_url)
        self.assertContains(response, self.recipe_name)

    def test_recipe_update_success(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.put(self.read_update_delete_url, data=self.put,
                                   content_type=self.content_type)
        self.assertContains(response, "another_recipe")

    def test_recipe_update_failure_unauthenticated(self):
        response = self.client.put(self.read_update_delete_url, data=self.put,
                                   content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_recipe_update_failure_access_denied(self):
        self.client.login(username='another', password='another-pass')
        response = self.client.put(self.read_update_delete_url, data=self.put,
                                   content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_recipe_delete_success(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.delete(self.read_update_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Recipe.objects.count(), 0)

    def test_recipe_delete_failure_unauthenticated(self):
        response = self.client.delete(self.read_update_delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_recipe_delete_failure_access_denied(self):
        self.client.login(username='another', password='another-pass')
        response = self.client.delete(self.read_update_delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class RecipeListQuerySearchViewTests(ViewTests):
    """
    Test the recipe-list-query-search view.
    """

    def setUp(self):
        super(RecipeListQuerySearchViewTests, self).setUp()
        self.list_url = reverse("recipe-list-query-search") + '?owner_username=' + self.username

    def test_recipe_list_query_search_success_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.list_url)
        self.assertContains(response, self.username)
        self.assertContains(response, self.recipe_name)

    def test_plugin_list_query_search_success_unauthenticated(self):
        response = self.client.get(self.list_url)
        self.assertContains(response, self.username)
        self.assertContains(response, self.recipe_name)


class IngredientListViewTests(ViewTests):
    """
    Test the ingredient-list view.
    """

    def setUp(self):
        super(IngredientListViewTests, self).setUp()

        recipe = Recipe.objects.get(name=self.recipe_name)
        self.create_read_url = reverse("ingredient-list", kwargs={"pk": recipe.id})
        self.text = "Great ingredient"
        self.post = json.dumps({
            "template": {"data": [{"name": "text", "value": self.text}]}})

        # add ingredient :-)
        Ingredient.objects.get_or_create(recipe=recipe, text=self.text)

    def test_ingredient_create_success(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(self.create_read_url, data=self.post,
                                    content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_ingredient_create_failure_unauthenticated(self):
        response = self.client.post(self.create_read_url, data=self.post,
                                    content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ingredient_create_failure_access_denied(self):
        self.client.login(username='another', password='another-pass')
        response = self.client.post(self.create_read_url, data=self.post,
                                   content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_ingredient_list_success_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.create_read_url)
        self.assertContains(response, self.text)

    def test_ingredient_list_success_unauthenticated(self):
        response = self.client.get(self.create_read_url)
        self.assertContains(response, self.text)


class IngredientDetailViewTests(ViewTests):
    """
    Test the ingredient-detail view.
    """

    def setUp(self):
        super(IngredientDetailViewTests, self).setUp()

        # add ingredient :-)
        recipe = Recipe.objects.get(name=self.recipe_name)
        self.text = "Great ingredient"
        (ingredient, tf) = Ingredient.objects.get_or_create(recipe=recipe,
                                                            text=self.text)

        self.read_update_delete_url = reverse("ingredient-detail",
                                              kwargs={"pk": ingredient.id})
        self.update_text = "Another great ingredient"
        self.put = json.dumps({
            "template": {"data": [{"name": "text", "value": self.update_text}]}})

    def test_ingredient_detail_success_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.read_update_delete_url)
        self.assertContains(response, self.text)

    def test_ingredient_detail_success_unauthenticated(self):
        response = self.client.get(self.read_update_delete_url)
        self.assertContains(response, self.text)

    def test_ingredient_update_success(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.put(self.read_update_delete_url, data=self.put,
                                   content_type=self.content_type)
        self.assertContains(response, self.update_text)

    def test_ingredient_update_failure_unauthenticated(self):
        response = self.client.put(self.read_update_delete_url, data=self.put,
                                   content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ingredient_update_failure_access_denied(self):
        self.client.login(username='another', password='another-pass')
        response = self.client.put(self.read_update_delete_url, data=self.put,
                                   content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_ingredient_delete_success(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.delete(self.read_update_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ingredient.objects.count(), 0)

    def test_ingredient_delete_failure_unauthenticated(self):
        response = self.client.delete(self.read_update_delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ingredient_delete_failure_access_denied(self):
        self.client.login(username='another', password='another-pass')
        response = self.client.delete(self.read_update_delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class StepListViewTests(ViewTests):
    """
    Test the step-list view.
    """

    def setUp(self):
        super(StepListViewTests, self).setUp()

        recipe = Recipe.objects.get(name=self.recipe_name)
        self.create_read_url = reverse("step-list", kwargs={"pk": recipe.id})
        self.text = "Great step"
        self.post = json.dumps({
            "template": {"data": [{"name": "step_text", "value": self.text}]}})

        # add step
        Step.objects.get_or_create(recipe=recipe, step_text=self.text)

    def test_step_create_success(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(self.create_read_url, data=self.post,
                                    content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_step_create_failure_unauthenticated(self):
        response = self.client.post(self.create_read_url, data=self.post,
                                    content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_step_create_failure_access_denied(self):
        self.client.login(username='another', password='another-pass')
        response = self.client.post(self.create_read_url, data=self.post,
                                   content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_step_list_success_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.create_read_url)
        self.assertContains(response, self.text)

    def test_step_list_success_unauthenticated(self):
        response = self.client.get(self.create_read_url)
        self.assertContains(response, self.text)


class StepDetailViewTests(ViewTests):
    """
    Test the step-detail view.
    """

    def setUp(self):
        super(StepDetailViewTests, self).setUp()

        # add step
        recipe = Recipe.objects.get(name=self.recipe_name)
        self.text = "Great step"
        (step, tf) = Step.objects.get_or_create(recipe=recipe, step_text=self.text)

        self.read_update_delete_url = reverse("step-detail",  kwargs={"pk": step.id})
        self.update_text = "Another great step"
        self.put = json.dumps({
            "template": {"data": [{"name": "step_text", "value": self.update_text}]}})

    def test_step_detail_success_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.read_update_delete_url)
        self.assertContains(response, self.text)

    def test_step_detail_success_unauthenticated(self):
        response = self.client.get(self.read_update_delete_url)
        self.assertContains(response, self.text)

    def test_step_update_success(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.put(self.read_update_delete_url, data=self.put,
                                   content_type=self.content_type)
        self.assertContains(response, self.update_text)

    def test_step_update_failure_unauthenticated(self):
        response = self.client.put(self.read_update_delete_url, data=self.put,
                                   content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_step_update_failure_access_denied(self):
        self.client.login(username='another', password='another-pass')
        response = self.client.put(self.read_update_delete_url, data=self.put,
                                   content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_step_delete_success(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.delete(self.read_update_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ingredient.objects.count(), 0)

    def test_step_delete_failure_unauthenticated(self):
        response = self.client.delete(self.read_update_delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_step_delete_failure_access_denied(self):
        self.client.login(username='another', password='another-pass')
        response = self.client.delete(self.read_update_delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
