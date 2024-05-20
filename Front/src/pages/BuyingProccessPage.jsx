import React, { useState, useEffect } from 'react';
import { Box, Container, Typography, Grid, Button } from '@mui/material';
import TopBar from '../components/topbar/TopBar';
import Footer from '../components/footer/Footer';
import styles from '../styles/styles';
import SelectCardAndShipping from '../components/buysystem/SelectCardAndShipping';
import ProductSummary from '../components/buysystem/ProductSummary';
import ReviewProduct from '../components/buysystem/ReviewProduct';
import { getCartItems } from '../api/services/products/ShoppingCartService';
import CartSummary from '../components/buysystem/CartSummary';

const BuyingProcessPage = () => {
    const [step, setStep] = useState(1);
    const [cartItems, setCartItems] = useState([]);
    const [selectedCard, setSelectedCard] = useState(null);
    const [selectedAddress, setSelectedAddress] = useState(null);

    useEffect(() => {
        const fetchCartData = async () => {
            try {
                const items = await getCartItems();
                setCartItems(items);
            } catch (error) {
                console.error('Error al cargar los datos del carrito:', error);
            }
        };
        fetchCartData();
    }, []);

    const handleContinue = () => {
        setStep(step + 1);
    };

    const handleBack = () => {
        setStep(step - 1);
    };

    return (
        <Box sx={styles.mainBox}>
            <TopBar showLogoutButton={true} />
            <Container component="main" maxWidth="md" sx={styles.mainContainer}>
                {step === 1 && (
                    <SelectCardAndShipping
                        onCardSelect={setSelectedCard}
                        onAddressSelect={setSelectedAddress}
                        selectedCard={selectedCard}
                        selectedAddress={selectedAddress}
                        onContinue={handleContinue}
                        onBack={handleBack}
                    />
                )}
                {step === 2 && (
                    <ProductSummary
                        cartItems={cartItems}
                        selectedCard={selectedCard}
                        selectedAddress={selectedAddress}
                        onConfirm={handleContinue}
                        onBack={handleBack}
                    />
                )}
                {step === 3 && <ReviewProduct onBack={handleBack} />}
            </Container>
            <Footer />
        </Box>
    );
};

export default BuyingProcessPage;