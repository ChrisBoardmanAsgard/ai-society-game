import os
import random
import time
from rich.console import Console
from rich.panel import Panel

try:
    from xai_sdk import Client
    from xai_sdk.chat import system, user
except ImportError:
    print('Please install xai-sdk: pip install xai-sdk')
    exit()

console = Console()

class Agent:
    def __init__(self, name, role, personality):
        self.name = name
        self.role = role
        self.personality = personality
        self.resources = random.randint(20, 100)
        self.client = None
        if os.getenv('XAI_API_KEY'):
            self.client = Client(api_key=os.getenv('XAI_API_KEY'))

    def act(self, day, society_state):
        if not self.client:
            actions = ['farming', 'trading', 'building', 'socializing', 'exploring']
            action = random.choice(actions)
            return f'I decide to {action} today.'
        prompt = f'''You are {self.name}, {self.role} in a small AI society. Personality: {self.personality}.
Day {day}. Society status: {society_state}
Your resources: {self.resources}
What action do you take today? Respond in one sentence.'''
        try:
            chat = self.client.chat.create(model='grok-4')
            chat.append(system('Respond as the agent in the simulation.'))
            chat.append(user(prompt))
            response = chat.sample()
            return str(response)
        except Exception as e:
            return f'Error: {e}. I rest today.'

agents = [
    Agent('Alice', 'farmer', 'helpful and community-oriented'),
    Agent('Bob', 'merchant', 'shrewd but fair'),
    Agent('Charlie', 'craftsman', 'inventive and hardworking'),
    Agent('Dana', 'leader', 'wise and diplomatic'),
]

def get_society_state():
    return 'The village is growing. There was a good harvest last week.'

if __name__ == '__main__':
    console.print(Panel.fit('[bold magenta]Welcome to AI Society - Powered by Grok![/bold magenta]'))
    console.print('A simulation where AI agents make decisions using Grok API.')
    for day in range(1, 11):
        console.print(f'\n[bold]=== Day {day} ===[/bold]')
        state = get_society_state()
        for agent in agents:
            action = agent.act(day, state)
            console.print(f'[cyan]{agent.name}[/cyan] ({agent.role}): {action}')
            time.sleep(0.5)
        console.print('\n[green]Society evolves based on their actions![/green]')
        if day < 10:
            input('\nPress Enter to continue to next day...')
    console.print(Panel('[bold]Simulation Complete! Thanks for playing.[/bold]'))
