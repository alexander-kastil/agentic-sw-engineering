import { RemoveCircleOutlined, AddCircleOutlined } from '@mui/icons-material';
import { IconButton, Box, Typography } from '@mui/material';

interface Props {
  value: number;
  onChange: (value: number) => void;
}

export function NumberPicker({ value, onChange }: Props) {
  const handleRemove = () => { if (value > 0) onChange(value - 1); };
  const handleAdd = () => onChange(value + 1);

  return (
    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
      <IconButton onClick={handleRemove} color="primary" size="small">
        <RemoveCircleOutlined />
      </IconButton>
      <Typography>{value}</Typography>
      <IconButton onClick={handleAdd} color="primary" size="small">
        <AddCircleOutlined />
      </IconButton>
    </Box>
  );
}
