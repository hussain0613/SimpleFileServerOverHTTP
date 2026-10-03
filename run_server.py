if __name__ == "__main__":
    import uvicorn

    from settings import settings

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )

