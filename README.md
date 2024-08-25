MSDS-434

This is a Final project as part of the MSDS-434-DL program.

GCP:
1. Search for cloud shell
2. In shell:
   gcloud projects list # lists all projects with an identifier
   gcloud config set project <project name with id>  # now the prompt is adjusted to the new project

   sudo apt update
   sudo apt install python3-pip python3-venv docker.io
   


   
4. Go to APIs and Services --> Enable APIs and Services. Enable "App Engine Admin API"
5. Back in the terminal, clone your github repo:
   git clone https://github.com/sai20-creator/DE_Final_project
   pip install -r requirements.txt
   python app.py
   docker build -t trip-time-prediction .
   docker run -p 5000:5000 trip-time-prediction
   gcloud app deploy.yml
