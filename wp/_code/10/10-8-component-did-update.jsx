import React, { Component } from 'react';

class DidUpdateDemo extends Component {
  constructor(props) {
    super(props);
    this.state = { value: '' };
  }

  componentDidUpdate(prevProps) {
    if (prevProps.inputValue !== this.props.inputValue) {
      console.log('Input value changed!');
    }
  }

  render() {
    return <input value={this.props.inputValue} readOnly />;
  }
}

export default DidUpdateDemo;
