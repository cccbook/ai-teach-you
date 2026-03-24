import React, { Component } from 'react';

class RenderDemo extends Component {
  state = { showContent: true };

  toggleContent = () => {
    this.setState({ showContent: !this.state.showContent });
  };

  render() {
    return (
      <div>
        <button onClick={this.toggleContent}>Toggle</button>
        {this.state.showContent && <p>Content is visible!</p>}
      </div>
    );
  }
}

export default RenderDemo;
