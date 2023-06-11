/**
 * Import function triggers from their respective submodules:
 *
 * const {onCall} = require("firebase-functions/v2/https");
 * const {onDocumentWritten} = require("firebase-functions/v2/firestore");
 *
 * See a full list of supported triggers at https://firebase.google.com/docs/functions
 */

const {onRequest} = require("firebase-functions/v2/https");
const logger = require("firebase-functions/logger");

const functions = require('firebase-functions');
const admin = require('firebase-admin');
const axios = require('axios'); // Importamos axios
admin.initializeApp();

exports.userCreated = functions.auth.user().onCreate((user) => {
  // Aquí puedes realizar tareas necesarias, como enviar una notificación.
  console.log('El usuario ' + user.uid + ' fue creado');

  // Configuramos la data que queremos enviar
  let data = {
    uid: user.uid,
    email: user.email,
    // Agrega aquí cualquier otro campo que quieras enviar
  };

  // Hacemos un POST a la URL
  axios.post('https://p845ryq0vh.execute-api.eu-west-1.amazonaws.com/prod/user', data)
    .then((response) => {
      console.log('Respuesta recibida: ', response);
    })
    .catch((error) => {
      console.error('Error al hacer el POST: ', error);
      // Elimina al usuario en caso de error
      admin.auth().deleteUser(user.uid)
        .then(() => {
          console.log('Usuario eliminado debido a error: ', user.uid);
        })
        .catch((error) => {
          console.error('Error al eliminar al usuario: ', error);
        });
    });
});


// Create and deploy your first functions
// https://firebase.google.com/docs/functions/get-started

// exports.helloWorld = onRequest((request, response) => {
//   logger.info("Hello logs!", {structuredData: true});
//   response.send("Hello from Firebase!");
// });
