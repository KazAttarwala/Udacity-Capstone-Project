import React from 'react'

function Error(props) {
    let isAuthError = props.error.code;
    let code = props.error.error;
    let description = props.error.message;

    if (isAuthError) {
        code = props.error.code;
        description = props.error.description
    }
    
    return (
        <div>
            <div>Error Code: {code}</div>
            <div>Description: {description}</div>
        </div>
    )
    
}

export default Error;