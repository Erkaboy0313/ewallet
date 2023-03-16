from django.db import models
from datetime import datetime,date
from django.db.models.functions import TruncMonth,Coalesce


class ReportManager(models.Manager):

    def get_this_date(self):
        return (datetime.now().year,datetime.now().month)

    def filter_this_month_income(self,user,year = None,month = None): 
        this_year,this_month = (year,month) if (year and month) else self.get_this_date()
        return self.get_queryset().filter(user = user,date__year = this_year,date__month = this_month,type = "Income")

    def filter_this_month_expence(self,user,year = None,month = None):
        this_year,this_month = (year,month) if (year and month) else self.get_this_date()
        return self.get_queryset().filter(user = user,date__year = this_year,date__month = this_month,type = "Expense")

    def filter_this_month_fund(self,user,year = None,month = None):
        this_year,this_month = (year,month) if (year and month) else self.get_this_date()
        return self.get_queryset().filter(user = user,date__year = this_year,date__month = this_month,fund_percent__gt = 0)

    
    def tottal_month_report(self,user,year = None,month = None,income = None,expence = None): 
        this_year,this_month = (year,month) if (year and month) else self.get_this_date()
        this_month_objects = self.get_queryset().filter(user = user,date__year = this_year, date__month = this_month)
        expence_from_income = this_month_objects.aggregate(expense = Coalesce(models.Sum("amount",filter=models.Q(type = "Expense", source_expence = "Soft_Amount")),0))
        if not (income or expence):
            income = this_month_objects.filter(type = "Income").aggregate(sum_income = Coalesce(models.Sum("amount"),0))
            expence = this_month_objects.filter(type = "Expense").aggregate(sum_expence = Coalesce(models.Sum("amount"),0))
            context = {
                "income":income.get("sum_income"),
                "expence":expence.get("sum_expence"),
            }
        
        else:
            if income:
                income = this_month_objects.filter(type = "Income").aggregate(sum_income = Coalesce(models.Sum("clean_amount"),0))
                context = {
                    "income":income.get("sum_income") - expence_from_income.get('expense')  
                }
            elif expence:
                expence = this_month_objects.filter(type = expence).aggregate(sum_expence = Coalesce(models.Sum("amount"),0))
                context = {
                    "expence":expence.get("sum_expence")   
                }
        return context
    
    def today_report(self,user):
        today_objects = self.get_queryset().filter(user = user,date = date.today())
        income = today_objects.filter(type = "Income").aggregate(income = Coalesce(models.Sum("amount"),0))
        expence = today_objects.filter(type = "Expense").aggregate(expence = Coalesce(models.Sum("amount"),0))
        return {"income":income.get("income"),"expence":expence.get("expence")}
    
    def tottal_loan(self,user):
        tottal_loan = self.get_queryset().filter(user = user,source__name__icontains = "Қарз"
                                                 ).aggregate(sum_loan = Coalesce(models.Sum("amount",filter=models.Q(type = "Income")),0
                                                                                 )-Coalesce(models.Sum("amount",filter=models.Q(type="Expense")),0))
        return tottal_loan

    def tottal_fund(self,user):
        expense_from_fund = self.get_queryset().filter(user = user,type = "Expense",source_expence = "Fund").aggregate(sum_expence_from_fund = Coalesce(models.Sum("amount"),0))
        tottla_fund = self.get_queryset().filter(user = user,fund_percent__gt = 0).aggregate(sum_fund = Coalesce(models.Sum("fund"),0))
        fund = tottla_fund.get("sum_fund") - expense_from_fund.get("sum_expence_from_fund")
        return {"fund":fund}
    
    def year_report(self,user,year = None):
        if not year:
            year = datetime.now().year
        income = models.Sum('amount', filter=models.Q(type = "Income"))
        soft_amount = models.Sum('clean_amount', filter=models.Q(type = "Income"))
        expence = models.Sum('amount', filter=models.Q(type = "Expense"))
        fund = models.Sum('fund' , filter=models.Q(type = "Income"))
        loan = models.Sum('amount', filter=models.Q(type = "Income" , source__name__icontains = "Қарз"))
        borrow = models.Sum('amount',filter=models.Q(type = "Expense" , source__name__icontains = "Қарз"))
        daycount = self.get_queryset().filter(user = user,date__year = int(year)
                                                ).annotate(
                                                    month = TruncMonth('date',output_field=models.DateField())
                                                    ).values('month'
                                                            ).annotate(income=Coalesce(income,0)
                                                                        ).annotate(soft_amount=Coalesce(soft_amount,0)
                                                                                ).annotate(expence = Coalesce(expence,0)
                                                                                            ).annotate(fund=Coalesce(fund,0)
                                                                                                        ).annotate(loan =Coalesce(loan,0)
                                                                                                                    ).annotate(borrow = Coalesce(borrow,0))
        return daycount
    
    def final_income(self,user):
        income = models.Sum('clean_amount',filter=models.Q(type = "Income"))
        expence = models.Sum('amount',filter=models.Q(type = "Expense", source_expence = "Soft_Amount"))
        amount = self.get_queryset().filter(user= user).aggregate(amount = Coalesce(income,0) - Coalesce(expence,0))
        return amount
    
