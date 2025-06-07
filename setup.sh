#!/bin/bash
# Google ADK Agent Template - Quick Setup Script

echo "🚀 Google ADK Agent Template Setup"
echo "=================================="
echo ""

# Check if .env exists
if [ -f .env ]; then
    echo "✅ .env file already exists"
else
    echo "📝 Creating .env from example.env..."
    cp example.env .env
    echo "⚠️  Please edit .env and add your API keys!"
    echo ""
fi

# Prompt for agent name
read -p "🤖 Enter your agent name (default: my_agent): " agent_name
agent_name=${agent_name:-my_agent}

# Update settings.py with the agent name
if [ "$agent_name" != "my_agent" ]; then
    echo "📝 Updating agent name to: $agent_name"

    # Update APP_NAME in settings.py
    sed -i.bak "s/APP_NAME = \"my_agent\"/APP_NAME = \"$agent_name\"/" agents/my_agent/settings.py

    # Update docker-compose.yml database name
    sed -i.bak "s/DB_NAME=myagent/DB_NAME=$agent_name/" docker-compose.yml
    sed -i.bak "s/myagent:5432\/$agent_name/$agent_name:5432\/$agent_name/" docker-compose.yml
    sed -i.bak "s/POSTGRES_DB=myagent/POSTGRES_DB=$agent_name/" docker-compose.yml

    # Clean up backup files
    rm -f agents/my_agent/settings.py.bak docker-compose.yml.bak

    echo "✅ Agent name updated!"
fi

echo ""
echo "🐳 Building Docker containers..."
docker-compose build

echo ""
echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your API keys"
echo "2. Customize your agent in agents/my_agent/agent.py"
echo "3. Run: docker-compose up -d"
echo "4. Visit: http://localhost:8000"
echo ""
echo "Happy building! 🎉"