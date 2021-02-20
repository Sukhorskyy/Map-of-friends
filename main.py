from flask import Flask, request, render_template
import friends_map

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def friend():
    # handle the POST request
    if request.method == 'POST':
        name = request.form.get('user_name')
        friends_map.main(name)
        return render_template('index.html')
    # otherwise handle the GET request
    return """<form method="post">
                <input type="text" name="user_name">
                <input type="submit">
              </form>
            """

if __name__ == "__main__":
    app.run(debug=True)