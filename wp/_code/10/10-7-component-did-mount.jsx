import React, { Component } from 'react';

class DidMountDemo extends Component {
  constructor(props) {
    super(props);
    this.state = { data: null };
  }

  componentDidMount() {
    fetch('https://api.example.com/data')
      .then(res => res.json())
      .then(data => this.setState({ data }));
  }

  render() {
    return <p>Data: {this.state.data || 'Loading...'}</p>;
  }
}

export default DidMountDemo;
