def format_money(money:int):
    if isinstance(money,int):
        return "{:,}".format(money)
    else:
        return money

    