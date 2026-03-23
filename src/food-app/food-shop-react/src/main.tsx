import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { createTheme, ThemeProvider, CssBaseline } from '@mui/material';
import App from './App.tsx';
import './index.css';

const theme = createTheme({
  palette: {
    primary: { main: '#3f51b5' },
    secondary: { main: '#ff4081' },
  },
});

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <App />
      </ThemeProvider>
    </BrowserRouter>
  </StrictMode>,
);
