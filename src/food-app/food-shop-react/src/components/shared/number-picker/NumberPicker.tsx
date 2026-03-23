import { Box, IconButton, Typography } from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import RemoveCircleOutlineIcon from '@mui/icons-material/RemoveCircleOutline';

interface NumberPickerProps {
  value: number;
  onChange: (value: number) => void;
  min?: number;
}

export default function NumberPicker({ value, onChange, min = 0 }: NumberPickerProps) {
  const handleAdd = () => onChange(value + 1);
  const handleRemove = () => {
    if (value > min) onChange(value - 1);
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between', width: 100, alignItems: 'center' }}>
      <IconButton onClick={handleRemove} color="primary" size="small">
        <RemoveCircleOutlineIcon />
      </IconButton>
      <Typography sx={{ fontSize: 24 }}>{value}</Typography>
      <IconButton onClick={handleAdd} color="primary" size="small">
        <AddCircleOutlineIcon />
      </IconButton>
    </Box>
  );
}
