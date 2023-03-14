from rest_framework import viewsets,permissions,status
from rest_framework.response import Response
from . serializers import IncomeSerializer,ExpenceSerializer,UserSerializer,FundSerializer,SourceSerializer,YearReport
from . models import Report,User,Source
from rest_framework.decorators import action
from django.db.models.functions import TruncMonth
from django.db import models
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    # http_method_names = ['get','delete']

class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    permission_classes = (permissions.AllowAny,)

class HomePageViewSet(viewsets.ViewSet):

    def list(self,request,*args,**kwargs):
        month_report = Report.filters.tottal_month_report()
        day_report = Report.filters.today_report()
        tottal_loan = Report.filters.tottal_loan()
        tottal_fund = Report.filters.tottal_fund()
        data = {
            'month_income':month_report.get('income'),
            'month_expence':month_report.get('expence'),
            'day_income':day_report.get('income'),
            'day_expence':day_report.get('expence'),
            'loan':tottal_loan.get('sum_loan'),
            'fund':tottal_fund.get('fund'),
        }
        return Response(data,status=status.HTTP_200_OK)

class IncomeViewset(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = (permissions.AllowAny,)

    def list(self,request,*args,**kwargs):
        income_list = Report.filters.filter_this_month_income(year = request.data.get('year',None),month=request.data.get('month',None))
        serizlizer = self.get_serializer(income_list,many = True)
        data = {}
        data['items'] = serizlizer.data
        data['income'] = (Report.filters.tottal_month_report(year = request.data.get('year',None),month=request.data.get('month',None),income=Report.INCOME))
        return Response(data,status=status.HTTP_200_OK)
    
class ExpenceViewset(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ExpenceSerializer
    permission_classes = (permissions.AllowAny,)

    def list(self,request,*args,**kwargs):
        income_list = Report.filters.filter_this_month_expence(year = request.data.get('year',None),month=request.data.get('month',None))
        serizlizer = self.get_serializer(income_list, many = True)
        data = {}
        data['items'] = serizlizer.data
        data['expence'] = (Report.filters.tottal_month_report(year = request.data.get('year',None),month=request.data.get('month',None),expence=Report.EXPENSE))
        return Response(data,status=status.HTTP_200_OK)


class FundViewset(viewsets.ModelViewSet):
    queryset = []
    serializer_class = FundSerializer
    permission_classes = (permissions.AllowAny,)

    def list(self,request,*args,**kwargs):
        income_list = Report.filters.filter_this_month_fund(year = request.data.get('year',None),month=request.data.get('month',None))
        serizlizer = self.get_serializer(income_list, many = True)
        data = serizlizer.data
        data.append(Report.filters.tottal_fund())
        return Response(data,status=status.HTTP_200_OK)

class YearlyViewSet(viewsets.ViewSet):

    def list(self,request,*args,**kwargs):
        data = Report.filters.year_report(request.data.get('year',None))
        serializer = YearReport(data,many = True)
        return Response(serializer.data)