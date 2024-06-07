import React, { useEffect, useState } from "react";
import { Box, Container, Typography, Paper } from "@mui/material";
import TopBar from "../components/topbar/TopBar";
import Footer from "../components/footer/Footer";
import styles from "../styles/styles";
import OrdersTable from "../components/products/ordersProducts/OrdersTable";
import { getOrders } from "../api/services/orders/OrderService";
import { getProductLines } from "../api/services/product_lines/ProductLinesService";

const OrdersPage = () => {
  const userType = localStorage.getItem('type');
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      const responseData = userType === 'Buyer' ? await getOrders() : await getProductLines();
      setData(responseData);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [userType]);

  if (loading) {
    return <Typography variant="h6">Loading...</Typography>;
  }

  if (error) {
    return <Typography variant="h6">Error: {error.message}</Typography>;
  }

  return (
    <Box sx={styles.mainBox}>
      <TopBar />
      <Container sx={styles.mainContainer}>
        <Paper sx={styles.paperContainer}>
          <Typography variant="h4" gutterBottom sx={{ mb: 2, color: '#629c44' }}>
            {userType === 'Buyer' ? "Ordered Products" : "Product Lines"}
          </Typography>
          <OrdersTable data={data} isSeller={userType === 'Seller'} reloadData={fetchData} />
        </Paper>
      </Container>
      <Footer />
    </Box>
  );
};

export default OrdersPage;