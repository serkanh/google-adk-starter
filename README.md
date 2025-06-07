# Google ADK Agent Template

A production-ready template for building AI agents with Google's Agent Development Kit (ADK). Clone this repo to quickly start building your own agents with built-in session persistence, Docker support, and ADK best practices.

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Clone this template
git clone <this-repo-url> my-awesome-agent
cd my-awesome-agent

# Run the setup script
./setup.sh

# The script will:
# - Create .env from example
# - Let you name your agent
# - Build Docker containers
# - Provide next steps
```

### Option 2: Manual Setup

```bash
# Clone this template
git clone <this-repo-url> my-awesome-agent
cd my-awesome-agent

# Create .env file with your API key
echo "OPENAI_API_KEY=your-key-here" > .env
# Or use Google Gemini:
# echo "GOOGLE_API_KEY=your-key-here" > .env
```

### 2. Customize Your Agent

Edit `agents/my_agent/agent.py` to define your agent:

```python
def create_my_agent() -> Agent:
    return Agent(
        name="my_awesome_agent",  # Your agent's name
        model="gemini-2.0-flash"  # Your preferred model
        description="An AI that helps with...",  # What it does
        instruction="""You are an expert in...

        Your capabilities include:
        - Skill 1
        - Skill 2
        - Skill 3
        """,  # Define personality & expertise
        tools=[],  # Add tools (see below)
        sub_agents=[],  # Add sub-agents
    )
```

### 3. Run Your Agent

```bash
# Start with Docker (recommended)
docker-compose up -d

# Or run locally
pip install -r agents/my_agent/requirements.txt
adk web --agent agents.my_agent.agent:root_agent
```

### 4. Access Your Agent

- **Web UI**: <http://localhost:8000>
- **API**: <http://localhost:8001>
- **Database**: localhost:5432

## 📁 Project Structure

```
my-agent/
├── agents/
│   └── my_agent/              # Your agent module
│       ├── __init__.py        # Package exports
│       ├── agent.py           # Main agent definition
│       ├── settings.py        # Configuration
│       ├── requirements.txt   # Python dependencies
│       ├── Dockerfile         # Container setup
│       └── tools/            # Custom tools (optional)
│           └── __init__.py
├── docker-compose.yml         # Service orchestration
├── .env                      # Environment variables
├── .gitignore               # Git exclusions
└── README.md                # This file
```

## 🛠️ Customization Guide

### Step 1: Update Settings

Edit `agents/my_agent/settings.py`:

```python
# Change the app name
APP_NAME = "my_awesome_agent"  # Used for session management

# Add your API keys
YOUR_API_KEY = os.getenv("YOUR_API_KEY", "")
```

### Step 2: Choose Your Model

Popular model options in `agent.py`:

```python
# OpenAI
model=LiteLlm(model="gpt-4")
model=LiteLlm(model="gpt-3.5-turbo")

# Google Gemini
model=LiteLlm(model="gemini-pro")
model=LiteLlm(model="gemini-1.5-pro")

# Anthropic Claude
model=LiteLlm(model="claude-3-opus")
model=LiteLlm(model="claude-3-sonnet")

# Local/Open models
model=LiteLlm(model="ollama/llama2")
```

### Step 3: Add Tools

Create tools to extend your agent's capabilities:

```python
from google.adk.tools import Tool

# Simple function tool
def calculate_something(x: int, y: int) -> int:
    """Add two numbers."""
    return x + y

calc_tool = Tool(
    name="calculator",
    description="Performs calculations",
    function=calculate_something
)

# Add to your agent
agent = Agent(
    # ... other config ...
    tools=[calc_tool],
)
```

### Step 4: Create Sub-Agents

Build complex systems with specialized sub-agents:

```python
research_agent = Agent(
    name="researcher",
    model=LiteLlm(model="gpt-4"),
    description="Specializes in research",
    instruction="You excel at finding and analyzing information..."
)

