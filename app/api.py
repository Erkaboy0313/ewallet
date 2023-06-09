from rest_framework.routers import SimpleRouter,DefaultRouter
from . views import FundViewset,IncomeViewset,UserViewSet,ExpenceViewset,SourceViewSet,ExpenceSourceViewSet,HomePageViewSet,YearlyViewSet
from django.conf import settings

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(r'user',UserViewSet,basename='user')
router.register(r'source',SourceViewSet,basename='source')
router.register(r'expencesource',ExpenceSourceViewSet,basename='expencesource')
router.register(r'home',HomePageViewSet,basename='home')
router.register(r'income',IncomeViewset,basename='income')
router.register(r'fund',FundViewset,basename='fund')
router.register(r'expence',ExpenceViewset,basename='expence')
router.register(r'years',YearlyViewSet,basename='years')