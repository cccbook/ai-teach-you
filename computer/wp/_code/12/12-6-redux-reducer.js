const initialState = { count: 0 };

const counterReducer = (state = initialState, action) => {
  switch (action.type) {
    case 'INCREMENT':
      return { count: state.count + (action.payload || 1) };
    case 'DECREMENT':
      return { count: state.count - (action.payload || 1) };
    case 'RESET':
      return { count: 0 };
    default:
      return state;
  }
};

export default counterReducer;