writer_agent = Agent(
    name="writer",
    model=LiteLlm(model="gpt-4"),
    description="Specializes in writing",
    instruction="You create compelling content..."
)

# Orchestrate them
main_agent = Agent(
    name="coordinator",
    model=LiteLlm(model="gpt-4"),
    description="Coordinates research and writing",
    sub_agents=[research_agent, writer_agent],
)
```

### Step 5: Update Docker Configuration

Modify `docker-compose.yml` for your needs:

```yaml
environment:
  - YOUR_API_KEY=${YOUR_API_KEY}
  - CUSTOM_VAR=${CUSTOM_VAR}
  - DB_NAME=myawesomeagent  # Update database name
```

## 🔧 Advanced Features

### Session Persistence

Sessions are automatically managed with PostgreSQL:

- Conversation history is preserved
- User preferences are maintained
- Automatic fallback to in-memory if DB fails

### Multi-Agent Orchestration

```python
from google.adk.agents import Sequential, Parallel

# Sequential workflow
workflow = Sequential(
    agents=[analyze_agent, process_agent, output_agent]
)

# Parallel processing
parallel_tasks = Parallel(
    agents=[checker1_agent, checker2_agent]
)
```

### Custom Tools with External APIs

```python
import requests
from google.adk.tools import Tool

async def fetch_weather(city: str) -> dict:
    """Fetch current weather for a city."""
    response = await requests.get(f"https://api.weather.com/{city}")
    return response.json()

weather_tool = Tool(
    name="weather",
    description="Get current weather",
    function=fetch_weather
)
```

### Adding Dependencies

1. Add to `agents/my_agent/requirements.txt`:

   ```
   requests>=2.31.0
   beautifulsoup4>=4.12.0
   pandas>=2.0.0
   ```

2. Rebuild: `docker-compose build`

## 📊 Monitoring & Debugging

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f agent-web

# With timestamps
docker-compose logs -f -t
```

### Debug Mode

```bash
# Set in .env
echo "LOG_LEVEL=DEBUG" >> .env
docker-compose restart
```

### Database Access

```bash
# Connect to PostgreSQL
docker exec -it adk-agent-template_postgres_1 psql -U postgres -d myagent

# View sessions
\dt  # List tables
SELECT * FROM sessions LIMIT 5;
```

## 🚢 Deployment

### Production Checklist

- [ ] Set strong database password
- [ ] Use environment-specific API keys
- [ ] Configure proper logging
- [ ] Set up monitoring
- [ ] Enable HTTPS
- [ ] Configure backup strategy

### Deploy to Cloud Run

```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT/my-agent

# Deploy
gcloud run deploy my-agent \
  --image gcr.io/YOUR_PROJECT/my-agent \
  --platform managed \
  --allow-unauthenticated
```

### Environment Variables

Production `.env` example:

```bash
# API Keys
OPENAI_API_KEY=sk-prod-...
GOOGLE_API_KEY=AIza-prod-...

# Database
DB_HOST=your-db-host.com
DB_NAME=myagent_prod
DB_USER=myagent_user
DB_PASSWORD=strong-password-here

# Application
LOG_LEVEL=WARNING
ENV=production
```

## 📚 Resources

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [ADK GitHub Repository](https://github.com/google/adk)
- [LiteLLM Models](https://docs.litellm.ai/docs/providers)
- [ADK Examples](https://github.com/google/adk/tree/main/examples)

## 🤝 Contributing

1. Fork this template
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This template is open source and available under the [MIT License](LICENSE).

## 🎯 Next Steps

1. **Define your agent's purpose** - What problem will it solve?
2. **Add relevant tools** - What capabilities does it need?
3. **Test thoroughly** - Ensure sessions persist and tools work
4. **Deploy** - Share your agent with the world!

---

Built with ❤️ using [Google ADK](https://google.github.io/adk-docs/)
