from django.db.models.functions import Lower
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse
# from jaro import  jaro
# from .consts import DB
import numpy as np

import pandas as pd
from django.views import View
from sqlalchemy import create_engine
from Levenshtein import jaro_winkler, hamming, jaro, distance

from .consts import DB


from .models import JobSeekerUserDetail, CleanNationality, FilterNationality
from django.core.paginator import Paginator

# Create your views here.
from django.views.generic import ListView, TemplateView, CreateView
from sqlalchemy.engine.url import URL

nationality = ["Afghan", "Albanian", "Algerian", "American Samoan", "Andorran", "Angolan", "Anguillan", "Antarctic",
                   "Antiguan or Barbudan", "Argentine", "Armenian", "Aruban", "Australian", "Austrian", "Azerbaijani",
                   "Bahamian", "Bahraini", "Bangladeshi", "Barbadian", "Belarusian", "Belgian", "Belizean", "Beninese",
                   "Bermudan", "Bhutanese", "Bolivian", "Bonaire", "Bosnian or Herzegovinian", "Botswanan",
                   "Bouvet Island", "Brazilian", "BIOT", "Bruneian", "Bulgarian", "Burkinabé", "Burundian",
                   "Cabo Verdean", "Cambodian", "Cameroonian", "Canadian", "Caymanian", "Central African", "Chadian",
                   "Chilean", "Chinese", "Christmas Island", "Cocos Island", "Colombian", "Comorian", "Congolese",
                   "Congolese", "Cook Island", "Costa Rican", "Ivorian", "Croatian", "Cuban", "Curacaoan", "Cypriot",
                   "Czech", "Danish", "Djiboutian", "Dominican", "Dominican", "Ecuadorian", "Egyptian", "Salvadoran",
                   "Equatorial Guinean", "Eritrean", "Estonian", "Ethiopian", "Falkland Island", "Faroese", "Fijian",
                   "Finnish", "French", "French Guianese", "French Polynesian", "French Southern Territories",
                   "Gabonese", "Gambian", "Georgian", "German", "Ghanaian", "Gibraltar", "Greek", "Greenlandic",
                   "Grenadian", "Guadeloupe", "Guamanian", "Guatemalan", "Channel Island", "Guinean", "Bissau-Guinean",
                   "Guyanese", "Haitian", "Heard Island or McDonald Islands", "Vatican", "Honduran", "Hong Kongese",
                   "Hungarian", "Icelandic", "Indian", "Indonesian", "Iranian", "Iraqi", "Irish", "Manx", "Israeli",
                   "Italian", "Jamaican", "Japanese", "Channel Island", "Jordanian", "Kazakhstani", "Kenyan",
                   "I-Kiribati", "North Korean", "South Korean", "Kuwaiti", "Kyrgyzstani", "Laotian", "Latvian",
                   "Lebanese", "Basotho", "Liberian", "Libyan", "Liechtenstein", "Lithuanian", "Luxembourgish",
                   "Macanese", "Macedonian", "Malagasy", "Malawian", "Malaysian", "Maldivian", "Malinese", "Maltese",
                   "Marshallese", "Martinican", "Mauritanian", "Mauritian", "Mahoran", "Mexican", "Micronesian",
                   "Moldovan", "Monacan", "Mongolian", "Montenegrin", "Montserratian", "Moroccan", "Mozambican",
                   "Burmese", "Namibian", "Nauruan", "Nepalese", "Nepali", "Dutch", "New Caledonian", "New Zealand",
                   "Nicaraguan", "Nigerien", "Nigerian", "Niuean", "Norfolk Island", "Northern Marianan", "Norwegian",
                   "Omani", "Pakistani", "Palauan", "Palestinian", "Panamanian", "Papua New Guinean", "Paraguayan",
                   "Peruvian", "Filipino", "Pitcairn Island", "Polish", "Portuguese", "Puerto Rican", "Qatari",
                   "Romanian", "Russian", "Rwandan", "Saint Helenian", "Kittitian or Nevisian", "Saint Lucian",
                   "Saint-Martinoise", "Saint-Pierrais or Miquelonnais", "Vincentian", "Samoan", "Sammarinese",
                   "Sao Tomean", "Saudi Arabian", "Senegalese", "Serbian", "Seychellois", "Sierra Leonean",
                   "Singaporean", "Sint Maarten", "Slovak", "Slovenian", "Solomon Island", "Somalian", "South African",
                   "South Georgia or South Sandwich Islands", "South Sudanese", "Spanish", "Sri Lankan", "Sudanese",
                   "Surinamese", "Svalbard", "Swazi", "Swedish", "Swiss", "Syrian", "Taiwanese", "Tajikistani",
                   "Tanzanian", "Thai", "Timorese", "Togolese", "Tokelauan", "Tongan", "Trinidadian or Tobagonian",
                   "Tunisian", "Turkish", "Turkmen", "Turks and Caicos Island", "Tuvaluan", "Ugandan", "Ukrainian",
                   "Emirian", "British", "American", "American", "Uruguayan", "Uzbekistani", "Vanuatuan", "Venezuelan",
                   "Vietnamese", "British Virgin Island", "U.S. Virgin Island", "Wallisian or Futunan", "Sahrawian",
                   "Yemeni", "Zambian", "Zimbabwean"]

