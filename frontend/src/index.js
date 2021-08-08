import 'bootstrap/dist/css/bootstrap.css';
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom';
import './index.css';
import App from './App';
import registerServiceWorker from './registerServiceWorker';
import { Auth0Provider } from "@auth0/auth0-react";

//const baseUrl = document.getElementsByTagName('base')[0].getAttribute('href');
//const rootElement = document.getElementById('root');

ReactDOM.render(
  <Auth0Provider
    domain="udacity-coffee-full-stack.us.auth0.com"
    clientId="HYvLh1Lx749x5OP7TJsmq2cQF0JjHQ9S"
    redirectUri={window.location.origin}
    audience="https://localhost:5000"
    scope="create:actor create:movie delete:actor delete:movie update:actor update:movie read:actors read:movies"
  >
    <BrowserRouter basename="/">
      <App />
    </BrowserRouter>
  </Auth0Provider>,

  document.getElementById('root')
);

registerServiceWorker();
