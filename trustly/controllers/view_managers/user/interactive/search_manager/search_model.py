from app_manager.elastic_manager.elastic_controller import elastic_controller
from app_manager.elastic_manager.elastic_enums import ELASTIC_CRUD_COMMANDS, ELASTIC_REQUEST_COMMANDS
from trustly.controllers.constants.constant import CONSTANTS
from trustly.controllers.constants.strings import GENERAL_STRINGS
from trustly.controllers.view_managers.user.interactive.search_manager.search_enums import SEARCH_CALLBACK, SEARCH_MODEL_TOKENIZATION_COMMANDS, SEARCH_SESSION_COMMANDS, SEARCH_MODEL_COMMANDS
from trustly.controllers.view_managers.user.interactive.search_manager.search_session_controller import search_session_controller
from trustly.controllers.view_managers.user.interactive.search_manager.spell_checker import spell_checker
from trustly.controllers.view_managers.user.interactive.search_manager.tokenizer import tokenizer
from app_manager.request_manager.request_handler import request_handler


class search_model(request_handler):

    # Private Variables
    __instance = None
    __m_session = None
    __m_spell_checker = None
    __m_tokenizer = None

    # Initializations
    def __init__(self):
        self.__m_session = search_session_controller()
        self.__m_tokenizer = tokenizer()
        self.__m_spell_checker = spell_checker()

    def __parse_filtered_documents(self, p_paged_documents, documents_per_page=15):
        mRelevanceListData = []
        mDescription = set()
        total_pages = 0

        try:
            # Extract the total number of hits from the response
            total_hits = p_paged_documents.get('hits', {}).get('total', {}).get('value', 0)

            # Calculate total pages
            if total_hits > 0:
                total_pages = total_hits / CONSTANTS.S_SETTINGS_SEARCHED_DOCUMENT_SIZE

            m_result_final = p_paged_documents.get('hits', {}).get('hits', [])

            for m_document in m_result_final:
                m_service = m_document.get('_source', None)
                if not m_service:
                    continue

                m_service['m_sub_host'] = m_service.get('m_sub_host', '/')
                m_service['m_host'] = m_service.get('m_host', '')

                m_content_preview = m_service.get("m_content", "")[:500]
                if type(m_content_preview) is not list and m_content_preview in mDescription:
                    continue
                else:
                    if type(m_content_preview) is not list:
                        mDescription.add(m_content_preview)
                    else:
                        for item in m_content_preview:
                            mDescription.add(item)

                mRelevanceListData.append(m_service)

            content_suggestions = p_paged_documents.get('suggest', {}).get('content_suggestion', [])

            return mRelevanceListData, content_suggestions, total_pages

        except Exception as e:
            print("Error parsing filtered documents:", e)
            return mRelevanceListData, [], total_pages

    def __check_hate_query(self, p_query):
        p_query = p_query.lower()
        for item in ["2g1c", "acrotomophilia", "anal", "anilingus", "anus", "apeshit", "arsehole", "ass", "asshole", "assmunch", "erotic", "autoerotic", "babeland", "baby batter", "baby juice", "ball gag", "ball gravy", "ball kicking", "ball licking", "ball sack", "ball sucking", "bangbros", "bangbus", "bareback", "barely legal", "barenaked", "bastard", "bastardo", "bastinado", "bbw", "bdsm", "beaner", "beaners", "beaver cleaver", "beaver lips", "beastiality", "bestiality", "big black", "breasts", "knockers", "tits", "bimbos", "birdlock", "bitch", "bitches", "black cock", "blonde action", "blonde on blonde action", "blowjob", "blow job", "blow your load", "blue waffle", "blumpkin", "bollocks", "bondage", "boner", "boob", "boobs", "booty", "brown showers", "brunette action", "bukkake", "bulldyke", "bullet vibe", "bullshit", "bung hole", "bunghole", "busty", "butt", "buttcheeks", "butthole", "camel toe", "camgirl", "camslut", "camwhore", "carpet muncher", "carpetmuncher", "chocolate rosebuds", "cialis", "circlejerk", "cleveland steamer", "clit", "clitoris", "clover clamps", "clusterfuck", "cock", "cocks", "coprolagnia", "coprophilia", "cornhole", "coon", "coons", "creampie", "cum", "cumming", "cumshot", "cumshots", "cunnilingus", "cunt", "darkie", "date rape", "daterape", "deep throat", "deepthroat", "dendrophilia", "dick", "dildo", "dingleberry", "dingleberries", "dirty pillows", "dirty sanchez", "doggie style", "doggiestyle", "doggy style", "doggystyle", "dog style", "dolcett", "domination", "dominatrix", "dommes", "donkey punch", "double dong", "double penetration", "dp action", "dry hump", "dvda", "eat my ass", "ecchi", "ejaculation", "erotic", "erotism", "escort", "eunuch", "fag", "faggot", "fecal", "felch", "fellatio", "feltch", "female squirting", "femdom", "figging", "fingerbang", "fingering", "fisting", "foot fetish", "footjob", "frotting", "fuck", "fuck buttons", "fuckin", "fucking", "fucktards", "fudge packer", "fudgepacker", "futanari", "gangbang", "gang bang", "gay sex", "genitals", "giant cock", "girl on", "girl on top", "girls gone wild", "goatcx", "goatse", "god damn", "gokkun", "golden shower", "goodpoop", "goo girl", "goregasm", "grope", "group sex", "g-spot", "guro", "hand job", "handjob", "hard core", "hardcore", "hentai", "homoerotic", "honkey", "hooker", "horny", "hot carl", "hot chick", "how to kill", "how to murder", "huge fat", "humping", "incest", "intercourse", "jack off", "jail bait", "jailbait", "jelly donut", "jerk off", "jigaboo", "jiggaboo", "jiggerboo", "jizz", "juggs", "kike", "kinbaku", "kinkster", "kinky", "knobbing", "leather restraint", "leather straight jacket", "lemon party", "livesex", "lolita", "lolli", "lovemaking", "make me come", "male squirting", "masturbate", "masturbating", "masturbation", "menage a trois", "milf", "missionary position", "mong", "motherfucker", "mound of venus", "mr hands", "muff diver", "muffdiving", "nambla", "nawashi", "negro", "neonazi", "nigga", "nigger", "nig nog", "nimphomania", "nipple", "nipples", "nsfw", "nsfw images", "nude", "nudity", "nutten", "nympho", "nymphomania", "octopussy", "omorashi", "one cup two girls", "one guy one jar", "orgasm", "orgy", "paedophile", "paki", "panties", "panty", "pedobear", "pedophile", "cuck", "pegging", "penis", "phone sex", "piece of shit", "pikey", "pissing", "piss pig", "pisspig", "playboy", "pleasure chest", "pole smoker", "ponyplay", "poof", "poon", "poontang", "punany", "poop chute", "poopchute", "porn", "porno", "pornography", "prince albert piercing", "pthc", "pubes", "pussy", "queaf", "queef", "quim", "raghead", "raging boner", "rape", "raping", "rapist", "rectum", "reverse cowgirl", "rimjob", "rimming", "rosy palm", "rosy palm and her 5 sisters", "rusty trombone", "sadism", "santorum", "scat", "schlong", "scissoring", "semen", "sex", "sexcam", "sexo", "sexy", "sexual", "sexually", "sexuality", "shaved beaver", "shaved pussy", "shemale", "shibari", "shit", "shitblimp", "shitty", "shota", "shrimping", "skeet", "slanteye", "slut", "s&m", "smut", "snatch", "snowballing", "sodomize", "sodomy", "spastic", "spic", "splooge", "splooge moose", "spooge", "spread legs", "spunk", "strap on", "strapon", "strappado", "strip club", "style doggy", "suck", "sucks", "suicide girls", "sultry women", "swastika", "swinger", "tainted love", "taste my", "tea bagging", "threesome", "throating", "thumbzilla", "tied up", "tight white", "tit", "tits", "titties", "titty", "tongue in a", "topless", "tosser", "towelhead", "tranny", "tribadism", "tub girl", "tubgirl", "tushy", "twat", "twink", "twinkie", "two girls one cup", "undressing", "upskirt", "urethra play", "urophilia", "vagina", "venus mound", "viagra", "vibrator", "violet wand", "vorarephilia", "voyeur", "voyeurweb", "voyuer", "vulva", "wank", "wetback", "wet dream", "white power", "whore", "worldsex", "wrapping men", "wrinkled starfish", "xx", "xxx", "yaoi", "yellow showers", "yiffy", "zoophilia"]:
            if item in p_query:
                return "True"
        return "False"


    def __query_results(self, p_data):
        m_query_model = self.__m_session.invoke_trigger(SEARCH_SESSION_COMMANDS.INIT_SEARCH_PARAMETER, [p_data])
        if m_query_model.m_search_query == GENERAL_STRINGS.S_GENERAL_EMPTY:
           return False, None

        m_status, m_documents = elastic_controller.get_instance().invoke_trigger(ELASTIC_CRUD_COMMANDS.S_READ, [ELASTIC_REQUEST_COMMANDS.S_SEARCH,[m_query_model],[None]])
        m_parsed_documents, m_suggestions_content, total_pages = self.__parse_filtered_documents(m_documents)

        m_query_model.set_total_documents(len(m_parsed_documents))

        m_query_model.set_hate_query(self.__check_hate_query(m_query_model.m_search_query))
        m_context, m_status = self.__m_session.invoke_trigger(SEARCH_SESSION_COMMANDS.M_INIT, [m_parsed_documents, m_query_model, total_pages])
        m_context[SEARCH_CALLBACK.M_QUERY_ERROR_URL], m_context[SEARCH_CALLBACK.M_QUERY_ERROR] = self.__m_spell_checker.generate_suggestions(m_query_model.m_search_query, m_suggestions_content)

        return m_status, m_context

    def __init_page(self, p_data):
        mStatus, mResult = self.__query_results(p_data)
        return mStatus, mResult

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == SEARCH_MODEL_COMMANDS.M_INIT:
            return self.__init_page(p_data)
