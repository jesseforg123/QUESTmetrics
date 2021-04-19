import React, { useState, useEffect } from 'react';
import { GoogleLogin } from 'react-google-login';
import jwt_decode from 'jwt-decode';

import { useRouteMatch, Route } from 'react-router-dom';

import Main from './Main';
import { usePersistedState } from '../utils/usePersistedState';

const App = () => {
  const [id, setId] = useState('');
  const [privilege, setPrivilege] = usePersistedState('privilege', 0); // 0 is nothing, 1 is student, 2 is admin
  const { url } = useRouteMatch();

  const [token, setToken] = usePersistedState('token', '');

  const onSignIn = googleUser => {
    var profile = googleUser.getBasicProfile();
    var splitEmail = profile.getEmail().split('@');
    if (
      splitEmail[1] === 'terpmail.umd.edu' ||
      splitEmail[1] === 'g.umd.edu' ||
      splitEmail[1] === 'umd.edu'
    ) {
      setId(splitEmail[0]);
    } else {
      onFail();
    }
  };

  const onFail = () => {
    alert('You must sign in with a VALID UMD email');
  };

  const fetchToken = async id => {
    const token_url = `http://valerian.cs.umd.edu:5000/auth?key=katcBDCk0UhDDUjvfQxoaZNxFAwNZLZl&directoryId=${id}`;
    await fetch(token_url, { method: 'GET' })
      .then(res => res.json())
      .then(r => r['access_token'])
      .then(token => {
        setToken(token);
        const access_token = jwt_decode(token)['identity']['privilege'];
        if (access_token === 'admin') setPrivilege(1);
        else setPrivilege(2);
      });
  };

  useEffect(() => {
    if (id !== '') fetchToken(id);
  }, [token, id]);

  const loginstyle = {
    height: '100vh',
    width: '100%',
    background: 'black',
    display: 'flex',
    justifyContent: 'center',
    textAlign: 'center',
    alignItems: 'center',
  };

  const loginbutton = {
    color: 'white',
    background: '#CF102D',
    fontSize: '2rem',
    // height: '2rem',
    padding: '2rem',
    borderRadius: '3rem',
    cursor: 'pointer',
  };

  return (
    <div>
      <Route path={url}>
        {privilege === 0 ? (
          <div style={loginstyle}>
            <GoogleLogin
              clientId="497269533533-jnl5jihqvnmhjadhf7pf2ckl9sej21ja.apps.googleusercontent.com"
              buttonText="Login"
              onSuccess={onSignIn}
              onFailure={onFail}
              render={renderProps => (
                <div
                  style={loginbutton}
                  onClick={renderProps.onClick}
                  disabled={renderProps.disabled}>
                  Log In Through UMD CAS
                </div>
              )}
            />
          </div>
        ) : (
          <div></div>
        )}
      </Route>

      <Main privilege={privilege} token={token} />
    </div>
  );
};

export default App;
