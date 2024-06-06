import React, { useState } from 'react';
import { Table, Typography, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Modal, Box, TextField } from '@mui/material';
import OrderDetails from '../ordersProducts/OrderDetails';
import styles from '../../../styles/styles';
import { addEstimatedDate } from '../../../api/services/product_lines/ProductLinesService';

const OrdersTable = ({ data, isSeller, reloadData }) => {
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [selectedProductLine, setSelectedProductLine] = useState(null);
  const [estimatedDate, setEstimatedDate] = useState('');

  const handleClose = () => {
    setSelectedOrder(null);
    setSelectedProductLine(null);
    setEstimatedDate('');
  };

  const handleAddDate = async () => {
    try {
      await addEstimatedDate(selectedProductLine.id, { estimated_date: estimatedDate });
      handleClose();
      reloadData(); // Volver a cargar los datos
    } catch (error) {
      console.error("Error adding estimated date:", error);
    }
  };

  return (
    <>
      <TableContainer component={Paper} sx={{ borderRadius: '16px', boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.2)' }}>
        <Table sx={{ minWidth: 650 }} aria-label="orders table">
          <TableHead style={{ backgroundColor: '#cbe8ba' }}>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>{isSeller ? "Product Name" : "Total Price"}</TableCell>
              {isSeller ? null : <TableCell>State</TableCell>}
              <TableCell>Expected Arrival</TableCell>
              <TableCell sx={{ textAlign: 'center' }}>Actions</TableCell> 
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((item, index) => (
              <TableRow key={index}>
                <TableCell>{item.id}</TableCell>
                <TableCell>{isSeller ? item.name : item.total}</TableCell>
                {isSeller ? null : <TableCell>{item.state}</TableCell>}
                <TableCell>{item.estimated_date ? item.estimated_date : 'Pending'}</TableCell>
                <TableCell sx={{ textAlign: 'center' }}>
                  <Button
                    variant="contained"
                    color="primary"
                    sx={{
                      ...styles.greenRoundedButton 
                    }}
                    onClick={() => isSeller ? setSelectedProductLine(item) : setSelectedOrder(item)}
                  >
                    {isSeller ? "Add Date" : "View Details"}
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      
      <Modal
        open={!!selectedOrder || !!selectedProductLine}
        onClose={handleClose}
        aria-labelledby="order-details-modal"
        aria-describedby="order-details-description"
      >
        <Box sx={{ ...styles.modalBox, width: '650px' }}>
          {selectedOrder && <OrderDetails order={selectedOrder} />}
          {selectedProductLine && (
            <Box>
              <Typography variant="h6" sx={{ mb: 2 }}>Add Estimated Date for {selectedProductLine.name}</Typography>
              <TextField
                label="Estimated Date"
                type="date"
                fullWidth
                value={estimatedDate}
                onChange={(e) => setEstimatedDate(e.target.value)}
                sx={{ mb: 2 }}
                InputLabelProps={{
                  shrink: true,
                }}
              />
              <Button
                variant="contained"
                color="primary"
                sx={{ ...styles.greenRoundedButton }}
                onClick={handleAddDate}
              >
                Save
              </Button>
            </Box>
          )}
        </Box>
      </Modal>
    </>
  );
};

export default OrdersTable;