def home(request):
    return render(request, 'NationalityCleaner/home.html')



def getData(**kwargs):

    cs = "%s://%s:%s@%s:%s/%s" % (
    kwargs['DRIVER'], kwargs['USER'], kwargs['PASSWORD'], kwargs['HOST'], kwargs['PORT'],
    kwargs['NAME'])
    # cs = "%s://%s:%s@%s:%s/%s" % (
    # kwargs['drivername'], kwargs['username'], kwargs['password'], kwargs['servername'], kwargs['port'],
    # kwargs['database'])
    engine = create_engine(cs)
    df = pd.read_sql_query('SELECT DISTINCT lower(nationality) AS nationality FROM "NationalityClean_jobseekeruserdetail";',
                           con=engine)

    return df['nationality']


def clean_data():
    df = pd.DataFrame(nationality)
    df_nationality = df[0].str.lower()

    db_nationality = getData(**DB)

    # Jaro Winkler distance
    dist = [[jaro_winkler(df_nationality[i], db_nationality[j]) for i in range(len(df_nationality))] for j in
            range(len(db_nationality))]
    df_dist = pd.DataFrame(dist, columns=df_nationality, index=db_nationality)
    best_score = df_dist.max(axis=1)
    best_match = df_dist.idxmax(axis=1)
    best_score_rounded = best_score.round(5)
    best_score_nationality = best_score_rounded.to_dict()
    best_match_nationality = best_match.to_dict()
    results={}
    final = []
    for k, v in best_score_nationality.items():
        final.append([k, v, best_match_nationality[k]])
        results[k] = {v, best_match_nationality[k]}


    return final



class IndexView(ListView):
    template_name = 'NationalityCleaner/index.html'
    model = FilterNationality
    # extra_context = {}
    paginate_by = 50
    context_object_name = 'all_nationality'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx['df_nationality'] = nationality
        return ctx

    # def get_queryset(self):
    #
    #     all_data = FilterNationality.objects.all()
    #
    #     return all_data


    # def get_context_data(self, **kwargs):
    #     ctx = super().get_context_data(**kwargs)
    #     results = {}
    #     val= clean_data()
    #     best_score = val.max(axis=1)
    #     best_match = val.idxmax(axis=1)
    #     best_score_rounded = best_score.round(5)
    #     best_score_nationality = best_score_rounded.to_dict()
    #     best_match_nationality = best_match.to_dict()
    #
    #     self.extra_context['nationality']= nationality
    #     final = []
    #     for k, v in best_score_nationality.items():
    #         final.append([k, v, best_match_nationality[k]])
    #         results[k] = {v, best_match_nationality[k]}
    #
    #     bulk_list = list()
    #     for each_user_data in final:
    #         bulk_list.append(
    #             FilterNationality(
    #                 unverified_nationality=each_user_data[0],
    #                 score = each_user_data[1],
    #                 verified_nationality=each_user_data[2],
    #                 input_data = each_user_data[1] if each_user_data[1] >= 0.98 else None
    #             )
    #         )
    #
    #     self.extra_context['all_nationality']= final
    #
    #     if self.extra_context is not None:
    #         kwargs.update(self.extra_context)
    #
    #
    #     remove_data= list(CleanNationality.objects.values_list('old_nationality','score','cleaned_nationality'))
    #     old_nationality_data = kwargs['all_nationality']
    #
    #
    #
    #     final_data = [
    #         i for i in kwargs['all_nationality']  if tuple(i) not in remove_data
    #     ]
    #
    #     ctx['all_nationality'] = final_data
    #     ctx['nationality'] = nationality
    #
    #     # for each_tuple in remove_data:
    #     #     all_nationality_data=list(each_tuple)
    #
    #
    #         # numpy_value = np.array(old_nationality_data)
    #         # lst = [list(x) for x in numpy_value]
    #         # lst.index(all_nationality_data)
    #
    #         # num_value=numpy_value.where(all_nationality_data)
    #
    #     # for i in kwargs['all_nationality']:
    #     #     old_nationality = i[0]
    #     #     score = i[1]
    #     #     new_nationality = i[2]
    #     #
    #     #     if score > 0.98:
    #     #         bool= True
    #     #     else:
    #     #         bool= False
    #     #
    #     #     nationality_data =    CleanNationality.objects.create(old_nationality=old_nationality, cleaned_nationality=new_nationality, score= score, correct_status=bool )
    #     #
    #
    #     if self.request.GET.get('post_all') == 'post_all_data':
    #         print('user clicked button')
    #         print('button clicked')
    #         import ipdb
    #         ipdb.set_trace()
    #
    #     # paginator = Paginator(kwargs['old_nationality'], 25)  # Show 25 contacts per page
    #     #
    #     # page = self.request.GET.get('page')
    #     # old_nationality = paginator.get_page(page)
    #     # return render(self.request, 'list.html', {'contacts': old_nationality})
    #
    #     return ctx


