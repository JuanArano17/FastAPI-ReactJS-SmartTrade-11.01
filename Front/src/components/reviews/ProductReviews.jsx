import React, { useEffect, useState } from 'react';
import { Box, Typography, Divider, CircularProgress, Rating } from '@mui/material';
import { getProductReviews } from '../../api/services/products/ReviewsService'; // Ajusta esta ruta según tu estructura de proyecto

const ProductReviews = ({ productId }) => {
    const [reviews, setReviews] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchReviews = async () => {
            try {
                const response = await getProductReviews(productId); 
                setReviews(response);
                setLoading(false);
            } catch (err) {
                setError(err.response ? err.response.status : err.message);
                setLoading(false);
            }
        };
        fetchReviews();
    }, [productId]);

    if (loading) {
        return <CircularProgress />;
    }

    if (error) {
        return <Typography color="error">Request failed with status code {error}</Typography>;
    }

    return (
        <Box>
            <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                Reviews
            </Typography>
            <Divider sx={{ my: 2 }} />
            {reviews.length === 0 ? (
                <Typography>No reviews available for this product.</Typography>
            ) : (
                reviews.map((review) => (
                    <Box key={review.id} sx={{ mb: 2 }}>
                        <Typography variant="h6">{review.buyer.name} {review.buyer.surname}</Typography>
                        <Typography variant="body1">{review.comment}</Typography>
                        <Rating name="read-only" value={review.stars} readOnly />
                    </Box>
                ))
            )}
        </Box>
    );
};

export default ProductReviews;
