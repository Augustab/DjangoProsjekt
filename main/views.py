from .forms import sumForm
from .models import Sum
from django.http import HttpResponsePermanentRedirect
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


def redirect(response):
    return HttpResponsePermanentRedirect(reverse('home'))


def regnskap(response):
    if response.method=="POST":
        form = sumForm(response.POST)
        if form.is_valid():
            date = form.data.get('date')
            sum = int(form.data.get('sum'))
            beskrivelse = form.data.get('beskrivelse')
            kategori = KATEGORIER[int(form.data.get('kategori'))]
            print(kategori)
            month = int(datetime.today().strftime("%Y%m"))
            print(month)
            new_sum = Sum(date=date, sum=sum, beskrivelse=beskrivelse, kategori=kategori, user=response.user, month=month)
            new_sum.save()
    pos_sums = Sum.objects.filter(sum__gte=0)
    neg_sums = Sum.objects.filter(sum__lt=0)
    total = 0
    for value in neg_sums:
        total += int(value.sum)
    for value in pos_sums:
        total += int(value.sum)
    print(total)
    context = {"pos_sums": pos_sums, "neg_sums": neg_sums, "month": stringMonth, "total": total}
    return render(response, "../templates/regnskap.html", context)


def slettSum(request):
    if request.method == "POST":
        form = slettSum(request.POST)
        if form.is_valid():
            # bookingid henter jeg fra det SKJULTE INPUTFELTET I FORM'en.
            sumid = form.data.get('sumid')
            if sumid is not None:
                # sletter den valgte bookingen
                Sum.objects.get(bookingid=sumid).delete()
                user = request.user
                # henter ut den oppdaterte listen over brukerens bookinger
                return render(
                    request,
                    "../templates/regnskap.html")
