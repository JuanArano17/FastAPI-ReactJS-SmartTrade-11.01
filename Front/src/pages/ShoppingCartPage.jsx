import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import { Box, Container, Typography, Grid } from '@mui/material';
import TopBar from '../components/topbar/TopBar';
import Footer from '../components/footer/Footer';
import CartItem from '../components/products/shoppingcart/CartItem';
import CartTotal from '../components/products/shoppingcart/CartTotal';
import styles from '../styles/styles';
import { getCartItems } from '../api/services/products/ShoppingCartService';
import { getAllProducts } from '../api/services/products/ProductsService';

const ShoppingCartPage = () => {
    const [cartItems, setCartItems] = useState([]);

    useEffect(() => {
        const fetchCartData = async () => {
            try {
                const cartItems = await getCartItems();
                const allProducts = await getAllProducts();

                const itemsWithDetails = cartItems.map(cartItem => {
                    const product = allProducts.find(p => p.id_seller_product === cartItem.id_seller_product);
                    return { ...cartItem, ...product };
                });

                console.log("Items recibidos del backend:", itemsWithDetails);
                setCartItems(itemsWithDetails);
            } catch (error) {
                console.error('Error al cargar los datos del carrito:', error);
            }
        };

        fetchCartData();
    }, []);

    const calculateTotal = () => cartItems.reduce((acc, item) => acc + item.price * item.quantity, 0);

    const history = useHistory();

    useEffect(() => {
        const token = localStorage.getItem('accessToken');
        if (!token) {
            history.push('/');
        }
    }, [history]);
    return (
        <Box sx={styles.mainBox}>
            <TopBar showLogoutButton={true} />
            <Container component="main" maxWidth="md" sx={styles.mainContainer}>
                <Typography variant="h4" sx={{color:'#629C44', my: 2, fontWeight:'bold' }}>
                    Shopping Cart
                </Typography>
                <Grid container spacing={2}>
                    {cartItems.map((item) => (
                        <CartItem key={item.id_seller_product} item={item} setCartItems={setCartItems} />
                    ))}
                    <Grid item xs={12}>
                        <CartTotal total={calculateTotal()} />
                    </Grid>
                </Grid>
            </Container>
            <Footer />
        </Box>
    );
};
export default ShoppingCartPage;