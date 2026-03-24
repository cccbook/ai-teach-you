import { createStore } from 'redux';
import counterReducer from './12-6-redux-reducer.js';

const store = createStore(counterReducer);

console.log('Initial state:', store.getState());

store.subscribe(() => {
  console.log('State changed:', store.getState());
});

export default store;
