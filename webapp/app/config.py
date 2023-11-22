import os
from .pd_scraper import get_relevant_repo_data

class Config:
    # Static configurations
    GITHUB_TOKEN = os.environ.get('GITHUB_READONLY_TOKEN', 'default_token')
    SECRET_KEY = os.environ.get('PSEUDODOJO_SECRET_KEY', 'default_token')
    
    @staticmethod
    def load_dynamic_config(app):
        repo_data = get_relevant_repo_data(Config.GITHUB_TOKEN)
        app.config['REPO_DATA'] = repo_data