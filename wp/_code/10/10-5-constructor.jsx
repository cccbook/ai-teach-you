import React, { Component } from 'react';

class ConstructorDemo extends Component {
  constructor(props) {
    super(props);
    this.state = {
      name: props.initialName || 'Guest',
      count: 0
    };
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    this.setState({ count: this.state.count + 1 });
  }

  render() {
    return (
      <div>
        <h1>Hello, {this.state.name}</h1>
        <p>Count: {this.state.count}</p>
        <button onClick={this.handleClick}>Click</button>
      </div>
    );
  }
}

export default ConstructorDemo;
