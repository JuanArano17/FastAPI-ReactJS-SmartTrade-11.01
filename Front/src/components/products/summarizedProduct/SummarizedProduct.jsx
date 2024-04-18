import React from 'react';
import { Card, CardMedia, CardContent, Typography, CardActions, Button, Grid } from '@mui/material';

const SummarizedProduct = ({ product }) => {
    const { id, name, image, price, description } = product;

    return (
        <Card sx={{ maxWidth: 345, m: 2, display: 'flex', flexDirection: 'column', justifyContent: 'space-between', height: 400 }}>
            <CardMedia
                component="img"
                image={image || 'default-product-image.jpg'} 
                alt={name}
                sx={{ height: 140, backgroundSize: 'contain' }} 
            />
            <CardContent>
                <Typography gutterBottom variant="h6" component="div" sx={{ textAlign: 'left' }}>
                    {name}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'left' }}>
                    {description}
                </Typography>
            </CardContent>
            <CardActions sx={{ justifyContent: 'space-between', p: 2 }}>
                <Typography variant="body1" color="text.secondary" sx={{ textAlign: 'left' }}>
                    &nbsp;
                </Typography>
                <Button size="small" sx={{ textAlign: 'right' }}>
                    Price $: {price.toFixed(2)}
                </Button>
            </CardActions>
        </Card>
    );
};

export default SummarizedProduct;
