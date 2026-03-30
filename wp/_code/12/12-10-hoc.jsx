import React from 'react';

const withLogger = (WrappedComponent) => {
  return (props) => {
    console.log('Props received:', props);
    return <WrappedComponent {...props} />;
  };
};

const MyComponent = ({ name, value }) => (
  <div>{name}: {value}</div>
);

const EnhancedComponent = withLogger(MyComponent);

export { withLogger, EnhancedComponent };
