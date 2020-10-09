from .forms import sumForm, slettForm, AccountForm
from .models import Sum, Account
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import render
from datetime import datetime

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
from django.urls import reverse

KATEGORIER = ["Generelt", "Mat", "Trening", "Reise", "Drip"]


def home(response):
    context = {"useren": response.user.username}
    return render(response, "../templates/base.html", context)


def kontoer(response):
    accounts = Account.objects.filter(user=response.user)
    fortune = get_fortune(response.user)
    context = {"useren": response.user.username, "kontoer": accounts, "fortune": fortune}
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
        print(total)
        accounts = Account.objects.filter(user=user)
        print(accounts)
    context = {"pos_sums": pos_sums, "neg_sums": neg_sums, "month": stringMonth, "total": total, "accounts": accounts}
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
                new_sum = Sum(date=date, sum=sum, beskrivelse=beskrivelse, user=response.user,
                              month=month)
                new_sum.save()
            else:
                account = account[int(form.data.get('account')) - 1]
                new_sum = Sum(date=date, sum=sum, beskrivelse=beskrivelse, account=account, user=response.user,
                              month=month)
                account.belop = account.belop+sum
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


def add_account(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            new_account = Account(name=form.data.get('name'), belop=form.data.get('belop'),
                                  interest=form.data.get('interest'), user=request.user)
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
