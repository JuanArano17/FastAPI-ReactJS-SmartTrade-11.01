import React from 'react';
import { Route, Redirect } from 'react-router-dom';

const PrivateRoute = ({ component: Component, allowedTypes, redirectPath = "/login", ...rest }) => (
    <Route
        {...rest}
        render={props => {
            const userType = localStorage.getItem('type') || "Unknown";
            if (allowedTypes.includes(userType)) {
                return <Component {...props} />;
            } else {
                return <Redirect to={{ pathname: redirectPath, state: { from: props.location } }} />;
            }
        }}
    />
);
