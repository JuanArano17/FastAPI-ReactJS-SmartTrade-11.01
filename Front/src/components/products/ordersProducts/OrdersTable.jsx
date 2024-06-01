import React, { useState } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Modal, Box } from '@mui/material';
import OrderDetails from '../ordersProducts/OrderDetails';
import styles from '../../../styles/styles';

const OrdersTable = ({ data, isSeller }) => {
  const [selectedOrder, setSelectedOrder] = useState(null);

  const handleClose = () => {
    setSelectedOrder(null);
  };

  return (
    <>
      <TableContainer component={Paper} sx={{ borderRadius: '16px', boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.2)' }}>
        <Table sx={{ minWidth: 650 }} aria-label="orders table">
          <TableHead style={{ backgroundColor: '#cbe8ba' }}>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Total Price</TableCell>
              <TableCell >State</TableCell>
              <TableCell>Expected Arrival</TableCell>
              <TableCell sx={{ textAlign: 'center' }}>Actions</TableCell> 
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((order, index) => (
              <TableRow key={index}>
                <TableCell>{order.id}</TableCell>
                <TableCell>{order.total}</TableCell>
                <TableCell>{order.state}</TableCell>
                <TableCell>{order.estimated_date ? order.estimated_date : 'Pending'}</TableCell>
                <TableCell sx={{ textAlign: 'center' }}>
                  <Button
                    variant="contained"
                    color="primary"
                    sx={{
                      ...styles.greenRoundedButton 
                    }}
                    onClick={() => setSelectedOrder(order)}
                  >
                    View Details
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      
      <Modal
        open={!!selectedOrder}
        onClose={handleClose}
        aria-labelledby="order-details-modal"
        aria-describedby="order-details-description"
      >
        <Box sx={{ ...styles.modalBox }}>
          {selectedOrder && <OrderDetails order={selectedOrder} />}
        </Box>
      </Modal>
    </>
  );
};

export default OrdersTable;
