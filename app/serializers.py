from rest_framework import serializers
from . models import Report,User,Source

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'

class IncomeSerializer(serializers.ModelSerializer):
    source = SourceSerializer(read_only = True)
    class Meta:
        model = Report
        exclude = ['user','type','source_expence']
    
    def create(self, validated_data):
        report = Report.objects.create(type =Report.INCOME,**validated_data)
        return report

class ExpenceSerializer(serializers.ModelSerializer):
    source = SourceSerializer(read_only = True)
    class Meta:
        model = Report
        exclude = ['user','type','gift','fund_percent','fund','clean_amount']

    def create(self, validated_data):
        report = Report.objects.create(type =Report.EXPENSE,**validated_data)
        return report

class FundSerializer(serializers.ModelSerializer):
    source = SourceSerializer(read_only = True)
    class Meta:
        model = Report
        exclude = ['user','type','source_expence','clean_amount','gift']

class YearReport(serializers.Serializer):
    # <QuerySet [{'month': datetime.date(2023, 2, 1), 'income': 100000, 'soft_amount': 90000, 'expence': None, 'fund': 10000, 'loan': None, 'borrow': None}, {'month': datetime.date(2023, 3, 1), 'income': 120000, 'soft_amount': 110000, 'expence': 30000, 'fund': 10000, 'loan': 20000, 'borrow': None}]>
    month = serializers.DateField()
    income = serializers.IntegerField()
    soft_amount = serializers.IntegerField()
    expence = serializers.IntegerField()
    fund = serializers.IntegerField()
    loan = serializers.IntegerField()
    borrow = serializers.IntegerField()