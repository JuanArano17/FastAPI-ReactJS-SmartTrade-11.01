import React, { useState, useEffect } from 'react';
import { Box, Button, Container, Typography,Fab  } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import TopBar from '../components/topbar/TopBar';
import Footer from '../components/footer/Footer';
import ArrowBackIcon from '@mui/icons-material/ArrowBack'; 
import AddProductForm from '../components/products/sellerproducts/AddProductForm';
import ProductList from '../components/products/sellerproducts/ProductList';
import styles from '../styles/styles';
import { editSellerProduct,deleteSellerProduct, getAllSellerProducts } from '../api/services/products/ProductsService';

const SellerProductsPage = () => {
  const [showAddForm, setShowAddForm] = useState(false);
  const [sellerproducts, setSellerProducts] = useState([]);
  
  useEffect(() => {
    const fetchSellerProducts = async () => {
      try {
        const sellerproductsData = await getAllSellerProducts();
        setSellerProducts(sellerproductsData);
        console.log(sellerproductsData)
      } catch (error) {
        console.error('Error fetching sellerproducts:', error);
      }
    };

    fetchSellerProducts();
  }, []);

  const toggleAddForm = () => {
    setShowAddForm(prev => !prev);
  };

  const handleAddProduct = async () => {
    try {
      
    }catch(error){

    }
  };

  const handleEditProduct = async (updatedProduct) => {
    try {
      const savedProduct = await editSellerProduct(updatedProduct);
      setSellerProducts(prevProducts =>
        prevProducts.map(product =>
          product.id === savedProduct.id ? { ...product, ...savedProduct } : product
        )
      );
    } catch (error) {
      console.error('Error saving product:', error);
    }
  };
  


  const handleDeleteProduct = async (seller_product_id) => {
    try {
      await deleteSellerProduct(seller_product_id);
      setSellerProducts(prevSellerProducts => prevSellerProducts.filter(sellerproducts => sellerproducts.id !== seller_product_id));
    } catch (error) {
      console.error('Error al eliminar la dirección:', error);
    }
  };

  return (
    <Box sx={styles.mainBox}>
      <TopBar />
      <Container sx={styles.mainContainer}>
        <Typography variant="h4" gutterBottom sx={{ mb: 2, color: '#629c44' }}>
          Your Products
        </Typography>
        <Box sx={{ position: 'relative', marginBottom: 2 }}>
          {showAddForm ? (
            <Fab color="secondary" sx={styles.addButton} onClick={toggleAddForm}>
              <ArrowBackIcon />
            </Fab>
          ) : (
            <Fab color="primary" sx={styles.addButton} onClick={toggleAddForm}>
              <AddIcon />
            </Fab>
          )}
          {!showAddForm ? (
            <ProductList products={sellerproducts} onDelete={handleDeleteProduct} onEdit={handleEditProduct} onSave={handleEditProduct} />
          ) : (
            <AddProductForm onSave={toggleAddForm} />
          )}
        </Box>
      </Container>
      <Footer />
    </Box>
  );
};

export default SellerProductsPage;