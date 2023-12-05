const axios = require('axios');

function getApiEndpoint() {
  return axios.get('http://127.0.0.1:8000/adminapp/api_endpoint')
    .then(response => {
      return response.data;
    })
    .catch(error => {
      console.error(error);
    });
}

module.exports = getApiEndpoint;
