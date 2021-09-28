#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------

#
# Usei "json" para "despejar" a saída do respectivo script em arquivo .json.
import json

#
# "unicodedata" foi usado por mim para limpar caracteres especiais nao regidos sob parametro "UTF-8".
import unicodedata

# We use the "bs4" feature to transform our html into a beautifulsoup object.
# Usamos o recurso "bs4" para podermos transformar / "parsear" html's em objetos "beautifulsoup".
from bs4 import BeautifulSoup

# "pandas" will help us organize our data list.
# "pandas" nos ajudará a estruturar nossas listas de dados .
import pandas as pd

# The "requests" feature will "ask for permission" to the websites.
# "requests" nos ajudarão a "pedir permissão" para entrar nos sites.
import requests

# Wizard Terminate Function
#----------------------------------------------------------------------------------------------------------------------
def wizard_terminate():
    print('\n')
    print('Crawler Process Terminated!!!')
    quit()

# Html Objectification Function
#----------------------------------------------------------------------------------------------------------------------              
def bs_objectify(url_to_objectify):   

    main_url = requests.get(url_to_objectify)

    url_content = main_url.content

    url_parsed = BeautifulSoup(url_content, 'html.parser')
       
    urls_found = url_parsed.findAll('div', attrs={'class': 'dados-agenda'})  

    if(urls_found == []):
        urls_found = url_parsed.findAll('p', attrs={'class': 'callout'})      
    
    return urls_found

# String Clean Up Function
#----------------------------------------------------------------------------------------------------------------------
def special_char_cleanup(string: str) -> str:
    normalized  = unicodedata.normalize('NFD', string)
    return normalized.encode('ascii', 'ignore').decode('utf8')

# General Variables
#----------------------------------------------------------------------------------------------------------------------

# Abaixo está o site inicial, por onde todo o proceso partirá.
start_url = 'https://www.gov.br/ana/pt-br/acesso-a-informacao/agenda-de-autoridades'

# A variável em questão representa o site atual, dos vários sites que o "crawler" percorrerá.
current_url = start_url

# Uma lista com todos os sites úteis encontrados a partir da página inicial.
urls_found_list = bs_objectify(current_url)

# Booleana que retornará a escolha do usuário sobre a criação de um arquivo .json.
create_json = False

create_mongodb_lib = False

# Criação de arquivos .html nesta pasta para visualização offline das urls acessadas (a ser implementada).
#create_offline_view_url_list = False

# Lista de TODOS os sites acessados para visualização offline (a ser implementada).
#offline_view_list = []

# Wizard Behaviour
#----------------------------------------------------------------------------------------------------------------------
print('Crawler Process Initialized!!! \n')

wizard_guide = input('Would you like to START? [y/n]\n')
print('\n')

if(wizard_guide == "n"):
    print('Canceling Crawler Process...\n')
    print('\n')
    wizard_terminate()

if(wizard_guide is None):
    print('Invalid Command!!! \n')
    wizard_terminate()    

wizard_guide = input('Would you like to create .json files? [y/n]\n')
print('\n')

if(wizard_guide == "y"):

    create_json = True    
    print('Warming up the .json files...')    
    print('\n') 

elif(wizard_guide == "n"):
    print('No json file will be created!!!\n')
    print('\n')  

elif(wizard_guide is not None):
    print('Invalid Command!!! \n')
    wizard_terminate()


print('Acquiring Necessary Data...\nThis May Take a While...')
print('\n') 

# Structured Collections
#----------------------------------------------------------------------------------------------------------------------
structured_dict = {
    'Authority Type': '',
    'Agent Name/Occupation': '',    
    'Date': '',
    'Hour': '',
    'Agent Link': ''
}

structured_dict_list = [
    
]

structured_list = []

