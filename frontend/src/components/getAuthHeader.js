import { withAuth0 } from '@auth0/auth0-react';
import React from 'react';

async function getAuthHeader (permission) {
    debugger
    
    const { getAccessTokenSilently } = this.props.auth0;
    const domain = "https://localhost:5000";
    const accessToken = await getAccessTokenSilently({
        audience: domain,
        scope: permission,
    });

    return accessToken;
}

export default withAuth0(getAuthHeader);