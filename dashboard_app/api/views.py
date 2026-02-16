from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.db.models.functions import Round
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from offers_app.models import Offer
from reviews_app.models import Review

User = get_user_model()


@api_view()
@permission_classes([AllowAny])
def base_info_view(request):
    data = {}
    data["review_count"] = Review.objects.all().count()
    data["average_rating"] = Review.objects.aggregate(
        average_rating=Round(Avg("rating", default=0), precision=1)
    )["average_rating"]

    data["business_profile_count"] = User.objects.filter(
        type="business"
    ).count()
    data["offer_count"] = Offer.objects.all().count()

    return JsonResponse(data)
