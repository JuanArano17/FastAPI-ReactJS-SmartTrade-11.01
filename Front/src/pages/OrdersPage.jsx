import React, { useEffect, useState } from "react";
import { Box, Container, Typography, Paper, Fab } from "@mui/material";
import TopBar from "../components/topbar/TopBar";
import Footer from "../components/footer/Footer";
import styles from "../styles/styles";
import AddIcon from '@mui/icons-material/Add';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import OrdersTable from "../components/products/ordersProducts/OrdersTable";

const OrdersPage = () => {
  const userType = localStorage.getItem('type');
  const [ordersData, setOrdersData] = useState([]);

  useEffect(() => {

    if (userType === 'Buyer') {
      setOrdersData([
        {
          image: "Image1",
          name: "Product 1",
          info: "Lorem ipsum",
          quantity: 10,
          price: "$25",
          state: "Packaging",
          expectedArrival: "19/06/2024"
        },
        {
          image: "Image2",
          name: "Product 2",
          info: "Lorem ipsum",
          quantity: 20,
          price: "$60",
          state: "On the way",
          expectedArrival: "20/08/2024"
        },
        {
          image: "Image3",
          name: "Product 3",
          info: "Lorem ipsum",
          quantity: 1,
          price: "$100",
          state: "Arrived",
          expectedArrival: "07/05/2024"
        }
      ]);
    } else {
      setOrdersData([
        {
          image: "Image1",
          name: "Product 1",
          info: "Lorem ipsum",
          quantity: 10,
          price: "$25",
          state: "Packaging",
          expectedArrival: "19/06/2024",
          actions: "Edit/Delete"
        },
        {
          image: "Image2",
          name: "Product 2",
          info: "Lorem ipsum",
          quantity: 20,
          price: "$60",
          state: "On the way",
          expectedArrival: "20/08/2024",
          actions: "Edit/Delete"
        },
        {
          image: "Image3",
          name: "Product 3",
          info: "Lorem ipsum",
          quantity: 1,
          price: "$100",
          state: "Arrived",
          expectedArrival: "07/05/2024",
          actions: "Edit/Delete"
        }
      ]);
    }
  }, [userType]);

  const handleBack = () => {
    // Handle back action here
  };

  return (
    <Box sx={styles.mainBox}>
      <TopBar />
      <Container sx={styles.mainContainer}>
        <Paper sx={styles.paperContainer}>
          <Typography variant="h4" gutterBottom sx={{ mb: 2, color: '#629c44' }}>
            {userType === 'Buyer' ? "Ordered Products" : "Sold Products"}
          </Typography>
          <OrdersTable data={ordersData} isSeller={userType === 'Seller'} />
        </Paper>
      </Container>
      <Footer />
    </Box>
  );
};

export default OrdersPage;
