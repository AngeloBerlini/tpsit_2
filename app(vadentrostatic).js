window.onload = function () {

    loadUsers();

    document.getElementById('userForm')
        .addEventListener('submit', saveUser);
};


function loadUsers() {

    var xhr = new XMLHttpRequest();

    xhr.open('GET', '/users/', true);

    xhr.onreadystatechange = function () {

        if (xhr.readyState === 4 && xhr.status === 200) {

            var users = JSON.parse(xhr.responseText);

            var tbody = document.getElementById('userTableBody');

            tbody.innerHTML = '';

            for (var i = 0; i < users.length; i++) {

                var u = users[i];

                    var tr = document.createElement('tr');

                    var tdId = document.createElement('td');
                    tdId.textContent = u.id;
                    tr.appendChild(tdId);

                    var tdNome = document.createElement('td');
                    tdNome.textContent = u.nome;
                    tr.appendChild(tdNome);

                    var tdCognome = document.createElement('td');
                    tdCognome.textContent = u.cognome;
                    tr.appendChild(tdCognome);

                    var tdData = document.createElement('td');
                    tdData.textContent = u.data_nascita;
                    tr.appendChild(tdData);

                    var tdMansione = document.createElement('td');
                    tdMansione.textContent = u.mansione;
                    tr.appendChild(tdMansione);

                    var tdActions = document.createElement('td');

                    var btnDettaglio = document.createElement('button');
                    btnDettaglio.textContent = 'Dettaglio';
                    // capture id
                    (function(id){
                        btnDettaglio.addEventListener('click', function(){ editUser(id); });
                    })(u.id);
                    tdActions.appendChild(btnDettaglio);

                    var btnElimina = document.createElement('button');
                    btnElimina.textContent = 'Elimina';
                    (function(id){
                        btnElimina.addEventListener('click', function(){ deleteUser(id); });
                    })(u.id);
                    tdActions.appendChild(btnElimina);

                    tr.appendChild(tdActions);

                    tbody.appendChild(tr);
            }
        }
    };

    xhr.send();
}


function saveUser(event) {

    event.preventDefault();

    var id = document.getElementById('userId').value;

    var user = {

        nome: document.getElementById('nome').value,
        cognome: document.getElementById('cognome').value,
        data_nascita: document.getElementById('data_nascita').value,
        mansione: document.getElementById('mansione').value
    };

    var method = 'POST';
    var url = '/users/';

    if (id !== '') {
        method = 'PUT';
        url = '/users/' + id;
    }

    var xhr = new XMLHttpRequest();

    xhr.open(method, url, true);

    xhr.setRequestHeader(
        'Content-Type',
        'application/json;charset=UTF-8'
    );

    xhr.onreadystatechange = function () {

        if (xhr.readyState === 4) {

            if (xhr.status === 200 || xhr.status === 201) {

                document.getElementById('userForm').reset();

                document.getElementById('userId').value = '';

                loadUsers();

            } else {

                alert('Errore richiesta');
            }
        }
    };

    xhr.send(JSON.stringify(user));
}


function editUser(id) {

    var xhr = new XMLHttpRequest();

    xhr.open('GET', '/users/' + id, true);

    xhr.onreadystatechange = function () {

        if (xhr.readyState === 4 && xhr.status === 200) {

            var user = JSON.parse(xhr.responseText);

            document.getElementById('userId').value = user.id;
            document.getElementById('nome').value = user.nome;
            document.getElementById('cognome').value = user.cognome;
            document.getElementById('data_nascita').value = user.data_nascita;
            document.getElementById('mansione').value = user.mansione;
        }
    };

    xhr.send();
}


function deleteUser(id) {

    if (!confirm('Eliminare utente?')) {
        return;
    }

    var xhr = new XMLHttpRequest();

    xhr.open('DELETE', '/users/' + id, true);

    xhr.onreadystatechange = function () {

        if (xhr.readyState === 4 && xhr.status === 200) {

            loadUsers();
        }
    };

    xhr.send();
}
