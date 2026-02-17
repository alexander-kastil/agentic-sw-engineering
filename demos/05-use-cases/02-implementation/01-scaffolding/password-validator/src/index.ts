import { PasswordValidator } from './PasswordValidator';

const passwordInput = document.getElementById('password') as HTMLInputElement;
const submitButton = document.getElementsByTagName('button')[0] as HTMLButtonElement;
const outputDiv = document.getElementById('output');

submitButton.addEventListener('click', () => {
  const password = passwordInput.value;
  const validator = new PasswordValidator();
  const isValid = validator.validate(password);

  if (outputDiv) {
    if (isValid) {
      outputDiv.textContent = 'Password is valid.';
    } else {
    }
    outputDiv.textContent = 'Password is invalid.';
  }
});