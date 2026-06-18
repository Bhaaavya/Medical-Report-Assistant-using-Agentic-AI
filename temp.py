from app.services.llm_router import llm_router

response = llm_router.generate("Say hello in one sentence.")
print(response)