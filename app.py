from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# In-memory database
books = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_book = {
            'id': len(books) + 1,
            'title': request.form['title'],
            'author': request.form['author']
        }
        books.append(new_book)
        return redirect(url_for('index'))

    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('query', '')
    if search_query:
        filtered_books = [book for book in books if search_query.lower() in book['title'].lower() or search_query.lower() in book['author'].lower()]
    else:
        filtered_books = books
    return jsonify(filtered_books)

@app.route('/delete/<int:book_id>')
def delete(book_id):
    global books
    books = [b for b in books if b['id'] != book_id]
    return redirect(url_for('index'))

@app.route('/update/<int:book_id>', methods=['GET', 'POST'])
def update(book_id):
    book = next((b for b in books if b['id'] == book_id), None)
    if request.method == 'POST':
        book['title'] = request.form['title']
        book['author'] = request.form['author']
        return redirect(url_for('index'))
    return render_template('update.html', book=book)

if __name__ == '__main__':
    app.run(debug=True)
