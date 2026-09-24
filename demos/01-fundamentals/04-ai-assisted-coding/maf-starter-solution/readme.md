# Microsoft Agent Framework Hello World (Python 3.12)

1. Open a terminal in this folder.
2. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install packages:

   ```powershell
   python -m pip install --pre -r requirements.txt
   ```

4. Fill in `.env`: `PROJECT_ENDPOINT` is your Microsoft Foundry project endpoint and `MODEL_DEPLOYMENT` is your model deployment name. Both are on your project page in Microsoft Foundry.
5. Sign in with `az login`.
6. Run `python main.py`.
