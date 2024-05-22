import React, { useState, useEffect } from 'react';
import { Box, Container, Typography, Grid, Button, Radio, RadioGroup, FormControlLabel, FormControl, FormLabel, Dialog, DialogTitle, DialogContent, DialogActions } from '@mui/material';
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
    const [openAddCard, setOpenAddCard] = useState(false);
    const [openAddAddress, setOpenAddAddress] = useState(false);
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
        setOpenAddCard(false);
    };

    const handleAddAddress = async (newAddress) => {
        const createdAddress = await createAddress(newAddress);
        setAddresses(prevAddresses => [...prevAddresses, createdAddress]);
        setOpenAddAddress(false);
    };

    return (
        <Box sx={styles.mainBox}>
            <TopBar showLogoutButton={true} />
            <Container component="main" maxWidth="md" sx={styles.mainContainer}>
                <Typography variant="h4" sx={{ color: '#629C44', my: 2, fontWeight: 'bold' }}>
                    Buying Process
                </Typography>
                <Grid container spacing={2}>
                    <Grid item xs={12}>
                        <FormControl component="fieldset">
                            <FormLabel component="legend">Select a Card</FormLabel>
                            <RadioGroup value={selectedCard} onChange={(e) => setSelectedCard(e.target.value)}>
                                {cards.map((card) => (
                                    <FormControlLabel key={card.id} value={card.card_name} control={<Radio />} label={`${card.card_name}`} />
                                ))}
                            </RadioGroup>
                            <Button variant="outlined" sx={{ mt: 2 }} onClick={() => setOpenAddCard(true)}>
                                Add New Card
                            </Button>
                        </FormControl>
                    </Grid>
                    <Grid item xs={12}>
                        <FormControl component="fieldset">
                            <FormLabel component="legend">Select a Shipping Address</FormLabel>
                            <RadioGroup value={selectedAddress} onChange={(e) => setSelectedAddress(e.target.value)}>
                                {addresses.map((address) => (
                                    <FormControlLabel key={address.id} value={address.street} control={<Radio />} label={`${address.street}, ${address.city}`} />
                                ))}
                            </RadioGroup>
                            <Button variant="outlined" sx={{ mt: 2 }} onClick={() => setOpenAddAddress(true)}>
                                Add New Address
                            </Button>
                        </FormControl>
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
                </Grid>
            </Container>
            <Footer />
            <Dialog open={openAddCard} onClose={() => setOpenAddCard(false)}>
                <DialogTitle>Add New Card</DialogTitle>
                <DialogContent>
                    <AddCard onSave={handleAddCard} />
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setOpenAddCard(false)} color="primary">
                        Cancel
                    </Button>
                </DialogActions>
            </Dialog>
            <Dialog open={openAddAddress} onClose={() => setOpenAddAddress(false)}>
                <DialogTitle>Add New Address</DialogTitle>
                <DialogContent>
                    <AddAddressForm onAddressCreated={handleAddAddress} />
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setOpenAddAddress(false)} color="primary">
                        Cancel
                    </Button>
                </DialogActions>
            </Dialog>
        </Box>
    );
};

export default BuyingProcessPage;
