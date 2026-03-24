import React, { Component } from 'react';

class UnmountDemo extends Component {
  componentWillUnmount() {
    console.log('Component Will Unmount - Cleanup!');
  }

  render() {
    return <p>Component will unmount soon...</p>;
  }
}

export default UnmountDemo;
