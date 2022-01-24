from Genesis.controllers.view_managers.user_views.search_manager.search_data_model.query_model import query_model
from Genesis.controllers.view_managers.user_views.search_manager.search_enums import SEARCH_MODEL_COMMANDS
from Genesis.controllers.view_managers.user_views.search_manager.search_model import search_model

m_query_model = query_model()
m_query_model.m_search_query = "mexico"
m_search_model = search_model()

m_status, m_response = m_search_model.invoke_trigger(SEARCH_MODEL_COMMANDS.M_INIT, m_query_model)
