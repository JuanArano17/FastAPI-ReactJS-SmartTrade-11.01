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
            <TableCell>More info</TableCell>
            <TableCell>Quantity</TableCell>
            <TableCell>Price</TableCell>
            <TableCell>State</TableCell>
            <TableCell>Expected Arrival</TableCell>
            {isSeller && <TableCell>Actions</TableCell>}
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((row, index) => (
            <TableRow key={index} sx={{ backgroundColor: index % 2 === 0 ? 'white' : '#f7f7f7' }}>
              <TableCell>{row.image}</TableCell>
              <TableCell>{row.name}</TableCell>
              <TableCell>{row.info}</TableCell>
              <TableCell>{row.quantity}</TableCell>
              <TableCell>{row.price}</TableCell>
              <TableCell>{row.state}</TableCell>
              <TableCell>{row.expectedArrival}</TableCell>
              {isSeller && <TableCell>{row.actions}</TableCell>}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default OrdersTable;
