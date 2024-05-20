import React, { useState } from 'react';
import { Box, Container, Typography, TextField, Button, Rating } from '@mui/material';
import styles from '../../styles/styles';

const ReviewProduct = ({ onBack }) => {
    const [rating, setRating] = useState(0);
    const [review, setReview] = useState('');

    const handleSubmitReview = () => {
        // Handle review submission
    };

    return (
        <Box>
            <Typography variant="h4" sx={{ color: '#629C44', my: 2, fontWeight: 'bold' }}>
                Review Item
            </Typography>
            <Box sx={{ mt: 2 }}>
                <Typography variant="h6">Product 1</Typography>
                <Rating
                    name="simple-controlled"
                    value={rating}
                    onChange={(event, newValue) => {
                        setRating(newValue);
                    }}
                />
                <TextField
                    fullWidth
                    label="Add some more info..."
                    multiline
                    rows={4}
                    value={review}
                    onChange={(e) => setReview(e.target.value)}
                    sx={{ mt: 2 }}
                />
                <Button
                    fullWidth
                    variant="contained"
                    color="primary"
                    sx={{ ...styles.greenRoundedButton, mt: 2 }}
                    onClick={handleSubmitReview}
                >
                    Submit Review
                </Button>
                <Button
                    fullWidth
                    variant="contained"
                    sx={{ ...styles.greenRoundedButton, mt: 2 }}
                    onClick={onBack}
                >
                    Back
                </Button>
            </Box>
        </Box>
    );
};

export default ReviewProduct;
