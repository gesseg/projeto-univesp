from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('emprestimos.db')
    conn.row_factory = sqlite3.Row
    return conn

# Criar tabela de empréstimos (executar uma vez)
def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_colaborador TEXT NOT NULL,
            itens TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Rota para listar os empréstimos
@app.route('/')
def index():
    conn = get_db_connection()
    emprestimos = conn.execute('SELECT * FROM emprestimos').fetchall()
    conn.close()
    return render_template('index.html', emprestimos=emprestimos)

# Rota para adicionar um empréstimo
@app.route('/add', methods=('GET', 'POST'))
def add_emprestimo():
    if request.method == 'POST':
        nome_colaborador = request.form['nome_colaborador']
        itens = ', '.join(request.form.getlist('itens'))  # Itens selecionados

        conn = get_db_connection()
        conn.execute('INSERT INTO emprestimos (nome_colaborador, itens) VALUES (?, ?)',
                     (nome_colaborador, itens))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_emprestimo.html')

# Rota para editar um empréstimo
@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_emprestimo(id):
    conn = get_db_connection()
    emprestimo = conn.execute('SELECT * FROM emprestimos WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        nome_colaborador = request.form['nome_colaborador']
        itens = ', '.join(request.form.getlist('itens'))

        conn.execute('UPDATE emprestimos SET nome_colaborador = ?, itens = ? WHERE id = ?',
                     (nome_colaborador, itens, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit_emprestimo.html', emprestimo=emprestimo)

# Rota para deletar um empréstimo
@app.route('/delete/<int:id>', methods=('POST',))
def delete_emprestimo(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM emprestimos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
