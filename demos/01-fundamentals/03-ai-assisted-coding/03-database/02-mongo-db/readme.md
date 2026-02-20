# Mongo DB

The [MongoDB for VS Code](https://marketplace.visualstudio.com/items?itemName=mongodb.mongodb-vscode) Extension offers a MongoDB Copilot Participant (Agent) with the following slash commands:

| Command | Purpose                                                                                                                                                                                  |
| ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| /docs   | Finds answers to coding-related questions in the MongoDB documentation.                                                                                                                  |
| /query  | Generates MongoDB queries from natural language for use with a connected MongoDB cluster. Creates queries and aggregations based on complexity, using schema to minimize hallucinations. |
| /schema | Analyzes and returns information about a collection's schema.                                                                                                                            |

## Demo

Step 1: Install MongoDB

```bash
winget install MongoDB.Server
```

Step 2: Install the MongoDB for VS Code Extension

```bash
code --install-extension mongodb.mongodb-vscode
```

Step 3: Create a MongoDB database using Copilot

Use the following prompt in GitHub Copilot to generate a schema with dog collection:

```bash
@workspace create a simple mongo db in the current subfolder of the terminal to maintain dogs with props name, age, race
```
