import React from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Checkbox, IconButton } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';

const ProductList = ({ products, onDelete, onEdit }) => {
  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple product table">
        <TableHead>
          <TableRow>
            <TableCell>Image</TableCell>
            <TableCell>Name</TableCell>
            <TableCell>More info</TableCell>
            <TableCell>Stock</TableCell>
            <TableCell>Price</TableCell>
            <TableCell>Publish</TableCell>
            <TableCell>Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {products.map((product) => (
            <TableRow key={product.id}>
              <TableCell component="th" scope="row">
                <img src="/placeholder-image.png" alt="product" style={{ width: 50, height: 50 }} />
              </TableCell>
              <TableCell>{product.name}</TableCell>
              <TableCell>{product.info}</TableCell>
              <TableCell>{product.stock}</TableCell>
              <TableCell>{product.price}</TableCell>
              <TableCell padding="checkbox">
                <Checkbox checked={product.publish} />
              </TableCell>
              <TableCell>
                <IconButton aria-label="edit" onClick={() => onEdit(product.id)}>
                  <EditIcon />
                </IconButton>
                <IconButton aria-label="delete" onClick={() => onDelete(product.id)}>
                  <DeleteIcon />
                </IconButton>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default ProductList;
