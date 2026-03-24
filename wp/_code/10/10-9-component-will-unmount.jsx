import React, { Component } from 'react';

class WillUnmountDemo extends Component {
  constructor(props) {
    super(props);
    this.timerID = null;
  }

  componentDidMount() {
    this.timerID = setInterval(() => {
      console.log('Timer running...');
    }, 1000);
  }

  componentWillUnmount() {
    clearInterval(this.timerID);
    console.log('Timer stopped!');
  }

  render() {
    return <p>Timer active...</p>;
  }
}

export default WillUnmountDemo;
