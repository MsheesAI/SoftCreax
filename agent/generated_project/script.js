// script.js – Calculator logic implementation

// Grab the display element and all calculator buttons
const display = document.getElementById('display');
const buttons = document.querySelectorAll('.buttons button');

// Calculator state
const state = {
  currentInput: '',   // string representation of what user is typing
  previousValue: null, // number stored before an operator is pressed
  operator: null      // '+', '-', '*', '/' or null
};

/**
 * Refreshes the calculator display.
 * Shows the currentInput if present, otherwise shows the previousValue
 * (useful after a computation) or a zero placeholder.
 */
function updateDisplay() {
  if (state.currentInput !== '') {
    display.textContent = state.currentInput;
  } else if (state.previousValue !== null) {
    display.textContent = String(state.previousValue);
  } else {
    display.textContent = '0';
  }
}

/**
 * Handles numeric button presses (including the decimal point).
 * Ensures no leading multiple zeros and only a single decimal point.
 * @param {string} num - The digit or '.' pressed.
 */
function handleNumber(num) {
  // Prevent multiple leading zeros (e.g., "00", "01")
  if (state.currentInput === '0' && num === '0') {
    return; // ignore extra leading zero
  }
  // If current input is "0" and a non‑decimal digit is entered, replace it.
  if (state.currentInput === '0' && num !== '.') {
    state.currentInput = num;
    updateDisplay();
    return;
  }
  // Allow only one decimal point
  if (num === '.' && state.currentInput.includes('.')) {
    return; // ignore additional decimal points
  }
  // Append the digit / decimal point
  state.currentInput += num;
  updateDisplay();
}

/**
 * Handles operator button presses (+, -, *, /).
 * Stores the current input as previousValue and remembers the operator.
 * Clears currentInput for the next number.
 * @param {string} op - One of '+', '-', '*', '/'
 */
function handleOperator(op) {
  // If there is already a pending operation, compute it first
  if (state.operator && state.currentInput !== '') {
    computeResult();
  }
  // Convert current input to a number (if any)
  const value = state.currentInput !== '' ? parseFloat(state.currentInput) : state.previousValue;
  state.previousValue = value;
  state.operator = op;
  state.currentInput = '';
  updateDisplay();
}

/**
 * Executes the pending arithmetic operation.
 * Handles division by zero gracefully.
 */
function computeResult() {
  if (state.operator === null || state.previousValue === null) {
    return; // nothing to compute
  }
  const current = state.currentInput !== '' ? parseFloat(state.currentInput) : state.previousValue;
  let result;
  switch (state.operator) {
    case '+':
      result = state.previousValue + current;
      break;
    case '-':
      result = state.previousValue - current;
      break;
    case '*':
      result = state.previousValue * current;
      break;
    case '/':
      if (current === 0) {
        alert('Error: Division by zero');
        handleClear();
        return;
      }
      result = state.previousValue / current;
      break;
    default:
      return;
  }
  // Prepare state for next operation
  state.previousValue = result;
  state.currentInput = '';
  state.operator = null;
  updateDisplay();
}

/**
 * Resets the calculator to its initial state.
 */
function handleClear() {
  state.currentInput = '';
  state.previousValue = null;
  state.operator = null;
  updateDisplay();
}

/**
 * Deletes the last character of the current input.
 */
function handleDelete() {
  if (state.currentInput !== '') {
    state.currentInput = state.currentInput.slice(0, -1);
    updateDisplay();
  }
}

// Attach click listeners to all buttons
buttons.forEach(button => {
  button.addEventListener('click', () => {
    const action = button.dataset.action; // e.g., "digit-7", "operator-add", "equals"
    if (!action) return;

    if (action.startsWith('digit-')) {
      const digit = action.split('-')[1];
      // The HTML does not provide a decimal button, but support it if present
      handleNumber(digit);
    } else if (action.startsWith('operator-')) {
      const opMap = {
        add: '+',
        subtract: '-',
        multiply: '*',
        divide: '/'
      };
      const opKey = action.split('-')[1];
      const op = opMap[opKey];
      if (op) handleOperator(op);
    } else if (action === 'equals') {
      computeResult();
    } else if (action === 'clear') {
      handleClear();
    } else if (action === 'delete') {
      handleDelete();
    }
  });
});

// Initialise display on page load
updateDisplay();
