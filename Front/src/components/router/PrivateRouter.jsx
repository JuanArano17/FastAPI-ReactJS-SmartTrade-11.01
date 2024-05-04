import React from 'react';
import { Route, Redirect } from 'react-router-dom';

const PrivateRouter = ({ component: Component, allowedTypes, redirectPaths, ...rest }) => (
    <Route
        {...rest}
        render={props => {
            const userType = localStorage.getItem('type') || "Unknown";
            if (allowedTypes.includes(userType)) {
                return <Component {...props} />;
            } else {
                const redirectPath = redirectPaths[userType] || '/login'; 
                return <Redirect to={{ pathname: redirectPath, state: { from: props.location } }} />;
            }
        }}
    />
);

export default PrivateRouter;