from screen_rekod import create_app

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
