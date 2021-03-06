import graphene
from graphene_django.types import DjangoObjectType
from cookbook.ingredients.models import Category, Ingredient


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient

class Query(object):
    category = graphene.Field(
        CategoryType,
        id=graphene.Int(),
        name=graphene.String(),
        price=graphene.Int()
    )
    all_categories = graphene.List(CategoryType)
    all_ingredients = graphene.List(IngredientType)

    ingredient = graphene.Field(
        IngredientType,
        id=graphene.Int(),
        name=graphene.String(),
        price=graphene.Int()
    )

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_all_ingredients(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Ingredient.objects.select_related('category').all()

    def resolve_category(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')
        price = kwargs.get('price')

        if id is not None:
            return Category.objects.get(pk=id)

        if name is not None:
            return Category.objects.get(name=name)

        if price is not None:
            return Ingredient.objects.get(price=price)

        return None

    def resolve_ingredient(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')
        price = kwargs.get('price')

        if id is not None:
            return Ingredient.objects.get(pk=id)

        if name is not None:
            return Ingredient.objects.get(name=name)

        if price is not None:
            return Ingredient.objects.get(price=price)

        return None