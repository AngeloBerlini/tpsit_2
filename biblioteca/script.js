const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.static(__dirname)); // serve index.html, biblioteca.html, libri.json

const filePath = path.join(__dirname, 'libri.json');

app.post('/aggiungi', (req, res) => {
    const nuovoLibro = req.body;

    fs.readFile(filePath, 'utf8', (err, data) => {
        if(err) return res.status(500).send('Errore lettura JSON');

        let libri = JSON.parse(data).libri;
        libri.push(nuovoLibro);

        fs.writeFile(filePath, JSON.stringify({ libri }, null, 2), (err) => {
            if(err) return res.status(500).send('Errore scrittura JSON');
            res.send('Libro aggiunto!');
        });
    });
});

app.listen(PORT, () => console.log(`Server attivo su http://localhost:${PORT}`));
