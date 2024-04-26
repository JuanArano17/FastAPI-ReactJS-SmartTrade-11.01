import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import { Box, Container, Typography, Grid } from '@mui/material';
import TopBar from '../components/topbar/TopBar';
import WishListItem from '../components/products/wishlist/WishListItem';
import Footer from '../components/footer/Footer';
import styles from '../styles/styles';
import { getWishItems } from '../api/services/products/WishListService';


const WishListPage = () => {
    const [wishItems, setWishItems] = useState([]);
    const removeItemFromWishList = (productId) => {
        setWishItems((currentItems) => currentItems.filter((item) => item.seller_product.id !== productId));
    };
    useEffect(() => {
        const fetchWishData = async () => {
            try {
                const wishListItems = await getWishItems();
                console.log("Items recibidos del backend para la lista de deseos:", wishListItems);
                setWishItems(wishListItems);
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
                        <WishListItem 
                        key={item.seller_product.id} 
                        item={item.seller_product} 
                        onRemove={removeItemFromWishList}
                        />
                    ))}
                </Grid>
            </Container>
            <Footer />
        </Box>
    );
};

export default WishListPage;
