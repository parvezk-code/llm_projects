from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import BaseMessage

from conf.settings.openai_config import OpenAIConfig


class ChainService:

    def __init__( self, config: OpenAIConfig ) -> None:

        self._config = config
        self._chain = self.createChain()

    def createChain( self ):

        llm = self.getModel()

        # Convert AIMessage → plain string
        output_parser = StrOutputParser()

        prompt = self.createTemplate()

        # Build chain : prompt → llm → parser
        chain = prompt | llm | output_parser

        return chain

    def run( self, system_prompt: str, history: list[BaseMessage], user_input: str ) -> str:

        # Runtime input values
        chain_input = {"system_prompt": system_prompt, "history": history, "user_input": user_input }

        # Run chain with runtime inputs
        result: str = self._chain.invoke( chain_input )

        return result

    def createTemplate( self ):

        # System message template
        system_msg = ( "system", "{system_prompt}" )

        # Previous conversation messages
        history_msg = MessagesPlaceholder( "history" )

        # Current user message template
        user_msg = ( "human", "{user_input}" )

        # All prompt message parts
        prompt_messages = [ system_msg, history_msg, user_msg ]

        # Create prompt template
        prompt = ChatPromptTemplate.from_messages( prompt_messages )

        return prompt

    def getModel( self ):

        key = self._config.openai_api_key
        model = self._config.openai_model

        # LLM wrapper : api key, model, temperature, tokens
        llm = ChatOpenAI( api_key=key, model=model )

        return llm