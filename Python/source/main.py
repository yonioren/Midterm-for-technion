from ProjectPlanner import create_app

app = create_app()

# If called interactively, start the webserver with Yoni's custom port
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8666)
