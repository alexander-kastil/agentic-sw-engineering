Microsoft Agent Framework hello world (Python 3.12)

1. Open a terminal in this folder.
2. Create and activate a virtual environment:
   - python -m venv .venv
   - .\.venv\Scripts\Activate.ps1
3. Install packages:
   - python -m pip install --pre -r requirements.txt
4. Fill in .env:
   - PROJECT_ENDPOINT is your Azure AI Foundry project endpoint.
   - MODEL_DEPLOYMENT is your Azure AI Foundry model deployment name.
   You can find both in Azure AI Foundry: open your project, then use the endpoint value and the deployment name from the Models or Deployments area.
5. Sign in with Azure CLI:
   - az login
6. Run:
   - python main.py