class PostNationality(View):


    def post(self, request, **kwargs):

        job_seeker_nationality =  request.POST['job_seeker_nationality']
        best_score = request.POST['best_score']
        score= float(best_score)
        old_jobseekers_nationality = request.POST['job_seeker_nationality']
        corrected_nationality = request.POST['each_nationality_data']

        data = CleanNationality.objects.create(old_nationality=old_jobseekers_nationality, cleaned_nationality=corrected_nationality, score= score)
        data.save()

        return redirect(reverse('NationalityClean:index') )



class InitialPost(View):


    def post(self, request, **kwargs):
        pass


class PostAllNationality(CreateView):

    def post(self,request, **kwargs):
        val = clean_data()
        best_score = val.max(axis=1)
        best_match = val.idxmax(axis=1)
        best_score_rounded = best_score.round(5)
        best_score_nationality = best_score_rounded.to_dict()
        best_match_nationality = best_match.to_dict()
        final=[]
        results= {}
        for old_nationality, best_score in best_score_nationality.items():
            if best_score > 0.98:
                final.append([old_nationality, best_score, best_match_nationality[old_nationality]])
                results[old_nationality] = {best_score, best_match_nationality[old_nationality]}



        bulk_list = list()
        for each_user_data in final:
            bulk_list.append(
                CleanNationality(
                    old_nationality=each_user_data[0],
                    score=each_user_data[1],
                    cleaned_nationality=each_user_data[2]
                )
            )

        import ipdb
        ipdb.set_trace()
        CleanNationality.objects.bulk_create(bulk_list)

        return redirect(reverse('NationalityClean:index'))

# class IndexView(ListView):
#     template_name  = 'NationalityCleaner/index.html'
#
#
#
#     def get_queryset(self):
#         context_object_name = 'all_posts'  # By default it gives object_list
#         model = JobSeekerUserDetail
#         df = pd.DataFrame(nationality)
#         df_nationality = df[0].str.lower()
#
#
#         db_nationality = getData(**DB)
#
#         # Jaro Winkler distance
#         dist = [[jaro_winkler(df_nationality[i], db_nationality[j]) for i in range(len(df_nationality))] for j in
#                 range(len(db_nationality))]
#
#
#
#         # Jaro distance
#         dist1 = [[jaro(df_nationality[i], db_nationality[j]) for i in range(len(df_nationality))] for j in
#                 range(len(db_nationality))]
#
#
#
#         # '0.
#         dist2 = [[distance(df_nationality[i], db_nationality[j]) for i in range(len(df_nationality))] for j in
#                 range(len(db_nationality))]
#         df_dist = pd.DataFrame(dist, columns=df_nationality, index=db_nationality)
#         df_dist1 = pd.DataFrame(dist1, columns=df_nationality, index=db_nationality)
#         df_dist2 = pd.DataFrame(dist2, columns=df_nationality, index=db_nationality)
#
#         best_score = df_dist.max(axis=1)
#         best_match = df_dist.idxmax(axis=1)
#
#         best_score1 = df_dist1.max(axis=1)
#         best_match1 = df_dist1.idxmax(axis=1)
#
#         best_score2 = df_dist2.max(axis=1)
#         best_match2 = df_dist2.idxmax(axis=1)
#
#
#         import ipdb
#         ipdb.set_trace()
#
#         value = JobSeekerUserDetail.objects.annotate(nationality_lower=Lower('nationality')).values_list( 'nationality',flat=True).order_by('nationality').distinct()
#         return value
#         """
#         Return ``True`` if the view should display empty lists and ``False``
#         if a 404 should be raised instead.
#         """


