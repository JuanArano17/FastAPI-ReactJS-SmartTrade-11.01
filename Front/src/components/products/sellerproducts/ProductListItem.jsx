import React, { useState } from 'react';
import { TableCell, TableRow, IconButton, TextField, Button } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';

function ProductListItem({ product, onDelete, onEdit, onSave }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedProduct, setEditedProduct] = useState({ ...product });

  const handleEditChange = (e) => {
    const { name, value } = e.target;
    setEditedProduct({ ...editedProduct, [name]: value });
  };

  const saveEdit = () => {
    onSave(editedProduct);
    setIsEditing(false);
  };

  return (
    <TableRow>
      <TableCell>
        <img src={product.image || "/placeholder-image.png"} alt={product.name} style={{ width: 50, height: 50 }} />
      </TableCell>
      <TableCell>
        {isEditing ? (
          <TextField
            value={editedProduct.name}
            name="name"
            onChange={handleEditChange}
            size="small"
          />
        ) : (
          product.name
        )}
      </TableCell>
      <TableCell>{product.stock}</TableCell>
      <TableCell>{isEditing ? <TextField value={editedProduct.price} name="price" onChange={handleEditChange} size="small" /> : product.price}</TableCell>
      <TableCell>
        <IconButton onClick={() => onDelete(product.id)}>
          <DeleteIcon />
        </IconButton>
        <IconButton onClick={() => setIsEditing(!isEditing)}>
          <EditIcon />
        </IconButton>
        {isEditing && <Button onClick={saveEdit}>Save</Button>}
      </TableCell>
    </TableRow>
  );
}

export default ProductListItem;
