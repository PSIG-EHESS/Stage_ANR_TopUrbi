# -*- coding: utf-8 -*-
"""1_TopUrbi_Stage_AlcedoToCSVv2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11LtayVVfu8DAwU9grLIh1bvo4mxEmZc1
"""

#Script pour traiter les entrées de lieux les plus repandues qui commencent par le nom de lieu tout en majuscule, par exemple :
# ZIPAQUIRA, Pueblo y Cabeza de partido del Corregimiento de su nombre en el Nuevo Reyno de Granada, es de temperamento frío, pero benigno y sano, situado en una hermosa y agradable llanura, produce con abundancia trigo, maiz, cebada, papas y legumbres, que vende para las demás Provincias, con lo que hace un lucroso comercio en el mercado que celebra cada cinco dias, tiene unas abundantísimas salinas de que saca 20.000 fanegas de sal cada año, su vecindario se compone de mas de 800 vecinos y 80 Indios, fue doctrina de los Religiosos de San Francisco; está 4 leguas al N de Santa Fé. 
# TODO : à traiter les entrées de mots composés, comme par exemple :
# ZELANDA, Nueva) Villa y fuerte de los Holandeses en la Provincia y Colonia de Surinam, situada á la orilla del rio Poumaron en el cabo ó punta de Nassau ó Orange. 

# ça prends presque toutes les varietés des noms composés ^ *[A-Z|Ñ|-]+(\s|\.|,|:|\))+([A-Z|a-z|é|í|ñ|.| ]+) "space c'est optionnel"


from lxml import etree
import csv
import glob
import re
from lxml import html
from bs4 import BeautifulSoup

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

def clean_text(entry):
    "Function used to remove blank new lines"
    entry = entry.replace("\n", "")
    entry = re.sub('\s{2,}', ' ', entry)
    return entry

def get_div(doc):
    data = []
    root = doc.getroot()
    for child in root:
      #print(child.tag, child.attrib)
      for cchild in child:
        #print(cchild)
        for ccchild in cchild:
          #print(ccchild.tag)
          if ccchild.tag == "{http://www.tei-c.org/ns/1.0}div":
            #print(ccchild.text)
            data.append(ccchild)
    return data 

# recupere tous les noms de lieu en maj

def detection_LieuCompose(line):
  # testé sur le site : [A-Z|Ñ|-]+(\s|\.|,|:|\))+([A-Z|a-z|é|í|ñ|.| ]+)
  # old :  ([A-Z|Ñ|-]+(\s|\.|,|:|\))+([A-Z|a-z|é|í|ñ|.| ]+))
  match = re.search(r'^ [A-Z|Ñ|-]+(\s|\.|,|:|\))+([A-Z|a-z|é|í|ñ|.| ]+\))', line, re.DOTALL|re.MULTILINE) #TODO cas particuliers à gérer : 1) "San Bernardo" 2) "ZAND, Puente de)"
  if match:
    return match.group(0)

def detection_nomLieu(line):
  match = re.search(r' ([A-Z|Ñ|-]*)', line, re.DOTALL|re.MULTILINE) #TODO cas particuliers à gérer : 1) "San Bernardo" 2) "ZAND, Puente de)"
  if match:
    return match.group(1)

        
# attrape le type de lieu après le nom en majusc; ex: Pueblo, etc.

def detection_nomLieu_general(line):
  nomcomp = detection_LieuCompose(line)
  #print("lieu compo : "+str(nomcomp))
  if (nomcomp is not None):
    return nomcomp
  else:
    return detection_nomLieu(line)
    
def detection_typeLieu(line):
  match = re.search(r' [A-Z|Ñ|-|À-Ÿ]+(\s|\.|,|:|\))+([A-Z_À-Ÿ][a-z_à-ÿ]+)', line, re.DOTALL|re.MULTILINE) #TODO cas particuliers à gérer : 1) "San Bernardo" 2) "ZAND, Puente de)"
  if match: #regex à vérifier 
    return match.group(2)


#Prends tout le texte dans div

def detection_descLieu(div):
  node = etree.strip_tags(div,'*')
  return div.text


def detection_listLieu(div):
  div_str = etree.tostring(div)
  soup = BeautifulSoup(div_str, "lxml")
  list_tag = [] 
  for j in soup.div.find_all(recursive=False):
    list_tag.append(j)
  #print(list_tag)
  return list_tag


# Prends tous les id's

def detection_entreeLieuID(div):
  div_str = etree.tostring(div)
  soup = BeautifulSoup(div_str, "lxml")
  return soup.div['xml:id']

# Prends tous les settlement's

def detection_settlement(div):
  div_str = etree.tostring(div)
  soup = BeautifulSoup(div_str, "lxml")
  if soup.div.get('settlement'):
    return soup.div['settlement']

## MAIN
from google.colab import drive
drive.mount('/content/drive', force_remount=True)
alcedo_xml = "/content/drive/MyDrive/Colab Notebooks/data/Alcedo/1_Alcedo_XML_Origine"
alcedo_csv = "/content/drive/MyDrive/Colab Notebooks/data/Alcedo/2_Alcedo_conversion_CSV"
if __name__ == "__main__":
    for tome in [1, 2, 3, 4, 5]:
        print(tome)
        with open(alcedo_csv+"/alcedo_tome"+str(tome)+"utf-8.csv", 'w+', newline='', encoding="utf-8") as csvfile:
          parser = etree.XMLParser(remove_blank_text=True)
          doc = etree.parse(alcedo_xml+"/alcedo-"+str(tome)+"-utf8.xml", parser)
          data = get_div(doc)
          writer = csv.writer(csvfile, delimiter='|')
          writer.writerow(['id_lieu','nom_lieu', 'settlement', 'desc_lieu', 'type_lieu', 'list_lieu', 'level1', 'level2'])
          tome = tome + 1
          for div in data:

            level1, level2 = [], []
            for child in div:
              print("level1: "+str(child.tag))
              print("level1: "+str(child.text))
              level1.append(str(child.text) + "|" + str(child.tag) + "|" + str(child.attrib))
              for cchild in child:
                print("level2: "+str(cchild.tag))
                print("level2: "+str(cchild.text)) 
                level2.append(str(cchild.text) + "|" + str(cchild.tag) + "|" + str(cchild.attrib))
                print("")

            list_lieu = detection_listLieu(div)
           
            div_id = detection_entreeLieuID(div)
           
            settlement = detection_settlement(div)
           
            desc_lieu = detection_descLieu(div)
           
            #lieu_compose = detection_LieuCompose(desc_lieu)
            #if (lieu_compose is not None):
            #  print("LIEU COMPOSE: " + str(lieu_compose))
            #nom_lieu = detection_nomLieu(desc_lieu)
            #print("nom_lieu:" + str(nom_lieu))
            nom_lieu = detection_nomLieu_general(desc_lieu)
           
            type_lieu = detection_typeLieu(desc_lieu)
           
            writer.writerow([div_id, nom_lieu, settlement, desc_lieu, type_lieu, str(list_lieu), level1, level2])

#Entrée type à traiter dans un autre script, les cas des entrées homonymes, un exemple :
# Otro Pueblo hay de este nombre en la Cabeza de partido de Huipuxla, y Alcaldía mayor de Tepetango  en Nueva España, tiene 53 familias de Indios. 
# Cependant ils sont déjà récupérés dans les div's

"""A la fin de ce traitement, les tomes en CSV ont été séparés chacun si applicable en deux, l'une pour le contenu principal du tome et l'autre pour les annexes."""