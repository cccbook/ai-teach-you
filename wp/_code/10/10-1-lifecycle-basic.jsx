import React, { Component } from 'react';

class LifecycleDemo extends Component {
  constructor(props) {
    super(props);
    this.state = { message: 'Component Created' };
  }

  render() {
    return <p>{this.state.message}</p>;
  }
}

export default LifecycleDemo;
