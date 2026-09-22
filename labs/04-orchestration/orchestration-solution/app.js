function handleCelsiusInput() {
  const celsiusInput = document.getElementById('celsius-input');
  const fahrenheitInput = document.getElementById('fahrenheit-input');
  const message = document.getElementById('message');
  const value = celsiusInput.value.trim();

  if (value === '') {
    fahrenheitInput.value = '';
    message.hidden = true;
    return;
  }

  const number = Number(value);
  if (!Number.isFinite(number)) {
    message.textContent = 'Enter a valid number';
    message.hidden = false;
    return;
  }

  fahrenheitInput.value = celsiusToFahrenheit(number).toFixed(1);
  message.hidden = true;
}

function handleFahrenheitInput() {
  const celsiusInput = document.getElementById('celsius-input');
  const fahrenheitInput = document.getElementById('fahrenheit-input');
  const message = document.getElementById('message');
  const value = fahrenheitInput.value.trim();

  if (value === '') {
    celsiusInput.value = '';
    message.hidden = true;
    return;
  }

  const number = Number(value);
  if (!Number.isFinite(number)) {
    message.textContent = 'Enter a valid number';
    message.hidden = false;
    return;
  }

  celsiusInput.value = fahrenheitToCelsius(number).toFixed(1);
  message.hidden = true;
}

document.getElementById('celsius-input').addEventListener('input', handleCelsiusInput);
document.getElementById('fahrenheit-input').addEventListener('input', handleFahrenheitInput);
