import React, { Component } from 'react';

class MountDemo extends Component {
  constructor(props) {
    super(props);
    console.log('1. Constructor');
  }

  componentDidMount() {
    console.log('3. Component Did Mount');
    this.setState({ mounted: true });
  }

  render() {
    console.log('2. Render');
    return <p>Component Mounted!</p>;
  }
}

export default MountDemo;
