import argparse
import yaml
from lk_scrapper_functions import get_profile_html, generate_profile

message = ('Given as input the url of a linkedin profile, '
            'creates a Profile instance of this linkedin profile.')
parser = argparse.ArgumentParser(description=message)

parser.add_argument('linkedin_url',
                       help='The ulr of the linkedin profile you want to scrap')

args = parser.parse_args()

config = yaml.safe_load(open("config.yml"))

firefox_profile_path = config['firefox_profile_path']

profile_soup = get_profile_html(args.linkedin_url, firefox_profile_path)
profile_instance = generate_profile(profile_soup)

print(profile_instance.name)
print(profile_instance.title)
print('Experiences :')
for exp in profile_instance.experience:
    print(f"{exp['title']}, {exp['company']} - {exp['length']}")
print('Education')
for edu in profile_instance.education:
    print(f"{edu['degree']}, {edu['school']} - {edu['years']}")