import React, { useState, useEffect } from 'react';
import { Grid, Typography, Button, RadioGroup, FormControlLabel, Radio } from '@mui/material';
import styles from '../../styles/styles';
import { getAddresssesInfo, getCardInfo } from '../../api/services/user/profile/ProfileService';
import AddCard from '../profile/cards/AddCard';
import AddAddressForm from '../profile/shipping-addresses/AddAddressForm';

const SelectCardAndShipping = ({ onCardSelect, onAddressSelect, selectedCard, selectedAddress, onContinue, onBack }) => {
    const [cards, setCards] = useState([]);
    const [addresses, setAddresses] = useState([]);
    const [showAddCard, setShowAddCard] = useState(false);
    const [showAddAddress, setShowAddAddress] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            const cardData = await getCardInfo();
            const addressData = await getAddresssesInfo();
            setCards(cardData);
            setAddresses(addressData);
        };
        fetchData();
    }, []);

    return (
        <div>
            <Typography variant="h4" sx={{ color: '#629C44', my: 2, fontWeight: 'bold' }}>
                Select Card and Shipping Address
            </Typography>
            <Grid container spacing={2}>
                <Grid item xs={6}>
                    {showAddCard ? (
                        <AddCard onSave={(card) => {
                            setCards([...cards, card]);
                            setShowAddCard(false);
                        }} />
                    ) : (
                        <>
                            <Typography variant="h6">Select Card</Typography>
                            <RadioGroup value={selectedCard} onChange={(e) => onCardSelect(e.target.value)}>
                                {cards.map((card) => (
                                    <FormControlLabel key={card.id} value={card.id} control={<Radio />} label={`${card.card_number} - ${card.card_name}`} />
                                ))}
                            </RadioGroup>
                            <Button onClick={() => setShowAddCard(true)}>Add new Card</Button>
                        </>
                    )}
                </Grid>
                <Grid item xs={6}>
                    {showAddAddress ? (
                        <AddAddressForm onAddressCreated={(address) => {
                            setAddresses([...addresses, address]);
                            setShowAddAddress(false);
                        }} />
                    ) : (
                        <>
                            <Typography variant="h6">Select Shipping Address</Typography>
                            <RadioGroup value={selectedAddress} onChange={(e) => onAddressSelect(e.target.value)}>
                                {addresses.map((address) => (
                                    <FormControlLabel key={address.id} value={address.id} control={<Radio />} label={`${address.street}, ${address.city}`} />
                                ))}
                            </RadioGroup>
                            <Button onClick={() => setShowAddAddress(true)}>Add new Address</Button>
                        </>
                    )}
                </Grid>
                <Grid item xs={12}>
                    <Button
                        fullWidth
                        variant="contained"
                        color="primary"
                        sx={{ ...styles.greenRoundedButton, mt: 2 }}
                        onClick={onContinue}
                        disabled={!selectedCard || !selectedAddress}
                    >
                        Continue
                    </Button>
                </Grid>
                <Grid item xs={12}>
                    <Button
                        fullWidth
                        variant="contained"
                        sx={{ ...styles.greenRoundedButton, mt: 2 }}
                        onClick={onBack}
                    >
                        Back
                    </Button>
                </Grid>
            </Grid>
        </div>
    );
};

export default SelectCardAndShipping;
