import factory

from auth_app.factories import UserFactory

from .models import Offer, OfferDetail


class OfferFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Offer

    user = factory.SubFactory(UserFactory(type="business"))
    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph")


class OfferDetailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OfferDetail

    offer = factory.SubFactory(OfferFactory)
    title = factory.Faker("sentence", nb_words=3)
    revisions = factory.Faker("random_int", min=1, max=10)
    delivery_time_in_days = factory.Faker("random_int", min=1, max=30)
    price = factory.Faker("random_int", min=10, max=500)
    features = factory.List(["Logo", "Flyer"])
    offer_type = "basic"
