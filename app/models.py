from django.db import models
from . managers import ReportManager
from django.contrib.auth.models import User
# Create your models here.


class Source(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name

class Report(models.Model):

    INCOME = 'Income'
    EXPENSE = 'Expense'
    
    SOFT_AMAUNT = "Soft_Amount"
    FUND = 'Fund'

    source_expence_choice = [
        (SOFT_AMAUNT,SOFT_AMAUNT),
        (FUND,FUND)
    ]

    type_choice = [
        (INCOME,INCOME),
        (EXPENSE,EXPENSE)
    ]

    LOAN = "Loan"
    BORROW = 'Borrow'

    loan_types = [
        (LOAN,LOAN),
        (BORROW,BORROW),
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    source = models.ForeignKey(Source,on_delete=models.CASCADE)
    type = models.CharField(max_length=30,choices=type_choice,null=True,blank=True)
    source_expence = models.CharField(choices=source_expence_choice,max_length=20,null=True,blank=True)
    amount = models.BigIntegerField(default=0,null=True,blank=True)
    fund_percent = models.IntegerField(default=0,null=True,blank=True)
    fund = models.BigIntegerField(default=0,null=True,blank=True)
    clean_amount = models.BigIntegerField(default=0,null=True,blank=True)
    gift = models.BooleanField(default=False)
    description = models.TextField(null=True,blank=True)
    date = models.DateField(null=True,blank=True)

    filters = ReportManager()
    objects = models.Manager()
    class Meta:
        ordering = ['-id']

    def fund_calculate(self):
        return self.amount * (100 / self.fund_percent)

    def __str__(self):
        return f"{self.type} - {self.amount} | {self.date}"

    def save(self, *args, **kwargs):
        if self.type == self.INCOME:
            if self.fund_percent:
                self.fund = self.amount * (self.fund_percent / 100)
                self.clean_amount = self.amount - self.fund
            else:
                self.clean_amount = self.amount
        super(Report,self).save(*args,**kwargs)
    
