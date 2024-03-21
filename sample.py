import logging
import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Tool, Part, Content, ChatSession
from services.flight_manager import search_flights

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

project = "gemini-flights"
vertexai.init(project=project)

# Define Tool
get_search_flights = generative_models.FunctionDeclaration(
    name="get_search_flights",
    description="Tool for searching a flight with origin, destination, and departure date",
    parameters={
        "type": "object",
        "properties": {
            "origin": {
                "type": "string",
                "description": "The airport of departure for the flight given in airport code such as LAX, SFO, BOS, etc."
            },
            "destination": {
                "type": "string",
                "description": "The airport of destination for the flight given in airport code such as LAX, SFO, BOS, etc."
            },
            "departure_city": {
                "type": "string",
                "description": "The city of departure for the flight"
            },
            "departure_date": {
                "type": "string",
                "format": "date",
                "description": "The date of departure for the flight in YYYY-MM-DD format"
            },
            "return_date": {
                "type": "string",
                "format": "date",
                "description": "The date of return for the flight in YYYY-MM-DD format"
            },
            "passengers": {
                "type": "integer",
                "description": "Number of passengers for the flight"
            },
            "travel_class": {
                "type": "string",
                "enum": ["economy", "business", "first"],
                "description": "The class of the flight (economy, business, first)"
            },
            "budget_range": {
                "type": "object",
                "properties": {
                    "min": {"type": "number", "description": "Minimum budget for the flight"},
                    "max": {"type": "number", "description": "Maximum budget for the flight"}
                },
                "description": "Budget range for the flight"
            },
        },
        "required": [
            "origin",
            "destination",
            "departure_date",
            "passengers",
            "travel_class",
            "budget_range"
        ]
    },
)

# Define tool and model with tools
search_tool = generative_models.Tool(
    function_declarations=[get_search_flights],
)

config = generative_models.GenerationConfig(temperature=0.4)
# Load model with config
model = GenerativeModel(
    "gemini-pro",
    tools=[search_tool],
    generation_config=config
)

# Helper function to unpack responses
def handle_response(response):
    logging.debug('Handling response...')
    try:
        # Check for function call with intermediate step, always return response
        if response.candidates[0].content.parts[0].function_call.args:
            # Function call exists, unpack and load into a function
            response_args = response.candidates[0].content.parts[0].function_call.args
            
            function_params = {}
            for key in response_args:
                value = response_args[key]
                function_params[key] = value
            
            results = search_flights(**function_params)
            
            if results:
                intermediate_response = chat.send_message(
                    Part.from_function_response(
                        name="get_search_flights",
                        response=results
                    )
                )
                
                return intermediate_response.candidates[0].content.parts[0].text
            else:
                return "Search Failed"
        else:
            # Return just text
            return response.candidates[0].content.parts[0].text
    except Exception as e:
        logging.error(f'Error handling response: {e}')

# Helper function to display and send streamlit messages
def llm_function(chat: ChatSession, query):
    logging.debug('Running llm_function...')
    try:
        response = chat.send_message(query)
        output = handle_response(response)
        
        with st.chat_message("model"):
            st.markdown(output)
        
        st.session_state.messages.append(
            {
                "role": "user",
                "content": query
            }
        )
        st.session_state.messages.append(
            {
                "role": "model",
                "content": output
            }
        )
    except Exception as e:
        logging.error(f'Error in llm_function: {e}')

st.title("Gemini Flights")

chat = model.start_chat()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display and load to chat history
for index, message in enumerate(st.session_state.messages):
    try:
        content = Content(
                role=message["role"],
                parts=[Part.from_text(message["content"])]
            )
        
        if index != 0:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        chat.history.append(content)
    except Exception as e:
        logging.error(f'Error loading chat history: {e}')

# For Initial message startup
if len(st.session_state.messages) == 0:
    try:
        # Invoke initial message
        initial_prompt = "Introduce yourself as a flights management assistant, ReX, powered by Google Gemini and designed to search/book flights. You use emojis to be interactive. For reference, the year for dates is 2024"

        llm_function(chat, initial_prompt)
    except Exception as e:
        logging.error(f'Error in initial message: {e}')

# For capture user input
query = st.chat_input("Gemini Flights")

if query:
    try:
        with st.chat_message("user"):
            st.markdown(query)
        llm_function(chat, query)
    except Exception as e:
        logging.error(f'Error processing user input: {e}')
