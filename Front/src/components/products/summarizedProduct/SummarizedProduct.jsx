import React from 'react';
import { Card, CardMedia, CardContent, Typography, CardActions, Button } from '@mui/material';

const SummarizedProduct = ({ product }) => {
    const { id, name, image, price, description } = product; // Asegúrate de que estas propiedades coincidan con la estructura de tus datos

    return (
        <Card sx={{ maxWidth: 500, m: 2 }}>
            <CardMedia
                component="img"
                height="140"
                image={image}
                alt={name}
            />
            <CardContent>
                <Typography gutterBottom variant="h5" component="div">
                    {name}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                    {description}
                </Typography>
            </CardContent>
            <CardActions>
                <Button size="small">Precio: ${price}</Button>
            </CardActions>
        </Card>
    );
};

export default SummarizedProduct;
