import React, { useState } from 'react';
import { Box, Container, Typography, Grid, Button, TextField, Rating } from '@mui/material';
import { useHistory } from 'react-router-dom';
import TopBar from '../components/topbar/TopBar';
import Footer from '../components/footer/Footer';
import styles from '../styles/styles';

const ReviewProductPage = () => {
    const [rating, setRating] = useState(0);
    const [comment, setComment] = useState('');
    const history = useHistory();

    const handleSubmitReview = () => {
        // Aquí puedes manejar el envío de la reseña a la API.
        console.log('Rating:', rating);
        console.log('Comment:', comment);
        history.push('/');
    };

    return (
        <Box sx={styles.mainBox}>
            <TopBar showLogoutButton={true} />
            <Container component="main" maxWidth="md" sx={styles.mainContainer}>
                <Typography variant="h4" sx={{ color: '#629C44', my: 2, fontWeight: 'bold' }}>
                    Review Product
                </Typography>
                <Grid container spacing={2}>
                    <Grid item xs={12}>
                        <Typography variant="h6">Rate your experience</Typography>
                        <Rating
                            name="rating"
                            value={rating}
                            onChange={(event, newValue) => {
                                setRating(newValue);
                            }}
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField
                            label="Leave a comment"
                            fullWidth
                            multiline
                            rows={4}
                            variant="outlined"
                            value={comment}
                            onChange={(e) => setComment(e.target.value)}
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <Button
                            fullWidth
                            variant="contained"
                            color="primary"
                            sx={{ ...styles.greenRoundedButton, mt: 2 }}
                            onClick={handleSubmitReview}
                        >
                            Submit Review
                        </Button>
                    </Grid>
                </Grid>
            </Container>
            <Footer />
        </Box>
    );
};

export default ReviewProductPage;
