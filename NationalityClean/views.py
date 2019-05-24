from django.shortcuts import render, redirect
from django.urls import reverse
import pandas as pd
from django.views import View
from sqlalchemy import create_engine
from Levenshtein import jaro_winkler, hamming, jaro, distance
from .consts import DB
from .models import FilterNationality
from django.views.generic import ListView
import json

nationality = ['Afghan',
               'Albanian',
               'Algerian',
               'American',
               'American Samoan',
               'Andorran',
               'Angolan',
               'Anguillan',
               'Antarctic',
               'Antiguan or Barbudan',
               'Argentine',
               'Armenian',
               'Aruban',
               'Australian',
               'Austrian',
               'Azerbaijani',
               'BIOT',
               'Bahamian',
               'Bahraini',
               'Bangladeshi',
               'Barbadian',
               'Basotho',
               'Belarusian',
               'Belgian',
               'Belizean',
               'Beninese',
               'Bermudan',
               'Bhutanese',
               'Bissau-Guinean',
               'Bolivian',
               'Bonaire',
               'Bosnian or Herzegovinian',
               'Botswanan',
               'Bouvet Island',
               'Brazilian',
               'British',
               'British Virgin Island',
               'Bruneian',
               'Bulgarian',
               'Burkinabé',
               'Burmese',
               'Burundian',
               'Cabo Verdean',
               'Cambodian',
               'Cameroonian',
               'Canadian',
               'Caymanian',
               'Central African',
               'Chadian',
               'Channel Island',
               'Channel Island',
               'Chilean',
               'Chinese',
               'Christmas Island',
               'Cocos Island',
               'Colombian',
               'Comorian',
               'Congolese',
               'Congolese',
               'Cook Island',
               'Costa Rican',
               'Croatian',
               'Cuban',
               'Curacaoan',
               'Cypriot',
               'Czech',
               'Danish',
               'Djiboutian',
               'Dominican',
               'Dominican',
               'Dutch',
               'Ecuadorian',
               'Egyptian',
               'Emirian',
               'Equatorial Guinean',
               'Eritrean',
               'Estonian',
               'Ethiopian',
               'Falkland Island',
               'Faroese',
               'Fijian',
               'Filipino',
               'Finnish',
               'French',
               'French Guianese',
               'French Polynesian',
               'French Southern Territories',
               'Gabonese',
               'Gambian',
               'Georgian',
               'German',
               'Ghanaian',
               'Gibraltar',
               'Greek',
               'Greenlandic',
               'Grenadian',
               'Guadeloupe',
               'Guamanian',
               'Guatemalan',
               'Guinean',
               'Guyanese',
               'Haitian',
               'Heard Island or McDonald Islands',
               'Honduran',
               'Hong Kongese',
               'Hungarian',
               'I-Kiribati',
               'Icelandic',
               'Indian',
               'Indonesian',
               'Iranian',
               'Iraqi',
               'Irish',
               'Israeli',
               'Italian',
               'Ivorian',
               'Jamaican',
               'Japanese',
               'Jordanian',
               'Kazakhstani',
               'Kenyan',
               'Kittitian or Nevisian',
               'Korean',
               'Kuwaiti',
               'Kyrgyzstani',
               'Laotian',
               'Latvian',
               'Lebanese',
               'Liberian',
               'Libyan',
               'Liechtenstein',
               'Lithuanian',
               'Luxembourgish',
               'Macanese',
               'Macedonian',
               'Mahoran',
               'Malagasy',
               'Malawian',
               'Malaysian',
               'Maldivian',
               'Malinese',
               'Maltese',
               'Manx',
               'Marshallese',
               'Martinican',
               'Mauritanian',
               'Mauritian',
               'Mexican',
               'Micronesian',
               'Moldovan',
               'Monacan',
               'Mongolian',
               'Montenegrin',
               'Montserratian',
               'Moroccan',
               'Mozambican',
               'Namibian',
               'Nauruan',
               'Nepalese',
               'Nepali',
               'New Caledonian',
               'New Zealand',
               'Nicaraguan',
               'Nigerian',
               'Nigerien',
               'Niuean',
               'Norfolk Island',
               'North Korean',
               'Northern Marianan',
               'Norwegian',
               'Omani',
               'Pakistani',
               'Palauan',
               'Palestinian',
               'Panamanian',
               'Papua New Guinean',
               'Paraguayan',
               'Peruvian',
               'Pitcairn Island',
               'Polish',
               'Portuguese',
               'Puerto Rican',
               'Qatari',
               'Romanian',
               'Russian',
               'Rwandan',
               'Sahrawian',
               'Saint Helenian',
               'Saint Lucian',
               'Saint-Martinoise',
               'Saint-Pierrais or Miquelonnais',
               'Salvadoran',
               'Sammarinese',
               'Samoan',
               'Sao Tomean',
               'Saudi Arabian',
               'Senegalese',
               'Serbian',
               'Seychellois',
               'Sierra Leonean',
               'Singaporean',
               'Sint Maarten',
               'Slovak',
               'Slovenian',
               'Solomon Island',
               'Somalian',
               'South African',
               'South Georgia or South Sandwich Islands',
               'South Korean',
               'South Sudanese',
               'Spanish',
               'Sri Lankan',
               'Sudanese',
               'Surinamese',
               'Svalbard',
               'Swazi',
               'Swedish',
               'Swiss',
               'Syrian',
               'Taiwanese',
               'Tajikistani',
               'Tanzanian',
               'Thai',
               'Timorese',
               'Togolese',
               'Tokelauan',
               'Tongan',
               'Trinidadian or Tobagonian',
               'Tunisian',
               'Turkish',
               'Turkmen',
               'Turks and Caicos Island',
               'Tuvaluan',
               'U.S. Virgin Island',
               'Ugandan',
               'Ukrainian',
               'Uruguayan',
               'Uzbekistani',
               'Vanuatuan',
               'Vatican',
               'Venezuelan',
               'Vietnamese',
               'Vincentian',
               'Wallisian or Futunan',
               'Yemeni',
               'Zambian',
               'Zimbabwean']


