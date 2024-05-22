import React, { useState, useEffect } from 'react';
import { Box, Container, Typography, Paper, Grid, Button, Radio, RadioGroup, FormControlLabel, FormControl, FormLabel } from '@mui/material';
import { useHistory } from 'react-router-dom';
import TopBar from '../components/topbar/TopBar';
import Footer from '../components/footer/Footer';
import { getCardInfo, getAddresssesInfo, createCard, createAddress } from '../api/services/user/profile/ProfileService';
import styles from '../styles/styles';
import AddCard from '../components/profile/cards/AddCard';
import AddAddressForm from '../components/profile/shipping-addresses/AddAddressForm';

const BuyingProcessPage = () => {
    const [cards, setCards] = useState([]);
    const [addresses, setAddresses] = useState([]);
    const [selectedCard, setSelectedCard] = useState(null);
    const [selectedAddress, setSelectedAddress] = useState(null);
    const [showAddCardForm, setShowAddCardForm] = useState(false);
    const [showAddAddressForm, setShowAddAddressForm] = useState(false);
    const history = useHistory();

    useEffect(() => {
        const fetchData = async () => {
            const cardData = await getCardInfo();
            const addressData = await getAddresssesInfo();
            setCards(cardData);
            setAddresses(addressData);
            console.log("cards", cardData);
            console.log("addresses", addressData);
        };
        fetchData();
    }, []);

    const handleContinue = () => {
        if (selectedCard && selectedAddress) {
            history.push('/buy-summary', { selectedCard, selectedAddress });
        }

        console.log("selectedCard: ", selectedCard);
        console.log("selectedAddress:", selectedAddress);
    };

    const handleAddCard = async (newCard) => {
        const createdCard = await createCard(newCard);
        setCards(prevCards => [...prevCards, createdCard]);
        setShowAddCardForm(false);
    };

    const handleAddAddress = async (newAddress) => {
        const createdAddress = await createAddress(newAddress);
        setAddresses(prevAddresses => [...prevAddresses, createdAddress]);
        setShowAddAddressForm(false);
    };

    return (
        <Box sx={styles.mainBox}>
            <TopBar showLogoutButton={true} />
            <Container component="main" maxWidth="md" sx={styles.mainContainer}>
                <Paper sx={styles.paperContainer}>
                    <Typography variant="h4" sx={{ color: '#629C44', my: 2, fontWeight: 'bold' }}>
                        Buying Process
                    </Typography>
                    <Grid container spacing={2}>
                        {!showAddCardForm && !showAddAddressForm && (
                            <>
                                <Grid container spacing={2}>
                                    <Grid item xs={12} md={6}>
                                        <FormControl component="fieldset">
                                            <FormLabel component="legend">Select a Card</FormLabel>
                                            <RadioGroup value={selectedCard} onChange={(e) => setSelectedCard(e.target.value)}>
                                                {cards.map((card) => (
                                                    <FormControlLabel key={card.id} value={card.card_name} control={<Radio />} label={`${card.card_name}`} />
                                                ))}
                                            </RadioGroup>
                                            <Button sx={styles.greenRoundedButton} onClick={() => setShowAddCardForm(true)}>
                                                Add New Card
                                            </Button>
                                        </FormControl>
                                    </Grid>
                                    <Grid item xs={12} md={6}>
                                        <FormControl component="fieldset">
                                            <FormLabel component="legend">Select a Shipping Address</FormLabel>
                                            <RadioGroup value={selectedAddress} onChange={(e) => setSelectedAddress(e.target.value)}>
                                                {addresses.map((address) => (
                                                    <FormControlLabel key={address.id} value={address.street} control={<Radio />} label={`${address.street}, ${address.city}`} />
                                                ))}
                                            </RadioGroup>
                                            <Button  sx={styles.greenRoundedButton} onClick={() => setShowAddAddressForm(true)}>
                                                Add New Address
                                            </Button>
                                        </FormControl>
                                    </Grid>
                                </Grid>
                                <Grid item xs={12}>
                                    <Button
                                        fullWidth
                                        variant="contained"
                                        color="primary"
                                        sx={{ ...styles.greenRoundedButton, mt: 2 }}
                                        onClick={handleContinue}
                                        disabled={!selectedCard || !selectedAddress}
                                    >
                                        Continue
                                    </Button>
                                </Grid>
                            </>
                        )}
                        {showAddCardForm && (
                            <Grid item xs={12}>
                                <AddCard onSave={handleAddCard} />
                                <Button variant="outlined" sx={{ mt: 2 }} onClick={() => setShowAddCardForm(false)}>
                                    Cancel
                                </Button>
                            </Grid>
                        )}
                        {showAddAddressForm && (
                            <Grid item xs={12}>
                                <AddAddressForm onAddressCreated={handleAddAddress} />
                                <Button variant="outlined" sx={{ mt: 2 }} onClick={() => setShowAddAddressForm(false)}>
                                    Cancel
                                </Button>
                            </Grid>
                        )}
                    </Grid>
                </Paper>
            </Container>
            <Footer />
        </Box>
    );
};

export default BuyingProcessPage;
