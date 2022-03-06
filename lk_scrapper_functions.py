from selenium import webdriver
from bs4 import BeautifulSoup
import time
import unicodedata
import warnings

class Profile:

    '''A class used to represent a profile

    ---

    Attributes:
    name : str
    title : str
    experience : list
    education : list

    Methods:
    add_xp (self, company, title, length) : adds an experience to the experience attribute
    add_edu (self, school, degree='Degree not specified', years='Years not specified') : adds an education to the education attribute
    '''

    def __init__(self, name, title):

        '''Parameters :
        name : str - a string of the name on the linkedin profile
        title : str - a string of the title displayed at the top of the linkedin profile
        '''
        
        self.experience = []
        self.education = []
        self.name = name
        self.title = title
    def add_xp(self, company, title, length):

        '''Adds an experience to the experience attribute

        ---

        Arguments :
        company : str - A string of the company name
        title : str - A string of the title
        length : str - A string of the length
        '''

        xp = {}
        xp['company'] = company
        xp['title'] = title
        xp['length'] = length
        self.experience.append(xp)

    def add_ed(self, school, degree='Degree not specified', years='Years not specified'):

        '''Adds an education to the education attribute

        ---

        Arguments :
        school : str - A string of the school name
        degree : str - A string of the degree
        years : str - A string of the years
        '''

        ed = {}
        ed['school'] = school
        ed['degree'] = degree
        ed['years'] = years
        self.education.append(ed)

def get_profile_html(url_profile, firefox_profile_path):

    '''Given a linkedin url and a path to a firefox profile where a user is logged in on linkedin, returns the html of the linkedin profile corresponding to the linkedin url.
    ---

    Arguments :
    url_profile : string - the url of the profile you want to scrap
    firefox_profile_path : string - a raw string representing the path to the firefox profile where a user is logged in

    Returns :
    bs4.BeautifulSoup of the scrapped profile
    '''

    # This raises a deprecation warning but the suggested replacement fails to keep persistent cookies
    # and therefore does not enable us to be logged in on Linkedin and to see all profiles

    with warnings.catch_warnings():
        warnings.simplefilter('ignore', DeprecationWarning)
        fp = webdriver.FirefoxProfile(firefox_profile_path)
        driver = webdriver.Firefox(firefox_profile=fp)
    driver.get(url_profile)
    scroll_pause_time = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    driver.execute_script("window.scrollTo(0, 0);")

    html = driver.page_source
    profile_soup = BeautifulSoup(html, 'html.parser')

    driver.close()

    return profile_soup

def generate_profile(profile_soup):

    '''Given a bs4.BeautifulSoup of a Linkedin profile, returns an instance of the Profile class.

    ---
    Arguments :
    bs4.BeautifulSoup of the scrapped profile

    Returns :
    An instance of the Profile class
    '''

    name = profile_soup.find('h1', {'class': 'text-heading-xlarge inline t-24 v-align-middle break-words'}).getText()
    title = profile_soup.find('div', {'class': 'text-body-medium break-words'}).getText().strip()

    sections = profile_soup.find_all('section', {'class': 'artdeco-card ember-view break-words pb3 mt4'})

    profile = Profile(name, title)

    for section in sections :
        category = section.find('div', {'class': 'pv-profile-card-anchor'}).get('id')
        if category == 'experience':
            boxes = section.find_all('div', {'class': 'pvs-entity pvs-entity--padded pvs-list__item--no-padding-when-nested'})
            for box in boxes :
                multiple_post = False
                # This is to handle the case in which the scrapped profile had held multiple posts in the same company, which has a page
                if box.find('span', {'class': 't-bold mr1 hoverable-link-text'}):
                    cl = 't-bold mr1 hoverable-link-text'
                    multiple_post = True
                # This is to handle the case in which the scrapped profile had held multiple posts in the same company, which does not have a page
                elif len(box.find_all('span', {'class': 't-bold mr1'})) > 1:
                    cl = 't-bold mr1'
                    multiple_post = True
                else :
                    pass
                if multiple_post:
                    company_double = box.find('span', {'class': cl}).getText().strip()
                    company = company_double[:int(len(company_double)/2)]
                    postes = box.find_all('div', {'class': 'display-flex flex-column full-width align-self-center'})
                    for post in postes[1:] :
                        title_double = post.find('span', {'class': cl}).getText().strip()
                        title = title_double[:int(len(title_double)/2)]
                        length_double = post.find('span', {'class' : 't-14 t-normal t-black--light'}).getText().strip()
                        length = unicodedata.normalize('NFKD', length_double[:int(len(length_double)/2)]).split('·')[1].strip()
                        profile.add_xp(company, title, length)
                        
                # This is to handle the case where the scrapped profile has only held one title in the company
                else :
                    title_double = box.find('span', {'class': 't-bold mr1'}).getText().strip()
                    title = title_double[:int(len(title_double)/2)]
                    company_double = box.find('span', {'class': 't-14 t-normal'}).getText().strip()
                    company = company_double[:int(len(company_double)/2)]
                    length_double = box.find('span', {'class' : 't-14 t-normal t-black--light'}).getText().strip()
                    length = unicodedata.normalize('NFKD', length_double[:int(len(length_double)/2)]).split('·')[1].strip()
                    profile.add_xp(company, title, length)
            
        elif category == 'education':
            boxes = section.find_all('div', {'class': 'pvs-entity pvs-entity--padded pvs-list__item--no-padding-when-nested'})
            for box in boxes :
                try :
                    school_double = box.find('span', {'class': 't-bold mr1 hoverable-link-text'}).getText().strip()
                except :
                    school_double = box.find('span', {'class': 't-bold mr1'}).getText().strip()
                school = school_double[:int(len(school_double)/2)]
                degree_double = box.find('span', {'class': 't-14 t-normal'}).getText().strip()
                degree = degree_double[:int(len(degree_double)/2)]
                years_double = box.find('span', {'class' : 't-14 t-normal t-black--light'}).getText().strip()
                years = years_double[:int(len(years_double)/2)]
                profile.add_ed(school, degree, years)

    return profile