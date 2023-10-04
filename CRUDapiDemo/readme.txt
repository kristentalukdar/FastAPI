Go to command prompt

Change directory to your project folder

Make sure you are connected to Internet

Run the following command: pip install -r requirements.txt

Once successfully Installed, please run the following command: uvicorn main:app --reload

This will activate the following URL: http://127.0.0.1:8000/

Open the URL browse the options available in  the UI

Open the URL browser with 'URL/docs' that leads to the API documentation which inckudes the following:
    Get
    Post:
          Example-{
                    "id": 101,
                    "name": "Television",
                    "description": "Televison DESC",
                    "price_per_unit": 100000,
                    "base_unit": "No",
                    "stock": 100
                  }
    Put
    Delete
