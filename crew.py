import os
from textwrap import dedent
from dotenv import load_dotenv

from crewai import Crew
from crewai import LLM

from agents import AnthemAIAgents
from tasks import AnthemAITasks

load_dotenv()


class AnthomAICrew:
    
    # Change the URL if you are using another port
    print("\nKeys:\n")
    LLM = LLM(
        api_key=os.environ.get("LLM_API_KEY"),
        model=os.environ.get("LLM_MODEL"),
        base_url=os.environ.get("LLM_BASE_URL")
    )

    SUNO_API_KEY = os.environ.get("SUNO_API_KEY")

    
    def __init__(self, topic: str, genre: str):
        self.topic = topic
        self.genre = genre
        
    def run(self):
        
        agents = AnthemAIAgents(
            genre=self.genre,
            llm=self.LLM,
            api_key=self.SUNO_API_KEY)
        
        tasks = AnthemAITasks()
        
        web_researcher_agent = agents.web_researcher_agent()
        lyrics_creator_agent = agents.lyrics_creator_agent()
        song_generator_agent = agents.song_generator_agent()
        
        web_research_task = tasks.web_research_task(
            agent=web_researcher_agent, 
            topic=self.topic
        )
        lyrics_creation_task = tasks.lyrics_creation_task(
            agent=lyrics_creator_agent, 
            topic=self.topic, 
            genre=self.genre
        )
        song_generation_task = tasks.song_generation_task(
            agent=song_generator_agent
        )
        
        crew = Crew(
            agents=[
                web_researcher_agent,
                lyrics_creator_agent,
                song_generator_agent
            ],
            tasks=[
                web_research_task,
                lyrics_creation_task,
                song_generation_task
            ],
        )
                
        return crew.kickoff()