# Crawler Process
#----------------------------------------------------------------------------------------------------------------------
# Para cada site de autoridade encontrado a partir do inicial, e
# armazenado em uma lista, acessa o proximo site a ser analisado.
for new_url in urls_found_list:

    # Acha o site da autoridade encontrado dentro do site inicial 
    # e o guarda nesta variável para ser acessada futuramente, 
    # repete para cada autoridade encontrada.
    authority_data = new_url.find('a', attrs={'class': 'internal-link'}) 


    # Se houver algum site encontrado, continua o processo...                
    if(authority_data) != None:       
                             
        # Retorna uma lista com todos os sites
        # encontrados dentro do site da autoridade 
        # em questão.
        agents_url_found_list = bs_objectify(authority_data['href'])        
        
        #"Limpa" os caracteres especiais do nome da 
        # autoridade e guarda esse novo dado nesta variável.
        authority_data = special_char_cleanup(authority_data.text)

        # Adiciona o nome da autoridade ao parametro  
        # entre aspas simples correspondente no dicionário.
        structured_dict['Authority Type'] = authority_data       


        # Para cada site de agentes encontrado, a partir do site da autoridade, e
        # armazenado em uma lista, acessa o proximo site a ser analisado (site com agentes).
        for new_agent_url in agents_url_found_list:

            # Guarda nesta variável o nome e a ocupação do agente encontrado no site com os agentes.
            agent_data = new_agent_url.find('a', attrs={'class': 'internal-link'})                        
            
            
            if(agent_data) != None:                 
                 
                # Retorna uma lista com todos os sites objetificados
                # encontrados dentro do site com o nome dos agente 
                # em questão.
                agent_appointment_found_list = bs_objectify(agent_data['href'])  

                # No terminal, printa o dado que está sendo extraído e
                # o link de onde ele está.
                print('\n\nData Acquired: ' + agent_data.text) 
                print('Accessing: ' + agent_data['href'])                         
                   
                # Adiciona o LINK para conferir a agenda do agente ao parametro  
                # entre aspas simples correspondente no dicionário.
                structured_dict['Agent Link'] = agent_data['href'] 

                # "Limpa" os caracteres especiais do nome do agente e de sua 
                # ocupação e guarda esse novo dado nesta variável.
                agent_data = special_char_cleanup(agent_data.text)

                # Adiciona o nome do AGENTE e sua OCUPAÇÃO ao parametro  
                # entre aspas simples correspondente no dicionário.
                structured_dict['Agent Name/Occupation'] = agent_data              
                  

                # Dentro do site objetificado do agente, o "crawler" retornará informações básicas.
                for new_agent_appointment in agent_appointment_found_list:                    

                    # Guarda nesta variável a estrutura "crua" onde está a informação da "data de hoje".
                    agent_appointment_date = new_agent_appointment.find('li', attrs={'class': 'day is-selected has-appointment'})                     

                    # Lista os compromissos encontrados pelo "crawler".
                    agent_appointment_data_list = new_agent_appointment.findAll('div', attrs={'class': 'item-compromisso'})                
                              
                    # Para cada compromisso encontrado e listado, o "crawler" irá
                    # extrair os dados úteis que ali estão.
                    for agent_appointment_data in agent_appointment_data_list:

                        # Guarda em uma variável a estrutura "crua" onde está a informação do local de reunião.    
                        # agent_appointment_title = agent_appointment_data.find('h4', attrs={'class': 'compromisso-titulo'})                                               

                        # Guarda nesta variável a estrutura "crua" onde está a informação do local de reunião.
                        agent_appointment_place = agent_appointment_data.find('div', attrs={'class': 'compromisso-local'})


                        # Se houver horário de início e término da reunião,
                        # tais horários comporão a variável da hora, se não houver, 
                        # apenas o horário de início aparecerá.
                        if(agent_appointment_data.find('time', attrs={'class': 'compromisso-inicio'}) and agent_appointment_data.find('time', attrs={'class': 'compromisso-fim'})) != None:
                                
                            agent_appointment_hour = agent_appointment_data.find('time', attrs={'class': 'compromisso-inicio'}).get_text() + ' - ' + agent_appointment_data.find('time', attrs={'class': 'compromisso-fim'}).get_text()
                                                
                        elif(agent_appointment_data.find('time', attrs={'class': 'compromisso-inicio'})) != None:

                            agent_appointment_hour = agent_appointment_data.find('time', attrs={'class': 'compromisso-inicio'}).get_text()
                                                                    

                        # Se houver DATA de início da reunião, adiciona tal valor 
                        # ao parâmetro correspondente no dicionário.  
                        if(agent_appointment_date) is not None:
                                                  
                            structured_dict['Date'] = agent_appointment_date['data-day']   

                        else:

                            agent_appointment_date = ''  
                        

                        # Se houver HORA de início da reunião, adiciona tal valor 
                        # ao parâmetro correspondente no dicionário.                                            
                        if(agent_appointment_hour) is not None:

                            structured_dict['Hour'] = agent_appointment_hour 

                        else:

                            agent_appointment_hour = '' 


                        # Se houver LOCAL DE REUNIÃO, o nome do local irá para 
                        # o parâmetro correspondente no dicionário, se não houver,
                        # uma mensagem aparecerá no local.
                        if(agent_appointment_place) is not None:

                            agent_appointment_place = special_char_cleanup(agent_appointment_place.text)
                            structured_dict['Appointment Place'] = agent_appointment_place                           
                            structured_list.append([authority_data, agent_data, agent_appointment_date['data-day'], agent_appointment_hour, agent_appointment_place])                                                  
                                                     
                        else: 
                            
                            structured_dict['Appointment Place'] = 'Not Declared' 
                            structured_list.append([authority_data, agent_data, agent_appointment_date['data-day'], agent_appointment_hour, 'Not Declared'])                      


                        # Adiciona uma cópia do dicionário após todas as informações
                        # necessárias terem sido inseridas e parte para adicionar o
                        # dicionário do próximo agente.
                        structured_dict_list.append(structured_dict.copy())                        

                        # (test variable)
                        date = agent_appointment_date['data-day'] 

                        # (hora da execução do "crawler" para compor o nome do arquivo .json)   
                        #hour = ...                                                                           

# List Tabulation                                               
#----------------------------------------------------------------------------------------------------------------------
structured_table = pd.DataFrame(structured_list, columns=['Authority Type', 'Authority Name/Occupation', 'Date', 'Hour', 'Appointment Place'])

# .json Dump Archives
#----------------------------------------------------------------------------------------------------------------------
if(create_json) == True:

    structured_table.to_json('StructuredTable' + date + '.json')

    with open('StructuredDictList' + date + '.json', "w") as outfile:
        json.dump(structured_dict_list, outfile, ensure_ascii=True)

# MongoDB Dump Section
#----------------------------------------------------------------------------------------------------------------------


# Process Finalization
#----------------------------------------------------------------------------------------------------------------------
print("\nCrawler Process Ended!!!")

#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------