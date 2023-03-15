from rest_framework import viewsets,permissions,status
from rest_framework.response import Response
from . serializers import IncomeSerializer,ExpenceSerializer,UserSerializer,FundSerializer,SourceSerializer,YearReport
from . models import Report,User,Source
from datetime import datetime
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        data = Source.objects.filter(user = request.user)
        serializer = self.get_serializer(data,many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class HomePageViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def list(self,request,*args,**kwargs):
        month_report = Report.filters.tottal_month_report(user = request.user)
        day_report = Report.filters.today_report(user = request.user)
        tottal_loan = Report.filters.tottal_loan(user = request.user)
        tottal_fund = Report.filters.tottal_fund(user = request.user)
        amount = Report.filters.final_income(user = request.user)
        data = {
            'month_income':month_report.get('income'),
            'month_expence':month_report.get('expence'),
            'day_income':day_report.get('income'),
            'day_expence':day_report.get('expence'),
            'loan':tottal_loan.get('sum_loan'),
            'fund':tottal_fund.get('fund'),
            'final_income':amount.get('amount')
        }
        return Response(data,status=status.HTTP_200_OK)

class IncomeViewset(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self,request,*args,**kwargs):
        income_list = Report.filters.filter_this_month_income(user = request.user,year = request.GET.get('year',None),month=request.GET.get('month',None))
        serizlizer = self.get_serializer(income_list,many = True)
        data = {}
        data['items'] = serizlizer.data
        data['income'] = (Report.filters.tottal_month_report(user = request.user,year = request.GET.get('year',None),month=request.GET.get('month',None),income=Report.INCOME))
        return Response(data,status=status.HTTP_200_OK)
    
class ExpenceViewset(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ExpenceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self,request,*args,**kwargs):
        income_list = Report.filters.filter_this_month_expence(user = request.user,year = request.GET.get('year',None),month=request.GET.get('month',None))
        serizlizer = self.get_serializer(income_list, many = True)
        data = {}
        data['items'] = serizlizer.data
        data['expence'] = (Report.filters.tottal_month_report(user = request.user,year = request.GET.get('year',None),month=request.GET.get('month',None),expence=Report.EXPENSE))
        return Response(data,status=status.HTTP_200_OK)


class FundViewset(viewsets.ModelViewSet):
    queryset = []
    serializer_class = FundSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self,request,*args,**kwargs):
        income_list = Report.filters.filter_this_month_fund(user = request.user,year = request.GET.get('year',None),month=request.GET.get('month',None))
        serizlizer = self.get_serializer(income_list, many = True)
        data = {}
        data['items'] = serizlizer.data
        data['fund'] = Report.filters.tottal_fund(user = request.user)
        return Response(data,status=status.HTTP_200_OK)

class YearlyViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def list(self,request,*args,**kwargs):
        data = Report.filters.year_report(user = request.user,year = request.GET.get('year',None))
        serializer = YearReport(data,many = True)
        data = {}
        data['items'] = serializer.data
        data['year'] = request.GET.get('year') if request.GET.get('year') else datetime.now().year
        return Response(data)

