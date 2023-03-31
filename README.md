## AWS Lambda Discord bot

This Discord bot is a proof of concept: how to host Discord bots on AWS Lambda 
and API Gateway. Using serverless architecture can reduce costs for bot hosting: it 
will be basically free unless a lot of interactions happen with the bot.

## Invite URL

```
https://discord.com/api/oauth2/authorize?client_id=1089878825535549533&permissions=2048&scope=applications.commands%20bot
```

## Install dependencies

```
python -m pip install -r requirements-dev.txt
python -m pip install -e ./bot/commons
```