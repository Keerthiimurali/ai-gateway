from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from router import router

app = FastAPI(title="AI Gateway")
app.include_router(router)


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Gateway</title>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                font-family: Arial, sans-serif;
                background-color: #f9f9f9;
            }
            .container {
                text-align: center;
            }
            h1 {
                color: #333;
            }
            a {
                text-decoration: none;
                color: #0078d7;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>AI Gateway is Running</h1>
            <p>Try the <a href="/docs">Swagger UI</a> for interactive testing.</p>
        </div>
    </body>
    </html>
    """
