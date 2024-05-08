import React, { useState, useEffect } from 'react';
import { Box, Button, Snackbar, Alert } from '@mui/material';
import CardItem from './CardItem';
import AddCard from './AddCard'; 
import { getCardInfo, deleteCardItem, createCard, updateCard } from '../../../api/services/user/profile/ProfileService';
import styles from '../../../styles/styles';

const Cards = () => {
  const [cards, setCards] = useState([]);
  const [showAddCardForm, setShowAddCardForm] = useState(false);
  const [apiError, setApiError] = useState('');

  useEffect(() => {
    const fetchCards = async () => {
      try {
        const fetchedCards = await getCardInfo();
        setCards(fetchedCards);
      } catch (error) {
        console.error('Error fetching cards:', error);
        setApiError('Failed to fetch cards.');
      }
    };

    fetchCards();
  }, []);

  const handleDeleteCard = async (cardId) => {
    try {
      await deleteCardItem(cardId);
      setCards(prevCards => prevCards.filter(card => card.id !== cardId));
    } catch (error) {
      console.error('Error deleting card:', error);
      setApiError('Failed to delete card.');
    }
  };

  const handleUpdateCard = async (cardId, updatedCard) => {
    try {
      const updatedData = await updateCard(cardId, updatedCard);
      setCards(prevCards => prevCards.map(card => card.id === cardId ? { ...card, ...updatedData } : card));
    } catch (error) {
      console.error('Error updating card:', error);
      setApiError('Failed to update card.');
    }
  };

  const handleAddCardClick = () => {
    setShowAddCardForm(true);
  };

  const handleSaveCard = async (newCard) => {
    try {
      const savedCard = await createCard(newCard);
      setCards(prevCards => [...prevCards, savedCard]);
      setShowAddCardForm(false); 
    } catch (error) {
      console.error('Error saving new card:', error);
      setApiError('Failed to save new card.');
    }
  };

  const handleCloseSnackbar = () => {
    setApiError('');
  };

  return (
    <Box sx={{ my: 2 }}>
      {showAddCardForm ? (
        <AddCard onSave={handleSaveCard} />
      ) : (
        <>
          {cards.map(card => (
            <CardItem
              key={card.id}
              {...card}
              onDelete={() => handleDeleteCard(card.id)}
              onUpdate={handleUpdateCard}
            />
          ))}
          <Button sx={{...styles.greenRoundedButton, mt:4}} variant="contained" color="primary" onClick={handleAddCardClick}>
            Add Card
          </Button>
        </>
      )}
      <Snackbar open={!!apiError} autoHideDuration={6000} onClose={handleCloseSnackbar}>
        <Alert onClose={handleCloseSnackbar} severity="error" sx={{ width: '100%' }}>
          {apiError}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default Cards;
