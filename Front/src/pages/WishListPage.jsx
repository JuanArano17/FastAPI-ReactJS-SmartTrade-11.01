import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import { Box, Container, Typography, Grid } from '@mui/material';
import TopBar from '../components/topbar/TopBar';
import WishListItem from '../components/products/wishlist/WishListItem';
import Footer from '../components/footer/Footer';
import styles from '../styles/styles';
import { getAllProducts } from '../api/services/products/ProductsService';
import { getWishItems } from '../api/services/products/WishListService';


const WishListPage = () => {
    const [wishItems, setWishItems] = useState([]);

    useEffect(() => {
        const fetchWishData = async () => {
            try {
                const wishListItems = await getWishItems();
                const allProducts = await getAllProducts();

                // Combine the wish items with product details
                const itemsWithDetails = wishListItems.map(wishItem => {
                    const product = allProducts.find(p => p.id_seller_product === wishItem.id_seller_product);
                    return { ...wishItem, ...product };
                });

                console.log("Items recibidos del backend para la lista de deseos:", itemsWithDetails);
                setWishItems(itemsWithDetails);
            } catch (error) {
                console.error('Error al cargar los datos de la lista de deseos:', error);
            }
        };

        fetchWishData();
    }, []);
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
                <Typography variant="h4" sx={{ color: '#629C44', my: 2, fontWeight: 'bold' }}>
                    Wish List
                </Typography>
                <Grid container spacing={2}>
                    {wishItems.map((item) => (
                        <WishListItem key={item.id_seller_product} item={item} />
                    ))}
                </Grid>
            </Container>
            <Footer />
        </Box>
    );
};

export default WishListPage;
