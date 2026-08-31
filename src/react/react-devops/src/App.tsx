import { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [count, setCount] = useState(0);

  const increment = () => setCount((previous) => previous + 1);

  useEffect(() => {
    document.title = 'React Food Shop';
  }, []);

  return (
    <main className='app'>
      <h1>React Food Shop</h1>
      <div className='card'>
        <img src='food.png' alt='Cartoon dog enjoying a steak' />
        <button onClick={increment}>Click Me!</button>
        <p>Button clicked {count} times</p>
      </div>
    </main>
  );
}

export default App;
