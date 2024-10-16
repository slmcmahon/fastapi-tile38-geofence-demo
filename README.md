## Geofencing Demo

Just getting started here. More documentation to follow.

If you are using Visual Studio Code, then you should create a .vscode folder in the root of this project and add the following files:

launch.json

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug the API",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/env/bin/uvicorn",
      "preLaunchTask": "composeUp",
      "postDebugTask": "composeDown",
      "args": ["main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
      "console": "integratedTerminal",
      "env": {
        "APP_DEBUG": "True",
        "TILE38_CONNECTION_STRING": "redis://localhost:9851",
        "MONGO_CONNECTION_STRING": "mongodb://dbadmin:supersecret@localhost:27017",
        "MONGO_DB_NAME": "gpsdemo",
        "APPP_NAME": "gpsdemo",
        "APP_VERSION": "0.1.0",
        "HOST": "0.0.0.0",
        "PORT": "8000"
      },
      "justMyCode": true,
      "jinja": true
    }
  ]
}
```

tasks.json

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "composeUp",
      "type": "shell",
      "command": "docker-compose -f ${workspaceFolder}/docker-compose.yaml up -d"
    },
    {
      "label": "composeDown",
      "type": "shell",
      "command": "docker-compose -f ${workspaceFolder}/docker-compose.yaml down"
    }
  ]
}
```
