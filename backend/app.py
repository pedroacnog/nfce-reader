from flask import Flask

app = Flask('app')


@app.route('/')
def test():
    return "<p>Hello World<p>"


app.run()
