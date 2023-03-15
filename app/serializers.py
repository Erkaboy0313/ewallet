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
    class Meta:
        model = Report
        exclude = ['type','source_expence']
        extra_kwargs = {'user': {'write_only': True}}
    
    def create(self, validated_data):
        report = Report.objects.create(type =Report.INCOME,**validated_data)
        return report
    
    def to_representation(self, instance):
        object = super().to_representation(instance)
        object['source'] = instance.source.name
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
        object['source'] = instance.source.name
        return object

class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        exclude = ['user','type','source_expence','clean_amount','gift']
    
    def to_representation(self, instance):
        object = super().to_representation(instance)
        object['source'] = instance.source.name
        return object

class YearReport(serializers.Serializer):
    month = serializers.DateField()
    income = serializers.IntegerField()
    soft_amount = serializers.IntegerField()
    expence = serializers.IntegerField()
    fund = serializers.IntegerField()
    loan = serializers.IntegerField()
    borrow = serializers.IntegerField()