import React from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import ProductListItem from './ProductListItem';

const ProductList = ({ products, onDelete, onEdit, onSave }) => {
  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple product table">
        <TableHead style={{ backgroundColor: '#cbe8ba' }}>
          <TableRow>
            <TableCell>Image</TableCell>
            <TableCell>Name</TableCell>
            <TableCell>Quantity</TableCell>
            <TableCell>Price</TableCell>
            <TableCell>Shipping Costs</TableCell>
            <TableCell>State</TableCell>
            <TableCell>Publish</TableCell>
            <TableCell>Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {products.map((product, index) => (
            <ProductListItem
              key={product.id}
              product={product}
              index={index}
              onDelete={onDelete}
              onEdit={onEdit}
              onSave={onSave}
            />
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default ProductList;
