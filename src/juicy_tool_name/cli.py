import typer

app = typer.Typer()

@app.command()
def foo():
    # call code from a module implementing the actual logic
    print("In CLI")

if __name__ == "__main__":
    app()
