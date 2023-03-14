from django.db import models
from datetime import datetime,date
from django.db.models.functions import TruncMonth


class ReportManager(models.Manager):

    def filter_this_month_income(self,year = None,month = None):
        if month and year:
            return self.get_queryset().filter(date__year = year, date__month = month, type = "Income")
        else:
            this_month = datetime.now().month
            this_year = datetime.now().year
            return self.get_queryset().filter(date__year = this_year,date__month = this_month,type = "Income")

    def filter_this_month_expence(self,year = None,month = None):
        if month and year:
            return self.get_queryset().filter(date__year = year, date__month = month, type = "Expense")
        else:
            this_month = datetime.now().month
            this_year = datetime.now().year
            return self.get_queryset().filter(date__year = this_year,date__month = this_month,type = "Expense")

    def filter_this_month_fund(self,year = None,month = None):
        if month and year:
            return self.get_queryset().filter(date__year = year, date__month = month, fund_percent__gt = 0)
        else:
            this_month = datetime.now().month
            this_year = datetime.now().year
            return self.get_queryset().filter(date__year = this_year,date__month = this_month,fund_percent__gt = 0)

    
    def tottal_month_report(self,year = None,month = None,income = None,expence = None): 
        this_month = month if month else datetime.now().month
        this_year = year if year else datetime.now().year
        this_month_objects = self.get_queryset().filter(date__year = this_year, date__month = this_month)
        expense_from_income = this_month_objects.filter(type = "Expense",source_expence = "Soft_Amount").aggregate(sum_expence_from_income = models.Sum("amount"))
        
        if not (income or expence):
            income = this_month_objects.filter(type = "Income").aggregate(sum_income = models.Sum("clean_amount"))
            expence = this_month_objects.filter(type = "Expense").aggregate(sum_expence = models.Sum("amount"))
            print(income,expence)
            if income.get("sum_income") or expense_from_income.get("sum_expence_from_income"):
                if income.get("sum_income") and expense_from_income.get("sum_expence_from_income"):
                    final_income = income.get("sum_income") - expense_from_income.get("sum_expence_from_income")
                elif income.get("sum_income") and not expense_from_income.get("sum_expence_from_income"):
                    final_income = income.get("sum_income")
                elif not income.get("sum_income") and expense_from_income.get("sum_expence_from_income"):
                    final_income = 0 - expense_from_income.get("sum_expence_from_income")
            else:
                final_income = 0
            context = {
                "income":final_income,
                "expence":expence.get("sum_expence"),
            }
        
        else:
            if income:
                income = this_month_objects.filter(type = "Income").aggregate(sum_income = models.Sum("clean_amount"))
                if income.get("sum_income") or expense_from_income.get("sum_expence_from_income"):
                    if income.get("sum_income") and expense_from_income.get("sum_expence_from_income"):
                        final_income = income.get("sum_income") - expense_from_income.get("sum_expence_from_income")
                    elif income.get("sum_income") and not expense_from_income.get("sum_expence_from_income"):
                        final_income = income.get("sum_income")
                    elif not income.get("sum_income") and expense_from_income.get("sum_expence_from_income"):
                        final_income = 0 - expense_from_income.get("sum_expence_from_income")
                else:
                    final_income = 0
                context = {
                    "income":final_income  
                }
            elif expence:
                expence = this_month_objects.filter(type = expence).aggregate(sum_expence = models.Sum("amount"))
                context = {
                    "expence":expence.get("sum_expence")   
                }
        return context
    
    def today_report(self):
        today_objects = self.get_queryset().filter(date = date.today())
        income = today_objects.filter(type = "Income").aggregate(income = models.Sum("amount"))
        expence = today_objects.filter(type = "Expense").aggregate(expence = models.Sum("amount"))
        return {"income":income.get("income"),"expence":expence.get("expence")}
    
    def tottal_loan(self):
        tottal_loan = self.get_queryset().filter(type = "Income",source__name = "Qarz").aggregate(sum_loan = models.Sum("amount"))
        return tottal_loan

    def tottal_fund(self):
        expense_from_fund = self.get_queryset().filter(type = "Expense",source_expence = "Fund").aggregate(sum_expence_from_fund = models.Sum("amount"))
        tottla_fund = self.get_queryset().filter(fund_percent__gt = 0).aggregate(sum_fund = models.Sum("fund"))
        if tottla_fund.get("sum_fund") or expense_from_fund.get("sum_expence_from_fund"):
            if tottla_fund.get("sum_fund") and expense_from_fund.get("sum_expence_from_fund"):
                fund = tottla_fund.get("sum_fund") - expense_from_fund.get("sum_expence_from_fund")
            elif tottla_fund.get("sum_fund") and (not expense_from_fund.get("sum_expence_from_fund")):
                fund = tottla_fund.get("sum_fund")
            elif (not tottla_fund.get("sum_fund")) and expense_from_fund.get("sum_expence_from_fund"):
                fund = 0 - expense_from_fund.get("sum_expence_from_fund")
        else:
            fund = 0
        return {"fund":fund}
    
    def year_report(self,year = None):
        if not year:
            year = datetime.now().year
        income = models.Sum('amount', filter=models.Q(type = "Income"))
        soft_amount = models.Sum('clean_amount', filter=models.Q(type = "Income"))
        expence = models.Sum('amount', filter=models.Q(type = "Expense"))
        fund = models.Sum('fund' , filter=models.Q(type = "Income"))
        loan = models.Sum('amount', filter=models.Q(type = "Income" , source__name = "Qarz"))
        borrow = models.Sum('amount',filter=models.Q(type = "Expense" , source__name = "Qarz"))
        daycount = self.get_queryset().filter(date__year = int(year)
        ).annotate(
            month = TruncMonth('date',output_field=models.DateField())
            ).values('month').annotate(income=income).annotate(soft_amount=soft_amount).annotate(expence = expence).annotate(fund=fund).annotate(loan =loan).annotate(borrow = borrow)
        return daycount
    
