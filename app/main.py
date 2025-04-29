from fastapi import FastAPI
import importlib
import pkgutil
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="xutil Dev Tools",
    description="A collection of developer utility tools.",
    version="1.0.0"
)

ROUTER_PACKAGE = "app.routers"

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def include_all_routers():
    router_path = Path(__file__).parent / "routers"

    for category in router_path.iterdir():
        if category.is_dir():
            package_name = f"{ROUTER_PACKAGE}.{category.name}"
            for _, module_name, is_pkg in pkgutil.iter_modules([str(category)]):
                if not is_pkg:
                    full_module_path = f"{package_name}.{module_name}"
                    module = importlib.import_module(full_module_path)
                    if hasattr(module, "router"):
                        app.include_router(module.router, prefix="/api")
                        print(f"Included: {full_module_path}")

include_all_routers()

@app.get("/api/health")
async def health_check():
    return {"status": "Online"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)