#!/usr/bin/env python3

import connexion

app = connexion.App(__name__, specification_dir='./swagger/')
app.add_api('swagger.yaml', arguments={'title': 'Addresses and Coordinates'}, pythonic_params=True)

if __name__ == '__main__':
    app.run()
