import React from 'react';
import { Card, CardMedia, CardContent, Typography, CardActions, Button, Box } from '@mui/material';
import FavoriteButton from '../../favorite-button/FavoriteButton';
import img_green_ecopoints from '../../../images/img_green_ecopoints.png';
import img_red_ecopoints from '../../../images/img_red_ecopoints.png';
import img_yellow_ecopoints from '../../../images/img_yellow_ecopoints.png'; 

const SummarizedProduct = ({ product }) => {
    const { idProduct, name, images, price, description, ecoPoints } = product;
    const image = images.length > 0 ? images[0] : 'default-product-image.jpg'; 

    
    const getEcoPointsImage = (points) => {
        if (points >= 75) return img_green_ecopoints;
        if (points >= 50) return img_yellow_ecopoints;
        return img_red_ecopoints; 
    };

    return (
        <Card 
            sx={{ 
                maxWidth: 350, 
                width: '100%',
                m: 2, 
                display: 'flex', 
                flexDirection: 'column', 
                justifyContent: 'space-between', 
                height: '100%'
            }}
        >
            <CardMedia
                component="img"
                image={image}
                alt={name}
                sx={{ height: 140, backgroundSize: 'contain' }} 
            />
            <CardContent sx={{ flexGrow: 1 }}>
                <FavoriteButton productId={product.id} />
                <Typography gutterBottom variant="h6" component="div" sx={{ textAlign: 'left' }}>
                    {name}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'left' }}>
                    {description}
                </Typography>
            </CardContent>
            <CardActions sx={{ justifyContent: 'space-between', p: 2, alignItems: 'center' }}>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <img
                        src={getEcoPointsImage(ecoPoints)}
                        alt="Eco Points"
                        style={{ height: 40, marginRight: 5 }}
                    />
                    <Typography variant="caption" sx={{ fontWeight: 'bold' }}>
                        {ecoPoints.toFixed(2)} PTS
                    </Typography>
                </Box>
                <Button size="small" sx={{ textAlign: 'right' }}>
                    Price $: {price.toFixed(2)}
                </Button>
            </CardActions>
        </Card>
    );
};

export default SummarizedProduct;
