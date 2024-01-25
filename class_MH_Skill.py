from bs4 import BeautifulSoup
import requests
from lxml import html
import re

class MonsterHunterSkill:
    def __init__(self, skill_name):
        # Initialization method called when an instance is created
        self.url = self.get_skill_url(skill_name)
        self.name = self.get_skill_name()
        self.lvl_list = self.organize_lvl_list()
        self.equip_list = self.get_equip_with_skill()

    def get_skill_url(self, skill_name):
        # Retrieves the URL for a given skill name from the Kiranico website
        url = 'https://mhworld.kiranico.com/en/skilltrees'
        html_content = requests.get(url).content
        soup = BeautifulSoup(html_content, 'html.parser')
        skill_element = soup.find(lambda tag: tag.name == 'a' and skill_name in tag.text.lower())

        if skill_element:
            skill_url = skill_element.get('href').strip()
            return skill_url

    def get_skill_name(self):
        # Retrieves the name of the skill from the skill's webpage
        html_content = requests.get(self.url).content
        tree = html.fromstring(html_content)
        skill_h5 = tree.xpath('/html/body/div[2]/div/div/div[3]/div[3]/div[1]/div[2]/div/div[1]/div[1]/h5')[0].text_content().strip()
        return skill_h5.rstrip()

    def get_skill_level_list(self):
        # Retrieves the skill level list from the skill's webpage
        html_content = requests.get(self.url).content
        soup = BeautifulSoup(html_content, 'html.parser')
        skill_level_element = soup.find('div', {'class': 'col-lg-12'})
        list_lvl_description = []
        for tr in skill_level_element.find_all('tr'):
            td_content = [td.get_text() for td in tr.find_all('td')]
            list_lvl_description.append(td_content)
        return list_lvl_description

    def get_equip_with_skill(self):
        # Retrieves a list of equipment with the skill from the skill's webpage
        html_content = requests.get(self.url).content
        soup = BeautifulSoup(html_content, 'html.parser')
        skill_equip_element = soup.find('div', {'class': 'table-responsive'})
        lista_conteudo_tr = []
        for tr in skill_equip_element.find_all('tr'):
            td_content = [td.get_text() for td in tr.find_all('td')]
            cleaned_strings = [re.sub(r'\s+', ' ', s.strip().replace('\n', '')) for s in td_content]
            cleaned_strings_with_space_validator = []
            for s in cleaned_strings:
                if re.search(r'\d\b', s):
                    s = re.sub(r'(\d)(?!\d)', r'\1 ', s)
                cleaned_strings_with_space_validator.append(s)
            lista_conteudo_tr.append(cleaned_strings_with_space_validator)
        return lista_conteudo_tr

    def organize_lvl_list(self):
        # Organizes the skill level list by modifying the format
        organized_list = []
        for lst in self.lvl_list[1:]:
            temp_list = []
            for index, item in enumerate(lst[0:-4]):
                if index % 2 == 0:
                    temp_list.append(item)
                else:
                    temp_list.append(item[:-2])
            organized_list.append(temp_list)
        return organized_list

# Create an instance of the MonsterHunterSkill class
skill_instance = MonsterHunterSkill(input('Digite o nome da skill: '))

# Access attributes of the skill instance
print("Skill URL:", skill_instance.url)
print('=´-`'*20)
print("Skill Name:", skill_instance.name)
print('=´-`'*20)
print("Skill Level List:", skill_instance.lvl_list)
print('=´-`'*20)
print("Equipment List with Skill:", skill_instance.equip_list)
print('=´-`'*20)
print("Organized Skill Level List:\n", skill_instance.organize_lvl_list())
