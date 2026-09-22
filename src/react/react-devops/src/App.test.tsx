import { describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';

describe('App', () => {
  it('renders heading text', () => {
    render(<App />);
    const heading = screen.getByRole('heading', { level: 1 });

    expect(heading).toHaveTextContent('React Food Shop');
  });

  it('renders image with correct src', () => {
    render(<App />);
    const image = screen.getByRole('img');

    expect(image).toBeInTheDocument();
    expect(image).toHaveAttribute('src', 'food.png');
  });

  it('increments count on button click', async () => {
    const user = userEvent.setup();
    render(<App />);

    const button = screen.getByRole('button', { name: /click me!/i });

    expect(screen.getByText(/Button clicked 0 times/i)).toBeInTheDocument();

    await user.click(button);

    expect(screen.getByText(/Button clicked 1 times/i)).toBeInTheDocument();
  });
});
