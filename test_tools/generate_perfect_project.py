from datetime import datetime, timedelta

def print_dates_between(debut, fin):
    debut_date = datetime.strptime(debut, '%Y-%m-%d')
    fin_date = datetime.strptime(fin, '%Y-%m-%d')

    date_actuelle = debut_date
    while date_actuelle <= fin_date:
        print(date_actuelle.strftime('%Y-%m-%d'))
        date_actuelle += timedelta(days=1)

print_dates_between('2015-01-01', '2020-12-31')