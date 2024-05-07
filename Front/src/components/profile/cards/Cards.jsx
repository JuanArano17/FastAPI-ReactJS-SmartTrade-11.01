import React, { useState, useEffect } from 'react';
import { Box, Button } from '@mui/material';
import CardItem from './CardItem';
import AddCardForm from './AddCard'; 
import { getCardInfo, deleteCardItem, createCard, updateCard } from '../../../api/services/user/profile/ProfileService';
import styles from '../../../styles/styles';

const Cards = () => {
  const [cards, setCards] = useState([]);
  const [showAddCardForm, setShowAddCardForm] = useState(false);

  useEffect(() => {
    const fetchCards = async () => {
      try {
        const fetchedCards = await getCardInfo();
        setCards(fetchedCards);
        console.log(fetchedCards);
      } catch (error) {
        console.error('Error fetching cards:', error);
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
    }
  };

  const handleUpdateCard = async (cardId, updatedCard) => {
    try {
      const updatedData = await updateCard(cardId, updatedCard);
      setCards(prevCards => prevCards.map(card => card.id === cardId ? { ...card, ...updatedData } : card));
    } catch (error) {
      console.error('Error updating card:', error);
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
    }
  };

  return (
    <Box>
      {showAddCardForm ? (
        <AddCardForm onSave={handleSaveCard} />
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
    </Box>
  );
};

export default Cards;
