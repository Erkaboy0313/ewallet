from rest_framework import serializers
from . models import Report,User,Source
from . utils import format_money
from . mixins import FormatMoneyMixin

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        exclude = ['type']
        extra_kwargs = {'user': {'write_only': True}}

class ExpenseSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        exclude = ['type']
        extra_kwargs = {'user': {'write_only': True}}
    
    def create(self, validated_data):
        source = Source.objects.create(type = Source.EXPENSE, **validated_data)
        return source

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        exclude = ['type','source_expence']
        extra_kwargs = {'user': {'write_only': True}}
    
    def create(self, validated_data):
        report = Report.objects.create(type =Report.INCOME,**validated_data)
        return report
    
    def to_representation(self, instance):
        object = super().to_representation(instance)
        object['source'] = instance.source.name if instance.source else 'Null'
        object['amount'] = format_money(instance.amount)
        object['fund'] = format_money(instance.fund)
        object['clean_amount'] = format_money(instance.clean_amount)
        return object

class ExpenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        exclude = ['type','gift','fund_percent','fund','clean_amount']
        extra_kwargs = {'user': {'write_only': True}}

    def create(self, validated_data):
        report = Report.objects.create(type =Report.EXPENSE,**validated_data)
        return report
    
    def to_representation(self, instance):
        object = super().to_representation(instance)
        object['source'] = instance.source.name if instance.source else 'Null'
        object['amount'] = format_money(instance.amount)
        return object

class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        exclude = ['user','type','source_expence','clean_amount','gift']
    
    def to_representation(self, instance):
        object = super().to_representation(instance)
        object['source'] = instance.source.name if instance.source else 'Null'
        object['amount'] = format_money(instance.amount)
        object['fund'] = format_money(instance.fund)
        return object

class YearReport(FormatMoneyMixin,serializers.Serializer):
    month = serializers.DateField()
    income = serializers.IntegerField()
    soft_amount = serializers.IntegerField()
    expence = serializers.IntegerField()
    fund = serializers.IntegerField()
    loan = serializers.IntegerField()
    borrow = serializers.IntegerField()