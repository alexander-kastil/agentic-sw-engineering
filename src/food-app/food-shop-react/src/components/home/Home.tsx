import { Box } from '@mui/material';

export default function Home() {
  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '80vh',
      }}
    >
      <img src="/images/food.png" alt="food" style={{ maxWidth: '100%', maxHeight: '70vh' }} />
    </Box>
  );
}
