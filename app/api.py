from rest_framework.routers import DefaultRouter
from . views import FundViewset,IncomeViewset,UserViewSet,ExpenceViewset,SourceViewSet,HomePageViewSet,YearlyViewSet
router = DefaultRouter()

router.register(r'user',UserViewSet,basename='user')
router.register(r'source',SourceViewSet,basename='source')
router.register(r'home',HomePageViewSet,basename='home')
router.register(r'income',IncomeViewset,basename='income')
router.register(r'fund',FundViewset,basename='fund')
router.register(r'expence',ExpenceViewset,basename='expence')
router.register(r'years',YearlyViewSet,basename='years')