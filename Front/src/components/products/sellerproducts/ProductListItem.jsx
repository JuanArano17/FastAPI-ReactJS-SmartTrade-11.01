import React, { useState } from 'react';
import { TableCell, TableRow, IconButton, TextField, Button, Checkbox } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';

function ProductListItem({ product, onDelete, onEdit, onSave, index }) {
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

  // Determine row color based on the product state
  const getRowColor = () => {
    if (product.state === 'approved') {
      return '#c8e6c9'; // green
    } else if (product.state === 'rejected') {
      return '#ffcdd2'; // red
    } else {
      return index % 2 === 0 ? 'white' : '#f7f7f7'; // default colors
    }
  };

  return (
    <TableRow sx={{ backgroundColor: getRowColor() }}>
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
      <TableCell>{isEditing ? <TextField value={editedProduct.quantity} name="quantity" onChange={handleEditChange} size="small" /> : product.quantity}</TableCell>
      <TableCell>{isEditing ? <TextField value={editedProduct.price} name="price" onChange={handleEditChange} size="small" /> : product.price}</TableCell>
      <TableCell>{isEditing ? <TextField value={editedProduct.shipping_costs} name="shipping_costs" onChange={handleEditChange} size="small" /> : product.shipping_costs}</TableCell>
      <TableCell>
        {isEditing ? (
          <TextField
            value={editedProduct.state}
            name="state"
            onChange={handleEditChange}
            size="small"
          />
        ) : (
          product.state
        )}
      </TableCell>
      <TableCell>
        {isEditing ? (
          <Checkbox
            checked={editedProduct.publish}
            onChange={(e) => setEditedProduct({ ...editedProduct, publish: e.target.checked })}
          />
        ) : (
          <Checkbox checked={product.publish} />
        )}
      </TableCell>
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
