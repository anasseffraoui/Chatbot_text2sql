from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from .config import settings

def install_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND_ORIGIN,
            "https://anasseffraoui.github.io",
            "https://*.trycloudflare.com",               
        ],
        allow_credentials=True,
        allow_methods=["GET","POST","OPTIONS"],
        allow_headers=["*"],
    )
