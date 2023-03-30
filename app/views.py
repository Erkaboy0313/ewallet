from rest_framework import viewsets,permissions,status
from rest_framework.response import Response
from . serializers import IncomeSerializer,ExpenceSerializer,UserSerializer,FundSerializer,SourceSerializer,YearReport,ExpenseSourceSerializer
from . models import Report,User,Source
from datetime import datetime
from . utils import format_money
from django.http import HttpResponse
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        data = Source.objects.filter(type = Source.INCOME)
        serializer = self.get_serializer(data,many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        if Source.objects.get(pk = kwargs.get('pk')).name == "Қарз":
            return Response({'message':'ok'},status=status.HTTP_200_OK)
        else:
            return super().destroy(request, *args, **kwargs)

class ExpenceSourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = ExpenseSourceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        data = Source.objects.filter(user = request.user, type = Source.EXPENSE)
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
            'month_income':format_money(month_report.get('income')),
            'month_expence':format_money(month_report.get('expence')),
            'day_income':format_money(day_report.get('income')),
            'day_expence':format_money(day_report.get('expence')),
            'loan':format_money(tottal_loan.get('sum_loan')),
            'fund':format_money(tottal_fund.get('fund')),
            'final_income':format_money(amount.get('amount'))
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
        data['income'] = format_money(Report.filters.tottal_month_report(user = request.user,year = request.GET.get('year',None),month=request.GET.get('month',None),income=Report.INCOME).get('income'))
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
        data['expence'] = format_money(Report.filters.tottal_month_report(user = request.user,year = request.GET.get('year',None),month=request.GET.get('month',None),expence=Report.EXPENSE).get('expence'))
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
        data['fund'] = format_money(Report.filters.tottal_fund(user = request.user).get('fund'))
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

def HomeView(request):
    return HttpResponse('<h1 style="text-align:center; margin-top:100px">Hello Welcome to eWallet Project</h1>')
