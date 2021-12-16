'''

from genesis.controllers.search_manager.search_data_model.query_model import query_model
from genesis.controllers.search_manager.search_enums import SEARCH_MODEL_COMMANDS
from genesis.controllers.search_manager.search_model import search_model

m_query_model = query_model()
m_query_model.m_search_query = "Bitcoin generator exploit is the most innovative and fastest bitcoin generator online. - choose amount of - choosing a larger amount will make the exploit take longer to run. - you must input a valid - the exploit was successful "
m_query_model.m_search_type = "all"
m_query_model.m_page_number = 1
m_query_model.m_safe_search = "False"

m_search_model = search_model()
m_status, m_response = m_search_model.invoke_trigger(SEARCH_MODEL_COMMANDS.M_INIT, m_query_model)
print("")

'''
