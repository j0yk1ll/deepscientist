from deepscientist.orchestrator.agent import create_orchestrator_agent
from deepscientist.settings import Settings


class DeepScientist:
    def __init__(self):
        self.settings = Settings()
    
        print(self.settings)
    
        self.agent = create_orchestrator_agent(settings=self.settings)
        
    def invoke(self, query: str) -> str:
        
        callbacks = [self.settings.langfuse_handler] if self.settings.langfuse_handler else []
        
        result = self.agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": query,
                    }
                ]
            },
            context={"settings": self.settings},
            config = {"callbacks": callbacks} if callbacks else {}

        )
        return result["messages"][-1].content
    
def create_deepscientist() -> DeepScientist:
    return DeepScientist()