from django.contrib import messages
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import json
import logging
import pandas as pd
from .forms import StudentProfileForm
from .models import ResearcherResearchProfile
from .utils import find_nearest_pis
import openai
openai.api_key = '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'

# Create your views here.
def index(request):
    context = {
        "researcher_research_profiles": ResearcherResearchProfile.objects.all()
    }
    return render(request, "profiles/index.html", context)

def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "uploads/upload_csv.html", data)
    # if not GET, then proceed with processing
    try:
        csv_file = request.FILES["csv_file"]

        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("upload_csv"))
        #if file is too large, return message
        # if csv_file.multiple_chunks():
        #     messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
        #     return HttpResponseRedirect(reverse("upload_csv"))
  
        file_data = csv_file.read().decode('utf-8')
        lines = file_data.split("\n")

        #loop over the lines and save them in db. If error shows up , store as string and then display
        for line in lines:               
            #print("line:", line)                           
            fields = line.split("\t")
            print(len(fields))
            data_dict = {}
            data_dict["department"] = fields[0]
            data_dict["description"] = fields[2]
            data_dict["name"] = fields[3]
            data_dict["num_tokens"] = fields[4]
            data_dict["embedding"] = fields[5]
            try:
                profile = ResearcherResearchProfile(department=data_dict['department'], description=data_dict['description'], name=data_dict['name'], num_tokens=data_dict['num_tokens'], embedding=data_dict['embedding'])
                profile.save()                                                                                                                   
            except Exception as e:
                logging.getLogger("error_logger").error(repr(e))                             
            pass
    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload CVS file. "+repr(e))

    return HttpResponseRedirect(reverse("upload_csv"))


def recommend_pis(request):
    context = {}
    if request.method == 'POST':
        form = StudentProfileForm(request.POST)
        context['form'] = form
        if form.is_valid():
            student_profile = form.cleaned_data['student_research_description']
            print(student_profile)
            # Process the received data as needed
            df = pd.DataFrame(list(ResearcherResearchProfile.objects.all().values()))  # Use the Pandas Manager
            result_df = find_nearest_pis(df, student_profile, 5)
            json_records = result_df.to_json(orient='records')
            data = json.loads(json_records)
            context['data'] = data
    else:
        form = StudentProfileForm()
        context['form'] = form
    return render(request, 'recommenders/recommend_pis.html', context)