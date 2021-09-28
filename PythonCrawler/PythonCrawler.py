#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#We use the bs4 feature to transform our html into a beautifulsoup object.
#Usamos o recurso "bs4" para podermos transformar / "parsear" html's em objetos "beautifulsoup".
import json
from bs4 import BeautifulSoup

#"pandas" will struct our data list.
#"pandas" nos ajudará a estruturar nossas listas de dados .
import pandas as pd

#The "requests" feature will "ask for permission" to the websites.
#"requests" nos ajudarão a "pedir permissão" para entrar nos sites.
import requests

#----------------------------------------------------------------------------------------------------------------------
def wizard_terminate():
    print('\n')
    print('Crawler Process Terminated!!!')
    quit()

#----------------------------------------------------------------------------------------------------------------------              
def bs_objectify(url_to_objectify):   

    main_url = requests.get(url_to_objectify)

    url_content = main_url.content

    url_parsed = BeautifulSoup(url_content, 'html.parser')
       
    urls_found = url_parsed.findAll('div', attrs={'class': 'dados-agenda'})  

    if(urls_found == []):
        urls_found = url_parsed.findAll('p', attrs={'class': 'callout'})      
    

    return urls_found

#Wizard behaviour
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

wizard_guide = input('Would you like to create a .json file? [y/n]\n')
print('\n')

if(wizard_guide == "y"):

    # json_create = True    
    print('Warming up the .json file...')    
    print('\n') 

elif(wizard_guide is not None):
    print('Invalid Command!!! \n')
    wizard_terminate()

elif(wizard_guide == "n"):
    print('No json file will be created!!!\n')
    print('\n')       


print('Acquiring Necessary Data...\nThis May Take a While...')
print('\n') 

#General Variables
#----------------------------------------------------------------------------------------------------------------------
start_url = 'https://www.gov.br/ana/pt-br/acesso-a-informacao/agenda-de-autoridades'

current_url = start_url

urls_found_list = bs_objectify(current_url)


authority_data_list = []

#Os agentes a serem encontrados pelo "crawler".
agent_data_list = []

#As agendas dos agentes a serem encontradas pelo "crawler".
agent_agenda_data_list = []

#----------------------------------------------------------------------------------------------------------------------

structured_dict = {
    'Authority Type': '',
    'Agent Name/Occupation': '[]',
    'Date': '',
    'Hour': '',
    'Appointment place': ''
}

structured_dict_list = [{
    
}]

structured_list = []

#Crawler Process
#----------------------------------------------------------------------------------------------------------------------
for new_url in urls_found_list:

    authority_data = new_url.find('a', attrs={'class': 'internal-link'}) 

                    
    if(authority_data) != None:
        
        
        authority_data_list.append([authority_data.text, authority_data['href']])
        #Nome/agenda da autoridade
        #Link da autoridade                

        agents_url_found_list = bs_objectify(authority_data['href']) 
        
        structured_dict['Authority Type'] = authority_data.text
        

        for new_agent_url in agents_url_found_list:

            agent_data = new_agent_url.find('a', attrs={'class': 'internal-link'}) 
            #Nome/cargo do agente
            #Link do agente            

            if(agent_data) != None:  
                
                agent_data_list.append([agent_data.text ,agent_data['href']]) 
            
                agent_appointment_url_found_list = bs_objectify(agent_data['href'])  

                print('\n\nData Acquired: ' + agent_data.text) 
                print('Accessing: ' + agent_data['href'])

                structured_dict['Agent Name/Occupation'] = agent_data.text             
                   
                # print(structured_dict) 


                for new_agent_appointment in agent_appointment_url_found_list:                    

                    agent_appointment_date = new_agent_appointment.find('li', attrs={'class': 'day is-selected has-appointment'})  

                    agent_appointment_data_local = new_agent_appointment.findAll('div', attrs={'class': 'item-compromisso'})                
                              
                     
                    for agent_appointment_data in agent_appointment_data_local:

                        agent_appointment_title = agent_appointment_data.find('h4', attrs={'class': 'compromisso-titulo'})                                               

                        agent_appointment_place = agent_appointment_data.find('div', attrs={'class': 'compromisso-local'})


                        if(agent_appointment_data.find('time', attrs={'class': 'compromisso-inicio'}) and agent_appointment_data.find('time', attrs={'class': 'compromisso-fim'})) != None:

                            agent_appointment_hour = agent_appointment_data.find('time', attrs={'class': 'compromisso-inicio'}).get_text() + ' - ' + agent_appointment_data.find('time', attrs={'class': 'compromisso-fim'}).get_text()
                        
                        elif(agent_appointment_data.find('time', attrs={'class': 'compromisso-inicio'})) != None:

                            agent_appointment_hour = agent_appointment_data.find('time', attrs={'class': 'compromisso-inicio'}).get_text()

                        
                        if(agent_appointment_date) is None:

                            agent_appointment_date = ''                             
                        
                        
                        if(agent_appointment_hour) is None:

                            agent_appointment_hour = '' 


                        if(agent_appointment_place) is not None: 

                            structured_list.append([authority_data.text, agent_data.text, agent_appointment_date['data-day'], agent_appointment_hour, agent_appointment_place.text])  
                            structured_dict['Date'] = agent_appointment_date['data-day']
                            structured_dict['Hour'] = agent_appointment_hour
                            structured_dict['Appointment Place'] = agent_appointment_place.text 
                            

                        elif(agent_appointment_place) is None:

                            structured_list.append([authority_data.text, agent_data.text, agent_appointment_date['data-day'], agent_appointment_hour, ''])
                            structured_dict['Date'] = agent_appointment_date['data-day']
                            structured_dict['Hour'] = agent_appointment_hour
                            structured_dict['Appointment Place'] = '' 

                        structured_dict_list.append([structured_dict])
                        date = agent_appointment_date['data-day']
                        # print(structured_dict_list)                                                           

                        
                    
    

#----------------------------------------------------------------------------------------------------------------------
structured_table = pd.DataFrame(structured_list, columns=['Authority Type', 'Authority Name/Occupation', 'Date', 'Hour', 'Appointment Place'])
#----------------------------------------------------------------------------------------------------------------------
# ... .to_json(str(agent_name) + 'Agenda' + '.json')
# authority_table.to_json('Authorities.json')
# agent_table.to_json('Agents.json')
# agent_agenda_table.to_json('AgentsAgenda.json')
structured_table.to_json('StructuredTable' + date + '.json')
with open('StructuredDictList' + date + '.json', "w") as f:
    json.dump(structured_dict_list, f)

#----------------------------------------------------------------------------------------------------------------------
print(structured_list)
# print(authority_table)
# print(agent_table)
# print(agent_agenda_table)
print("\nCrawler Process Successfully Ended!!!")
#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------