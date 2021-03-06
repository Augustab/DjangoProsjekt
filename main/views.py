import requests
from django.urls import reverse
import matplotlib.pyplot as plt
import base64
import io


from .forms import sumForm, slettForm, AccountForm
from .models import Sum, Account
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import render
from datetime import datetime
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies
import matplotlib
matplotlib.use('Agg')

months = ["Januar", "Februar", "Mars",
          "April", "Mai", "Juni", "Juli",
          "August", "September", "Oktober",
          "November", "Desember"
          ]
thisMonth = int(datetime.today().strftime("%Y%m"))
stringMonth = months[datetime.now().month - 1]
print(thisMonth)
print(stringMonth)

# Create your views here.

KATEGORIER = ["Generelt", "Mat", "Trening", "Reise", "Drip"]


def home(response):
    context = {"useren": response.user.username}
    return render(response, "../templates/base.html", context)


def kontoer(response):
    accounts = Account.objects.filter(user=response.user)
    fortune = get_fortune(response.user)
    context = {
        "useren": response.user.username,
        "kontoer": accounts,
        "fortune": fortune}
    return render(response, "../templates/kontoer.html", context)


def get_fortune(user):
    fortune = 0
    for account in Account.objects.filter(user=user):
        fortune += account.belop
    return fortune


def redirect(response):
    return HttpResponsePermanentRedirect(reverse('home'))


def regnskap(response):
    user = response.user
    pos_sums = None
    neg_sums = None
    total = 0
    accounts = 0
    currentmonth = int(datetime.today().strftime("%Y%m"))
    if not user.is_anonymous:
        user_sums = Sum.objects.filter(user=user)
        user_sums = user_sums.filter(month=currentmonth)
        pos_sums = user_sums.filter(sum__gte=0)
        neg_sums = user_sums.filter(sum__lt=0)
        total = 0
        for value in neg_sums:
            total += int(value.sum)
        for value in pos_sums:
            total += int(value.sum)
        accounts = Account.objects.filter(user=user)
        print("accountvariablen:", accounts)
    context = {
        "pos_sums": pos_sums,
        "neg_sums": neg_sums,
        "month": stringMonth,
        "total": total,
        "accounts": accounts}
    return render(response, "../templates/regnskap.html", context)


def legg_til_sum(response):
    if response.method == "POST":
        form = sumForm(response.POST)
        if form.is_valid():
            date = form.data.get('date')
            month = int(date[:4] + date[5:7])
            sum = int(form.data.get('sum'))
            beskrivelse = form.data.get('beskrivelse')
            account = Account.objects.filter(user=response.user)
            if not account:
                new_sum = Sum(
                    date=date,
                    sum=sum,
                    beskrivelse=beskrivelse,
                    user=response.user,
                    month=month)
                new_sum.save()
            else:
                account = account[int(form.data.get('account')) - 1]
                new_sum = Sum(
                    date=date,
                    sum=sum,
                    beskrivelse=beskrivelse,
                    account=account,
                    user=response.user,
                    month=month)
                account.belop = account.belop + sum
                account.save()
                new_sum.save()
        return HttpResponseRedirect(reverse('regnskap'))


def slett_sum(request):
    if request.method == "POST":
        form = slettForm(request.POST)
        if form.is_valid():
            # bookingid henter jeg fra det SKJULTE INPUTFELTET I FORM'en.
            sumid = form.data.get('sumid')
            if sumid is not None:
                # sletter den valgte bookingen
                Sum.objects.get(sumid=sumid).delete()
            return HttpResponseRedirect(reverse('regnskap'))


def slett_sum2(request):
    if request.method == "POST":
        form = slettForm(request.POST)
        if form.is_valid():
            # bookingid henter jeg fra det SKJULTE INPUTFELTET I FORM'en.
            sumid = form.data.get('sumid')
            if sumid is not None:
                # sletter den valgte bookingen
                Sum.objects.get(sumid=sumid).delete()
            return HttpResponseRedirect(reverse('oversikt'))


def add_account(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            new_account = Account(
                name=form.data.get('name'),
                belop=form.data.get('belop'),
                interest=form.data.get('interest'),
                user=request.user)
            new_account.save()
        return HttpResponseRedirect(reverse('kontoer'))


def slett_account(request):
    if request.method == "POST":
        form = slettForm(request.POST)
        if form.is_valid():
            # bookingid henter jeg fra det SKJULTE INPUTFELTET I FORM'en.
            kontoid = form.data.get('sumid')
            if kontoid is not None:
                # sletter den valgte bookingen
                Account.objects.get(accountid=kontoid).delete()
            return HttpResponseRedirect(reverse('kontoer'))


def oversikt(response):
    used_months = Sum.objects.values_list('month', flat=True)
    have_any_sums = Sum.objects.filter(user=response.user)
    month_dict = {}
    for month in used_months:
        key = month - 202001
        sum_this_month = Sum.objects.filter(month=month)
        month_dict[months[key]] = sum_this_month.filter(user=response.user)
    context = {"month_dict": month_dict, "have_any_sums": have_any_sums}
    return render(response, "../templates/oversikt.html", context)

cc = CryptoCurrencies(key='ALPA_KEY', output_format='pandas')
data = cc.get_digital_currency_daily(symbol='BTC', market='USD')
plt.rcParams['axes.facecolor'] = 'black'
data[0]['1a. open (USD)'].plot()
plt.tight_layout()
ax = plt.gca()
ax.get_lines()[0].set_color("#00FF1A")
figure = plt.gcf()
buffer = io.BytesIO()
figure.savefig(buffer, format='png')
buffer.seek(0)
string = base64.b64encode(buffer.read())
url = string.decode('utf-8')

def stocks(response):
    '''view for stocks-siden som skal vise grafer av bitcoin og etherum'''
    return render(response, "../templates/stocks.html", {"url": url})
