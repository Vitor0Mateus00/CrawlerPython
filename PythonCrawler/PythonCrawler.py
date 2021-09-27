import time

#We use the bs4 feature to transform our html into a beautifulsoup object.
#Usamos o recurso "bs4" para podermos transformar / "parsear" html's em objetos "beautifulsoup".
from bs4 import BeautifulSoup

#"pandas" will struct our data list.
#"pandas" nos ajudará a estruturar nossas listas de dados .
import pandas as pd

#The "requests" feature will "ask for permission" to the websites.
#"requests" nos ajudarão a "pedir permissão" para entrar nos sites.
import requests



print('Crawler Process Initialized!!! \n')



def Terminate():
    print('\n')
    print('Crawler Process Terminated!!!')
    quit()

               
def bs_objectify(url_to_objectify):   

    main_url = requests.get(url_to_objectify)

    url_content = main_url.content

    url_parsed = BeautifulSoup(url_content, 'html.parser')

    urls_found = url_parsed.findAll('p', attrs={'class': 'callout'})       

    return urls_found


wizard_guide = input("Would you like to continue? [y/n]\n")
print('\n')

if(wizard_guide == "y"):
    # wizard_guide = input("Would you like to finish? [y/n]\n")
    print("Acquiring Necessary Data...\nThis May Take a While...")
    print('\n')  
    

elif(wizard_guide == "n"):
    print("Canceling Crawler Process...\n")
    Terminate()

elif(wizard_guide != None):
    print("Invalid Command!!! \n")
    Terminate()



start_url = 'https://www.gov.br/ana/pt-br/acesso-a-informacao/agenda-de-autoridades'

current_url = start_url


urls_found_list = bs_objectify(current_url)




#Todos os "URL's" que comporão o caminho a ser percorrido pelo "crawler".
url_list = []

authority_data_list = []

#Os agentes a serem encontrados pelo "crawler".
agent_data_list = []

#As agendas dos agentes a serem encontradas pelo "crawler".
agent_agenda_data_list = []



#O "URL" inicial, daqui todo o processo partirá.


# urls_lenght = len(urls_found_list) 

url_count = 0
agent_count = 0
agent_agenda_count = 0
authority_count = 0
    
for new_url in urls_found_list:

    url = authority_data = new_url.find('a', attrs={'class': 'internal-link'})    
                    
    if(url) != None:
        
        url_count += 1
        authority_data_list.append([authority_data.text, authority_data['href'], authority_count])
        #Nome/agenda da autoridade
        #Link da autoridade
        url_list.append([url['href'].replace('\\', ''), url_count])             


        agents_url_found_list = bs_objectify(authority_data['href']) 
        

        for new_agent_url in agents_url_found_list:

            agent_url = agent_data = new_agent_url.find('a', attrs={'class': 'internal-link'}) 
            #Nome/cargo do agente
            #Link do agente
            if(agent_url) != None:  
                agent_count += 1
                agent_data_list.append([agent_data.text ,agent_url['href'], agent_count]) 
            
                agents_agenda_url_found_list = bs_objectify(agent_url['href'])


            for new_agent_agenda_url in agents_agenda_url_found_list:

                agent_agenda_url = agent_agenda_date = new_agent_agenda_url.find('li', attrs={'class': 'day is-selected has-appointment'})     
                #Data do evento
                #Nome do evento
                #Local do evento              
                
                if(agent_agenda_date) != None:
                    
                    agent_agenda_date_name = agent_agenda_url['data-day']
                    agent_agenda_event_list = new_agent_agenda_url.findAll('ul', attrs={'class': 'list-compromissos'})

                    for agent_appointment in agent_agenda_event_list:
                        
                        agent_agenda_event_name = agent_appointment.find('h4', attrs={'class': 'compromisso-titulo'})

                        agent_agenda_count += 1
                        agent_agenda_data_list.append([agent_agenda_event_name.text, agent_agenda_date_name.text ,agent_agenda_count, agent_agenda_url['href']])          
       




authority_table = pd.DataFrame(authority_data_list, columns=['NAME', 'LINK', 'NUMBER'])
agent_table = pd.DataFrame(agent_data_list, columns=['NAME', 'LINK', 'NUMBER'])
agent_agenda_table = pd.DataFrame(agent_agenda_data_list, columns=['NOME DO EVENTO', 'DATA DO EVENTO', 'HORÁRIO DO EVENTO', 'LOCAL DO EVENTO', 'LINK'])


'''... .to_json(str(agent_name) + 'Agenda' + '.json')'''
authority_table.to_json('Authorities.json')
agent_table.to_json('Agents.json')
agent_agenda_table.to.json('AgentsAgenda.json')


print(authority_table)
print(agent_table)
print(agent_agenda_table)
print("\nCrawler Process Successfully Ended!!!")