def home(request):
    return render(request, 'nationalityclean/home.html')


def get_data(**kwargs):
    cs = "%s://%s:%s@%s:%s/%s" % (
        kwargs['DRIVER'],
        kwargs['USER'],
        kwargs['PASSWORD'],
        kwargs['HOST'],
        kwargs['PORT'],
        kwargs['NAME'])
    engine = create_engine(cs)
    df = pd.read_sql_query('SELECT DISTINCT lower(nationality) AS nationality FROM "NationalityClean_jobseekeruserdetail";',
                           con=engine)

    return df['nationality']


def clean_data():
    df = pd.DataFrame(nationality)
    df_nationality = df[0].str.lower()

    db_nationality = get_data(**DB)

    # Jaro Winkler distance
    dist = [[jaro_winkler(df_nationality[i], db_nationality[j])
             for i in range(len(df_nationality))]
            for j in range(len(db_nationality))]
    df_dist = pd.DataFrame(dist, columns=df_nationality, index=db_nationality)
    best_score = df_dist.max(axis=1)
    best_match = df_dist.idxmax(axis=1)
    best_score_rounded = best_score.round(5)
    best_score_nationality = best_score_rounded.to_dict()
    best_match_nationality = best_match.to_dict()
    final = []
    for k, v in best_score_nationality.items():
        final.append([k, v, best_match_nationality[k]])
    return final




class IndexView(ListView):
    template_name = 'nationalityclean/index.html'
    paginate_by = 20
    queryset = FilterNationality.objects.filter(verified_status=False)
    context_object_name = 'all_nationality'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx['df_nationality'] = nationality
        ctx['offset']= self.get_paginate_by(self.get_queryset())*(ctx['page_obj'].number-1)
        return ctx


class PostNationality(View):

    def post(self, request, **kwargs):
        pk = self.kwargs['pk']
        verified_nationality = request.POST['select_nationality']
        update_nationality = FilterNationality.objects.filter(pk=pk).update(
            verified_nationality=verified_nationality,
            verified_status=True
        )
        return redirect(request.META['HTTP_REFERER'])


class PostAllNationality(View):

    def post(self,request, **kwargs):
        # request_getdata = request.POST.get('best_score_list', None)
        ajax_val=json.loads(request.POST.get('best_score_list'))
        for i in ajax_val:
            nationality_id = int(i['id'])
            best_score= float(i['score']),
            correct_nationality = i['Nationality']
            nationality = FilterNationality.objects.filter(pk=nationality_id).values('verified_nationality')
            na_val=nationality[0]['verified_nationality']

            if na_val ==(correct_nationality).lower():
                FilterNationality.objects.filter(pk=nationality_id).update(verified_status=True)
            else:
                FilterNationality.objects.filter(pk=nationality_id).update(verified_nationality=correct_nationality,
                                                                           verified_status=True)
        return redirect(reverse('nationality_clean:index'))

