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
const axios = require('axios');
admin.initializeApp();

exports.userCreated = functions.auth.user().onCreate((user) => {
  console.log('User ' + user.uid + ' was created');

  let data = {
    uid: user.uid,
    email: user.email,
  };

  let token = admin.auth().createCustomToken(user.uid);

  let config = {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  };

  axios.post('https://p845ryq0vh.execute-api.eu-west-1.amazonaws.com/prod/user', data, config)
    .then((response) => {
      console.log('Received response: ', response);
    })
    .catch((error) => {
      console.error('Error on POST request: ', error);
      admin.auth().deleteUser(user.uid)
        .then(() => {
          console.log('Deleted user due to an error creating it: ', user.uid);
        })
        .catch((error) => {
          console.error('Error deleting user: ', error);
        });
    });
});


// Create and deploy your first functions
// https://firebase.google.com/docs/functions/get-started

// exports.helloWorld = onRequest((request, response) => {
//   logger.info("Hello logs!", {structuredData: true});
//   response.send("Hello from Firebase!");
// });
