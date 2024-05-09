import React, { useState } from 'react';
import { TableCell, TableRow, IconButton, TextField, Button, Checkbox } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CancelIcon from '@mui/icons-material/Cancel';
import PendingIcon from '@mui/icons-material/Pending';
import styles from '../../../styles/styles'

function ProductListItem({ product, onDelete, onEdit, onSave, index }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedProduct, setEditedProduct] = useState({ ...product });

  const handleEditChange = (e) => {
    const { name, value } = e.target;
    setEditedProduct(prev => ({ ...prev, [name]: value }));
  };

  const saveEdit = () => {
    onSave(editedProduct);
    setIsEditing(false);
  };

  const canPublish = product.state === 'Approved';

  const toggleEditing = () => {
    setIsEditing(!isEditing);
    if (!isEditing && product.state === 'Rejected') {
      setEditedProduct(prev => ({ ...prev, state: 'Pending' })); // Set state to 'Pending' when editing a 'Rejected' product
    }
  };

  console.log('Product state:', product.state);  // Debug: log the product state

  return (
    <TableRow sx={{ backgroundColor: index % 2 === 0 ? 'white' : '#f7f7f7' }}>
      <TableCell>
        <img src={product.images || "/placeholder-image.png"} alt={product.name} style={{ width: 100, height: 100 }} />
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
          product.state === 'Approved' ? <CheckCircleIcon color="success" /> :
          product.state === 'Rejected' ? <CancelIcon color="error" /> :
          product.state === 'Pending' ? <PendingIcon color="info"/> :
          product.state
        )}
      </TableCell>
      <TableCell>
        {isEditing ? (
          <Checkbox
            checked={editedProduct.publish}
            onChange={(e) => setEditedProduct(prev => ({ ...prev, publish: e.target.checked }))}
            disabled={!canPublish}  
          />
        ) : (
          <Checkbox
            checked={product.publish}
            disabled={!canPublish}  
          />
        )}
      </TableCell>
      <TableCell>
        <IconButton onClick={() => onDelete(product.id)}>
          <DeleteIcon />
        </IconButton>
        <IconButton onClick={toggleEditing}>
          <EditIcon />
        </IconButton>
        {isEditing && <Button sx={styles.greenRoundedButton} onClick={saveEdit}>Save</Button>}
      </TableCell>
    </TableRow>
  );
}

export default ProductListItem;
