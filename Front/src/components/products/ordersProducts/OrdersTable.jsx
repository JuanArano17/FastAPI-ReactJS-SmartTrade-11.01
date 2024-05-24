import React from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

const OrdersTable = ({ data, isSeller }) => {
  return (
    <TableContainer component={Paper} sx={{ borderRadius: '16px', boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.2)' }}>
      <Table sx={{ minWidth: 650 }} aria-label="orders table">
        <TableHead style={{ backgroundColor: '#cbe8ba' }}>
          <TableRow>
            <TableCell>Image</TableCell>
            <TableCell>Name</TableCell>
            <TableCell>Info</TableCell>
            <TableCell>Quantity</TableCell>
            <TableCell>Price</TableCell>
            <TableCell>State</TableCell>
            <TableCell>Expected Arrival</TableCell>
            {isSeller && <TableCell>Actions</TableCell>}
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((order, index) => (
            <TableRow key={index}>
              <TableCell>{order.image}</TableCell>
              <TableCell>{order.name}</TableCell>
              <TableCell>{order.info}</TableCell>
              <TableCell>{order.quantity}</TableCell>
              <TableCell>{order.price}</TableCell>
              <TableCell>{order.state}</TableCell>
              <TableCell>{order.expectedArrival}</TableCell>
              {isSeller && <TableCell>{order.actions}</TableCell>}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default OrdersTable;
