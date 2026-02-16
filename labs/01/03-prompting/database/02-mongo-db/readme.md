# Mongo DB

 The [MongoDB for VS Code](https://marketplace.visualstudio.com/items?itemName=mongodb.mongodb-vscode) Extension offers a MongoDB Copilot Participant (Agent) which offers the following slash commands:

- **/docs**: Finds answers to coding-related questions in the MongoDB documentation.
- **/query**: Generates MongoDB queries from natural language for use with a connected MongoDB cluster. It can create both queries and aggregations based on the request's complexity. It uses schema to minimize model hallucinations and provides actions to open generated code in a playground or run it directly from the Copilot chat interface.
- **/schema**: Analyzes and returns information about a collection's schema.

## Demo

Install MongoDB:

```bash
winget install MongoDB.Server
```

Install the MongoDB for VS Code Extension:

```bash
code --install-extension mongodb.mongodb-vscode
```

Use the following prompt in GitHub Copilot:

```bash
@workspace create a simple mongo db in the current subfolder of the terminal to maintain dogs with props name, age, race
```

